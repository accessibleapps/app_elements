import unittest

from babel import Locale

from support import load_component


class LanguageSelectionTests(unittest.TestCase):
    def panel(self, component, modules, identifiers):
        modules["i18n_core"].get_available_locales.return_value = [
            identifier for identifier in identifiers
        ]
        panel = component.LanguageSelectionPanel()
        panel.render()
        return panel

    def test_existing_regional_catalog_identity_round_trips(self):
        # Existing catalogs include fr_CA/fr in this package and hi_IN in QRead.
        # Construct locales the same way i18n_core.locale_from_locale_id does.
        for language, territory in (("fr", "CA"), ("hi", "IN")):
            with self.subTest(language=language, territory=territory):
                with load_component("app_elements.i18n", locale="%s-%s.UTF-8" % (language, territory)) as (component, app, modules):
                    panel = self.panel(component, modules, [
                        Locale("fr"), Locale("fr", "CA"), Locale("hi", "IN"), Locale("en", "US")
                    ])
                    identifier = "%s_%s" % (language, territory)
                    index = next(n for n, item in enumerate(panel.locales) if str(item) == identifier)
                    panel.language.set_index.assert_called_once_with(index)
                    panel.language.get_index.return_value = index
                    panel.set_config_values()
                    self.assertEqual(app.config["UI"]["language"], identifier)

    def test_regions_have_distinct_native_and_english_labels(self):
        with load_component("app_elements.i18n", locale="fr_CA") as (component, _, modules):
            panel = self.panel(component, modules, [Locale("fr"), Locale("fr", "CA"), Locale("en", "US")])
            labels = panel.language.set_value.call_args.args[0]
            self.assertEqual(len(labels), len(set(labels)))
            self.assertTrue(any("Canada" in label for label in labels))
            selected = panel.language.set_index.call_args.args[0]
            self.assertEqual(str(panel.locales[selected]), "fr_CA")

    def test_base_language_then_default_then_first_available(self):
        for requested, available, expected in [
            ("fr_BE", [Locale("fr"), Locale("en", "US")], "fr"),
            ("fr_BE", [Locale("fr", "CA"), Locale("en", "US")], "fr_CA"),
            ("de_DE", [Locale("fr"), Locale("en", "US")], "en_US"),
            ("de_DE", [Locale("fr")], "fr"),
        ]:
            with self.subTest(requested=requested, available=available):
                with load_component("app_elements.i18n", locale=requested) as (component, _, modules):
                    panel = self.panel(component, modules, available)
                    index = panel.language.set_index.call_args.args[0]
                    self.assertEqual(str(panel.locales[index]), expected)

    def test_no_selection_does_not_write_configuration(self):
        for index in (None, -1, 99):
            with self.subTest(index=index):
                with load_component("app_elements.i18n") as (component, app, modules):
                    panel = self.panel(component, modules, [Locale("en", "US")])
                    panel.language.get_index.return_value = index
                    panel.set_config_values()
                    self.assertEqual(app.config, {})

    def test_no_available_locales_disables_control_and_preserves_config(self):
        with load_component("app_elements.i18n") as (component, app, modules):
            panel = self.panel(component, modules, [])
            panel.language.set_enabled.assert_called_once_with(False)
            panel.language.set_index.assert_not_called()
            panel.language.get_index.return_value = None
            panel.set_config_values()
            self.assertEqual(app.config, {})
