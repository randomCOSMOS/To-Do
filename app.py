from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())


@app.route('/')
def hello_world():
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks=tasks)


# entering task
@app.route('/enterTask', methods=['POST'])
def ok():
    task_content = request.form['content']
    if task_content != "":
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            error = "There was an issue adding your request"
            return redirect(url_for('got_error', err=error))
    else:
        error = "Input can't be blank"
        return redirect(url_for('got_error', err=error))


# deleting task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        error = 'There was a problem deleting that'
        return redirect(url_for('got_error', err=error))


# updating task
@app.route('/edit/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task_content = request.form['content']

        if task_content != "":
            task.content = task_content
            try:
                db.session.commit()
                return redirect('/')
            except:
                return redirect(url_for('got_error', err="There was a problem updating that."))
        else:
            return redirect(url_for('got_error', err="Oops! Can't be blank."))
    else:
        return render_template('update.html', task=task)


# handling error
@app.route('/error/<err>')
def got_error(err):
    tasks = Todo.query.order_by(Todo.date_created).all()
    return render_template('index.html', tasks=tasks, error=err)


if __name__ == '__main__':
    app.run(debug=True)
