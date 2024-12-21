from datetime import datetime
import os
import pandas as pd
from azure.storage.blob import BlobServiceClient
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor


class AzureCSVToExcelConverter:
    def __init__(self, connection_string: str):
        self.connection_string = connection_string

    def __get_blob_service_client(self):
        return BlobServiceClient.from_connection_string(self.connection_string)


 
    def csv_to_excel(self, container_name: str, csv_blob_name: str):
        """
        This function takes a CSV file from Azure Blob Storage, converts it to Excel, and uploads it back to Azure Blob Storage.
        """
        try:
            # Initialize Blob Service Client
            blob_service_client = self.__get_blob_service_client()
            container_client = blob_service_client.get_container_client(container=container_name)

            # Read the CSV file from Azure Blob Storage
            blob_client = container_client.get_blob_client(csv_blob_name)
            download_stream = blob_client.download_blob()
            csv_file = BytesIO(download_stream.readall())

            # Convert the CSV file to Excel
            excel_file = BytesIO()
            chunk_size = 10**5 
            writer = pd.ExcelWriter(excel_file, engine="openpyxl")

            with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
                start_row = 0
                for chunk in pd.read_csv(csv_file, chunksize=chunk_size):
                    chunk.to_excel(writer, index=False, header=start_row == 0, sheet_name='Sheet1', startrow=start_row)
                    start_row += len(chunk)

            excel_file.seek(0)

            # Upload the Excel file back to Azure Blob Storage
            excel_blob_name = csv_blob_name.replace(".csv", ".xlsx")
            excel_blob_client = container_client.get_blob_client(excel_blob_name)
            excel_blob_client.upload_blob(excel_file, overwrite=True)

            print(f"Converted {csv_blob_name} to {excel_blob_name} and uploaded successfully.")
        except Exception as e:
            print(f"Error occurred: {e}")

