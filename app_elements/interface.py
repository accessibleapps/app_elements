from logging import getLogger

logger = getLogger("app_elements.interface")
import datetime
import sys
import webbrowser
from pathlib import Path

import app_framework
import app_framework.shutdown
import i18n_core
import wx
from app_framework.background import Task, asynchronous
from platform_utils import paths
from wx_utils import popups

import app_elements

application = app_elements.find_application_module()

import i18n_core

i18n_core.install_module_translation("app_elements", module=sys.modules[__name__])


def view_documentation():
    if paths.is_frozen():
        docpath = Path(paths.embedded_data_path())
    else:
        docpath = Path(paths.app_path()).parent / "documentation"
    locale = application.locale.split(".")[0].split("@")[0].replace("-", "_")
    for language in (locale, locale.split("_")[0], ""):
        document = docpath / language / "readme.html"
        if document.is_file():
            webbrowser.open(document.resolve().as_uri())
            return
    popups.warning_message(
        title=_("Documentation unavailable"),
        message=_("Documentation could not be found. Check that the documentation files are installed with this application."),
    )


def show_about_dialog():
    popups.about_box(
        name=application.name,
        version=application.version,
        website=application.website,
        copyright=_("Copyright %d %s")
        % (datetime.date.today().year, application.author),
    )


def exit():
    app_framework.shutdown.shutdown(application)


@asynchronous
def report_issue(*args, **kwargs):
    import gui_builder
    import issue_reporter.gui

    dlg = issue_reporter.gui.IssueReporterDialog(
        parent=application.main_window, title=__("Report an Issue")
    )
    if dlg.display_modal() != gui_builder.OK:
        dlg.destroy()
        return
    report = dlg.get_report()
    report.application_name = application.name
    report.application_version = application.version
    report.log_paths.append(application.error_log_path)
    dlg.destroy()
    try:
        yield Task(application.issue_reporter.send_report, report)
    except Exception as e:
        logger.exception("Error submitting issue report")
        popups.warning_message(
            title=_("Issue report not submitted"),
            message=_("Your issue report could not be submitted. Please try again later."),
        )
        return
    popups.message_box(title=_("Issue submitted"), message=_("Thanks for your report!"))


def activate_app():
    application.activation_manager.prompt_for_activation()


def check_for_update():
    import app_framework.updates

    app_framework.updates.check_for_update(application)


def launch_website():
    webbrowser.open(application.website)
