import tkinter as tk
from tkinter import ttk
import sqlite3

# Create or connect to the SQLite database
connection = sqlite3.connect("task_manager.db")
cursor = connection.cursor()

# Create a tasks table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY,
    task_text TEXT,
    completed INTEGER
)
""")
connection.commit()

# Define functions for database operations
def add_task_to_db(task_text):
    cursor.execute("INSERT INTO tasks (task_text, completed) VALUES (?, ?)", (task_text, 0))
    connection.commit()

def load_tasks_from_db():
    cursor.execute("SELECT task_text, completed FROM tasks")
    tasks = cursor.fetchall()
    for task_text, completed in tasks:
        task_list.insert(tk.END, task_text)
        if completed:
            task_list.itemconfig(tk.END, {'bg': '#DFF0D8', 'selectbackground': '#DFF0D8'})

def add_task():
    task_text = task_entry.get()
    if task_text:
        task_list.insert(tk.END, task_text)
        add_task_to_db(task_text)
        task_entry.delete(0, tk.END)

def remove_task():
    selected_task = task_list.curselection()
    if selected_task:
        task_text = task_list.get(selected_task[0])
        cursor.execute("DELETE FROM tasks WHERE task_text=?", (task_text,))
        connection.commit()
        task_list.delete(selected_task)

def mark_completed():
    selected_task = task_list.curselection()
    if selected_task:
        task_text = task_list.get(selected_task[0])
        cursor.execute("UPDATE tasks SET completed=1 WHERE task_text=?", (task_text,))
        connection.commit()
        task_list.itemconfig(selected_task, {'bg': '#DFF0D8', 'selectbackground': '#DFF0D8'})

# Create the main window
root = tk.Tk()
root.title("Task Manager")
root.geometry("600x400")

# Create and configure a style using the 'clam' theme
style = ttk.Style()
style.theme_use('clam')

# Customize the 'TButton' style for buttons
style.configure("TButton", foreground="white", background="#4CAF50", font=("Arial", 12))
style.map("TButton", foreground=[('active', 'white')], background=[('active', '#45a049')])

# Set the 'TFrame' style's background color to change the frame background
style.configure("TFrame", background="#f2f2f2")

# Create and configure a frame for styling
style_frame = ttk.Frame(root, style="TFrame")
style_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

# Create a container frame without specifying background
container = ttk.Frame(style_frame)
container.pack(fill=tk.BOTH, expand=True)

# Create and configure the task list with a different selection color
task_list = tk.Listbox(container, selectbackground="#42a5f5", font=("Arial", 12), selectmode=tk.SINGLE, height=10)
task_list.pack(pady=10, fill=tk.BOTH, expand=True)

# Create and configure the task entry field
task_entry = ttk.Entry(container, font=("Arial", 12))
task_entry.pack(pady=5, fill=tk.BOTH)

# Load tasks from the database
load_tasks_from_db()

# Create and configure buttons with improved styling
add_button = ttk.Button(container, text="Add Task", command=add_task)
remove_button = ttk.Button(container, text="Remove Task", command=remove_task)
done_button = ttk.Button(container, text="Mark Completed", command=mark_completed)

add_button.pack(pady=5, fill=tk.BOTH)
remove_button.pack(pady=5, fill=tk.BOTH)
done_button.pack(pady=5, fill=tk.BOTH)

# Run the application
root.mainloop()

# Close the database connection when the application exits
connection.close()
