from flask import Blueprint, render_template, request, flash, jsonify
from .models import Note
from . import db
import json

# login mechanism
from flask_login import current_user, login_required

views = Blueprint("views", __name__)

@views.route("/", methods=["POST", "GET"])
@login_required # note: this is needed for login mechanism
def home():

    if request.method == "POST":
        note = request.form.get("note")
        if len(note) < 1:
            flash("Note is too short.", category="error")
        else:
            new_note = Note(Data=note, UserID=current_user.ID)
            db.session.add(new_note)
            db.session.commit()
            flash("Note is added.", category="success")

    return render_template("home.html", user=current_user)

@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteID = note["noteID"]
    note = Note.query.get(noteID)
    if note:
        if note.UserID == current_user.ID:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})