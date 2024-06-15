from uuid import uuid4

from httpx import AsyncClient

from tests.consttest import test_user_1

ACCESS_TOKEN: str
REFRESH_TOKEN: str

USERS: list = []

USER_ID: str


async def test_login(ac: AsyncClient):
    correct_data = test_user_1.copy()
    response = await ac.post(
        url="/auth/login",
        json=correct_data,
    )
    global ACCESS_TOKEN, REFRESH_TOKEN
    ACCESS_TOKEN = response.json().get("access_token")
    REFRESH_TOKEN = response.json().get("refresh_token")
    response = await ac.get(
        url="/users",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    assert len(response.json()) == 2
    global USERS
    USERS = response.json()


async def test_subscribe_wrong_uuid(ac: AsyncClient):
    response = await ac.post(
        url="/subscribes",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        params={"following_id": str(uuid4())},
    )
    assert response.status_code == 403
    assert response.json().get("detail") == "subscribe already exist or wrong user id"


async def test_subscribe(ac: AsyncClient):
    response = await ac.post(
        url="/subscribes",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        params={"following_id": USERS[1].get("id")},
    )
    assert response.status_code == 201
    assert response.json().get("following_id") is not None
    assert response.json().get("follower_id") is not None


async def test_subscribe_duplicate(ac: AsyncClient):
    response = await ac.post(
        url="/subscribes",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        params={"following_id": USERS[1].get("id")},
    )
    assert response.status_code == 403
    assert response.json().get("detail") == "subscribe already exist or wrong user id"


async def test_unsubscribe(ac: AsyncClient):
    response = await ac.delete(
        url="/subscribes",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        params={"following_id": USERS[1].get("id")},
    )
    assert response.status_code == 204
