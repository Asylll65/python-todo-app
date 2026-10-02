from flask import Flask, redirect, render_template, request

app = Flask(__name__)


# Паттерн Наблюдатель (Observer)
class EventManager:

  def __init__(self):
    self.listeners = []

  def subscribe(self, fn):
    self.listeners.append(fn)

  def notify(self, event, data):
    for fn in self.listeners:
      fn(event, data)


event_bus = EventManager()
event_bus.subscribe(
    lambda e, d: print(f"[LOG] Событие: {e}, Данные: {d}")
)


# Паттерн Модуль / Репозиторий (Module Pattern)
class TaskManager:

  def __init__(self):
    self.tasks = [{"id": 1, "title": "Изучить паттерны", "completed": False}]

  def get_all(self):
    return self.tasks

  def add(self, title):
    new_task = {
        "id": self.tasks[-1]["id"] + 1 if self.tasks else 1,
        "title": title,
        "completed": False,
    }
    self.tasks.append(new_task)
    event_bus.notify("ADD", new_task)

  def toggle(self, task_id):
    for t in self.tasks:
      if t["id"] == task_id:
        t["completed"] = not t["completed"]
        event_bus.notify("TOGGLE", t)

  def delete(self, task_id):
    self.tasks = [t for t in self.tasks if t["id"] != task_id]
    event_bus.notify("DELETE", task_id)


manager = TaskManager()


@app.route("/")
def index():
  return render_template("index.html", tasks=manager.get_all())


@app.route("/add", methods=["POST"])
def add():
  if title := request.form.get("title"):
    manager.add(title)
  return redirect("/")


@app.route("/toggle/<int:task_id>")
def toggle(task_id):
  manager.toggle(task_id)
  return redirect("/")


@app.route("/delete/<int:task_id>")
def delete(task_id):
  manager.delete(task_id)
  return redirect("/")


if __name__ == "__main__":
  app.run(debug=True)