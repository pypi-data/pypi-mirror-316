import io

import geojson
import pandas as pd
import geopandas as gpd
from azure.storage.blob import BlobServiceClient


class BlobServiceClientReader(BlobServiceClient):
    """
    Description
    ------------
    The class is used to read data from Azure Blob Storage
    """

    def __init__(self, account_url: str, credential: str, **kwargs):
        super().__init__(account_url=account_url, credential=credential, **kwargs)

    def csv_to_dataframe(self, container: str, blob_name: str) -> pd.DataFrame:
        """
        Description
        ------------
        The method read csv file and returns pandas DataFrame

        Parameters
        ------------
        :param container : Azure Blob Storage container name
        :param blob_name : csv blob file name in blob storage

        Returns
        ------------
        df : data converted into pandas dataframe
        """

        # Connect to Azure Blob Service client
        blob_client = self.get_blob_client(container=container, blob=blob_name)

        # Reading csv file from blob bytes into dataframe
        with io.BytesIO() as input_blob:
            blob_client.download_blob().download_to_stream(input_blob)
            input_blob.seek(0)
            df = pd.read_csv(input_blob)

        return df

    # TODO : Add functionality for filtering blobs
    def get_blob_names(self, container: str) -> list:
        """
        Description
        ----------
        List all blobs in Azure Blob Storage container

        Parameters
        ----------
        :param container: container name in Azure Blob Storage

        Returns
        ----------
        blobs: list of blob names in Azure Blob Storage container
        """
        container_client = self.get_container_client(container=container)
        blob_list = container_client.list_blobs()
        blobs = [blob.name for blob in blob_list]

        return blobs

    def read_geojson(self, container: str, filename: str) -> dict:
        """
        The function reads GeoJSON data from container

        Arguments
        ----------
        container: str
            Azure Storage container name
        filename: str
            the filename to use for the blob
        conf: yaml
            configuration file
        """
        blob_client = self.get_blob_client(container=container, blob=filename)
        downloaderpath = blob_client.download_blob()
        geojson_data = geojson.loads(downloaderpath.readall())

        return geojson_data

    def geoparquet_to_geodataframe(
        self,
        container: str,
        blob_name: str,
    ):
        blob_client = self.get_blob_client(container, blob_name)

        with io.BytesIO() as input_blob:
            blob_client.download_blob().download_to_stream(input_blob)
            input_blob.seek(0)
            gdf = gpd.read_parquet(input_blob)

        return gdf

    def geojson_to_geodaframe(self, container: str, blob_name: str) -> gpd.GeoDataFrame:
        # Connect to Azure Blob Service client
        blob_client = self.get_blob_client(container=container, blob=blob_name)

        with io.BytesIO() as input_blob:
            blob_client.download_blob().download_to_stream(input_blob)
            input_blob.seek(0)
            gdf = gpd.read_file(input_blob)

        return gdf

    def download_image(
        self, container_name: str, blob_name: str, output_path: str
    ) -> None:
        """
        Description
        ------------
        Download image from Azure Blob Storage

        Parameters
        ------------
        :param container_name : container name in Azure Blob Storage
        :param blob_name : image name
        :param output_path : output path for downloaded image
        """

        # Get a BlobClient object for the blob to download
        blob_client = self.get_blob_client(container=container_name, blob=blob_name)

        # Download the blob to a local file
        with open(output_path, "wb") as blob:
            try:
                download_stream = blob_client.download_blob()
                blob.write(download_stream.readall())
            except Exception as e:
                print(f"Cannot download blob: {e}")

    def get_zip(self, container: str, blob_name: str) -> bytes:
        """
        Description
        ------------
        Load zip file from Azure Blob Storage into memory

        Parameters
        ------------
        :param container : container name in Azure Blob Storage
        :param blob_name : blob name in container

        Returns
        ------------
        bytes : zip file bytes
        """

        # Connect to Azure Blob Service client
        container_client = self.get_container_client(container=container)
        bytes = container_client.get_blob_client(blob_name).download_blob().readall()

        return bytes

    def download_blob(self, container: str, blob_name: str, output_path: str) -> str:
        """
        Description
        ----------
        Download blob from Azure Blob Storage to local machine

        Parameters
        ----------
        :param container: container name in Azure Blob Storage
        :param blob_name: blob name in container
        :param destination: destination path for downloaded blob

        Returns
        ----------
        :return: output_path : output path of downloaded file
        """

        blob_client = self.get_blob_client(container=container, blob=blob_name)

        with open(
            file=output_path,
            mode="wb",
        ) as _blob:
            download_stream = blob_client.download_blob()
            _blob.write(download_stream.readall())

        return output_path
    
    def parquet_to_dataframe(
        self,
        container: str,
        blob_name: str,
    ):
        blob_client = self.get_blob_client(container, blob_name)

        with io.BytesIO() as input_blob:
            blob_client.download_blob().download_to_stream(input_blob)
            input_blob.seek(0)
            df = pd.read_parquet(input_blob)

        return df