import argparse
import sys

from . import db, service


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser de comandos de la CLI."""
    parser = argparse.ArgumentParser(prog="tareas", description="CLI de gestion de tareas")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Crear tarea")
    add_parser.add_argument("--title", required=True, help="Titulo obligatorio")
    add_parser.add_argument("--description", default="", help="Descripcion opcional")
    add_parser.add_argument("--priority", default="media", choices=["alta", "media", "baja"])
    add_parser.add_argument("--deadline", default=None, help="Fecha limite YYYY-MM-DD")

    list_parser = subparsers.add_parser("list", help="Listar tareas")
    list_parser.add_argument("--status", choices=["pendiente", "completada", "todas"], default="todas")

    complete_parser = subparsers.add_parser("complete", help="Marcar tarea como completada")
    complete_parser.add_argument("--id", type=int, required=True)

    delete_parser = subparsers.add_parser("delete", help="Eliminar tarea")
    delete_parser.add_argument("--id", type=int, required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Ejecuta la CLI de tareas."""
    parser = build_parser()
    args = parser.parse_args(argv)
    conn = db.get_connection()
    db.init_db(conn)
    try:
        if args.command == "add":
            task = service.create_task(conn, args.title, args.description, args.priority, args.deadline)
            print(f"Tarea creada: id={task.id}, prioridad={task.priority}, estado={task.status}")
        elif args.command == "list":
            tasks = service.list_tasks(conn, args.status)
            if not tasks:
                print("No hay tareas.")
            for task in tasks:
                deadline = task.deadline or "-"
                print(f"[{task.id}] {task.priority} | {task.status} | {task.title} | deadline={deadline}")
        elif args.command == "complete":
            task = service.complete_task(conn, args.id)
            print(f"Tarea {task.id} completada.")
        elif args.command == "delete":
            service.delete_task(conn, args.id)
            print(f"Tarea {args.id} eliminada.")
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    finally:
        conn.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
