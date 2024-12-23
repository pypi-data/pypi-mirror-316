import os
from dataclasses import dataclass
import importlib.resources

ARTIFACT_PATH = "litemodel_cli.artifacts"
STATIC_PATH = "litemodel_cli.artifacts.static"
JS_PATH = "litemodel_cli.artifacts.static.js"
CSS_PATH = "litemodel_cli.artifacts.static.css"
TEMPLATES_PATH = "litemodel_cli.artifacts.templates"


FILES = (
    "app.py",
    "jinja_filters.py",
    "middleware.py",
    "resources.py",
    "settings.py",
    "views.py",
    "admin.py",
    "event_handlers.py",
    "models.py",
    "routes.py",
    "sqlite.db",
)

DIRECTORIES = (
    "static",
    "static/js",
    "static/css",
    "managment",
    "templates",
)


def list_files_in_subfolder(module_name, subfolder_name):
    files = []
    with importlib.resources.path(module_name, subfolder_name) as subfolder_path:
        for file_path in subfolder_path.iterdir():
            if file_path.is_file():
                files.append(file_path.name)
    return files


def get_artifact_content(module: str, filename: str) -> str:
    return importlib.resources.read_text(module, filename)


@dataclass
class File:
    name: str
    content: str

    def __str__(self):
        return f"File: {self.name}"

    def write(self) -> None:
        with open(self.name, "w") as f:
            f.write(self.content)


class ProjectStructure:
    def __call__(self) -> None:
        self.files: list[File] = []
        self.make_dirs()
        self.get_files()
        self.write_to_project()

    def make_dirs(self) -> None:
        for directory in DIRECTORIES:
            os.makedirs(directory, exist_ok=True)

    def get_files(self) -> None:
        self._get_static_files()
        self._get_templates()
        self._get_top_level_artifacts()

    def write_to_project(self) -> None:
        for file in self.files:
            file.write()

    def _get_top_level_artifacts(self) -> None:
        artifacts = list_files_in_subfolder("litemodel_cli", "artifacts")
        for artifact in artifacts:
            self.files.append(File(artifact, get_artifact_content(ARTIFACT_PATH, artifact)))

    def _get_static_files(self) -> None:
        js_files = list_files_in_subfolder(STATIC_PATH, "js")
        css_files = list_files_in_subfolder(STATIC_PATH, "css")
        for js_file in js_files:
            self.files.append(File(f"static/js/{js_file}", get_artifact_content(JS_PATH, js_file)))
        for css_file in css_files:
            self.files.append(File(f"static/css/{css_file}", get_artifact_content(CSS_PATH, css_file)))

    def _get_templates(self) -> None:
        templates = list_files_in_subfolder(ARTIFACT_PATH, "templates")
        for template in templates:
            self.files.append(File(f"templates/{template}", get_artifact_content(TEMPLATES_PATH, template)))
