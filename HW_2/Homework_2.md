## Разработка инструмента для визуализации графа зависимостей в Git-репозитории

### Задача:
Целью данной задачи является разработка инструмента командной строки для визуализации графа зависимостей в Git-репозитории. Необходимо построить граф для коммитов, где изменялся конкретный файл (с заданным хеш-значением), и представить зависимости в формате PlantUML. Граф должен включать коммиты в хронологическом порядке и показывать отношения "родитель-потомок" между ними.

### Решение:
Инструмент реализован на Python и использует:
- **Git** для извлечения информации о коммитах и их родительских зависимостях.
- **PlantUML** для визуализации графа коммитов и их зависимостей.

Программа читает конфигурационный файл формата `.ini`, где указаны:
- Путь к файлу PlantUML для визуализации.
- Путь к репозиторию, который анализируется.
- Хэш-значение файла, для которого необходимо построить граф зависимостей.

Программа выполняет следующие шаги:
1. Читает конфигурационный файл для получения параметров.
2. Извлекает список коммитов, которые содержат изменения в файле с указанным хэш-значением.
3. Для каждого коммита извлекает его родительские коммиты, чтобы построить зависимости.
4. Строит граф в формате PlantUML и запускает визуализацию.

### Основные методы и элементы кода:

#### 1. Чтение конфигурационного файла
Этот метод использует библиотеку `configparser`, чтобы извлечь параметры из конфигурационного файла `.ini`, такие как пути к репозиторию и файлу для визуализации, а также хэш-значение файла.

```python
def read_config(config_path):
    config = configparser.ConfigParser()
    config.read(config_path)
    return config['DEFAULT']['visualizer_path'], config['DEFAULT']['repo_path'], config['DEFAULT']['file_hash']
```

#### 2. Получение коммитов, связанных с файлом
Команда Git используется для поиска всех коммитов, в которых изменялся файл с заданным хэш-значением.

```python
def get_commits_with_file(repo_path, file_hash):
    command = f"git -C {repo_path} log --pretty=format:%H -- {file_hash}"
    result = subprocess.run(command, capture_output=True, shell=True, text=True)
    if result.returncode != 0:
        raise Exception("Error getting commits")
    return result.stdout.splitlines()
```

#### 3. Извлечение родительских коммитов для каждого коммита
Используя Git, мы получаем информацию о родительских коммитах для каждого коммита, чтобы построить граф зависимостей.

```python
def get_commit_parents(repo_path, commit_hash):
    command = f"git -C {repo_path} log --pretty=format:%P -n 1 {commit_hash}"
    result = subprocess.run(command, capture_output=True, shell=True, text=True)
    if result.returncode != 0:
        raise Exception("Error getting commit parents")
    return result.stdout.split()
```

#### 4. Построение графа зависимостей в формате PlantUML
На основании полученных данных строится граф, в котором каждая зависимость родитель-потомок представлена стрелкой.

```python
def build_dependency_graph(repo_path, commits):
    edges = []
    for commit in commits:
        parents = get_commit_parents(repo_path, commit)
        for parent in parents:
            edges.append(f'"{parent}" --> "{commit}"')
    graph = "@startuml\n"
    graph += "\n".join(edges)
    graph += "\n@enduml"
    return graph
```

#### 5. Визуализация графа
Создаётся временный файл с кодом PlantUML, который передаётся на вход Java-программе PlantUML для генерации графического изображения.

```python
def visualize_graph(uml_code, visualizer_path):
    with open('graph.puml', 'w') as f:
        f.write(uml_code)
    command = f"java -jar {visualizer_path} graph.puml"
    os.system(command)
    os.remove('graph.puml')  # Удаление временного файла
```

### Тестирование:
Система была протестирована на следующих окружениях:
- **Git репозиторий**: Локальный тестовый репозиторий с несколькими коммитами.
- **PlantUML**: Версия `1.2024.7`, использующая Java для рендеринга графов.
- **Операционная система**: Ubuntu 22.04

### Результаты:
- Граф коммитов был успешно визуализирован в формате PlantUML, отображая зависимости между коммитами, где изменялся файл с заданным хэш-значением.
- Программа корректно обрабатывает ситуации, когда коммиты не найдены, выводя соответствующее сообщение.

