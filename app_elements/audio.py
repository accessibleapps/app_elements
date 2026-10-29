import app_framework.helpers
from app_framework.configuration import get_configuration_value
import i18n_core
import sys
from gui_builder import fields
from wx_utils import forms as wx_forms

import app_elements

i18n_core.install_module_translation("app_elements", module=sys.modules[__name__])
application = app_elements.find_application_module()


class DeviceSelectionPanel(wx_forms.AutoSizedPanel):
    output_device = fields.ComboBox(label=__("&Output audio device"), read_only=True)
    if app_framework.helpers.has_sound_recording(application):
        input_device = fields.ComboBox(label=__("&Input Audio Device"), read_only=True)

    def render(self, *args, **kwargs):
        super(DeviceSelectionPanel, self).render(*args, **kwargs)
        self._render_device(self.output_device, getattr(application, "sound_output", None), "device")
        if app_framework.helpers.has_sound_recording(application):
            self._render_device(self.input_device, getattr(application, "sound_input", None), "input_device")

    def _render_device(self, field, device, config_key):
        sound_devices = device.get_device_names() if device is not None else []
        field.set_items(sound_devices)
        field.set_enabled(bool(sound_devices))
        if not sound_devices:
            return
        current_device = get_configuration_value(application.config, ["audio", config_key], "Default")
        if current_device in sound_devices:
            field.set_index_to_item(current_device)
        elif "Default" in sound_devices:
            field.set_index_to_item("Default")
        else:
            field.set_index(0)

    def set_config_values(self):
        fields_to_save = [(self.output_device, "device")]
        if app_framework.helpers.has_sound_recording(application):
            fields_to_save.append((self.input_device, "input_device"))
        for field, config_key in fields_to_save:
            choice = field.get_choice()
            if choice is None or choice not in field.get_items():
                continue
            if "audio" not in application.config:
                application.config["audio"] = {}
            application.config["audio"][config_key] = choice
