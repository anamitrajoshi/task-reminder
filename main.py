import tkinter as tk
from tkinter import messagebox
from datetime import datetime, timedelta
from tkcalendar import DateEntry
from tkinter import ttk
import threading
import pickle

class TaskListApp:

    def __init__(self, master):
        self.master = master
        self.master.title("Task Checklist")

        # Using a list to store tasks and their due dates
        self.tasks_queue = []

        # Adding background color to the master window
        self.master.configure(bg='#E2D1F9')

        self.task_entry = tk.Entry(master, width=30, bg='#FFFFFF', font='Montserrat')  
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        self.due_date_entry = DateEntry(master, width=15, background='#FFFFFF', font='Montserrat')  
        self.due_date_entry.grid(row=0, column=1, padx=5, pady=10)

        # Time picker with hours and minutes
        self.due_time_entry_hours = ttk.Combobox(master, values=[f"{i:02d}" for i in range(24)], state="readonly", width=5)
        self.due_time_entry_hours.grid(row=0, column=2, padx=5, pady=10)
        self.due_time_entry_hours.set("00")  # Default hour

        self.due_time_entry_minutes = ttk.Combobox(master, values=[f"{i:02d}" for i in range(0, 60, 15)], state="readonly", width=5)
        self.due_time_entry_minutes.grid(row=0, column=3, padx=5, pady=10)
        self.due_time_entry_minutes.set("00")  # Default minutes

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task, bg='#317773', fg='white', font='Montserrat')  # Green button
        self.add_button.grid(row=0, column=4, padx=10, pady=10)

        self.task_listbox = tk.Listbox(master, width=40, height=10, bg='#F9E795', font='Montserrat') 
        self.task_listbox.grid(row=1, column=0, columnspan=4, padx=10, pady=10)

        self.remove_button = tk.Button(master, text="Remove Task", command=self.remove_task,
                                       bg='#F96167', fg='white', font='Montserrat')  
        self.remove_button.grid(row=0, column=5, padx=10, pady=10)

        self.save_button = tk.Button(master, text="Save Tasks", command=self.save_tasks, bg='#FFA07A', font='Montserrat')
        self.save_button.grid(row=1, column=4, padx=10, pady=10)

        self.load_tasks()  # Load saved tasks on startup
        self.update_reminders()  # Start the reminder thread

        self.master.protocol("WM_DELETE_WINDOW", self.on_close)

    def add_task(self):
        task = self.task_entry.get()
        due_date = self.due_date_entry.get_date()
        due_time_hours = self.due_time_entry_hours.get()
        due_time_minutes = self.due_time_entry_minutes.get()

        if task and due_date and due_time_hours and due_time_minutes:
            due_datetime = datetime.combine(due_date, datetime.min.time()) + timedelta(hours=int(due_time_hours), minutes=int(due_time_minutes))
            formatted_due_datetime = due_datetime.strftime("%Y-%m-%d %H:%M:%S")
            
            task_with_due_date = f"{task} (Due: {formatted_due_datetime})"
            self.tasks_queue.append((task_with_due_date, due_datetime))
            self.task_listbox.insert(tk.END, task_with_due_date)
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

    def update_reminders(self):
        # Separate thread to continuously check for reminders
        def check_reminders():
            while True:
                now = datetime.now()
                for task, due_datetime in self.tasks_queue:
                    if now >= due_datetime:
                        self.show_reminder(task)
                        self.tasks_queue.remove((task, due_datetime))
                        self.task_listbox.delete(0, tk.END)  # Refresh the listbox
                        for t, _ in self.tasks_queue:
                            self.task_listbox.insert(tk.END, t)
                tk._default_root.after(60000, check_reminders)  # Check every minute

        threading.Thread(target=check_reminders, daemon=True).start()

    def show_reminder(self, task):
        messagebox.showinfo("Reminder", f"It's time for:\n{task}")

    def save_tasks(self):
        # Save tasks to a file using pickle
        with open("tasks.pkl", "wb") as file:
            pickle.dump(self.tasks_queue, file)

    def load_tasks(self):
        # Load tasks from a file using pickle
        try:
            with open("tasks.pkl", "rb") as file:
                self.tasks_queue = pickle.load(file)
                for task, _ in self.tasks_queue:
                    self.task_listbox.insert(tk.END, task)
        except FileNotFoundError:
            pass

    def on_close(self):
        # Save tasks on exit
        self.save_tasks()
        if messagebox.askokcancel("Exit", "Do you want to exit?"):
            self.master.destroy()

def main():
    root = tk.Tk()
    app = TaskListApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
