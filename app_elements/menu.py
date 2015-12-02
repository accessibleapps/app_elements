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
 if hasattr(application, 'website'):
  website = MenuItem(label=__("{application_name} &Website").format(application_name=application.name), callback=app_elements.interface.launch_website)
 if app_framework.helpers.has_issue_reporter(application):
  report_issue = MenuItem(label=__("&Report an Issue..."), callback=app_elements.interface.report_issue)
 if app_framework.helpers.has_activation(application):
  activate = MenuItem(label=__("&Activate %s...") % application.name, callback=app_elements.interface.activate_app)
 if app_framework.helpers.is_autoupdating(application):
  check_for_update = MenuItem(label=__("Check for &Update"), callback=app_elements.interface.check_for_update)
 about = MenuItem(label=__("&About %s...") % application.name, callback=app_elements.interface.show_about_dialog)

 def render(self, *args, **kwargs):
  super(HelpMenu, self).render(*args, **kwargs)
  self.about.set_as_mac_about_menu_item()
