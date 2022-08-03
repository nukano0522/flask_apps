import os
from azure.storage.filedatalake import DataLakeServiceClient

def initialize_storage_account(storage_account_name, storage_account_key):
    
    try:  
        global service_client

        service_client = DataLakeServiceClient(account_url="{}://{}.dfs.core.windows.net".format(
            "https", storage_account_name), credential=storage_account_key)
    
    except Exception as e:
        print(e)


def download_file_from_directory():
    try:
        file_system_client = service_client.get_file_system_client(file_system="nukano0522container01")
        directory_client = file_system_client.get_directory_client("image_detection/model")
        local_file = open("c:\\Users\\nukan\\Desktop\\work\\git\\flask_apps\\model.pt",'wb')
        file_client = directory_client.get_file_client("model.pt")
        download = file_client.download_file()
        downloaded_bytes = download.readall()
        local_file.write(downloaded_bytes)
        local_file.close()

    except Exception as e:
     print(e)


def main():
    storage_account_name = os.environ['STORAGE_ACCOUNT_NAME']
    storage_account_key = os.environ['STORAGE_ACCOUNT_KEY']
    initialize_storage_account(storage_account_name, storage_account_key)

    download_file_from_directory()


if __name__ == '__main__':
    main()