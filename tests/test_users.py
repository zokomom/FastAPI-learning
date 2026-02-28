from app.schemas import UsersOut,Token
import pytest
from jose import jwt
from app.config import settings

# def test_root(client):
#     res = client.get("/")
#     print(res.text)
#     assert res.status_code == 200

def test_create_user(client):
    res=client.post(
        "/users/",json={"email":"atharv_new@gmail.com",
                        "password":"1234"} 
    )
    new_user=UsersOut(**res.json())
    assert new_user.email=="atharv_new@gmail.com"
    assert res.status_code==201

def test_login_user(client,test_user):
    res=client.post(
        "/login",data={'username':test_user['email'],'password':test_user['password']}
    )
    login_res=Token(**res.json())
    payload=jwt.decode(login_res.access_token,settings.secret_key,algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id==test_user['user_id']
    assert login_res.token_type=='bearer'
    assert res.status_code==200

@pytest.mark.parametrize("email,password,status_code",[
    ('wrongemail@gmail.com','1234',403),
    ('atharv@gmail.com','wrongpassword',403),
    ('wrong@gmail.com', 'wrongpassword',403),
    (None, '1234', 422),
    ('atharv@gmail.com', None, 422)
])
def test_invalid_credentials(email,password,status_code,client,test_user):
    res=client.post("/login/",data={"username":email,"password":password})
    print(res.json())
    if status_code==422:
        assert res.status_code==422
    elif status_code==403:
        assert res.status_code == status_code
        assert res.json().get("detail")=="Invalid Credentials"