import os
import zipfile
import tkinter as tk
from tkinter import scrolledtext


class ShellEmulator:
    def __init__(self, root, hostname, fs_zip):
        self.root = root
        self.root.title(f"Shell Emulator - {hostname}")
        self.hostname = hostname
        self.current_dir = "/"
        self.fs_zip = fs_zip
        self.virtual_fs = []
        self.create_gui()
        self.load_virtual_fs()

    def create_gui(self):
        # Textbox for output
        self.output = scrolledtext.ScrolledText(
            self.root, wrap=tk.WORD, height=20, width=80)
        self.output.pack(padx=10, pady=10)
        self.output.insert(tk.END, f"{self.hostname}:{self.current_dir}$ ")

        # Textbox for input
        self.input_field = tk.Entry(self.root, width=80)
        self.input_field.pack(padx=10, pady=5)
        self.input_field.bind('<Return>', self.handle_command)

    def load_virtual_fs(self):
        # Import virtual files from archive
        with zipfile.ZipFile(self.fs_zip, 'r') as z:
            self.virtual_fs = z.namelist()

    def handle_command(self, event):
        command = self.input_field.get()
        self.input_field.delete(0, tk.END)
        self.output.insert(tk.END, command + "\n")
        self.execute_command(command)
        self.output.insert(tk.END, f"{self.hostname}:{self.current_dir}$ ")

    def execute_command(self, command):
        parts = command.split()
        if not parts:
            return

        if parts[0] == "ls":
            self.list_directory()
        elif parts[0] == "cd":
            if len(parts) == 2:
                self.change_directory(parts[1])
            else:
                self.output.insert(tk.END, "Usage: cd <directory>\n")
        elif parts[0] == "mv":
            if len(parts) == 3:
                self.move_file(parts[1], parts[2])
            else:
                self.output.insert(
                    tk.END, "Usage: mv <source> <destination>\n")
        elif parts[0] == "who":
            self.output.insert(tk.END, "user\n")
        elif parts[0] == "exit":
            self.root.quit()
        else:
            self.output.insert(tk.END, f"Command not found: {command}\n")

    def list_directory(self):
        dir_prefix = self.current_dir.lstrip("/")
        if dir_prefix and not dir_prefix.endswith("/"):
            dir_prefix += "/"

        # filter current directory
        files_in_dir = set()
        for path in self.virtual_fs:
            if path.startswith(dir_prefix):
                stripped_path = path[len(dir_prefix):]
                if "/" in stripped_path:
                    files_in_dir.add(stripped_path.split("/")[0])
                else:
                    files_in_dir.add(stripped_path)

        for file in sorted(files_in_dir):
            self.output.insert(tk.END, f"{file}\n")

    def change_directory(self, dir_name):
        if dir_name == "..":
            if self.current_dir != "/":
                self.current_dir = os.path.dirname(
                    self.current_dir.rstrip("/"))
                if not self.current_dir:
                    self.current_dir = "/"
        else:
            new_dir = os.path.join(self.current_dir, dir_name).lstrip("/")
            if new_dir + "/" in self.virtual_fs or any(f.startswith(new_dir + "/") for f in self.virtual_fs):
                self.current_dir = new_dir
            else:
                self.output.insert(tk.END, f"No such directory: {dir_name}\n")

    def move_file(self, src, dest):
        src_path = os.path.join(self.current_dir, src).lstrip("/")
        dest_path = os.path.join(self.current_dir, dest).lstrip("/")

        def exists_in_fs(path):
            return path in self.virtual_fs or any(f.startswith(path + '/') for f in self.virtual_fs)

        if not exists_in_fs(src_path):
            self.output.insert(
                tk.END, f"Нет такого файла или директории: {src}\n")
            return

        if dest_path in self.virtual_fs and dest_path.endswith("/"):
            dest_path = os.path.join(dest_path, os.path.basename(src_path))

        parent_dir = os.path.dirname(dest_path)
        if parent_dir and not exists_in_fs(parent_dir):
            self.output.insert(
                tk.END, f"Родительская директория не существует: {parent_dir}\n")
            return

        self.virtual_fs = [dest_path + item[len(src_path):] if item == src_path or item.startswith(
            src_path + '/') else item for item in self.virtual_fs if item != dest_path]
        self.output.insert(tk.END, f"Перемещено {src} в {dest}\n")


if __name__ == "__main__":
    import sys
    zip_path = "test_fs.zip"
    hostname = "my_computer"
    root = tk.Tk()
    app = ShellEmulator(root, hostname, zip_path)
    root.mainloop()
