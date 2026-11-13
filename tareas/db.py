import sqlite3
from pathlib import Path

DB_FILENAME = "tareas.db"


def get_connection(path: str | Path = DB_FILENAME) -> sqlite3.Connection:
    """Abre la conexion SQLite a la base de datos de tareas."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Crea la tabla tasks si no existe."""
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT NOT NULL DEFAULT '',
            priority TEXT NOT NULL CHECK (priority IN ('alta', 'media', 'baja')),
            deadline TEXT,
            status TEXT NOT NULL DEFAULT 'pendiente',
            created_at TEXT NOT NULL,
            completed_at TEXT
        )
        """
    )
    conn.commit()
