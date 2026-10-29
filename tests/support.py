"""Load real app_elements modules with controlled desktop-service boundaries.

These doubles exercise composition and configuration, not native wx behavior.
Each test import has fresh fields and restores sys.modules on exit.
"""

import importlib
import sys
import types
from contextlib import contextmanager
from unittest.mock import Mock, patch


class Panel:
    def __init__(self, *args, **kwargs):
        pass

    def render(self, *args, **kwargs):
        pass


@contextmanager
def load_component(name, **application_values):
    application = types.ModuleType("application")
    application.name = "Example"
    application.locale = "en_US"
    application.config = {}
    application.__dict__.update(application_values)

    def module(name, **values):
        result = types.ModuleType(name)
        result.__dict__.update(values)
        return result

    helpers = module(
        "app_framework.helpers",
        has_sound_recording=lambda app: bool(getattr(app, "record_sound", False)),
        has_issue_reporter=lambda app: False,
        has_activation=lambda app: False,
        is_autoupdating=lambda app: False,
    )
    configuration = module(
        "app_framework.configuration", get_configuration_value=Mock(return_value="Default")
    )
    shutdown = module("app_framework.shutdown", shutdown=Mock())
    background = module(
        "app_framework.background", Task=Mock(), asynchronous=lambda func: func
    )
    framework = module(
        "app_framework", helpers=helpers, configuration=configuration, shutdown=shutdown
    )
    fields = module("gui_builder.fields", ComboBox=Mock(), CheckBox=Mock(), MenuItem=Mock())
    # A distinct control per declaration, just as a bound form has distinct fields.
    fields.ComboBox.side_effect = lambda **kwargs: Mock()
    fields.CheckBox.side_effect = lambda **kwargs: Mock()
    fields.MenuItem.side_effect = lambda **kwargs: Mock()
    forms = module("gui_builder.forms", Menu=Panel)
    gui = module("gui_builder", fields=fields, forms=forms, OK=1)
    wx_forms = module("wx_utils.forms", AutoSizedPanel=Panel)
    popups = module("wx_utils.popups", warning_message=Mock(), message_box=Mock())
    paths = module(
        "platform_utils.paths", is_frozen=Mock(return_value=False),
        app_path=Mock(), embedded_data_path=Mock(), get_executable=Mock()
    )
    translation = module(
        "i18n_core", DEFAULT_LOCALE="en_US", get_available_locales=Mock(return_value=[])
    )

    def install_translation(domain, module):
        module._ = module.__ = lambda text: text

    translation.install_module_translation = install_translation
    registry = module(
        "winreg", HKEY_CURRENT_USER=1, KEY_READ=2, KEY_SET_VALUE=4, REG_SZ=1,
        OpenKey=Mock(), CreateKeyEx=Mock(), QueryValueEx=Mock(),
        SetValueEx=Mock(), DeleteValue=Mock()
    )
    modules = {
        "application": application, "app_framework": framework,
        "app_framework.helpers": helpers, "app_framework.configuration": configuration,
        "app_framework.shutdown": shutdown, "app_framework.background": background,
        "gui_builder": gui, "gui_builder.fields": fields, "gui_builder.forms": forms,
        "wx_utils": module("wx_utils", forms=wx_forms, popups=popups),
        "wx_utils.forms": wx_forms, "wx_utils.popups": popups,
        "platform_utils": module("platform_utils", paths=paths),
        "platform_utils.paths": paths, "i18n_core": translation,
        "wx": module("wx"), "winreg": registry,
    }
    with patch.dict(sys.modules, modules):
        # Ensure the production module and its application binding are re-evaluated.
        for key in list(sys.modules):
            if key == "app_elements" or key.startswith("app_elements."):
                del sys.modules[key]
        with patch("builtins.__", lambda text: text, create=True):
            yield importlib.import_module(name), application, modules
