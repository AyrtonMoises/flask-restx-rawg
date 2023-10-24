from app.api.models.user import UserModel 


def test_create_user(client):
    data = {
        'username': 'user_test',
        'password': 'testpassword',
        'email': 'user_test@example.com'
    }
    user = UserModel.create_user(data)
    assert user.id == 1
    assert user.username == 'user_test'
    assert user.email == 'user_test@example.com'
    assert user.verify_password(data['password'], user.password) == True
    assert user.is_admin == False

def test_get_user_by_username(client, user_regular_fixture):
    data = {
        'username': 'myusername',
        'password': 'mypassword',
        'email': 'user@test.com',
        'is_admin': False
    }
    user = UserModel.get_user_by_username(data['username'])
    assert user is not None
    assert user.id == 1
    assert user.username == data['username']
    assert user.verify_password(data['password'], user.password) == True
    assert user.email == data['email']
    assert user.is_admin == data['is_admin']

def test_get_user_by_id(client, user_regular_fixture):
    data = {
        'username': 'myusername',
        'password': 'mypassword',
        'email': 'user@test.com',
        'is_admin': False
    }
    user = UserModel.get_user_by_id(1)
    assert user is not None
    assert user.id == 1
    assert user.username == data['username']
    assert user.verify_password(data['password'], user.password) == True
    assert user.email == data['email']
    assert user.is_admin == data['is_admin']

def test_get_all_users(client, user_regular_fixture):
    users = UserModel.get_all_users()
    assert len(users) == 1

def test_update_user(client, user_regular_fixture):
    data = {
        'username': 'newname',
        'email': 'newemail@test.com'
    }
    user = UserModel.update_user(user_regular_fixture.id, data)
    assert user.username == data['username']
    assert user.email == data['email']

def test_update_password(client, user_regular_fixture):
    new_password = 'newpassword'
    user = UserModel.update_password(user_regular_fixture.id, new_password)
    assert user.verify_password(new_password, user.password) == True

def test_delete_user(client, user_regular_fixture):
    UserModel.delete_user(user_regular_fixture)
    user = UserModel.get_user_by_username(user_regular_fixture.username)
    assert user is None