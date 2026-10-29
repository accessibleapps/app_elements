from logging import getLogger
import subprocess
import sys
import winreg

logger = getLogger("app_elements.startup")
import i18n_core
from gui_builder import fields
from platform_utils import paths
from wx_utils import forms as wx_forms
from wx_utils import popups

import app_elements

i18n_core.install_module_translation("app_elements", module=sys.modules[__name__])
application = app_elements.find_application_module()
RUN_KEY = r"Software\Microsoft\Windows\CurrentVersion\Run"


class RunAtStartupPanel(wx_forms.AutoSizedPanel):
    run_at_startup = fields.CheckBox(label=__("&Run at startup"))

    def render(self, *args, **kwargs):
        super(RunAtStartupPanel, self).render(*args, **kwargs)
        self.run_at_startup.set_value(get_startup())

    def set_config_values(self):
        try:
            old_startup = get_startup()
            if self.run_at_startup.get_value() != old_startup:
                set_startup(self.run_at_startup.get_value())
        except OSError:
            logger.exception("Unable to change startup registration")
            popups.warning_message(
                title=_("Startup setting not saved"),
                message=_("Unable to change the Windows startup setting. Check your account permissions and try again."),
            )


def get_startup():
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_READ) as key:
            winreg.QueryValueEx(key, application.name)
            return True
    except FileNotFoundError:
        pass
    return False


def set_startup(value):
    if value:
        arguments = [paths.get_executable()]
        if not paths.is_frozen():
            arguments.insert(0, sys.executable)
        command = subprocess.list2cmdline(arguments)
        with winreg.CreateKeyEx(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
            winreg.SetValueEx(key, application.name, 0, winreg.REG_SZ, command)
    else:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, RUN_KEY, 0, winreg.KEY_SET_VALUE) as key:
                winreg.DeleteValue(key, application.name)
        except FileNotFoundError:
            pass
