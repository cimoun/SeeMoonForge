from dataclasses import dataclass
from datetime import datetime

from .db import get_db


@dataclass
class Note:
    id: int
    title: str
    content: str
    pinned: bool
    created_at: datetime
    updated_at: datetime


def _row_to_note(row) -> Note:
    return Note(
        id=row["id"],
        title=row["title"],
        content=row["content"],
        pinned=bool(row["pinned"]),
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def get_all_notes() -> list[Note]:
    rows = get_db().execute(
        "SELECT * FROM notes ORDER BY pinned DESC, updated_at DESC"
    ).fetchall()
    return [_row_to_note(r) for r in rows]


def get_note_by_id(note_id: int) -> Note | None:
    row = get_db().execute(
        "SELECT * FROM notes WHERE id = ?", (note_id,)
    ).fetchone()
    return _row_to_note(row) if row else None


def create_note(title: str, content: str) -> Note:
    db = get_db()
    cursor = db.execute(
        "INSERT INTO notes (title, content) VALUES (?, ?)",
        (title, content),
    )
    db.commit()
    return get_note_by_id(cursor.lastrowid)  # type: ignore[arg-type]


def update_note(note_id: int, title: str, content: str) -> Note | None:
    db = get_db()
    db.execute(
        """UPDATE notes
           SET title = ?, content = ?, updated_at = strftime('%Y-%m-%dT%H:%M:%S', 'now')
           WHERE id = ?""",
        (title, content, note_id),
    )
    db.commit()
    return get_note_by_id(note_id)


def toggle_pin(note_id: int) -> bool | None:
    db = get_db()
    db.execute(
        """UPDATE notes
           SET pinned = 1 - pinned, updated_at = strftime('%Y-%m-%dT%H:%M:%S', 'now')
           WHERE id = ?""",
        (note_id,),
    )
    db.commit()
    note = get_note_by_id(note_id)
    return note.pinned if note else None


def delete_note(note_id: int) -> bool:
    db = get_db()
    cursor = db.execute("DELETE FROM notes WHERE id = ?", (note_id,))
    db.commit()
    return cursor.rowcount > 0
