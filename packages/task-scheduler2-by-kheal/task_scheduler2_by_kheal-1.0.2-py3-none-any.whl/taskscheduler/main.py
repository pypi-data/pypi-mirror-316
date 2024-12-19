# Main entry point of the application
from tkinter import Tk
from taskscheduler.ui import TaskSchedulerApp

root = Tk()
app = TaskSchedulerApp(root)
root.mainloop()
