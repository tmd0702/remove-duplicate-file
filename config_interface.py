import tkinter as tk
import json
from tkinter import filedialog
settings = {
  "BUFF_SIZE": 65536,
  "FILE_EXTENSIONS": [],
  "DEST_PATH": None,
  "BASE_PATH": [],
  "IS_CACHE_WRITABLE": None,
  "IS_CACHE_READABLE": None
}#json.loads(open("configs/config.json", "r", encoding='utf-8').read())
def save_settings():
    settings["BUFF_SIZE"] = 65536
    settings["IS_CACHE_WRITABLE"] = bool(cache_writable_var.get())
    settings["IS_CACHE_READABLE"] = bool(cache_readable_var.get())
    print(settings)
    with open("configs/config.json", "w", encoding='utf8') as outfile:
        json.dump(settings, outfile, ensure_ascii=False)

    pass

def browse_base_directory():
    base_directory_path = filedialog.askdirectory()
    settings['BASE_PATH'] = [base_directory_path + "/" if base_directory_path[-1] != "/" else base_directory_path]
    base_directory_entry.delete(0, tk.END)
    base_directory_entry.insert(0, base_directory_path)

def browse_target_directory():
    target_directory_path = filedialog.askdirectory()
    settings['DEST_PATH'] = target_directory_path + "/" if target_directory_path[-1] != "/" else target_directory_path
    target_directory_entry.delete(0, tk.END)
    target_directory_entry.insert(0, target_directory_path)

def open_extension_window():
    extension_window = tk.Toplevel(root)
    extension_window.title("Extension Selection")

    # Define the list of image and audio extensions
    extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'wav', 'mp3', 'mp4', 'ogg', 'mov']

    # Create a list to store the checkbox variables
    checkbox_vars = []

    # Create a checkbox for selecting all extensions
    select_all_var = tk.IntVar()
    select_all_checkbox = tk.Checkbutton(extension_window, text="*.* (Select All)", variable=select_all_var)
    select_all_checkbox.pack()

    checkbox_vars.append(select_all_var)

    # Create checkboxes for each extension
    for ext in extensions:
        var = tk.IntVar()
        checkbox = tk.Checkbutton(extension_window, text=ext, variable=var)
        checkbox.pack()
        checkbox_vars.append(var)

    def confirm_selection():
        selected_extensions = []

        # Check the state of each checkbox
        for i in range(len(checkbox_vars)):
            if checkbox_vars[i].get() == 1:
                if i == 0:
                    selected_extensions.append("*.*")
                else:
                    selected_extensions.append(extensions[i - 1])

        # Display the selected extensions in the console (replace with desired functionality)
        settings["FILE_EXTENSIONS"] = selected_extensions
        print("Selected Extensions:")
        for ext in selected_extensions:
            print(ext)

        extension_window.destroy()

    confirm_button = tk.Button(extension_window, text="Confirm", command=confirm_selection)
    confirm_button.pack()

root = tk.Tk()

# Create a label and an entry widget for the base directory path
base_directory_label = tk.Label(root, text="Base Directory Path:")
base_directory_label.pack()

base_directory_entry = tk.Entry(root, width=50)
base_directory_entry.pack()

# Create a button to browse for the base directory
browse_base_button = tk.Button(root, text="Browse", command=browse_base_directory)
browse_base_button.pack()

# Create a label and an entry widget for the target directory path
target_directory_label = tk.Label(root, text="Target Directory Path:")
target_directory_label.pack()

target_directory_entry = tk.Entry(root, width=50)
target_directory_entry.pack()

# Create a button to browse for the target directory
browse_target_button = tk.Button(root, text="Browse", command=browse_target_directory)
browse_target_button.pack()

# Create a label and an entry widget for the buffer size
buffer_size_label = tk.Label(root, text="Buffer Size:")
buffer_size_label.pack()

buffer_size_entry = tk.Entry(root, width=10)
buffer_size_entry.insert(tk.END, "65536")
buffer_size_entry.pack()

# Create a button to open the extension selection window
extension_button = tk.Button(root, text="Select Extensions", command=open_extension_window)
extension_button.pack()

# Create checkboxes for cache writability and readability
cache_writable_var = tk.IntVar()
cache_writable_checkbox = tk.Checkbutton(root, text="Cache Writable", variable=cache_writable_var)
cache_writable_checkbox.pack()

cache_readable_var = tk.IntVar()
cache_readable_checkbox = tk.Checkbutton(root, text="Cache Readable", variable=cache_readable_var)
cache_readable_checkbox.pack()

save_button = tk.Button(root, text="Save", command=save_settings)
save_button.pack()

root.mainloop()
