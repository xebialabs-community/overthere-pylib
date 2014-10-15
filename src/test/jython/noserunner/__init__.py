#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from java.lang import Thread
from org.python.core.imp import getSyspathJavaLoader
from com.xebialabs.deployit.plugin.otpylib.jython import PatchedSyspathJavaLoader

Thread.currentThread().contextClassLoader = PatchedSyspathJavaLoader(getSyspathJavaLoader())

# Setup the environment
import os
import sys
import site
import urllib2

class LocalEZSetup(object):

    def __init__(self, base_dir):
        self._base_dir = base_dir
        site_dir = os.path.join(base_dir, 'site-packages')
        self._site_dir = site_dir
        if not os.path.exists(site_dir): os.mkdir(site_dir)
        site.addsitedir(site_dir)
        sys.executable = ''
        os.environ['PYTHONPATH'] = ':'.join(sys.path)
        self._ez_setup = self._init_ez_setup()

    def _init_ez_setup(self):
        ez_setup_path = os.path.join(self._site_dir, 'ez_setup.py')
        if not os.path.exists(ez_setup_path):
            f = file(ez_setup_path, 'w')
            f.write(urllib2.urlopen('http://peak.telecommunity.com/dist/ez_setup.py').read())
            f.close()
        return self._import('ez_setup')

    def _fix_sys_path(self, mod_name):
        for mod in sys.modules.keys():
            if mod.startswith(mod_name):
                del sys.modules[mod]
        for path in sys.path:
            if path.startswith(self._site_dir):
                sys.path.remove(path)
        site.addsitedir(self._site_dir)

    def _install_module(self, mod_name):
        self._ez_setup.main(['--install-dir', self._site_dir, mod_name])
        self._fix_sys_path(mod_name)

    def _import(self, mod_name):
        return __import__(mod_name, globals(), locals(), [], -1)

    def ensure_module(self, mod_name):
        try:
            mod = self._import(mod_name)
        except ImportError:
            self._install_module(mod_name)
            mod = self._import(mod_name)
        return mod
