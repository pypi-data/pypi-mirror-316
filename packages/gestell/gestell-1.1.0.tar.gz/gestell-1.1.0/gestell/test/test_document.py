import pytest
from gestell import Gestell
from pathlib import Path
from aiofile import AIOFile
import aiohttp


gestell = Gestell()
organization_id = ''
collection_id = ''
document_id = ''
job_id = ''


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
        type='frame',
    )
    assert response.status == 'OK'
    assert len(response.id) > 1
    collection_id = response.id


@pytest.mark.asyncio
async def test_presign_upload_and_create_document():
    global document_id
    test_file_path = Path(__file__).parent / 'sample.jpg'

    presign_response = await gestell.document.presign(
        collection_id=collection_id, filename='sample.jpg', type='image/jpeg'
    )
    assert presign_response.status == 'OK'

    async with AIOFile(str(test_file_path), 'rb') as f:
        file_content = await f.read()

    async with aiohttp.ClientSession() as session:
        await session.put(
            presign_response.url,
            headers={'ContentType': 'image/jpeg'},
            data=file_content,
        )

    create_response = await gestell.document.create(
        collection_id=collection_id,
        name='sample.jpg',
        path=presign_response.path,
        type='image/jpeg',
    )
    assert create_response.status == 'OK'
    document_id = create_response.id


@pytest.mark.asyncio
async def test_upload_document_as_buffer_and_string():
    test_file_path = Path(__file__).parent / 'sample.jpg'
    response = await gestell.document.upload_document(
        collection_id=collection_id, name='sample-2.jpg', file=str(test_file_path)
    )

    assert response.status == 'OK'

    async with AIOFile(str(test_file_path), 'rb') as f:
        file_content = await f.read()
    response2 = await gestell.document.upload_document(
        collection_id=collection_id,
        name='sample-2.jpg',
        type='image/jpeg',
        file=file_content,
    )

    assert response2.status == 'OK'


@pytest.mark.asyncio
async def test_update_document():
    response = await gestell.document.update(
        collection_id=collection_id, document_id=document_id, name='sample-updated.jpg'
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_get_document():
    global job_id
    response = await gestell.document.get(
        collection_id=collection_id, document_id=document_id
    )
    assert response.status == 'OK'
    job_id = response.result.job.id if response.result and response.result.job else ''


@pytest.mark.asyncio
async def test_get_document_job():
    response = await gestell.job.get(collection_id=collection_id, job_id=job_id)
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_reprocess_document_job():
    response = await gestell.job.reprocess(
        collection_id=collection_id, type='status', ids=[job_id]
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_cancel_document_job():
    response = await gestell.job.cancel(collection_id=collection_id, ids=[job_id])
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_delete_document():
    response = await gestell.document.delete(
        collection_id=collection_id, document_id=document_id
    )
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_delete_collection():
    response = await gestell.collection.delete(collection_id=collection_id)
    assert response.status == 'OK'


@pytest.mark.asyncio
async def test_delete_organization():
    response = await gestell.organization.delete(id=organization_id)
    assert response.status == 'OK'
