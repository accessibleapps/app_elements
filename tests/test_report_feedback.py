import types
import unittest
from unittest.mock import Mock, patch

from support import load_component


class ReportFeedbackTests(unittest.TestCase):
    def dialog(self, modules, result=1):
        report = types.SimpleNamespace(log_paths=[])
        dialog = Mock()
        dialog.display_modal.return_value = result
        dialog.get_report.return_value = report
        gui = types.ModuleType("issue_reporter.gui")
        gui.IssueReporterDialog = Mock(return_value=dialog)
        package = types.ModuleType("issue_reporter")
        package.gui = gui
        modules.update({"issue_reporter": package, "issue_reporter.gui": gui})
        return dialog, report

    def application_values(self):
        return dict(main_window=object(), version="1.2", error_log_path="example.log",
                    issue_reporter=Mock())

    def test_send_failure_warns_without_a_success_message(self):
        with load_component("app_elements.interface", **self.application_values()) as (component, app, modules):
            dialog, report = self.dialog(modules)
            with patch.dict("sys.modules", modules):
                operation = component.report_issue()
                next(operation)
                dialog.destroy.assert_called_once()
                modules["app_framework.background"].Task.assert_called_once_with(app.issue_reporter.send_report, report)
                with self.assertLogs("app_elements.interface", level="ERROR"):
                    with self.assertRaises(StopIteration):
                        operation.throw(ConnectionError("offline"))
            warning = modules["wx_utils.popups"].warning_message
            warning.assert_called_once_with(
                title="Issue report not submitted",
                message="Your issue report could not be submitted. Please try again later.",
            )
            modules["wx_utils.popups"].message_box.assert_not_called()

    def test_success_keeps_report_metadata_and_confirmation(self):
        with load_component("app_elements.interface", **self.application_values()) as (component, app, modules):
            dialog, report = self.dialog(modules)
            with patch.dict("sys.modules", modules):
                operation = component.report_issue()
                next(operation)
                with self.assertRaises(StopIteration):
                    operation.send(None)
            self.assertEqual(report.application_name, app.name)
            self.assertEqual(report.application_version, app.version)
            self.assertEqual(report.log_paths, [app.error_log_path])
            dialog.destroy.assert_called_once()
            modules["wx_utils.popups"].message_box.assert_called_once()
            modules["wx_utils.popups"].warning_message.assert_not_called()

    def test_cancel_destroys_dialog_without_sending_or_announcing_success(self):
        with load_component("app_elements.interface", **self.application_values()) as (component, _, modules):
            dialog, _ = self.dialog(modules, result=0)
            with patch.dict("sys.modules", modules):
                with self.assertRaises(StopIteration):
                    next(component.report_issue())
            dialog.destroy.assert_called_once()
            modules["app_framework.background"].Task.assert_not_called()
            modules["wx_utils.popups"].message_box.assert_not_called()
            modules["wx_utils.popups"].warning_message.assert_not_called()
