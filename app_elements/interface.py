from logging import getLogger
logger = getLogger('app_elements.interface')
import datetime
import os
import sys
import wx
import i18n_core
from platform_utils import web_browser, paths
from wx_utils import popups
import app_framework
import app_framework.shutdown
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
 web_browser.open(docpath)

def show_about_dialog():
 popups.about_box(application.name, application.version, website=application.website, copyright=_(u"Copyright %d %s") % (datetime.date.today().year, application.author))

def exit():
 app_framework.shutdown.shutdown(application)

def report_issue():
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
 def future_complete(future):
  try:
   result = future.result()
  except Exception as e:
   logger.exception("Error submitting issue report. Not a good day.")
   popups.warning_message(title=_("Error"), message=_("There was an issue submitting your issue report. Badness."))
   return
  popups.message_box(title=_("Issue submitted"), message=_("Thanks for your report!"))
 f = application.executor.submit(application.issue_reporter.send_report, report)
 f.add_done_callback(lambda f: wx.CallAfter(future_complete, f))

def activate_app():
 application.activation_manager.check_activation_status()

def check_for_update():
 import app_framework.updates
 app_framework.updates.check_for_update(application)
