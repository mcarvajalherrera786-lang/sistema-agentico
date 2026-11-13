# SPEC: Aplicación CLI de tareas con SQLite

## Requisitos funcionales
- RF-001: Crear tarea con título obligatorio, descripción opcional, prioridad (`alta`, `media`, `baja`) y fecha límite en formato `YYYY-MM-DD`.
- RF-002: Listar tareas filtrando por estado (`pendiente`, `completada`, `todas`) y ordenadas por prioridad.
- RF-003: Marcar una tarea como completada por su ID.
- RF-004: Eliminar una tarea por su ID.
- RF-005: Validar entradas: rechazar títulos vacíos, prioridades inválidas o fechas mal formateadas con mensajes de error claros.

## Contratos de funciones / APIs
- `init_db(conn) -> None`: crea la tabla `tasks` si no existe.
- `create_task(conn, title: str, description: str = "", priority: str = "media", deadline: str | None = None) -> Task`: valida y persiste; lanza `ValueError` con mensaje claro si el título está vacío, la prioridad es inválida o la fecha no tiene formato `YYYY-MM-DD`.
- `list_tasks(conn, status: str = "todas") -> list[Task]`: devuelve tareas filtradas por estado y ordenadas por prioridad (alta > media > baja).
- `complete_task(conn, task_id: int) -> Task`: marca la tarea como `completada` (con timestamp); lanza error si el ID no existe.
- `delete_task(conn, task_id: int) -> bool`: elimina la tarea por ID; lanza error si el ID no existe.

## Casos borde
- Título vacío o solo espacios → rechazar con error de validación.
- Prioridad fuera de {`alta`, `media`, `baja`} → rechazar.
- Fecha límite con formato distinto de `YYYY-MM-DD` o valor inválido (ej. `2026-13-45`) → rechazar.
- `complete_task` / `delete_task` con ID inexistente → error claro.

## Criterios de aceptación
- AC-001: crear tarea válida persiste y retorna la tarea con ID asignado.
- AC-002: crear tarea con título vacío no persiste y retorna error de validación.
- AC-003: listar con `status` = `pendiente` / `completada` / `todas`.
- AC-004: listar ordena por prioridad.
- AC-005: `complete_task` marca la tarea como completada.
- AC-006: `delete_task` elimina la tarea.
- AC-007: las validaciones de prioridad y fecha funcionan.

## Estructura prevista
- Paquete `tareas/`: `db.py` (SQLite en `tareas.db`), `service.py` (lógica de negocio + validación), `cli.py` (interfaz de línea de comandos).
