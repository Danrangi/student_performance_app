import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import StudentPerformanceApp

def main():
    try:
        # Create the main application window
        root = tk.Tk()
        app = StudentPerformanceApp(root)
        
        # Start the application
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Application Error", f"Failed to start application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
