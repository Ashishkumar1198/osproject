def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# If not running as admin, restart with admin rights

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()


# Function to list files in a directory

def list_files():
    try:
        directory = filedialog.askdirectory(title="Select a Folder")  # Let user choose directory
        if not directory:  # If user cancels selection
            return  

        if not os.path.exists(directory):  # Check if directory exists
            messagebox.showerror("Error", f"Directory not found: {directory}")
            return

        files = "\n".join(os.listdir(directory))  # Get list of files
        output_text.delete("1.0", tk.END)  # Clear previous output
        output_text.insert(tk.END, f"Files in {directory}:\n{files}")  # Display files in the GUI

    except Exception as e:
        messagebox.showerror("Error", f"Could not list files: {str(e)}")

# Function to deleted files 

def delete_file():
    file_path = filedialog.askopenfilename(title="Select File to Delete")

    if not file_path:
        return  # User canceled the file selection

    file_path = os.path.normpath(file_path)  # Normalize the path

    confirm = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete:\n{file_path}")
    if not confirm:
        return

    try:
        send2trash.send2trash(file_path)
        messagebox.showinfo("Success", f"Moved to Recycle Bin: {file_path}")

    except PermissionError:
        try:
            os.chmod(file_path, stat.S_IWRITE)  # Remove Read-Only
            os.remove(file_path)  # Delete the file
            messagebox.showinfo("Success", f"Deleted: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not delete file due to permission error:\n{e}")

    except Exception as e:
        messagebox.showerror("Error", f"Could not delete file:\n{e}")

# Function to list deleted files using PowerShell


def list_deleted_files():
    """Fetch actual deleted files from the Recycle Bin UI (not system metadata)."""
    try:
        pythoncom.CoInitialize()
        shell = win32com.client.Dispatch("Shell.Application")
        recycle_bin = shell.NameSpace(10)  # 10 is the Recycle Bin special folder

        files = [
            f"Deleted File: {item.Name}\nOriginal Path: {item.Path}"
            for item in recycle_bin.Items()
        ]

        if not files:
            messagebox.showinfo("Info", "🗑️ No files currently in the Recycle Bin.")
            return

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, "\n\n".join(files))

    except Exception as e:
        messagebox.showerror("Error", f"⚠️ Error: {str(e)}")


# Function to restore files using Shadow Copies


def recover_files():
    try:
        pythoncom.CoInitialize()
        shell = win32com.client.Dispatch("Shell.Application")
        recycle_bin = shell.NameSpace(10)

        files = {item.Name: item.Path for item in recycle_bin.Items()}
        if not files:
            messagebox.showinfo("Info", "🗑️ No files in the Recycle Bin.")
            return

        file_to_restore = simpledialog.askstring(
            "Restore File", f"Enter the name of the file to restore:\n{', '.join(files.keys())}"
        )
        if not file_to_restore or file_to_restore not in files:
            messagebox.showerror("Error", f"⚠️ File '{file_to_restore}' not found in the Recycle Bin.")
            return

        restore_location = "C:\\os\\recovered_file"
        os.makedirs(restore_location, exist_ok=True)

        original_extension = os.path.splitext(files[file_to_restore])[1]
        new_file_path = os.path.join(restore_location, file_to_restore + original_extension)

        shutil.move(files[file_to_restore], new_file_path)

        messagebox.showinfo("Success", f"✅ '{file_to_restore}' has been restored to {restore_location}!")

    except Exception as e:
        messagebox.showerror("Error", f"⚠️ Restore failed: {str(e)}")

    finally:
        pythoncom.CoUninitialize()
