#
# Copyright (c) 2008-2014, XebiaLabs B.V., All rights reserved.
#
#
# Overtherepy is licensed under the terms of the GPLv2
# <http://www.gnu.org/licenses/old-licenses/gpl-2.0.html>, like most XebiaLabs Libraries.
# There are special exceptions to the terms and conditions of the GPLv2 as it is applied to
# this software, see the FLOSS License Exception
# <http://github.com/xebialabs/overthere/blob/master/LICENSE>.
#
# This program is free software; you can redistribute it and/or modify it under the terms
# of the GNU General Public License as published by the Free Software Foundation; version 2
# of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with this
# program; if not, write to the Free Software Foundation, Inc., 51 Franklin St, Fifth
# Floor, Boston, MA 02110-1301  USA
#

from java.lang import Thread
from org.python.core.imp import getSyspathJavaLoader
from com.xebialabs.overtherepy.jython import PatchedSyspathJavaLoader

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
