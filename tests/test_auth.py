from httpx import AsyncClient

from tests.consttest import test_user_1, test_user_2

ACCESS_TOKEN: str
REFRESH_TOKEN: str

USER_ID: str


async def test_registration_wrong_email(ac: AsyncClient):
    wrong_data = test_user_1.copy()
    wrong_data.update({"email": "awdawdawd"})
    response = await ac.post(
        url="/auth/registration",
        json=wrong_data,
    )
    assert response.status_code == 422
    assert response.json().get("detail")[0].get("type") == "value_error"


async def test_registration_password_more_than_max_len(ac: AsyncClient):
    wrong_data = test_user_1.copy()
    wrong_data.update({"password": "x" * 21})
    response = await ac.post(
        url="/auth/registration",
        json=wrong_data,
    )
    assert response.status_code == 422
    assert response.json().get("detail")[0].get("type") == "string_too_long"


async def test_registration_password_low_than_min_len(ac: AsyncClient):
    wrong_data = test_user_1.copy()
    wrong_data.update({"password": "x" * 1})
    response = await ac.post(
        url="/auth/registration",
        json=wrong_data,
    )
    assert response.status_code == 422
    assert response.json().get("detail")[0].get("type") == "string_too_short"


async def test_registration_user_1(ac: AsyncClient):
    response = await ac.post(
        url="/auth/registration",
        json=test_user_1,
    )
    assert response.status_code == 201
    assert response.json().get("id") is not None
    global USER_ID
    USER_ID = response.json().get("id")


async def test_registration_user_2(ac: AsyncClient):
    response = await ac.post(
        url="/auth/registration",
        json=test_user_2,
    )
    assert response.status_code == 201
    assert response.json().get("id") is not None


async def test_registration_duplicate_email(ac: AsyncClient):
    duplicate_name = test_user_1.copy()
    response = await ac.post(
        url="/auth/registration",
        json=duplicate_name,
    )
    assert response.status_code == 403
    assert response.json().get("detail") == "user already exist"


async def test_login_wrong_email(ac: AsyncClient):
    wrong_data = test_user_1.copy()
    wrong_data.update({"email": "awdawdawd@dawd.com"})
    response = await ac.post(
        url="/auth/login",
        json=wrong_data,
    )
    assert response.status_code == 401
    assert response.json().get("detail") == "wrong email or password"


async def test_login_wrong_password(ac: AsyncClient):
    wrong_data = test_user_1.copy()
    wrong_data.update({"password": "awdawdawd"})
    response = await ac.post(
        url="/auth/login",
        json=wrong_data,
    )
    assert response.status_code == 401
    assert response.json().get("detail") == "wrong email or password"


async def test_login(ac: AsyncClient):
    correct_data = test_user_1.copy()
    response = await ac.post(
        url="/auth/login",
        json=correct_data,
    )
    assert response.status_code == 200
    assert response.json().get("access_token") is not None
    assert response.json().get("refresh_token") is not None
    global ACCESS_TOKEN, REFRESH_TOKEN
    ACCESS_TOKEN = response.json().get("access_token")
    REFRESH_TOKEN = response.json().get("refresh_token")


async def test_refresh_use_access_token(ac: AsyncClient):
    response = await ac.get(
        url="/auth/refresh",
        headers={"Authorization": f"Bearer {ACCESS_TOKEN}"},
    )
    assert response.status_code == 401
    assert response.json().get("detail") == "invalid token"


async def test_refresh(ac: AsyncClient):
    response = await ac.get(
        url="/auth/refresh",
        headers={"Authorization": f"Bearer {REFRESH_TOKEN}"},
    )
    assert response.status_code == 200
    assert response.json().get("access_token") is not None
