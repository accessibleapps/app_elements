from gui_builder import forms
from gui_builder.fields import MenuItem
import sys
import app_framework.helpers
import app_elements
application = app_elements.find_application_module()
import app_elements.interface


import i18n_core
i18n_core.install_module_translation('app_elements', module=sys.modules['app_elements.menu'])

class HelpMenu(forms.Menu):
 documentation = MenuItem(label=__("%s &Documentation") % application.name, hotkey='f1', callback=app_elements.interface.view_documentation)
 if app_framework.helpers.has_issue_reporter(application):
  report_issue = MenuItem(label=__("&Report an Issue..."), callback=app_elements.interface.report_issue)
 about = MenuItem(label=__("&About %s...") % application.name, callback=app_elements.interface.show_about_dialog)

