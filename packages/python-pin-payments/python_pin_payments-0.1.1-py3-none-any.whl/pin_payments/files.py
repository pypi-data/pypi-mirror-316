from typing import Dict, Any

import requests

from config import get_api_key
from pin_payments.base import Base


class Files(Base):
    """
    The Files API allows for the management of file uploads, including uploading new files,
    retrieving details of uploaded files, and deleting files.
    """

    def __init__(self, api_key: str, mode: str = 'live'):
        """
        Initializes the Files API with an API key and mode.

        :param api_key: The secret API key for authentication.
        :param mode: The mode of operation, either 'live' or 'test' for sandbox testing.
        """
        super().__init__(api_key=api_key, mode=mode)
        self._base_url += 'files/'

    def upload_file(self, file_path: str, purpose: str) -> Dict[str, Any]:
        """
        Uploads a new file and returns its details.

        :param file_path: Local path to the file to be uploaded.
        :param purpose: The purpose of the file upload, such as 'dispute_evidence'.
        :return: A dictionary containing the details of the uploaded file.
        """
        files = {'file': open(file_path, 'rb')}
        data = {'purpose': purpose}
        response = requests.post(self._base_url, auth=self._auth, files=files, data=data)
        return self._handle_response(
            response,
            'upload_file',
            200
        )

    def get_file_details(self, file_token: str) -> Dict[str, Any]:
        """
        Retrieves the details of an uploaded file by its token.

        :param file_token: The token of the uploaded file.
        :return: A dictionary containing the details of the file.
        """
        response = requests.get(f'{self._base_url}{file_token}', auth=self._auth)
        return self._handle_response(
            response,
            'get_file_details',
            200
        )

    def delete_file(self, file_token: str) -> Dict[str, Any]:
        """
        Deletes an uploaded file by its token.

        :param file_token: The token of the file to be deleted.
        :return: A dictionary confirms the deletion of the file.
        """
        response = requests.delete(f'{self._base_url}{file_token}', auth=self._auth)
        return self._handle_response(
            response,
            'delete_file',
            204
        )


if __name__ == '__main__':
    files_api = Files(api_key=get_api_key(), mode='test')

    file_path = 'path/to/your/file.pdf'
    purpose = 'dispute_evidence'
    try:
        upload_response = files_api.upload_file(file_path=file_path, purpose=purpose)
        print("File Upload Response:", upload_response)
    except FileNotFoundError:
        print('ERROR:You need a file for uploading')

    file_token = 'file_token_example'

    file_details_response = files_api.get_file_details(file_token=file_token)
    print("File Details Response:", file_details_response)

    delete_file_response = files_api.delete_file(file_token=file_token)
    print("Delete File Response:", delete_file_response)
