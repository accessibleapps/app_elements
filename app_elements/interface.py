from logging import getLogger
logger = getLogger('app_elements.interface')
import datetime
import os
import sys
import webbrowser
import wx
import i18n_core
from platform_utils import paths
from wx_utils import popups
import app_framework
import app_framework.shutdown
from app_framework.background import asynchronous, Task
import app_elements
application = app_elements.find_application_module()

import i18n_core

i18n_core.install_module_translation('app_elements', module=sys.modules[__name__])

def view_documentation():
	if paths.is_frozen():
		docpath = paths.embedded_data_path()
	else:
		docpath = os.path.join(paths.app_path(), '..', 'documentation')
	locale = application.locale
	if os.path.exists(os.path.join(docpath, locale)):
		docpath = os.path.join(docpath, locale)
	else:
		locale = locale.split('_')[0]
		if os.path.exists(os.path.join(docpath, locale)):
			docpath = os.path.join(docpath, locale)
	docpath = os.path.join(docpath, 'readme.html')
	docpath = 'file://%s' % os.path.abspath(docpath)
	webbrowser.open(docpath)

def show_about_dialog():
	popups.about_box(name=application.name, version=application.version, website=application.website, copyright=_(u"Copyright %d %s") % (datetime.date.today().year, application.author))

def exit():
	app_framework.shutdown.shutdown(application)

@asynchronous
def report_issue(*args, **kwargs):
	import gui_builder
	import issue_reporter.gui
	dlg = issue_reporter.gui.IssueReporterDialog(parent=application.main_window, title=__("Report an Issue"))
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
		logger.exception("Error submitting issue report. Not a good day.")
		popups.warning_message(title=_("Error"), message=_("There was an issue submitting your issue report. Badness."))
		return
	popups.message_box(title=_("Issue submitted"), message=_("Thanks for your report!"))

def activate_app():
	application.activation_manager.prompt_for_activation()

def check_for_update():
	import app_framework.updates
	app_framework.updates.check_for_update(application)

def launch_website():
	webbrowser.open(application.website)
