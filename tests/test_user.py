from httpx import AsyncClient

from tests.consttest import test_user_1

ACCESS_TOKEN: str
REFRESH_TOKEN: str

USERS: list

USER_ID: str


async def test_login(ac: AsyncClient):
    response = await ac.post(
        url="/auth/login",
        json=test_user_1,
    )
    assert response.status_code == 200
    assert response.json().get("access_token") is not None
    assert response.json().get("refresh_token") is not None
    global ACCESS_TOKEN, REFRESH_TOKEN, USERS
    ACCESS_TOKEN = response.json().get("access_token")
    REFRESH_TOKEN = response.json().get("refresh_token")
    response = await ac.get(
        url="/users",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    assert len(response.json()) == 2
    USERS = response.json()
    response = await ac.post(
        url="/subscribes",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
        params={"following_id": USERS[1].get("id")},
    )
    assert response.status_code == 201


async def test_users_me(ac: AsyncClient):
    response = await ac.get(
        url="/users/me",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json().get("id") is not None
    assert response.json().get("email") == test_user_1.get("email")
    assert response.json().get("birthday") == test_user_1.get("birthday")


async def test_users_me_wrong_access_token(ac: AsyncClient):
    response = await ac.get(
        url="/users/me",
        headers={"Authorization": f"Bearer test"},
    )
    assert response.status_code == 401
    assert response.json().get("detail") == "invalid token"


async def test_get_users(ac: AsyncClient):
    response = await ac.get(
        url="/users",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_get_users_without_access_token(ac: AsyncClient):
    response = await ac.get(
        url="/users",
        headers={"Authorization": f"Bearer test"},
    )
    assert response.status_code == 401
    assert response.json().get("detail") == "invalid token"


async def test_me_followers_wrong_access_token(ac: AsyncClient):
    response = await ac.get(
        url="/users/me/followers",
        headers={"Authorization": f"Bearer test"},
    )
    assert response.status_code == 401
    assert response.json().get("detail") == "invalid token"


async def test_me_followers(ac: AsyncClient):
    response = await ac.get(
        url="/users/me/followers",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    assert response.status_code == 200
    assert type(response.json()) is list


async def test_me_following_wrong_access_token(ac: AsyncClient):
    response = await ac.get(
        url="/users/me/following",
        headers={"Authorization": f"Bearer test"},
    )
    assert response.status_code == 401
    assert response.json().get("detail") == "invalid token"


async def test_me_following(ac: AsyncClient):
    response = await ac.get(
        url="/users/me/following",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    assert response.status_code == 200
    for subscribe in response.json():
        assert USERS[0].get("id") == subscribe.get("follower_id")


async def test_user_id_followers_wrong_access_token(ac: AsyncClient):
    response = await ac.get(
        url=f"/users/{USERS[1].get('id')}/followers",
        headers={"Authorization": f"Bearer test"},
    )
    assert response.status_code == 401
    assert response.json().get("detail") == "invalid token"


async def test_user_id_followers(ac: AsyncClient):
    response = await ac.get(
        url=f"/users/{USERS[1].get('id')}/followers",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    assert response.status_code == 200
    assert type(response.json()) is list
    assert len(response.json()) == 1
    for subscribe in response.json():
        assert USERS[0].get("id") == subscribe.get("follower_id")


async def test_user_id_following_wrong_access_token(ac: AsyncClient):
    response = await ac.get(
        url=f"/users/{USERS[1].get('id')}/following",
        headers={"Authorization": f"Bearer test"},
    )
    assert response.status_code == 401
    assert response.json().get("detail") == "invalid token"


async def test_user_id_following(ac: AsyncClient):
    response = await ac.get(
        url=f"/users/{USERS[1].get('id')}/following",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    assert response.status_code == 200
    assert type(response.json()) is list
    assert len(response.json()) == 0
