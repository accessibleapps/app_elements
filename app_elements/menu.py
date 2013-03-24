from gui_builder import forms
from gui_builder.fields import MenuItem
import app_elements
application = app_elements.find_application_module()
import app_elements.interface

class HelpMenu(forms.Menu):
 documentation = MenuItem(label=__("%s &Documentation") % application.name, hotkey='f1', callback=app_elements.interface.view_documentation)
 about = MenuItem(label=__("&About %s...") % application.name, callback=app_elements.interface.show_about_dialog)

