import pytest
from gestell import Gestell

gestell = Gestell()
organization_id = ''
collection_id = ''
category_id = ''


@pytest.mark.asyncio
async def test_create_organization():
    global organization_id
    response = await gestell.organization.create(
        name='Automated Test Organization',
        description='This is an automated test organization',
    )
    assert response.status == 'OK'
    assert len(response.id) > 1
    organization_id = response.id


@pytest.mark.asyncio
async def test_create_collection():
    global collection_id
    response = await gestell.collection.create(
        organizationId=organization_id,
        name='Automated Test Collection',
        description='An automated test collection',
        type='canon',
    )
    assert response.status == 'OK'
    assert len(response.id) > 1
    collection_id = response.id


@pytest.mark.asyncio
async def test_list_collections():
    response = await gestell.collection.list()
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_list_collections_with_skip():
    response = await gestell.collection.list(skip=1000, take=0)
    assert response.status == 'OK'
    assert len(response.result) == 0


@pytest.mark.asyncio
async def test_list_collections_with_search():
    response = await gestell.collection.list(search='Unga Bunga 42 42')
    assert response.status == 'OK'
    assert len(response.result) == 0


@pytest.mark.asyncio
async def test_get_collection():
    response = await gestell.collection.get(collection_id)
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_update_collection():
    response = await gestell.collection.update(
        collection_id=collection_id,
        name='Automated Test Collection updated',
        description='An automated test collection updated',
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_add_category():
    global category_id
    response = await gestell.collection.add_category(
        collection_id=collection_id,
        name='Automated Test Category',
        type='concepts',
        instructions='Hello World',
    )
    assert response.status == 'OK'
    assert len(response.id) > 1
    category_id = response.id


@pytest.mark.asyncio
async def test_update_category():
    response = await gestell.collection.update_category(
        collection_id=collection_id,
        category_id=category_id,
        name='Automated Test Category Update',
        instructions='Hello World Update',
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_remove_category():
    response = await gestell.collection.remove_category(
        collection_id=collection_id, category_id=category_id
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_delete_collection():
    response = await gestell.collection.delete(collection_id)
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_delete_organization():
    response = await gestell.organization.delete(organization_id)
    assert response.status == 'OK'
