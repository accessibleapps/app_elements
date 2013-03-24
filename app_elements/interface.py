from logging import getLogger
logger = getLogger('app_elements.interface')
import datetime
from platform_utils import web_browser, paths
from wx_utils import popups
import app_framework
import app_elements
application = app_elements.find_application_module()

def view_documentation():
 if paths.is_frozen():
  docpath = os.path.join(paths.embedded_data_path(), 'readme.html')
 else:
  docpath = os.path.join(paths.app_path(), '..', 'doc', 'readme.html')
 docpath = 'file://%s' % os.path.abspath(docpath)
 web_browser.open(docpath)

def show_about_dialog():
 popups.about_box(application.name, application.version, website=application.website, copyright=_(u"Copyright %d %s") % (datetime.date.today().year, application.author))

def exit():
 app_framework.shutdown.shutdown(application)
