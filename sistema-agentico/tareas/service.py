from dataclasses import dataclass
from datetime import datetime
import re

from . import db

VALID_PRIORITIES = ("alta", "media", "baja")
VALID_STATUSES = ("pendiente", "completada")
_PRIORITY_ORDER = {priority: index for index, priority in enumerate(VALID_PRIORITIES)}


@dataclass
class Task:
    """Representa una tarea."""

    id: int
    title: str
    description: str
    priority: str
    deadline: str | None
    status: str
    created_at: str
    completed_at: str | None


def _validate_title(title: str) -> str:
    """Valida y normaliza el título."""
    cleaned = (title or "").strip()
    if not cleaned:
        raise ValueError("El título no puede estar vacío")
    return cleaned


def _validate_priority(priority: str) -> str:
    """Valida la prioridad de la tarea."""
    normalized = (priority or "").strip().lower()
    if normalized not in VALID_PRIORITIES:
        raise ValueError(f"Prioridad inválida: {priority}. Valores permitidos: alta, media, baja")
    return normalized


def _validate_deadline(deadline: str | None) -> str | None:
    """Valida la fecha límite con formato YYYY-MM-DD."""
    if deadline is None or deadline.strip() == "":
        return None
    value = deadline.strip()
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value):
        raise ValueError(f"Fecha límite inválida: {value}. Formato esperado: YYYY-MM-DD")
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as error:
        raise ValueError(f"Fecha límite inválida: {value}") from error
    return value


def _to_task(row) -> Task:
    """Convierte una fila SQLite a un Task."""
    return Task(
        id=row["id"],
        title=row["title"],
        description=row["description"],
        priority=row["priority"],
        deadline=row["deadline"],
        status=row["status"],
        created_at=row["created_at"],
        completed_at=row["completed_at"],
    )


def get_task(conn, task_id: int) -> Task:
    """Retorna la tarea por ID o lanza error si no existe."""
    row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        raise ValueError(f"Tarea no encontrada: {task_id}")
    return _to_task(row)


def create_task(
    conn,
    title: str,
    description: str = "",
    priority: str = "media",
    deadline: str | None = None,
) -> Task:
    """Crea y persiste una tarea con validaciones."""
    clean_title = _validate_title(title)
    clean_priority = _validate_priority(priority)
    clean_deadline = _validate_deadline(deadline)
    created_at = datetime.now().isoformat()
    cursor = conn.execute(
        "INSERT INTO tasks (title, description, priority, deadline, status, created_at) VALUES (?, ?, ?, ?, 'pendiente', ?)",
        (clean_title, description or "", clean_priority, clean_deadline, created_at),
    )
    conn.commit()
    return get_task(conn, cursor.lastrowid)


def list_tasks(conn, status: str = "todas") -> list[Task]:
    """Lista tareas filtrando por estado y ordenando por prioridad."""
    if status != "todas" and status not in VALID_STATUSES:
        raise ValueError(f"Estado inválido: {status}. Valores permitidos: pendiente, completada, todas")
    query = "SELECT * FROM tasks"
    params: list = []
    if status != "todas":
        query += " WHERE status = ?"
        params.append(status)
    query += " ORDER BY CASE priority WHEN 'alta' THEN 0 WHEN 'media' THEN 1 ELSE 2 END, id"
    tasks: list[Task] = []
    for row in conn.execute(query, params).fetchall():
        tasks.append(_to_task(row))
    return tasks


def complete_task(conn, task_id: int) -> Task:
    """Marca la tarea como completada."""
    task = get_task(conn, task_id)
    if task.status != "completada":
        conn.execute(
            "UPDATE tasks SET status = 'completada', completed_at = ? WHERE id = ?",
            (datetime.now().isoformat(), task_id),
        )
        conn.commit()
    return get_task(conn, task_id)


def delete_task(conn, task_id: int) -> bool:
    """Elimina la tarea por ID."""
    task = get_task(conn, task_id)
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    return True
