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

        # If source file exists
        if src_path in self.virtual_fs:
            # If dest — directory
            if dest_path in self.virtual_fs and dest_path.endswith("/"):
                dest_path = os.path.join(dest_path, os.path.basename(src_path))

            # Move file
            self.virtual_fs.remove(src_path)
            self.virtual_fs.append(dest_path)

            self.output.insert(tk.END, f"Moved {src} to {dest}\n")
        else:
            self.output.insert(tk.END, f"No such file: {src}\n")


if __name__ == "__main__":
    import sys
    zip_path = "test_fs.zip"
    hostname = "my_computer"
    root = tk.Tk()
    app = ShellEmulator(root, hostname, zip_path)
    root.mainloop()

```

```Shell
python3 emulator.py
```
------
# ReadMe

## Основные поля и свойства класса `ShellEmulator`

- **`root`**: Главное окно приложения, созданное с использованием библиотеки `Tkinter`.
- **`hostname`**: Имя хоста, которое отображается в приглашении к вводу команд в консоли.
- **`current_dir`**: Строка, представляющая текущую директорию в виртуальной файловой системе. Изначально установлена в корень (`"/"`).
- **`fs_zip`**: Путь к zip-архиву, который содержит виртуальную файловую систему.
- **`virtual_fs`**: Список файлов и директорий, полученный из zip-архива, который эмулирует файловую систему.
- **`output`**: Объект типа `ScrolledText`, используемый для отображения вывода консоли.
- **`input_field`**: Поле ввода команд, реализованное с помощью `Tkinter.Entry`.

## Описание методов

### `__init__(self, root, hostname, fs_zip)`
Конструктор класса `ShellEmulator`. Инициализирует главное окно, загружает виртуальную файловую систему из zip-архива и вызывает метод создания графического интерфейса.

- **Параметры**:
  - `root`: объект главного окна `Tk`.
  - `hostname`: строка, задающая имя компьютера для отображения в приглашении к вводу.
  - `fs_zip`: строка, содержащая путь к zip-архиву с виртуальной файловой системой.

### `create_gui(self)`
Создает графический интерфейс программы. Включает поле для вывода консоли (`ScrolledText`) и поле для ввода команд (`Entry`).

- **Назначение**: Создание интерфейса терминала, где пользователи могут вводить команды и получать результат.

### `load_virtual_fs(self)`
Загружает список файлов и директорий из zip-архива в поле `virtual_fs`.

- **Назначение**: Импорт файловой структуры из zip-архива для использования в эмуляторе.

### `handle_command(self, event)`
Обрабатывает ввод пользователя. При нажатии клавиши `Enter` вводит команду в консоль, очищает поле ввода, вызывает выполнение команды и обновляет приглашение к вводу.

- **Параметры**:
  - `event`: событие, связанное с нажатием клавиши `Enter`.

### `execute_command(self, command)`
Распознает и выполняет команду, введенную пользователем. Поддерживаются команды:
- `ls`: выводит содержимое текущей директории.
- `cd`: изменяет текущую директорию.
- `mv`: перемещает файл.
- `who`: выводит информацию о пользователе (заглушка).
- `exit`: завершает программу.

- **Параметры**:
  - `command`: строка, содержащая команду пользователя.

### `list_directory(self)`
Выводит содержимое текущей директории (список файлов и папок).

- **Назначение**: Реализует команду `ls`, выводя содержимое текущей директории.

### `change_directory(self, dir_name)`
Изменяет текущую директорию на указанную. Поддерживает переход в родительскую директорию (`cd ..`).

- **Параметры**:
  - `dir_name`: строка, представляющая имя директории для перехода.

- **Назначение**: Реализует команду `cd`, позволяя перемещаться между директориями.

### `move_file(self, src, dest)`
Перемещает файл из одной директории в другую. Если целевой путь является директорией, файл перемещается внутрь нее.

- **Параметры**:
  - `src`: строка, представляющая исходный файл.
  - `dest`: строка, представляющая целевой путь (файл или директорию).

- **Назначение**: Реализует команду `mv`, перемещая файлы в пределах виртуальной файловой системы.

## Основные зависимости

- **`tkinter`**: Библиотека для создания графического интерфейса.
- **`zipfile`**: Используется для работы с zip-архивом, который содержит виртуальную файловую систему.
- **`os`**: Модуль для работы с путями файловой системы.
---
## Заключение

Программа представляет собой графический эмулятор командной оболочки, который использует виртуальную файловую систему, загружаемую из zip-архива. Реализованные команды позволяют пользователю взаимодействовать с файловой системой и перемещаться по каталогам, аналогично терминалу в UNIX-подобных системах.

---