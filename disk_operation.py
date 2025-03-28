def check_disk():
    drive = simpledialog.askstring("Input", "Enter Drive Letter (e.g., C):")
    if drive:
        def run_chkdsk():
            try:
                process = subprocess.Popen(
                    ["chkdsk", f"{drive}:"],  # Removed /F to prevent blocking
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True
                )
                output, error = process.communicate()
                output_text.delete("1.0", tk.END)
                output_text.insert(tk.END, output if output else error)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to check disk:\n{e}")
        threading.Thread(target=run_chkdsk, daemon=True).start()


# Function to optimize disk (Windows defrag)


def optimize_disk():
    drive = simpledialog.askstring("Input", "Enter Drive Letter (e.g., C):")
    if drive:
        os.system(f"defrag {drive}: /U /V")
        messagebox.showinfo("Success", "Disk Optimized Successfully!")
