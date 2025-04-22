import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, simpledialog, ttk
from tkinter.font import Font
import os
import datetime
import ctypes
import magic
from PIL import Image, ImageTk
from io import BytesIO

# === Admin Rights Check ===
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    tk.Tk().withdraw()
    messagebox.showerror("Admin Required", "\u26a0\ufe0f Please run as Administrator.")
    exit()

# === File Signature Mapping (Cleaned) ===
file_signatures = {
    "PDF": b"%PDF",
    "DOC": b"\xD0\xCF\x11\xE0",
    "PPTX": b"PK\x03\x04",
    "PPT": b"\xD0\xCF\x11\xE0",
    "JPG": b"\xFF\xD8\xFF",
    "PNG": b"\x89PNG\r\n\x1a\n",
}

recovery_log = []
recovered_bytes = b""

# === Create Disk Image ===
def create_disk_image(drive_letter="E", save_folder="backups"):
    try:
        os.makedirs(save_folder, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
        filename = f"recovery_{timestamp}.img"
        full_path = os.path.join(save_folder, filename)
        drive_path = f"\\\\.\\{drive_letter.upper()}:"

        with open(drive_path, 'rb') as drive, open(full_path, 'wb') as img:
            while True:
                chunk = drive.read(1024 * 1024)
                if not chunk:
                    break
                img.write(chunk)

        return full_path
    except Exception as e:
        messagebox.showerror("Backup Error", f"Could not create disk image:\n{str(e)}")
        return None

def manual_disk_image():
    drive_letter = simpledialog.askstring("Drive Letter", "Enter drive letter (e.g., E):")
    if not drive_letter:
        return
    path = create_disk_image(drive_letter)
    if path:
        entry_img_path.delete(0, tk.END)
        entry_img_path.insert(0, path)
        messagebox.showinfo("Success", f"Disk image created:\n{path}")

# === File Type Detection ===
def detect_file_type_from_bytes(data):
    try:
        mime = magic.Magic(mime=True)
        return mime.from_buffer(data)
    except:
        return "application/octet-stream"

def get_extension_from_mime(mime_type):
    mapping = {
        "application/pdf": ".pdf",
        "image/jpeg": ".jpg",
        "image/png": ".png",
        "application/vnd.ms-powerpoint": ".ppt",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": ".pptx",
        "application/msword": ".doc",
    }
    return mapping.get(mime_type, ".bin")

# === Recovery Logic ===
def show_keyword_popup():
    info = "\n".join([f"{k}: '{v.decode(errors='ignore')}'" if v else f"{k}: [text based]" for k, v in file_signatures.items()])
    messagebox.showinfo("Keyword Help", f"Use these keywords for file types:\n\n{info}")

def recover_file():
    global recovered_bytes
    path = entry_img_path.get()
    filetype = combo_filetype.get()
    keyword = file_signatures.get(filetype, b"")

    if not path or not os.path.exists(path):
        messagebox.showerror("Missing File", "Please select a valid disk image file.")
        return

    try:
        with open(path, "rb") as f:
            data = f.read()
            index = data.find(keyword)
            if index == -1:
                messagebox.showinfo("Not Found", f"Keyword not found for {filetype}.")
                return

            recovered_bytes = data[index: index + 50 * 1024 * 1024]
            text_output.delete(1.0, tk.END)
            text_output.insert(tk.END, recovered_bytes[:300].decode(errors="replace"))
            messagebox.showinfo("Recovered", f"{filetype} recovered! Offset: {index}")
            recovery_log.append({"filetype": filetype, "offset": index, "status": "Success"})

    except Exception as e:
        recovery_log.append({"filetype": filetype, "offset": -1, "status": f"Error: {str(e)}"})
        messagebox.showerror("Error", str(e))

# === Save Recovered File ===
def save_recovered_file():
    global recovered_bytes
    if not recovered_bytes:
        messagebox.showwarning("Nothing to Save", "Recover file first.")
        return
    mime = detect_file_type_from_bytes(recovered_bytes)
    ext = get_extension_from_mime(mime)
    path = filedialog.asksaveasfilename(defaultextension=ext)
    if path:
        with open(path, "wb") as f:
            f.write(recovered_bytes)
        messagebox.showinfo("Saved", f"Saved as {os.path.basename(path)}")

# === Delete File ===
def delete_file():
    path = filedialog.askopenfilename(title="Select file to delete")
    if path:
        try:
            os.remove(path)
            messagebox.showinfo("Deleted", f"File deleted:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))

# === GUI Setup ===
root = tk.Tk()
root.title("\ud83d\udd0d Smart File Recovery Tool")
root.geometry("800x650")
root.resizable(False, False)

label_font = Font(family="Segoe UI", size=10)

tk.Label(root, text="\ud83d\udcc2 Disk Image Path", font=label_font).place(x=20, y=20)
entry_img_path = tk.Entry(root, width=70)
entry_img_path.place(x=160, y=22)
tk.Button(root, text="Browse", command=lambda: entry_img_path.insert(0, filedialog.askopenfilename())).place(x=650, y=20)

btns = [
    ("\ud83d\udcf8 Create Disk Image", manual_disk_image, 20),
    ("\ud83d\uddd1\ufe0f Delete File", delete_file, 240),
]
for label, command, x in btns:
    tk.Button(root, text=label, width=25, command=command).place(x=x, y=60)

tk.Label(root, text="\ud83d\udcc4 Select File Type to Recover", font=label_font).place(x=20, y=110)
combo_filetype = ttk.Combobox(root, values=list(file_signatures.keys()), width=30)
combo_filetype.place(x=220, y=110)
combo_filetype.set("PDF")

tk.Button(root, text="❓ File Keywords", command=show_keyword_popup).place(x=480, y=110)
tk.Button(root, text="\ud83d\udd0d Recover File", width=20, bg="darkgreen", fg="white", command=recover_file).place(x=620, y=108)

tk.Button(root, text="\ud83d\udcbe Save Recovered File", width=25, command=save_recovered_file).place(x=320, y=150)

text_output = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=92, height=22)
text_output.place(x=20, y=200)

root.mainloop()
