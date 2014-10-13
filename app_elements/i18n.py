import locale
import i18n_core
import babel

from wx_utils import forms as wx_forms
from gui_builder import fields
import app_elements
application = app_elements.find_application_module()

class LanguageSelectionPanel(wx_forms.AutoSizedPanel):
 language = fields.ComboBox(label=__("Application &Language (requires restart)"), read_only=True)

 def __init__(self, *args, **kwargs):
  super(LanguageSelectionPanel, self).__init__(*args, **kwargs)
  locales = list(i18n_core.get_available_locales(application.name))
  self.locales = sorted(locales, key=lambda i: i.language, cmp=locale.strcoll)

 def render(self, *args, **kwargs):
  super(LanguageSelectionPanel, self).render(*args, **kwargs)
  locales = [u"{name} ({english_name})".format(name=i.language_name, english_name=i.english_name) for i in self.locales]
  self.language.set_value(locales)
  current_locale = application.locale.split('.')[0]
  languages = [i.language for i in self.locales]
  try:
   index = languages.index(current_locale.split('_')[0])
  except ValueError:
   index = languages.index(i18n_core.DEFAULT_LOCALE.split('_')[0])
  self.language.set_index(index)

 def set_config_values(self):
  locale = self.locales[self.language.get_index()]
  if 'UI' not in application.config:
   application.config['UI'] = {}
  locale_id = locale.language
  if locale.territory:
   locale_id += "_%s" % locale.territory
  application.config['UI']['language'] = locale_id
