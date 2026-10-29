import locale
import sys

import i18n_core
from gui_builder import fields
from wx_utils import forms as wx_forms

import app_elements

i18n_core.install_module_translation(
    "app_elements", module=sys.modules["app_elements.i18n"]
)
application = app_elements.find_application_module()


class LanguageSelectionPanel(wx_forms.AutoSizedPanel):
    language = fields.ComboBox(
        label=__("Application &Language (requires restart)"), read_only=True
    )

    def __init__(self, *args, **kwargs):
        super(LanguageSelectionPanel, self).__init__(*args, **kwargs)
        locales = list(i18n_core.get_available_locales(application.name))
        self.locales = sorted(locales, key=lambda i: locale.strxfrm(str(i)))

    def render(self, *args, **kwargs):
        super(LanguageSelectionPanel, self).render(*args, **kwargs)
        locales = [
            "{name} ({english_name})".format(
                name=i.get_display_name(i), english_name=i.get_display_name("en")
            )
            for i in self.locales
        ]
        self.language.set_value(locales)
        self.language.set_enabled(bool(self.locales))
        if not self.locales:
            return
        identifiers = [str(i).casefold() for i in self.locales]
        index = 0
        for requested in (application.locale, i18n_core.DEFAULT_LOCALE):
            requested = requested.split(".")[0].split("@")[0].replace("-", "_").casefold()
            if requested in identifiers:
                index = identifiers.index(requested)
                break
            language = requested.split("_")[0]
            if language in identifiers:
                index = identifiers.index(language)
                break
            matches = [n for n, item in enumerate(self.locales) if item.language == language]
            if matches:
                index = matches[0]
                break
        self.language.set_index(index)

    def set_config_values(self):
        index = self.language.get_index()
        if index is None or not 0 <= index < len(self.locales):
            return
        locale = self.locales[index]
        if "UI" not in application.config:
            application.config["UI"] = {}
        application.config["UI"]["language"] = str(locale)
