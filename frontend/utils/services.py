import requests

from configs import Settings

settings = Settings()


def get_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def list_entities(entity: str, token: str, params: dict = None) -> list:
    entity_response = requests.get(f"{settings.api_url}/{entity}/", headers=get_headers(token), params=params)
    return entity_response.json() if entity_response.status_code == 200 else []


def get_entity(entity: str, entity_id: str, token: str, params: dict = None) -> dict:
    entity_response = requests.get(
        f"{settings.api_url}/{entity}/{entity_id}",
        headers=get_headers(token),
        params=params
    )
    if entity_response.status_code == 200:
        return {
            "success": True,
            "message": entity_response.json()
        }
    elif entity_response.status_code == 404:
        return {
            "success": False,
            "message": entity_response.json().get("detail")
        }
    else:
        return {
            "success": False,
            "message": entity_response.json().get("detail")
        }


def create_entity(entity: str, data: dict, token: str, params: dict = None) -> dict:
    entity_response = requests.post(
        f"{settings.api_url}/{entity}/",
        json=data, headers=get_headers(token),
        params=params
    )
    if entity_response.status_code == 201:
        return {
            "success": True,
            "message": entity_response.json()
        }
    elif entity_response.status_code == 400:
        return {
            "success": False,
            "message": entity_response.json().get('detail')
        }


def update_entity(
        entity: str,
        entity_id: str,
        token: str,
        data: dict,
        method: str = "patch",
        params: dict = None
) -> dict:
    if method == "patch":
        entity_response = requests.patch(
            f"{settings.api_url}/{entity}/{entity_id}",
            json=data,
            headers=get_headers(token),
            params=params
        )
    else:
        entity_response = requests.put(
            f"{settings.api_url}/{entity}/{entity_id}",
            json=data,
            headers=get_headers(token),
            params=params
        )
    if entity_response.status_code == 200:
        return {
            "success": True,
            "message": entity_response.json()
        }
    elif entity_response.status_code == 404:
        return {
            "success": False,
            "message": entity_response.json().get("detail")
        }
    else:
        return {
            "success": False,
            "message": entity_response.json()
        }


def delete_entity(entity: str, entity_id: str, token: str, params: dict = None) -> dict:
    entity_response = requests.delete(
        f"{settings.api_url}/{entity}/{entity_id}",
        headers=get_headers(token),
        params=params
    )
    if entity_response.status_code == 200:
        return {
            "success": True,
            "message": entity_response.json().get("message")
        }
    elif entity_response.status_code == 404:
        return {
            "success": False,
            "message": entity_response.json().get("detail")
        }
    else:
        return {
            "success": False,
            "message": entity_response.json()
        }
