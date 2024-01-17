import tkinter as tk
from tkinter import messagebox
from queue import Queue


class TaskListApp:

  def __init__(self, master):
    self.master = master
    self.master.title("Task Checklist")

    self.tasks_queue = Queue()

    self.task_entry = tk.Entry(master, width=30)
    self.task_entry.grid(row=0, column=0, padx=10, pady=10)

    self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
    self.add_button.grid(row=0, column=1, padx=10, pady=10)

    self.task_listbox = tk.Listbox(master, width=40, height=10)
    self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    self.remove_button = tk.Button(master,
                                   text="Remove Task",
                                   command=self.remove_task)
    self.remove_button.grid(row=0, column=2, padx=10, pady=10)

    self.checkboxes = []  # List to store checkboxes

    self.master.protocol("WM_DELETE_WINDOW", self.on_close)

  def add_task(self):
    task = self.task_entry.get()
    if task:
      self.tasks_queue.put(task)
      self.task_listbox.insert(tk.END, task)
      self.task_entry.delete(0, tk.END)

      # Add a checkbox for the new task
      checkbox = tk.Checkbutton(self.master, text=task)
      checkbox.grid(row=len(self.checkboxes) + 2, column=0, sticky="w")
      checkbox.var = tk.IntVar()
      checkbox.config(variable=checkbox.var)
      self.checkboxes.append(checkbox)

      checkbox.var.trace("w", self.dequeue_checked_tasks)
    else:
      messagebox.showwarning("Input Error", "Please enter a task.")

  def dequeue_checked_tasks(self, *args):
    for checkbox in self.checkboxes:
      if checkbox.var.get():
        task_index = self.task_listbox.get(0,
                                           tk.END).index(checkbox.cget("text"))
        self.task_listbox.delete(task_index)
        self.tasks_queue.get()

  def remove_task(self):
    selected_task_index = self.task_listbox.curselection()
    if selected_task_index:
      self.task_listbox.delete(selected_task_index)
      removed_task = self.tasks_queue.get()
      messagebox.showinfo("Task Removed",
                          f"Task '{removed_task}' removed successfully.")
    else:
      messagebox.showwarning("Selection Error",
                             "Please select a task to remove.")

  def on_close(self):
    if messagebox.askokcancel("Exit", "Do you want to exit?"):
      self.master.destroy()


def main():
  root = tk.Tk()
  app = TaskListApp(root)
  root.mainloop()


if __name__ == "__main__":
  main()

