import app_framework.helpers
from gui_builder import fields
from wx_utils import forms as wx_forms

import app_elements

application = app_elements.find_application_module()


class DeviceSelectionPanel(wx_forms.AutoSizedPanel):
    output_device = fields.ComboBox(label=__("&Output audio device"), read_only=True)
    if app_framework.helpers.has_sound_recording(application):
        input_device = fields.ComboBox(label=__("&Input Audio Device"), read_only=True)

    def render(self, *args, **kwargs):
        super(DeviceSelectionPanel, self).render(*args, **kwargs)
        sound_devices = application.sound_output.get_device_names()
        self.output_device.set_items(sound_devices)
        current_device = application.config["audio"]["device"]
        if current_device in sound_devices:
            self.output_device.set_index_to_item(current_device)
        elif "Default" in sound_devices:
            self.output_device.set_index_to_item("Default")
        else:
            self.output_device.set_index(0)
        if not app_framework.helpers.has_sound_recording(application):
            return
        sound_devices = application.sound_input.get_device_names()
        self.input_device.set_items(sound_devices)
        current_device = application.config["audio"]["input_device"]
        if current_device in sound_devices:
            self.input_device.set_index_to_item(current_device)
        elif "Default" in sound_devices:
            self.input_device.set_index_to_item("Default")
        else:
            self.input_device.set_index(0)

    def set_config_values(self):
        application.config["audio"]["device"] = self.output_device.get_choice()
        if app_framework.helpers.has_sound_recording(application):
            application.config["audio"]["input_device"] = self.input_device.get_choice()
