import io

from typing import Union

import pandas as pd
from azure.storage.blob import BlobServiceClient, ContentSettings

IMAGE_CONTENT_TYPE = ContentSettings(content_type="image/jpeg")


class BlobServiceClientWriter(BlobServiceClient):
    """
    Description
    ------------
    The class is used to write data into Azure Blob Storage
    """

    def __init__(self, account_url: str, credential: str, **kwargs):
        super().__init__(account_url=account_url, credential=credential, **kwargs)

    @staticmethod
    def dataframe_from_dict(data: list[dict]) -> pd.DataFrame:
        """
        Description
        ------------
        The method converts list of dictionaries into pandas DataFrame

        Parameters
        ------------
        :param data : list of dictionaries

        Returns
        ------------
        :return : pandas DataFrame
        """
        df = pd.DataFrame.from_dict(data)
        return df

    def upload_csv(self, container: str, blob_name: str, data: list[dict]) -> None:
        """
        Description
        ------------
        The method upload csv file into Azure Blob Storage

        Parameters
        ------------
        :param container : Azure Blob Storage container
        :param blob_name : blob_name filename that will be stored in container
        :param data : data that will be stored in csv file.
        """

        # Create dataframe
        df = self.dataframe_from_dict(data)

        # Creating StringIO class for storing data as bytes
        output = io.StringIO()
        # Convert dataframe into csv file and store it in memory
        output = df.to_csv()  #  test it without this

        # Connecting to Azure Blob Service client
        # and define csv file name for storing
        blob_client = self.get_blob_client(container=container, blob=blob_name)

        # Append data to output data
        output = df.to_csv(index=False, encoding="utf-8")
        # Upload csv files to Azure Blob Storage
        blob_client.upload_blob(output, blob_type="BlockBlob")

    def upload_geojson(self, file_path: str, container: str, blob_name: str) -> None:
        """
        Description
        ------------
        Upload local geojson file to Azure Blob Storage

        Parameters
        ------------
        :param container : container name in Azure Blob Storage
        :param blob_name : blob name
        """

        # Get Azure Blob Storage client
        container_client = self.get_container_client(container=container)

        # Upload geojson file into Azure Blob Storage
        with open(file_path, mode="rb") as data:
            container_client.upload_blob(
                name=blob_name,
                data=data,
                overwrite=True,
                content_settings=ContentSettings(content_type="text/plain"),
            )

    def upload_blob(
        self, input_stream: Union[bytes, str], container: str, blob_name: str
    ) -> None:
        """
        Description
        ------------
        Upload zip file to Azure Blob Storage

        Parameters
        ------------
        :param input_stream : input file bytes
        :param container : container name in Azure Blob Storage
        :param blob_name : blob name in container

        """

        # Get Azure Blob Storage client
        blob_client = self.get_blob_client(container=container, blob=blob_name)
        # Upload zip files into Azure Blob Storage
        blob_client.upload_blob(input_stream, blob_type="BlockBlob", overwrite=True)

    def delete_blob(self, container: str, blob_name: str):
        """
        Description
        ------------
        Delete blob from Azure Blob Storage

        Parameters
        ------------
        :param container : container name in Azure Blob Storage
        :param blob_name : blob name in container
        """

        blob_client = self.get_blob_client(container=container, blob=blob_name)
        blob_client.delete_blob()

    def upload_image_bytes(
        self, container_name, image_name: str, img_bytes: bytes
    ) -> None:
        """
        Description
        ------------
        Upload image to Azure Blob Storage

        Parameters
        ------------
        :param container_name : container name in Azure Blob Storage
        :param image_name : image name
        :param img_bytes : image bytes
        """

        # Get a BlobClient object for the container
        container_client = self.get_container_client(container_name)

        container_client.upload_blob(
            image_name, img_bytes, content_settings=IMAGE_CONTENT_TYPE
        )

    def upload_image(
        self, img_path: str, container: str, blob_name: str, overwrite: bool = True
    ) -> None:
        """
        Description
        --
        Upload local image file to Azure Blob Storage

        Parameters
        --
        :param img_path : local image path
        :param container : container name in Azure Blob Storage
        :param blob_name : blob name
        """
        # Get Azure Blob Storage client
        container_client = self.get_container_client(container=container)
        # Upload image file into Azure Blob Storage
        with open(img_path, mode="rb") as data:
            container_client.upload_blob(
                name=blob_name,
                data=data,
                overwrite=overwrite,
                content_settings=IMAGE_CONTENT_TYPE,
            )

    def upload_json(self, file_path: str, container: str, blob_name: str) -> None:
        """
        Description
        --
        Upload local geojson file to Azure Blob Storage

        Parameters
        --
        :param file_path : local file path
        :param container : container name in Azure Blob Storage
        :param blob_name : blob name
        """
        # Get Azure Blob Storage client
        container_client = self.get_container_client(container=container)
        # Upload geojson file into Azure Blob Storage
        with open(file_path, mode="rb") as data:
            container_client.upload_blob(
                name=blob_name,
                data=data,
                overwrite=True,
                content_settings=ContentSettings(content_type="text/plain"),
            )
