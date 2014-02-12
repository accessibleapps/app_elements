from logging import getLogger
logger = getLogger('app_elements.interface')
import datetime
import os
import sys
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
 locale = application.locale.split('_')[0]
 if os.path.exists(os.path.join(docpath, locale)):
  docpath = os.path.join(docpath, locale)
 docpath = os.path.join(docpath, 'readme.html')
 docpath = 'file://%s' % os.path.abspath(docpath)
 web_browser.open(docpath)

def show_about_dialog():
 popups.about_box(application.name, application.version, website=application.website, copyright=_(u"Copyright %d %s") % (datetime.date.today().year, application.author))

def exit():
 app_framework.shutdown.shutdown(application)
