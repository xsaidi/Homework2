import unittest
import os
from main import (
    get_dependencies,
    build_dependency_graph,
    generate_plantuml_script,
    visualize_graph,
)


class TestDependencyVisualizer(unittest.TestCase):
    def setUp(self):
        self.package_name = "requests"
        self.visualizer_path = r"C:\tools\plantuml.jar"
        self.graph = build_dependency_graph(self.package_name)
        self.script = generate_plantuml_script(self.graph)

    def test_get_dependencies(self):
        dependencies = get_dependencies(self.package_name)
        self.assertEqual(
            sorted(dependencies),
            sorted(["certifi", "charset-normalizer", "idna", "urllib3"]),
        )

    def test_build_dependency_graph(self):
        expected_graph = [
            "requests --> certifi",
            "requests --> charset-normalizer",
            "requests --> idna",
            "requests --> urllib3",
        ]
        self.assertEqual(sorted(self.graph), sorted(expected_graph))

    def test_generate_plantuml_script(self):
        expected_script = (
            "@startuml\n"
            "requests --> certifi\n"
            "requests --> charset-normalizer\n"
            "requests --> idna\n"
            "requests --> urllib3\n"
            "@enduml"
        )
        self.assertEqual(self.script, expected_script)

    def test_save_plantuml_script(self):
        temp_puml_path = "test_script.puml"

        with open(temp_puml_path, "w") as file:
            file.write(self.script)

        with open(temp_puml_path, "r") as file:
            saved_script = file.read()

        self.assertEqual(self.script, saved_script)

        try:
            os.remove(temp_puml_path)
        except Exception as e:
            print(f"Не удалось удалить временный файл {temp_puml_path}: {e}")

    def test_visualize_graph(self):
        temp_puml_path = "test_script.puml"

        # Сохраняем скрипт
        with open(temp_puml_path, "w") as file:
            file.write(self.script)

        # Проверяем визуализацию
        visualize_graph(self.visualizer_path, self.script)
        os.remove(temp_puml_path)


if __name__ == "__main__":
    unittest.main()
