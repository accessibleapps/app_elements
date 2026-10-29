import unittest
from unittest.mock import Mock

from support import load_component


class AudioSelectionTests(unittest.TestCase):
    def test_missing_section_uses_framework_default_and_saves_valid_choice(self):
        output = Mock(get_device_names=Mock(return_value=["Speakers", "Default"]))
        with load_component("app_elements.audio", sound_output=output) as (component, app, modules):
            panel = component.DeviceSelectionPanel()
            panel.render()
            modules["app_framework.configuration"].get_configuration_value.assert_called_once_with(
                app.config, ["audio", "device"], "Default"
            )
            panel.output_device.set_index_to_item.assert_called_once_with("Default")
            panel.output_device.get_choice.return_value = "Speakers"
            panel.output_device.get_items.return_value = ["Speakers", "Default"]
            panel.set_config_values()
            self.assertEqual(app.config, {"audio": {"device": "Speakers"}})

    def test_configured_device_is_selected_before_default(self):
        output = Mock(get_device_names=Mock(return_value=["Default", "USB Headset"]))
        with load_component("app_elements.audio", sound_output=output) as (component, _, modules):
            modules["app_framework.configuration"].get_configuration_value.return_value = "USB Headset"
            panel = component.DeviceSelectionPanel()
            panel.render()
            panel.output_device.set_index_to_item.assert_called_once_with("USB Headset")

    def test_missing_device_falls_back_to_first_when_no_default_is_enumerated(self):
        output = Mock(get_device_names=Mock(return_value=["Speakers"]))
        with load_component("app_elements.audio", sound_output=output) as (component, _, _):
            panel = component.DeviceSelectionPanel()
            panel.render()
            panel.output_device.set_index.assert_called_once_with(0)

    def test_no_outputs_or_failed_input_initialization_preserves_configuration(self):
        config = {"audio": {"device": "Disconnected", "input_device": "Microphone"}}
        output = Mock(get_device_names=Mock(return_value=[]))
        with load_component("app_elements.audio", sound_output=output, sound_input=None,
                            record_sound=True, config=config) as (component, app, _):
            panel = component.DeviceSelectionPanel()
            panel.render()
            for field in (panel.output_device, panel.input_device):
                field.set_items.assert_called_once_with([])
                field.set_enabled.assert_called_once_with(False)
                field.set_index.assert_not_called()
                field.get_choice.return_value = None
                field.get_items.return_value = []
            panel.set_config_values()
            self.assertEqual(app.config, config)
            self.assertEqual(app.config["audio"]["device"], "Disconnected")
            self.assertEqual(app.config["audio"]["input_device"], "Microphone")

    def test_recording_choice_saved_without_overwriting_other_audio_settings(self):
        output = Mock(get_device_names=Mock(return_value=["Default"]))
        input_device = Mock(get_device_names=Mock(return_value=["Default", "Mic"]))
        with load_component("app_elements.audio", sound_output=output, sound_input=input_device,
                            record_sound=True, config={"audio": {"global_volume": 40}}) as (component, app, _):
            panel = component.DeviceSelectionPanel()
            panel.render()
            panel.output_device.get_choice.return_value = "Default"
            panel.output_device.get_items.return_value = ["Default"]
            panel.input_device.get_choice.return_value = "Mic"
            panel.input_device.get_items.return_value = ["Default", "Mic"]
            panel.set_config_values()
            self.assertEqual(app.config["audio"], {
                "global_volume": 40, "device": "Default", "input_device": "Mic"
            })

    def test_invalid_selection_cannot_replace_an_existing_device(self):
        with load_component("app_elements.audio", config={"audio": {"device": "Saved"}}) as (component, app, _):
            panel = component.DeviceSelectionPanel()
            panel.output_device.get_choice.return_value = "Stale"
            panel.output_device.get_items.return_value = []
            panel.set_config_values()
            self.assertEqual(app.config["audio"]["device"], "Saved")
