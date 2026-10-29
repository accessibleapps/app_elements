import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from support import load_component


class DocumentationTests(unittest.TestCase):
    def test_exact_then_language_then_root_fallback_uses_existing_file(self):
        for available, expected in [
            (["fr_CA", "fr", ""], "fr_CA"),
            (["fr", ""], "fr"),
            ([""], ""),
        ]:
            with self.subTest(available=available), tempfile.TemporaryDirectory() as directory:
                root = Path(directory) / "My App #1 café"
                root.mkdir()
                for language in available:
                    folder = root / language
                    folder.mkdir(exist_ok=True)
                    (folder / "readme.html").touch()
                (root / "fr_CA").mkdir(exist_ok=True)
                with load_component("app_elements.interface", locale="fr-CA.UTF-8") as (component, _, modules):
                    paths = modules["platform_utils.paths"]
                    paths.is_frozen.return_value = True
                    paths.embedded_data_path.return_value = str(root)
                    with patch.object(component.webbrowser, "open") as browser:
                        component.view_documentation()
                    browser.assert_called_once_with((root / expected / "readme.html").resolve().as_uri())
                    modules["wx_utils.popups"].warning_message.assert_not_called()

    def test_source_run_uses_sibling_documentation_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            application_path = root / "Example"
            application_path.mkdir()
            docs = root / "documentation"
            docs.mkdir()
            (docs / "readme.html").touch()
            with load_component("app_elements.interface") as (component, _, modules):
                modules["platform_utils.paths"].app_path.return_value = str(application_path)
                with patch.object(component.webbrowser, "open") as browser:
                    component.view_documentation()
                browser.assert_called_once_with((docs / "readme.html").as_uri())

    def test_missing_document_warns_instead_of_opening_a_broken_url(self):
        with tempfile.TemporaryDirectory() as directory:
            with load_component("app_elements.interface") as (component, _, modules):
                paths = modules["platform_utils.paths"]
                paths.is_frozen.return_value = True
                paths.embedded_data_path.return_value = directory
                with patch.object(component.webbrowser, "open") as browser:
                    component.view_documentation()
                browser.assert_not_called()
                modules["wx_utils.popups"].warning_message.assert_called_once()
