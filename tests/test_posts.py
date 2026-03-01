from app import schemas

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/")
    assert res.status_code == 200
    assert len(res.json()) == len(test_posts)


def test_unauthorized_user_get_all_posts(client):
    res = client.get("/posts/")
    assert res.status_code == 401


def test_get_post_by_id(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


def test_unauthorized_get_post_by_id(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_by_id_not_exists(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/-1")
    assert res.status_code == 404


def test_create_post(authorized_client, test_user):
    res = authorized_client.post(
        "/posts/", json={"title": "Test Post", "content": "This is a test post", "published": True})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.title == "Test Post"
    assert created_post.content == "This is a test post"
    assert created_post.published == True
    assert created_post.owner_id == test_user['user_id']


def test_unauthorized_create_post(client):
    res = client.post(
        "/posts/", json={"title": "Test Post", "content": "This is a test post"})
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_delete_post_success(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204


def test_delete_post_not_exists(authorized_client):
    res = authorized_client.delete(f"/posts/-1")
    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_posts):
    res = authorized_client.delete(
        f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client,test_posts,test_user):
    data={"title":"Updated Title","content":"Updated Content"}
    res=authorized_client.put(f"/posts/{test_posts[0].id}",json=data)
    updated_post=schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title==data['title']
    assert updated_post.content==data['content']

def test_update_other_user_post(authorized_client,test_posts):
    data={"title":"Updated Title","content":"Updated Content"}
    res=authorized_client.put(f"/posts/{test_posts[3].id}",json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_post(client, test_posts):
    data={"title":"Updated Title","content":"Updated Content"}
    res = client.put(f"/posts/{test_posts[0].id}",json=data)
    assert res.status_code == 401

def test_update_post_not_exists(authorized_client):
    data={"title":"Updated Title","content":"Updated Content"}
    res = authorized_client.put(f"/posts/-1",json=data)
    assert res.status_code == 404