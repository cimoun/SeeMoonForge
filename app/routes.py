from flask import Blueprint, abort, jsonify, redirect, render_template, request, url_for

from .models import (
    create_note,
    delete_note,
    get_all_notes,
    get_note_by_id,
    toggle_pin,
    update_note,
)

bp = Blueprint("notes", __name__)


@bp.route("/")
def index():
    notes = get_all_notes()
    return render_template("index.html", notes=notes)


@bp.route("/notes/new")
def new():
    return render_template("edit.html", note=None, error=None)


@bp.route("/notes", methods=["POST"])
def create():
    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title:
        return render_template("edit.html", note=None, error="Заголовок обязателен"), 400

    create_note(title, content)
    return redirect(url_for("notes.index"))


@bp.route("/notes/<int:note_id>/edit")
def edit(note_id: int):
    note = get_note_by_id(note_id)
    if not note:
        abort(404)
    return render_template("edit.html", note=note, error=None)


@bp.route("/notes/<int:note_id>", methods=["POST"])
def update(note_id: int):
    note = get_note_by_id(note_id)
    if not note:
        abort(404)

    title = request.form.get("title", "").strip()
    content = request.form.get("content", "").strip()

    if not title:
        return render_template("edit.html", note=note, error="Заголовок обязателен"), 400

    update_note(note_id, title, content)
    return redirect(url_for("notes.index"))


@bp.route("/notes/<int:note_id>/pin", methods=["POST"])
def pin(note_id: int):
    new_state = toggle_pin(note_id)
    if new_state is None:
        abort(404)
    return jsonify({"pinned": new_state})


@bp.route("/notes/<int:note_id>/delete", methods=["POST"])
def delete(note_id: int):
    if not delete_note(note_id):
        abort(404)
    return redirect(url_for("notes.index"))
