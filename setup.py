from setuptools import setup, find_packages

from app_elements import __version__, __author__, __doc__


setup(
 name = 'app_elements',
 version = __version__,
 author = __author__,
 description = __doc__,
 packages = find_packages(),
 package_data = {'app_elements':[
   "locale/*/*/*",
  ], },
 zip_safe = False,
 install_requires = [
  'platform_utils',
 ],
 dependency_links = [
  'http://hg.q-continuum.net/platform_utils/archive/tip.tar.gz#egg=platform_utils',
 ],
 classifiers = [
  'Development Status :: 4 - Beta',
  'Intended Audience :: Developers',
  'Programming Language :: Python',
    'Topic :: Software Development :: Libraries',
 ],
)
