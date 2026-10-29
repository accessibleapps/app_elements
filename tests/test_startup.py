import unittest
from unittest.mock import MagicMock, patch

from support import load_component


class StartupTests(unittest.TestCase):
    def registry_key(self, registry, operation):
        context = MagicMock()
        getattr(registry, operation).return_value = context
        return context.__enter__.return_value

    def test_missing_run_key_and_missing_value_are_disabled(self):
        for missing in ("OpenKey", "QueryValueEx"):
            with self.subTest(missing=missing):
                with load_component("app_elements.startup") as (component, _, modules):
                    registry = modules["winreg"]
                    self.registry_key(registry, "OpenKey")
                    getattr(registry, missing).side_effect = FileNotFoundError()
                    self.assertFalse(component.get_startup())

    def test_render_sets_live_checkbox_without_changing_registry(self):
        with load_component("app_elements.startup") as (component, _, modules):
            self.registry_key(modules["winreg"], "OpenKey")
            panel = component.RunAtStartupPanel()
            panel.render()
            panel.run_at_startup.set_value.assert_called_once_with(True)
            modules["winreg"].SetValueEx.assert_not_called()

    def test_frozen_path_with_spaces_is_quoted_and_uses_write_only_rights(self):
        with load_component("app_elements.startup") as (component, app, modules):
            registry = modules["winreg"]
            key = self.registry_key(registry, "CreateKeyEx")
            modules["platform_utils.paths"].is_frozen.return_value = True
            modules["platform_utils.paths"].get_executable.return_value = r"C:\Program Files\Example\Example.exe"
            component.set_startup(True)
            registry.CreateKeyEx.assert_called_once_with(registry.HKEY_CURRENT_USER, component.RUN_KEY, 0, registry.KEY_SET_VALUE)
            registry.SetValueEx.assert_called_once_with(key, app.name, 0, registry.REG_SZ,
                                                       '"C:\\Program Files\\Example\\Example.exe"')

    def test_source_launch_includes_interpreter_and_script(self):
        with load_component("app_elements.startup") as (component, app, modules):
            registry = modules["winreg"]
            key = self.registry_key(registry, "CreateKeyEx")
            modules["platform_utils.paths"].get_executable.return_value = r"C:\My Apps\Example\main.pyw"
            with patch.object(component.sys, "executable", r"C:\Python Install\pythonw.exe"):
                component.set_startup(True)
            registry.SetValueEx.assert_called_once_with(key, app.name, 0, registry.REG_SZ,
                '"C:\\Python Install\\pythonw.exe" "C:\\My Apps\\Example\\main.pyw"')

    def test_disabling_deletes_only_this_application_value(self):
        with load_component("app_elements.startup") as (component, app, modules):
            registry = modules["winreg"]
            key = self.registry_key(registry, "OpenKey")
            component.set_startup(False)
            registry.OpenKey.assert_called_once_with(registry.HKEY_CURRENT_USER, component.RUN_KEY, 0, registry.KEY_SET_VALUE)
            registry.DeleteValue.assert_called_once_with(key, app.name)
            registry.SetValueEx.assert_not_called()

    def test_disabling_missing_registration_is_idempotent(self):
        for missing in ("OpenKey", "DeleteValue"):
            with self.subTest(missing=missing):
                with load_component("app_elements.startup") as (component, _, modules):
                    registry = modules["winreg"]
                    self.registry_key(registry, "OpenKey")
                    getattr(registry, missing).side_effect = FileNotFoundError()
                    component.set_startup(False)

    def test_access_denial_is_not_misreported_as_disabled(self):
        with load_component("app_elements.startup") as (component, _, modules):
            modules["winreg"].OpenKey.side_effect = PermissionError("denied")
            with self.assertRaises(PermissionError):
                component.get_startup()

    def test_save_failure_shows_a_warning_and_does_not_claim_success(self):
        with load_component("app_elements.startup") as (component, _, modules):
            registry = modules["winreg"]
            registry.OpenKey.side_effect = FileNotFoundError()
            registry.CreateKeyEx.side_effect = PermissionError("denied")
            panel = component.RunAtStartupPanel()
            panel.run_at_startup.get_value.return_value = True
            with self.assertLogs("app_elements.startup", level="ERROR"):
                panel.set_config_values()
            warning = modules["wx_utils.popups"].warning_message
            warning.assert_called_once()
            self.assertIn("not saved", warning.call_args.kwargs["title"])
            registry.SetValueEx.assert_not_called()
