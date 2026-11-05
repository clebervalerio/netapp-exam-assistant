import tkinter as tk
import time

class FloatingStopwatch:
    def __init__(self, root):
        self.root = root
        self.root.title("NetApp Timer")
        self.root.attributes("-topmost", True)
        self.root.geometry("210x90+50+50")
        self.root.configure(bg="#1e1e1e")
        self.root.resizable(False, False)
        
        self.start_time = None
        self.running = False
        self.elapsed = 0
        
        self.lbl_time = tk.Label(root, text="00:00.0", font=("Consolas", 24, "bold"), fg="#4ade80", bg="#1e1e1e")
        self.lbl_time.pack(pady=4)
        
        btn_frame = tk.Frame(root, bg="#1e1e1e")
        btn_frame.pack()
        
        self.btn_toggle = tk.Button(btn_frame, text="Iniciar", width=6, command=self.toggle, bg="#10b981", fg="white", relief="flat")
        self.btn_toggle.grid(row=0, column=0, padx=4)
        
        self.btn_reset = tk.Button(btn_frame, text="Zerar", width=6, command=self.reset, bg="#4b5563", fg="white", relief="flat")
        self.btn_reset.grid(row=0, column=1, padx=4)
        
        self.update_timer()

    def toggle(self):
        if self.running:
            self.running = False
            self.btn_toggle.config(text="Iniciar", bg="#10b981")
        else:
            self.start_time = time.time() - self.elapsed
            self.running = True
            self.btn_toggle.config(text="Pausar", bg="#f59e0b")

    def reset(self):
        self.running = False
        self.elapsed = 0
        self.btn_toggle.config(text="Iniciar", bg="#10b981")
        self.lbl_time.config(text="00:00.0")

    def update_timer(self):
        if self.running:
            self.elapsed = time.time() - self.start_time
            minutes = int(self.elapsed // 60)
            seconds = int(self.elapsed % 60)
            tenths = int((self.elapsed * 10) % 10)
            self.lbl_time.config(text=f"{minutes:02d}:{seconds:02d}.{tenths}")
        self.root.after(50, self.update_timer)

if __name__ == "__main__":
    root = tk.Tk()
    app = FloatingStopwatch(root)
    root.mainloop()

