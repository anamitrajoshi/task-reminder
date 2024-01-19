import tkinter as tk
from tkinter import messagebox

class TaskListApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Task Checklist")

        # Using a list as a simple queue
        self.tasks_queue = []

        # Adding background color to the master window
        self.master.configure(bg='#E2D1F9')

        self.task_entry = tk.Entry(master, width=30, bg='#FFFFFF', font='Montsserat')  
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task, bg='#317773', fg='white', font='Montsserat')  # Green button
        self.add_button.grid(row=0, column=1, padx=10, pady=10)

        self.task_listbox = tk.Listbox(master, width=40, height=10, bg='#F9E795', font='Montsserat') 
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.remove_button = tk.Button(master, text="Remove Task", command=self.remove_task,
                                       bg='#F96167', fg='white', font='Montsserat')  
        self.remove_button.grid(row=0, column=2, padx=10, pady=10)

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks_queue.append(task)
            self.task_listbox.insert(tk.END, task)
            self.task_entry.delete(0, tk.END)

    def remove_task(self):
        selected_task_index = self.task_listbox.curselection()
        if selected_task_index:
            removed_task = self.tasks_queue.pop(selected_task_index[0])
            self.task_listbox.delete(selected_task_index)
            messagebox.showinfo("Task Removed", "Task Removed successfully.")
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
