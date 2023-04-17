import os
from flask import Flask, render_template, request, redirect, url_for, jsonify, send_from_directory
from flask_wtf.csrf import generate_csrf
from filters import datetimeformat, timedeltaformat
from forms import NoteForm
from models import Note
from database import db, session_scope
from datetime import datetime, timedelta



project_root = os.path.dirname(__file__)
template_path = os.path.join(project_root, 'templates')
static_path = os.path.join(project_root, 'static')

app = Flask(__name__, template_folder=template_path, static_folder=static_path)
app.config.from_object('config')

db.init_app(app)

app.jinja_env.filters['datetimeformat'] = datetimeformat
app.jinja_env.filters['timedeltaformat'] = timedeltaformat
app.jinja_env.globals['csrf_token'] = generate_csrf

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    note = {'id': 1, 'title': 'My Note', 'body': 'Lorem ipsum dolor sit amet...'}
    form = NoteForm()
    return render_template('/notes.html', form=form, note=note)

# список заметок
@app.route('/notes', methods=['GET'])
def show_notes():
    notes = Note.query.all()
    if not notes:
        message = "No notes found."
    else:
        message = None
    form = NoteForm()
    return render_template('notes.html', form=form, notes=notes, message=message)

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

@app.route('/notes/<int:id>', methods=['POST', 'DELETE'])
def delete_note(id):
    if request.method == 'DELETE':
        note = Note.query.get_or_404(id)
        print('Deleting note:', note) # отладочная информация
        db.session.delete(note)
        db.session.commit()
        return jsonify({}), 204
    return jsonify({"error": "invalid method"}), 405

@app.errorhandler(500)
def internal_server_error(e):
    return str(e), 500

@app.route('/static/css/style.css')
def send_static():
    return send_from_directory('static', 'css/style.css')

@app.route('/static/<path:filename>')
def serve_static(filename):
    root_dir = os.path.dirname(os.getcwd())
    return send_from_directory(os.path.join(root_dir, 'static'), filename)

@app.after_request
def add_cache_control(response):
    response.headers['Cache-Control'] = 'public, max-age=60'
    expires = datetime.now() + timedelta(minutes=1)
    response.headers['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
    return response

if __name__ == '__main__':
    app.debug = True
    app.run()

