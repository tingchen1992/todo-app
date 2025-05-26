from flask import Flask, render_template, request, redirect, url_for
from models.task import Task
from form import TaskForm

app = Flask(__name__)
app.secret_key = "secret123"  


@app.route("/")
@app.route("/<filter_status>")
def index(filter_status="all"):
    tasks = Task.get_all(filter_status)
    form = TaskForm()
    return render_template(
        "index.html", tasks=tasks, form=form, filter_status=filter_status
    )


@app.route("/add", methods=["POST"])
def add_task():
    form = TaskForm()
    if form.validate_on_submit():
        Task.create(form.title.data)
    return redirect(url_for("index"))


@app.route("/complete/<int:task_id>")
def complete_task(task_id):
    task = Task(task_id, "", False)
    task.mark_complete()
    return redirect(request.referrer or url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    task = Task(task_id, "", False)
    task.soft_delete()
    return redirect(url_for("index"))
