from flask_wtf.csrf import generate_csrf
from datetime import datetime, timedelta
from forms import NoteForm
from flask import render_template, request, jsonify
from app import app
from models import Note


@app.route('/')
def index():
    return render_template('/notes.html')

# список заметок
@app.route('/notes', methods=['GET'])
def show_notes():
    notes = Note.query.all()
    if not notes:
        message = "No notes found."
    else:
        message = None
    return render_template('notes.html', notes=notes, message=message)

# добавление заметок
@app.route('/notes/add', methods=['GET', 'POST'])
def add_note():
    form = NoteForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        note = Note(title=title, content=content)
        db.session.add(note)
        db.session.commit()
        return redirect(url_for('show_notes'))
    return render_template('notes.html', form=form)

@app.route('/notes/<int:id>', methods=['GET'])
def get_note(id):
    note = Note.query.get_or_404(id)
    return jsonify(note.to_dict())

@app.route('/notes/<int:id>', methods=['PUT'])
def update_note(id):
    note = Note.query.get_or_404(id)
    data = request.get_json()
    note.title = data['title']
    note.content = data['content']
    db.session.commit()
    return jsonify({}), 204

@app.route('/notes/<int:id>', methods=['DELETE'])
def delete_note(id):
    note = Note.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return jsonify({}), 204

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['timedeltaformat'] = timedeltaformat

app.add_url_rule('/static/css/style.css', endpoint='static_css', view_func=app.send_static_file)

# if __name__ == '__main__':
#     app.debug = True
#     app.run()
