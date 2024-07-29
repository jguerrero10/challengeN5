import requests

from configs import Settings

settings = Settings()


def login(username: str, password: str):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'username': username,
        'password': password
    }
    response = requests.post(f"{settings.api_url}/auth/token", headers=headers, data=data)
    if response.status_code == 200:
        return {
            "success": True,
            "token": response.json().get("access_token")
        }
    return {
        "success": False,
        "message": "Incorrect username or password"
    }
