#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

import noserunner
import os
from overtherepy import LocalConnectionOptions, OverthereHost, OverthereHostSession
from com.xebialabs.overthere import OperatingSystemFamily

from  nose.tools import ok_, eq_

class TestOverthereSession(object):


    # preparing to test
    def setUp(self):
        self._linuxhost = OverthereHost(LocalConnectionOptions(os=OperatingSystemFamily.UNIX))
        self._session = OverthereHostSession(self._linuxhost)

    # ending the test
    def tearDown(self):
        self._session.close_conn()

    def test_not_windows_host(self):
        ok_(not self._session.is_windows())

    def test_work_dir_cleanup(self):
        workdir = self._session.work_dir()
        ok_(workdir.exists())
        workdir_path = workdir.path
        self._session.close_conn()
        ok_(not os.path.exists(workdir_path))

    def test_read_write_file(self):
        f = self._session.upload_text_content_to_work_dir("some text", "my.txt")
        text = self._session.read_file(f.path)
        eq_("some text", text)

    def test_upload_classpath_resource(self):
        f = self._session.upload_classpath_resource_to_work_dir("testfiles/singleline.txt")
        text = self._session.read_file(f.path)
        eq_("some text 1", text)

    def test_read_lines(self):
        f = self._session.upload_classpath_resource_to_work_dir("testfiles/multiline.txt")
        lines = self._session.read_file_lines(f.path)
        eq_(3, len(lines))

    def test_execute(self):
        f = self._session.upload_classpath_resource_to_work_dir("testfiles/echo.sh", executable=True)
        response = self._session.execute([f.path, "ping"])
        eq_(response['rc'], 0)
        eq_(response['stdout'][0], "Hi ping")


