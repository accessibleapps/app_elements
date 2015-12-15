from logging import getLogger
logger = getLogger('app_elements.startup')
import _winreg
from platform_utils import paths

from wx_utils import forms as wx_forms
from gui_builder import fields
import app_elements
application = app_elements.find_application_module()


class RunAtStartupPanel(wx_forms.AutoSizedPanel):
	run_at_startup = fields.CheckBox(label=__("&Run at startup"))

	def render(self, *args, **kwargs):
		super(RunAtStartupPanel, self).render(*args, **kwargs)
		self.run_at_startup.default_value = get_startup()

	def set_config_values(self):
		old_startup = get_startup()
		if self.run_at_startup.get_value() != old_startup:
			set_startup(self.run_at_startup.get_value())

def get_startup():
	with _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run') as key:
		try:
			_winreg.QueryValueEx(key, application.name)
			return True
		except WindowsError:
			pass
	return False

def set_startup(value):
	with _winreg.OpenKey(_winreg.HKEY_CURRENT_USER, r'Software\Microsoft\Windows\CurrentVersion\Run', 0, _winreg.KEY_ALL_ACCESS) as key:
		try:
			if value:
				_winreg.SetValueEx(key, application.name, 0, 1, paths.get_executable())
			else:
				_winreg.DeleteValue(key, application.name)
		except WindowsError as e:
			logger.exception("Unable to set startup to %r" % value)

