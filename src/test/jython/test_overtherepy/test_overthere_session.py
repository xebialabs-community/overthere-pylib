#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from __future__ import with_statement
import xlnoserunner

import os
from overtherepy import LocalConnectionOptions, OverthereHost, OverthereHostSession, OverthereSessionLogger, Diff
from com.xebialabs.overthere import OperatingSystemFamily
from java.io import File
from java.lang import Thread

from nose.tools import ok_, eq_

class TestOverthereSession(object):

    # preparing to test
    def setUp(self):
        self._linuxhost = OverthereHost(LocalConnectionOptions(os=OperatingSystemFamily.UNIX))
        self._session = OverthereHostSession(self._linuxhost)
        self._session.logger = OverthereSessionLogger(capture=True)

    # ending the test
    def tearDown(self):
        self._session.close_conn()

    def _clear_logs(self):
        self._session.logger.output_lines = []
        self._session.logger.error_lines = []

    def assert_in_list(self, list, expect):
        r = [s for s in list if str(s) == str(expect)]
        eq_(len(r), 1, "expect [%s] to be in list [%s]" % (expect, str(list)))

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

    def test_upload_executable_file(self):
        f = self._session.upload_text_content_to_work_dir("#!/bin/sh\necho hello", "my.sh", executable=True)
        r = self._session.execute(f.path)
        self.assert_in_list(r.stdout, "hello")

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

    def test_execute_automatic_system_exit_on_failure(self):
        success = False
        try:
            f = self._session.upload_classpath_resource_to_work_dir("testfiles/echo.sh", executable=True)
            self._session.execute([f.path, "ping", "1"])
        except SystemExit:
            success = True
            pass
        eq_(success, True)

    def test_execute_check_success_turned_off(self):
        f = self._session.upload_classpath_resource_to_work_dir("testfiles/echo.sh", executable=True)
        response = self._session.execute("%s ping 1" % f.path, check_success=False)
        eq_(response.rc, 1)
        eq_(response['stdout'][0], "Hi ping")
        eq_(response['stdout'][1], "Exiting with 1")

    def test_with_support(self):
        s = OverthereHostSession(self._linuxhost)
        with s:
            work_dir = s.work_dir().path
            eq_(os.path.exists(work_dir), True)

        eq_(os.path.exists(work_dir), False)

    def _local_file(self, resource):
        url = Thread.currentThread().contextClassLoader.getResource(resource)
        return self._session.local_file(File(url.toURI()))


    def test_mkdirs_on_dir_copy(self):
        target = self._session.work_dir_file("some/path")
        source = self._local_file("testfiles")
        eq_(os.path.exists(target.path), False)
        self._session.copy_to(source, target)
        eq_(os.path.exists(target.path), True)
        eq_(os.path.exists(target.path + "/echo.sh"), True)

        log_info = self._session.logger.output_lines
        eq_(len(log_info), 2)
        eq_(log_info[0], "Creating path %s" % target.path)
        eq_(log_info[1], "Copying %s to %s" % (source.path, target.path))

    def test_mkdirs_on_file_copy(self):
        target = self._session.work_dir_file("some/path/some.txt")
        source = self._local_file("testfiles/echo.sh")
        eq_(os.path.exists(target.path), False)
        self._session.copy_to(source, target)
        eq_(os.path.exists(target.path), True)

        log_info = self._session.logger.output_lines
        eq_(len(log_info), 2)
        eq_(log_info[0], "Creating path %s" % target.parentFile.path)
        eq_(log_info[1], "Copying %s to %s" % (source.path, target.path))

    def test_mkdirs_on_turned_off_on_copy(self):
        target = self._session.work_dir_file("some/path")
        source = self._local_file("testfiles")
        success = False
        try:
            self._session.copy_to(source, target, mkdirs=False)
        except:
            success = True
        eq_(success, True)

    def test_delete_from_when_target_does_not_exit(self):
        target = self._session.work_dir_file("some/path")
        source = None
        self._session.delete_from(source, target)
        log_info = self._session.logger.output_lines
        eq_(len(log_info), 1)
        eq_(log_info[0], "Target [%s] does not exist. No deletion to be performed" % target.path)

    def test_delete_from_file_target(self):
        target = self._session.work_dir_file("some/path/test.txt")
        self._session.copy_text_to_file("xxx", target)
        eq_(os.path.exists(target.path), True)

        source = None
        self._session.delete_from(source, target)
        eq_(os.path.exists(target.path), False)

        log_info = self._session.logger.output_lines
        eq_(len(log_info), 2)
        self.assert_in_list(log_info, "Deleting [%s]" % target.path)

    def test_delete_from_folder_target(self):
        target = self._session.work_dir_file("some/path")
        source = self._local_file("testfiles")
        self._session.copy_to(source, target)
        eq_(os.path.exists(target.path), True)

        self._clear_logs()
        self._session.delete_from(source, target)
        eq_(os.path.exists(target.path), False)
        log_info = self._session.logger.output_lines

        eq_(len(log_info), 5)
        self.assert_in_list(log_info, "Recursively deleting directory [%s/asubdir]" % target.path)
        self.assert_in_list(log_info, "Deleting file [%s/echo.sh]" % target.path)
        self.assert_in_list(log_info, "Deleting file [%s/multiline.txt]" % target.path)
        self.assert_in_list(log_info, "Deleting file [%s/singleline.txt]" % target.path)
        self.assert_in_list(log_info, "Deleting directory [%s]" % target.path)

    def test_delete_from_with_external_resources(self):
        target = self._session.work_dir_file("some/path")
        source = self._local_file("testfiles")
        self._session.copy_to(source, target)
        eq_(os.path.exists(target.path), True)
        external_resource = self._session.work_dir_file("some/path/ext.txt")
        self._session.copy_text_to_file("xxx", external_resource)
        eq_(os.path.exists(external_resource.path), True)

        self._clear_logs()
        self._session.delete_from(source, target)
        eq_(os.path.exists(target.path), True)
        log_info = self._session.logger.output_lines

        eq_(len(log_info), 5)
        self.assert_in_list(log_info, "Recursively deleting directory [%s/asubdir]" % target.path)
        self.assert_in_list(log_info, "Deleting file [%s/echo.sh]" % target.path)
        self.assert_in_list(log_info, "Deleting file [%s/multiline.txt]" % target.path)
        self.assert_in_list(log_info, "Deleting file [%s/singleline.txt]" % target.path)
        self.assert_in_list(log_info, "Target directory [%s] is not shared, but still has content from an external source. Will not delete" % target.path)

    def test_copy_diff(self):
        old = self._local_file("directorycompare/old")
        new = self._local_file("directorycompare/new")
        deployed_old = self._session.work_dir_file("olddeployed")
        self._session.copy_to(old, deployed_old)
        eq_(os.path.exists(deployed_old.path), True)
        self._clear_logs()
        diff = Diff.calculate_diff(old, new)
        self._session.copy_diff(deployed_old.path, diff)
        log_info = self._session.logger.output_lines
        eq_(len(log_info), 17)
        self.assert_in_list(log_info, "3 files to be removed.")
        self.assert_in_list(log_info, "3 new files to be copied.")
        self.assert_in_list(log_info, "2 modified files to be copied.")
        self.assert_in_list(log_info, "Start removal of files...")
        self.assert_in_list(log_info, "Removing file %s/removefile.txt" % deployed_old.path)
        self.assert_in_list(log_info, "Removing directory %s/subdirremove" % deployed_old.path)
        self.assert_in_list(log_info, "Removing file %s/subdirboth/removefile.txt" % deployed_old.path)
        self.assert_in_list(log_info, "Removal of files done.")
        self.assert_in_list(log_info, "Start copying of new files...")
        self.assert_in_list(log_info, "Copying directory %s/subdirnew" % deployed_old.path)
        self.assert_in_list(log_info, "Copying file %s/newfile.txt" % deployed_old.path)
        self.assert_in_list(log_info, "Copying file %s/subdirboth/newfile.txt" % deployed_old.path)
        self.assert_in_list(log_info, "Copying of new files done.")
        self.assert_in_list(log_info, "Start copying of modified files...")
        self.assert_in_list(log_info, "Updating file %s/changedfile.txt" % deployed_old.path)
        self.assert_in_list(log_info, "Updating file %s/subdirboth/changedfile.txt" % deployed_old.path)
        self.assert_in_list(log_info, "Copying of modified files done.")

    def test_execution_ctx_logging(self):
        class ExecutionContext(object):
            def __init__(self):
                self.output_success = False
                self.error_success = False
            def logOutput(self, msg):
                self.output_success = True
            def logError(self, msg):
                self.error_success = True
        exec_ctx = ExecutionContext()
        session = OverthereHostSession(self._linuxhost, execution_context=exec_ctx)
        session.logger.info("Check")
        eq_(exec_ctx.output_success, True)
        session.logger.error("Check")
        eq_(exec_ctx.error_success, True)














