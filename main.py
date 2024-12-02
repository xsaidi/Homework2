import argparse
import subprocess
import os
import time

def get_dependencies(package_name: str):
    """Возвращает список зависимостей для указанного пакета pip."""
    result = subprocess.run(
        ["pip", "show", package_name], capture_output=True, text=True
    )

    if result.returncode != 0:
        raise ValueError(f"Ошибка: Пакет '{package_name}' не найден.")

    dependencies = []
    for line in result.stdout.splitlines():
        if line.startswith("Requires:"):
            dependencies = line.split(": ")[1].split(", ")

    return [dep.strip() for dep in dependencies if dep]

def build_dependency_graph(package_name: str, max_depth: int = 5):
    """Рекурсивно строит граф зависимостей для пакета, включая транзитивные зависимости."""
    graph = []
    visited = set()

    def add_dependencies(pkg_name: str, current_depth: int):
        if current_depth > max_depth or pkg_name in visited:
            return
        visited.add(pkg_name)

        dependencies = get_dependencies(pkg_name)
        for dep in dependencies:
            graph.append(f"{pkg_name} --> {dep.strip()}")
            add_dependencies(dep.strip(), current_depth + 1)  # Рекурсивно добавляем транзитивные зависимости

    add_dependencies(package_name, 1)
    return graph

def generate_plantuml_script(graph):
    """Генерирует скрипт PlantUML на основе графа зависимостей."""
    plantuml_script = "@startuml\n"
    for relation in graph:
        plantuml_script += f"{relation}\n"
    plantuml_script += "@enduml"
    return plantuml_script

def visualize_graph(visualizer_path: str, script: str):
    """Визуализирует граф с помощью указанного визуализатора PlantUML."""
    try:
        temp_puml_path = "temp_script.puml"
        with open(temp_puml_path, "w") as temp_file:
            temp_file.write(script)

        subprocess.run(
            ["java", "-jar", visualizer_path, "-tpng", temp_puml_path], check=True
        )

        subprocess.run(["explorer", "temp_script.png"])
        time.sleep(1)
        os.remove("temp_script.puml")
        os.remove("temp_script.png")
    except subprocess.CalledProcessError as ex:
        print(f"Ошибка при запуске PlantUML: {ex}")
    except FileNotFoundError as ex:
        print(f"Ошибка: файл не найден - {ex}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="Визуализация графа зависимостей Python-пакета с использованием PlantUML."
    )
    parser.add_argument(
        "--visualizer-path",
        required=True,
        help="Путь к визуализатору PlantUML (JAR файл).",
    )
    parser.add_argument(
        "--package-name",
        required=True,
        help="Имя Python-пакета для анализа.",
    )
    args = parser.parse_args()

    try:
        # Строим граф зависимостей
        graph = build_dependency_graph(args.package_name)

        # Генерируем скрипт PlantUML
        script = generate_plantuml_script(graph)

        # Визуализируем граф
        visualize_graph(args.visualizer_path, script)

    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
