import pytest

from tareas import db, service


@pytest.fixture
def conn():
    conn = db.get_connection(":memory:")
    db.init_db(conn)
    yield conn
    conn.close()


def test_create_task_persists_task(conn):
    task = service.create_task(conn, "Comprar leche", "Necesaria en casa", "alta", "2026-12-01")
    assert task.id > 0
    assert task.title == "Comprar leche"
    assert task.description == "Necesaria en casa"
    assert task.priority == "alta"
    assert task.deadline == "2026-12-01"
    assert task.status == "pendiente"
    assert task.completed_at is None


def test_create_task_rejects_empty_title(conn):
    with pytest.raises(ValueError):
        service.create_task(conn, "   ")


def test_create_task_rejects_invalid_priority(conn):
    with pytest.raises(ValueError):
        service.create_task(conn, "Tarea", "", "urgente", None)


def test_create_task_rejects_invalid_deadline_format(conn):
    with pytest.raises(ValueError):
        service.create_task(conn, "Tarea", "", "media", "2026/12/01")


def test_create_task_rejects_invalid_deadline_value(conn):
    with pytest.raises(ValueError):
        service.create_task(conn, "Tarea", "", "media", "2026-13-45")


def test_list_tasks_returns_all_by_default(conn):
    service.create_task(conn, "A", "", "media", None)
    service.create_task(conn, "B", "", "alta", None)
    tasks = service.list_tasks(conn, "todas")
    assert len(tasks) == 2
    assert [task.title for task in tasks] == ["B", "A"]


def test_list_tasks_filters_by_status(conn):
    task_a = service.create_task(conn, "A", "", "media", None)
    task_b = service.create_task(conn, "B", "", "alta", None)
    service.complete_task(conn, task_b.id)
    pending = service.list_tasks(conn, "pendiente")
    assert [task.id for task in pending] == [task_a.id]
    completed = service.list_tasks(conn, "completada")
    assert [task.id for task in completed] == [task_b.id]


def test_list_tasks_orders_by_priority(conn):
    task_baja = service.create_task(conn, "Baja", "", "baja", None)
    task_media = service.create_task(conn, "Media", "", "media", None)
    task_alta = service.create_task(conn, "Alta", "", "alta", None)
    tasks = service.list_tasks(conn, "todas")
    assert [task.id for task in tasks] == [task_alta.id, task_media.id, task_baja.id]


def test_complete_task_marks_task_completed(conn):
    task = service.create_task(conn, "A", "", "media", None)
    completed = service.complete_task(conn, task.id)
    assert completed.status == "completada"
    assert completed.completed_at is not None


def test_complete_task_unknown_id_raises(conn):
    with pytest.raises(ValueError):
        service.complete_task(conn, 9999)


def test_delete_task_deletes_task(conn):
    task = service.create_task(conn, "A", "", "media", None)
    assert service.delete_task(conn, task.id) is True
    with pytest.raises(ValueError):
        service.get_task(conn, task.id)


def test_delete_task_unknown_id_raises(conn):
    with pytest.raises(ValueError):
        service.delete_task(conn, 9999)
