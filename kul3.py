import psutil
import tkinter as tk
from tkinter import ttk
from threading import Thread
import time

class SystemMonitor(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.title("System Monitor")

        self.label_ram = ttk.Label(self, text="RAM Kullanımı: ")
        self.label_ram.pack()

        self.label_cpu = ttk.Label(self, text="CPU Kullanımı: ")
        self.label_cpu.pack()

        self.tree = ttk.Treeview(self, columns=("PID", "İsim", "CPU Kullanımı", "RAM Kullanımı"))
        self.tree.heading("#0", text="PID")
        self.tree.heading("#1", text="İsim")
        self.tree.heading("#2", text="CPU Kullanımı")
        self.tree.heading("#3", text="RAM Kullanımı")
        self.tree.pack()

        self.update_labels()
        self.update_tree()

    def update_labels(self):
        ram = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)

        self.label_ram.config(text=f"RAM Kullanımı: {ram.percent}%")
        self.label_cpu.config(text=f"CPU Kullanımı: {cpu}%")

        self.after(1000, self.update_labels)

    def update_tree(self):
        self.tree.delete(*self.tree.get_children())

        processes = psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent'])
        for process in processes:
            self.tree.insert("", "end", values=(
                process.info['pid'],
                process.info['name'],
                f"{process.info['cpu_percent']}%",
                f"{process.info['memory_percent']}%"
            ))

        self.after(5000, self.update_tree)

def run_gui():
    app = SystemMonitor()
    app.geometry("400x300")
    app.mainloop()

def run_system_monitor():
    while True:
        time.sleep(5)
        print("Updating system info...")

if __name__ == "__main__":
    # Başka bir thread'de GUI çalıştır
    gui_thread = Thread(target=run_gui)
    gui_thread.start()

    # Ana thread'de sistem bilgilerini güncelle
    run_system_monitor()
