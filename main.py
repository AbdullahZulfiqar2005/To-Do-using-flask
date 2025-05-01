from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from flask import redirect, url_for

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=True)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"ToDo('{self.task}', '{self.completed}')"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        task = request.form.get("task")
        description = request.form.get("description")
        if task:
            new_todo = ToDo(task=task, description=description)
            db.session.add(new_todo)
            db.session.commit()

    todos = ToDo.query.all()
    return render_template("index.html", todos=todos)


@app.route("/delete/<int:id>")
def delete(id):
    task = ToDo.query.get_or_404(id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    task = ToDo.query.get_or_404(id)
    if request.method == "POST":
        task.task = request.form['task']
        task.description = request.form['description']
        task.completed = 'completed' in request.form
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("update.html", task=task)
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)