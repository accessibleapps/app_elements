import unittest

from support import load_component


class ApplicationContractTests(unittest.TestCase):
    def test_discovery_returns_the_bootstrapped_application_module(self):
        with load_component("app_elements") as (elements, application, _):
            self.assertIs(elements.find_application_module(), application)

    def test_minimal_help_menu_has_documentation_and_about(self):
        with load_component("app_elements.menu") as (menu, _, _):
            self.assertTrue(hasattr(menu.HelpMenu, "documentation"))
            self.assertTrue(hasattr(menu.HelpMenu, "about"))
            self.assertFalse(hasattr(menu.HelpMenu, "activate"))
            self.assertFalse(hasattr(menu.HelpMenu, "report_issue"))

    def test_exit_uses_the_framework_shutdown_owner(self):
        with load_component("app_elements.interface") as (interface, application, modules):
            interface.exit()
            modules["app_framework.shutdown"].shutdown.assert_called_once_with(application)


if __name__ == "__main__":
    unittest.main()
