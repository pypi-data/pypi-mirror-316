# CSV to Excel

This project contains a python program that converts CSV files available at azure storage container to Excel format ans save at the same location.

## Features

- Convert CSV files available in azure blob storage and convert it to Excel format and save it at the same container location



## Usage

- To import in your project

pip install csv-excel-azure


from azure_csv_to_excel import AzureBlobConverter

# Azure Blob Storage connection string
connection_string = "<your-azure-connection-string>"

# Initialize converter
converter = AzureBlobConverter(connection_string)

# Convert CSV to Excel
converter.csv_to_excel(container_name="my-container", blob_name="input.csv")




## License

This project is licensed under the MIT License.