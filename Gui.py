root = tk.Tk()
root.title("🖥 File System Recovery & Optimization")
root.geometry("750x500")
root.resizable(False, False)
root.configure(bg="#2C2F33")  # Dark Background

# --- Custom Styling ---

style = ttk.Style()
style.configure("TButton", font=("Arial", 11, "bold"), padding=8, background="#7289DA", foreground="white")
style.configure("TLabel", background="#2C2F33", foreground="white", font=("Arial", 14, "bold"))
style.configure("TFrame", background="#2C2F33")
style.configure("TText", font=("Arial", 11), background="#23272A", foreground="white")

# --- Gradient Header ---

header = tk.Canvas(root, width=750, height=80, bg="#7289DA", highlightthickness=0)
header.create_rectangle(0, 0, 750, 80, fill="#7289DA")
header.create_text(375, 40, text="💾 File System Recovery & Optimization", fill="white", font=("Arial", 16, "bold"))
header.pack()

# --- Buttons Frame ---

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

# --- Button Styles ---

def on_enter(e):
    e.widget["background"] = "#99AAB5"

def on_leave(e):
    e.widget["background"] = e.widget.default_color

buttons = [
    ("📂 List Files", list_files, "#3498db"),
    ("🗑 List Deleted Files", list_deleted_files, "#8e44ad"),
    ("🔄 Recover File", recover_files, "#27ae60"),
    ("🛠 Check Disk", check_disk, "#f39c12"),
    ("🚀 Optimize Disk", optimize_disk, "#e74c3c"),
    ("❌ Delete File", delete_file, "#c0392b")
]

for i, (text, cmd, color) in enumerate(buttons):
    row, col = divmod(i, 2)
    btn = tk.Button(button_frame, text=text, command=cmd, font=("Arial", 11, "bold"),
                    bg=color, fg="white", width=22, height=2, relief="flat")
    btn.default_color = color
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    btn.grid(row=row, column=col, padx=10, pady=5)

# --- Output Box ---

output_frame = ttk.Frame(root)
output_frame.pack(pady=15, fill="both", expand=True)

output_text = tk.Text(output_frame, height=10, width=80, font=("Arial", 11), bg="#23272A", fg="white", wrap="word")
output_text.pack(side="left", fill="both", expand=True)

scrollbar = ttk.Scrollbar(output_frame, command=output_text.yview)
scrollbar.pack(side="right", fill="y")
output_text.config(yscrollcommand=scrollbar.set)

# --- Run Tkinter Main Loop ---

root.mainloop()
