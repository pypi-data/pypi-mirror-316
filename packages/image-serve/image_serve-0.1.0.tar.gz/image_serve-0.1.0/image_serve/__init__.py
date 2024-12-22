import requests

class ImageServe:
    def __init__(self, api_key: str, base_url: str = "https://imageserve.pythonanywhere.com/user/api/v1/upload-image/"):
        self.api_key = api_key
        self.base_url = base_url

    def upload_image(self, file_path: str) -> dict:
        with open(file_path, "rb") as file:
            files = {"image": file}
            headers = {"Authorization": f"Token {self.api_key}"}
            response = requests.post(self.base_url, files=files, headers=headers)

        if response.status_code != 201:
            raise Exception(f"Failed to upload image: {response.text}")

        return response.json()
