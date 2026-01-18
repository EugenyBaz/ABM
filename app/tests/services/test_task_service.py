import pytest

from app.schemas.task import TaskCreate, TaskUpdate
from app.services.task_service import (
    create_task,
    delete_task,
    get_task_by_id,
    get_tasks,
    update_task,
)


@pytest.mark.asyncio
async def test_create_task(db_session):
    user_id = 123

    task_in = TaskCreate(
        title="Test task",
        description="Test description",
    )

    task = await create_task(
        db=db_session,
        task=task_in,
        user_id=user_id,
    )

    assert task.id is not None
    assert task.title == "Test task"
    assert task.description == "Test description"
    assert task.user_id == user_id
    assert task.status == "pending"


@pytest.mark.asyncio
async def test_get_tasks_returns_only_user_tasks(db_session):
    # user 1
    await create_task(
        db=db_session,
        task=TaskCreate(title="User1 task", description=""),
        user_id=1,
    )

    # user 2
    await create_task(
        db=db_session,
        task=TaskCreate(title="User2 task", description=""),
        user_id=2,
    )

    tasks_user_1 = await get_tasks(
        db=db_session,
        user_id=1,
    )

    assert len(tasks_user_1) == 1
    assert tasks_user_1[0].title == "User1 task"


@pytest.mark.asyncio
async def test_get_task_by_id(db_session):
    task = await create_task(
        db=db_session,
        task=TaskCreate(title="Find me", description=""),
        user_id=42,
    )

    found = await get_task_by_id(db_session, task.id)

    assert found is not None
    assert found.id == task.id


@pytest.mark.asyncio
async def test_update_task_success(db_session):
    task = await create_task(
        db=db_session,
        task=TaskCreate(title="Old", description="Old"),
        user_id=1,
    )

    updated, error = await update_task(
        db=db_session,
        task_id=task.id,
        user_id=1,
        task=TaskUpdate(title="New"),
    )

    assert error is None
    assert updated.title == "New"


@pytest.mark.asyncio
async def test_update_task_forbidden(db_session):
    task = await create_task(
        db=db_session,
        task=TaskCreate(title="Secret", description=""),
        user_id=1,
    )

    updated, error = await update_task(
        db=db_session,
        task_id=task.id,
        user_id=999,
        task=TaskUpdate(title="Hack"),
    )

    assert updated is None
    assert error == "forbidden"


@pytest.mark.asyncio
async def test_delete_task(db_session):
    task = await create_task(
        db=db_session,
        task=TaskCreate(title="Delete me", description=""),
        user_id=1,
    )

    deleted, error = await delete_task(
        db=db_session,
        task_id=task.id,
        user_id=1,
    )

    assert error is None
    assert deleted.id == task.id
