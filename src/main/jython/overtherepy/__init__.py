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


"""
    Module to wrap the Overthere (https://github.com/xebialabs/overthere) library
"""
import os
import sys
from com.xebialabs.overthere import CmdLine, ConnectionOptions, Overthere, OperatingSystemFamily
from com.xebialabs.overthere.ssh import SshConnectionType
from com.xebialabs.overthere.cifs import CifsConnectionType, WinrmHttpsCertificateTrustStrategy, WinrmHttpsHostnameVerificationStrategy
from com.xebialabs.overthere.local import LocalFile
from com.xebialabs.overthere.util import OverthereUtils, MultipleOverthereExecutionOutputHandler, CapturingOverthereExecutionOutputHandler
from com.google.common.io import Resources
from java.lang import Thread, Integer
import posixpath
import time
from com.xebialabs.overtherepy import DirectoryDiff, PyLogger, PyLoggerExecutionOutputHandler


class LocalConnectionOptions(object):
    """Local connection settings"""

    def __init__(self, protocol="local", **kwargs):
        """
        Constructor
        :param protocol: https://github.com/xebialabs/overthere#protocols
        :param kwargs: See https://github.com/xebialabs/overthere#local available options
        """
        self.protocol = protocol
        self.tmpDeleteOnDisconnect = True
        self.tmpFileCreationRetries = 1000
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def build(self):
        """
        :return: com.xebialabs.overthere.ConnectionOptions
        """
        options = ConnectionOptions()
        for k, v in self.__dict__.items():
            self._set_conn_opt(options, k, v)
        return options

    def _set_conn_opt(self, options, key, value):
        if key == "protocol" or key == "temporaryDirectoryPath":
            return

        if value is None or str(value) == "":
            return

        if isinstance(value, Integer) and value.intValue() == 0:
            return

        #TODO: Add Jumpstation support
        #TODO: Add winrs proxy support
        options.set(key, value)


class RemoteConnectionOptions(LocalConnectionOptions):
    """Base class for remote connection options"""
    def __init__(self, protocol, **kwargs):
        self.connectionTimeoutMillis=1200000
        super(LocalConnectionOptions, self).__init__(protocol, **kwargs)


class SshConnectionOptions(RemoteConnectionOptions):
    """SSH Connection options.  See https://github.com/xebialabs/overthere#ssh
    Defaults settings:
    connectionType = SshConnectionType.SFTP
    os = OperatingSystemFamily.UNIX
    address = address
    port = 22
    username = username
    allocateDefaultPty = False
    interactiveKeyboardAuthRegex = ".*Password:[ ]?"
    sudoCommandPrefix = "sudo -u {0}"
    sudoQuoteCommand = False
    sudoPreserveAttributesOnCopyFromTempFile = True
    sudoPreserveAttributesOnCopyToTempFile = True
    sudoPasswordPromptRegex = ".*[Pp]assword.*:"
    sudoOverrideUmask = True
    suCommandPrefix = "su - {0} -c"
    suQuoteCommand = True
    suPreserveAttributesOnCopyFromTempFile = True
    suPreserveAttributesOnCopyToTempFile = True
    suPasswordPromptRegex = ".*[Pp]assword.*:"
    suOverrideUmask = True
    """

    def __init__(self, address, username, **kwargs):
        """
        Constructor
        :param address: ip or address of target machine
        :param username: user to login as
        :param kwargs: See https://github.com/xebialabs/overthere#ssh for options
        """
        self.connectionType = SshConnectionType.SFTP
        self.os = OperatingSystemFamily.UNIX
        self.address = address
        self.port = 22
        self.username = username
        self.allocateDefaultPty = False
        self.interactiveKeyboardAuthRegex = ".*Password:[ ]?"
        self.sudoCommandPrefix = "sudo -u {0}"
        self.sudoQuoteCommand = False
        self.sudoPreserveAttributesOnCopyFromTempFile = True
        self.sudoPreserveAttributesOnCopyToTempFile = True
        self.sudoPasswordPromptRegex = ".*[Pp]assword.*:"
        self.sudoOverrideUmask = True
        self.suCommandPrefix = "su - {0} -c"
        self.suQuoteCommand = True
        self.suPreserveAttributesOnCopyFromTempFile = True
        self.suPreserveAttributesOnCopyToTempFile = True
        self.suPasswordPromptRegex = ".*[Pp]assword.*:"
        self.suOverrideUmask = True
        super(RemoteConnectionOptions, self).__init__("ssh", **kwargs)


class CifsConnectionOptions(RemoteConnectionOptions):
    """CIFS Connection options.  See https://github.com/xebialabs/overthere#cifs
    Defaults settings:
    connectionType = CifsConnectionType.WINRM_INTERNAL
    os = OperatingSystemFamily.WINDOWS
    cifsPort = 445
    winrmEnableHttps = False
    winrsAllowDelegate = False
    winrmContext = "/wsman"
    winrmEnvelopSize = 153600
    winrmLocale = "en-US"
    winrmTimeout = "PT60.000S"
    winrmHttpsCertificateTrustStrategy = WinrmHttpsCertificateTrustStrategy.STRICT
    winrmHttpsHostnameVerificationStrategy = WinrmHttpsHostnameVerificationStrategy.STRICT
    winrmKerberosDebug = False
    winrmKerberosAddPortToSpn = False
    winrmKerberosUseHttpSpn = False
    winrsCompression = False
    winrsNoecho = False
    winrsNoprofile = False
    winrsUnencrypted = False
    """

    def __init__(self, address, username, password, **kwargs):
        """
        Constructor
        :param address: ip or address of target machine
        :param username: user to login as
        :param kwargs: See https://github.com/xebialabs/overthere#ssh for options
        """
        self.connectionType = CifsConnectionType.WINRM_INTERNAL
        self.os = OperatingSystemFamily.WINDOWS
        self.address = address
        self.username = username
        self.password = password
        self.cifsPort = 445
        self.winrmEnableHttps = False
        self.winrsAllowDelegate = False
        self.winrmContext = "/wsman"
        self.winrmEnvelopSize = 153600
        self.winrmLocale = "en-US"
        self.winrmTimeout = "PT60.000S"
        self.winrmHttpsCertificateTrustStrategy = WinrmHttpsCertificateTrustStrategy.STRICT
        self.winrmHttpsHostnameVerificationStrategy = WinrmHttpsHostnameVerificationStrategy.STRICT
        self.winrmKerberosDebug = False
        self.winrmKerberosAddPortToSpn = False
        self.winrmKerberosUseHttpSpn = False
        self.winrsCompression = False
        self.winrsNoecho = False
        self.winrsNoprofile = False
        self.winrsUnencrypted = False
        super(RemoteConnectionOptions, self).__init__("cifs", **kwargs)


class OverthereHost(object):
    """Represents an Overthere host.  Compatible with XL Deploy's HostContainer class. """
    def __init__(self, options):
        """
        :param options: an instance of either SshConnectionOptions, CifsConnectionOptions or LocalConnectionOptions
        """
        self._options = options
        self.host = self
        """host variable contains a reference to this instance"""
        self.os = options.os
        """os variable containers a reference to the target host's com.xebialabs.overthere.OperatingSystemFamily"""
        self.temporaryDirectoryPath = options.os.defaultTemporaryDirectoryPath


    def __getattr__(self, name):
        if name == "connection":
            return self.getConnection()
        raise AttributeError( "'OverthereHost' object has no attribute '%s'" % name)

    def getConnection(self):
        """
        :return: a new com.xebialabs.overthere.OverthereConnection
        """
        return Overthere.getConnection(self._options.protocol, self._options.build())


class CommandResponse(object):
    """Response from the execution of a remote os command"""
    def __init__(self, rc=-1, stdout=[], stderr=[]):
        """
        Constructor
        :param rc:  the return code from the executed remote command
        :param stdout: Array containing the standard output from the executed remote command
        :param stderr: Array containing the standard output from the executed remote command
        :return:
        """
        self.rc = rc
        self.stdout = stdout
        self.stderr = stderr

    def __getitem__(self, name):
        return self.__getattribute__(name)


class OverthereSessionLogger(PyLogger):
    """Simple class to log to console"""

    def __init__(self, enabled=True, capture=False, exec_ctx=None):
        """
        :param enabled: True to print informational log statements
        :param capture: True to capture informational log statements
        """
        self._enabled = enabled
        self._capture = capture
        self.output_lines = []
        self.error_lines = []
        self._exec_ctx = exec_ctx

    def info(self, msg):
        if self._enabled:
            if self._exec_ctx is not None:
                self._exec_ctx.logOutput(msg)
            else:
                print msg
        if self._capture:
            self.output_lines.append(msg)

    def error(self, msg):
        if self._enabled:
            if self._exec_ctx is not None:
                self._exec_ctx.logError(msg)
            else:
                print >> sys.stderr, msg
        if self._capture:
            self.error_lines.append(msg)


class Diff(object):
    """
    Contains the difference between two folders.
    """
    def __init__(self, old, new):
        """
        Constructor
        :param old: com.xebialabs.overthere.OverthereFile folder with old content
        :param new: com.xebialabs.overthere.OverthereFile folder with new content
        """
        self._old = old
        self._old_path = old.path
        self._new = new
        self._new_path = new.path
        self.added, self.removed, self.changed = ([], [], [])

    @staticmethod
    def md5(otfile):
        """
        Calculates the md5 checksum for the give overthere file
        :param otfile: com.xebialabs.overthere.OverthereFile
        :return: md5 checksum
        """
        return DirectoryDiff.md5(otfile)

    @staticmethod
    def calculate_diff(old, new):
        """
        Calculates the differences between two folders.
        :return: Diff object with added, removed and changed attributes. Each contain a list of com.xebialabs.overthere.OverthereFile
        """
        dir_diff = DirectoryDiff(old, new).diff()
        diff = Diff(old, new)
        diff.added = dir_diff.added
        diff.removed = dir_diff.removed
        diff.changed = dir_diff.changed
        return diff

    def _strip_path_prefix(self, otfile, prefix):
        rel_path = otfile.path[len(prefix) + 1:]
        return rel_path.replace('\\', '/')

    def strip_old_path_prefix(self, old_file):
        return self._strip_path_prefix(old_file, self._old_path)

    def strip_new_path_prefix(self, new_file):
        return self._strip_path_prefix(new_file, self._new_path)


class StringUtils(object):

    @staticmethod
    def concat(sarray, delimiter='\n'):
        """
        Creates a String by joining the String array using the delimiter.
        :param sarray: strings to join
        :param delimiter: to separate each string
        :return: concatenated string
        """
        return delimiter.join(sarray)

    @staticmethod
    def contains(s, item):
        """
        Checks if string contains the sub-string
        :param s: to check
        :param item:  that should be contained in s
        :return:  True if exists
        """
        return item in s

    @staticmethod
    def empty(s):
        """
        Checks if a string is None or stripped lenght is 0
        :param s: string to check
        :return: True if empty
        """
        return s is None or len(s.strip()) == 0

    @staticmethod
    def notEmpty(s):
        """
        Checks if a string is not empty
        :param s: string to check
        :return: True if not empty
        """
        return not StringUtils.empty(s)


class BashScriptBuilder(object):
    """ Utility class to help generate sh scripts """

    def __init__(self):
        self._lines = ["#!/bin/sh"]

    def build(self):
        return "\n".join(self._lines)

    def add_line(self, line, check_rc=False):
        self._lines.append(line)
        if check_rc:
            self.add_rc_check()
        return self

    def add_rc_check(self):
        self._lines.extend(["res=$?", "if [ $res != 0 ] ; then", "exit $res", "fi"])
        return self

    def add_lines(self, lines):
        self._lines.extend(lines)
        return self

    def set_env_var(self, k, v):
        self._lines.append('%s="%s"' % (k, v))
        self._lines.append("export %s" % k)


class BatchScriptBuilder(object):
    """ Utility class to help generate batch scripts """

    def __init__(self):
        self._lines = ["@echo off", "setlocal"]

    def build(self):
        self.add_line("endlocal")
        return "\r\n".join(self._lines)

    def add_line(self, line, check_rc=False):
        self._lines.append(line)
        if check_rc:
            self.add_rc_check()
        return self

    def add_lines(self, lines):
        self._lines.extend(lines)
        return self

    def add_rc_check(self):
        self._lines.extend(["set RES=%ERRORLEVEL%", "if not %RES% == 0 (", " exit %RES%", ")"])
        return self

    def set_env_var(self, k, v):
        self._lines.append("set %s=%s" % (k, v))


class OverthereHostSession(object):
    """ Session with a target host """
    def __init__(self, host, enable_logging=True, stream_command_output=False, execution_context=None):
        """
        :param host: to connect to. Can either be an OverthereHost or an XL Deploy's HostContainer class
        :param enable_logging: Enables info logging to console.
        :param execution_context: XLD ExecutionContext. Can be None.
        :param stream_command_output: True when remote command execution output is to be send to stdout and stderr
        """
        self.os = host.os
        self._host = host
        self._stream_command_output = stream_command_output
        self._conn = None
        self._work_dir = None
        self.logger = OverthereSessionLogger(enabled=enable_logging, exec_ctx=execution_context)

    def __enter__(self):
        self.work_dir()
        return self

    def __exit__(self, type, value, traceback):
        self.close_conn()

    def is_windows(self):
        """
        :return: True if target host is a Windows machine
        """
        return str(self.os) == 'WINDOWS'

    def get_conn(self):
        """Get connection to host.  Create new connection if one does not exist.
        :return: com.xebialabs.overthere.OverthereConnection.
        """
        if self._conn is None:
            self._conn = self._host.connection
        return self._conn

    def close_conn(self):
        """Close connection to target host"""
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def work_dir(self):
        """
        Get the temporary working directory on the target system for the current session.
        :return: com.xebialabs.overthere.OverthereFile
        """
        if self._work_dir is None:
            self._work_dir = self.get_conn().getTempFile("otpylib_plugin", ".tmp")
            self._work_dir.mkdir()
        return self._work_dir

    def work_dir_file(self, filepath):
        """
        Create a file in the session's working directory
        :param filepath: relative path to working directory
        :return: com.xebialabs.overthere.OverthereFile
        """
        return self.work_dir().getFile(filepath)

    def remote_file(self, filepath):
        """
        Get reference to remote file
        :param filepath: absolute path on target system
        :return: com.xebialabs.overthere.OverthereFile
        """
        return self.get_conn().getFile(filepath)

    def local_file(self, file):
        """
        Get reference to local file as an OverthereFile
        :param file: java.util.File
        :return: com.xebialabs.overthere.OverthereFile
        """
        return LocalFile.valueOf(file)

    def read_file(self, filepath, encoding="UTF-8"):
        """
        Reads the content of a remote file as a string
        :param filepath: absolute path on target system
        :param encoding: target file encoding
        :return: String
        """
        otfile = self.get_conn().getFile(filepath)
        if not otfile.exists():
            raise Exception("File [%s] does not exist" % filepath)
        return OverthereUtils.read(otfile, encoding)

    def read_file_lines(self, filepath, encoding="UTF-8"):
        """
        Reads the content of a remote file split by newline
        :param filepath: absolute path on target system
        :param encoding: target file encoding
        :return: Array of String
        """
        return self.read_file(filepath, encoding).split(self.os.lineSeparator)

    def copy_diff(self, target_path, diff):
        """
        Apply the changes represented by the Diff object to the target path.
        :param target_path: absolute path to folder on target system
        :param diff: Diff containing all changes to be applied to target path
        """
        target = self.remote_file(target_path)
        if not target.exists():
            self.logger.info("Creating path " + target.path)
            target.mkdirs()
        self.logger.info(str(len(diff.removed)) + " files to be removed.")
        self.logger.info(str(len(diff.added)) + " new files to be copied.")
        self.logger.info(str(len(diff.changed)) + " modified files to be copied.")

        if len(diff.removed) > 0:
            self.logger.info("Start removal of files...")
            for f in diff.removed:
                remove_file = target.getFile(diff.strip_old_path_prefix(f))
                file_type = "directory" if f.isDirectory() else "file"
                if remove_file.exists():
                    self.logger.info("Removing %s %s" % (file_type, remove_file.path))
                    remove_file.deleteRecursively()
                else:
                    self.logger.info("File %s does not exist. Ignoring." % remove_file.path)
            self.logger.info("Removal of files done.")

        if len(diff.added) > 0:
            self.logger.info("Start copying of new files...")
            for f in diff.added:
                add_file = target.getFile(diff.strip_new_path_prefix(f))
                file_type = "file"
                if f.isDirectory():
                    file_type = "directory"
                    add_file.mkdirs()
                else:
                    parent_dir = add_file.parentFile
                    if not parent_dir.exists():
                        parent_dir.mkdirs()
                self.logger.info("Copying %s %s" % (file_type, add_file.path))
                f.copyTo(add_file)
            self.logger.info("Copying of new files done.")

        if len(diff.changed) > 0:
            self.logger.info("Start copying of modified files...")
            for f in diff.changed:
                changed_file = target.getFile(diff.strip_new_path_prefix(f))
                self.logger.info("Updating file %s" % changed_file.path)
                f.copyTo(changed_file)
            self.logger.info("Copying of modified files done.")

    def copy_to(self, source, target, mkdirs=True):
        """
        Copy the source file to the target file
        :param source: com.xebialabs.overthere.OverthereFile
        :param target: com.xebialabs.overthere.OverthereFile
        :param mkdirs: Automatically create target directory
        :return:
        """
        if mkdirs and not target.exists():
            if source.isDirectory():
                self.logger.info("Creating path " + target.path)
                target.mkdirs()
            else:
                parent = target.parentFile
                if not parent.exists():
                    self.logger.info("Creating path " + parent.path)
                    parent.mkdirs()

        self.logger.info("Copying %s to %s" %(source.path, target.path))
        source.copyTo(target)

    def delete_from(self, source, target, target_dir_shared=False):
        """
        Uses the source directory to determine the files to delete from the target directory.
        Only the immediate sub-directories and files in the source directory base are used.
        If the target is a file, then it is deleted without analysing the source.
        When there are files present in the target directory after deleting source files from it, the target is not deleted.
        :param source: directory of files to be deleted.
        :param target: directory or file to be deleted.
        :param target_dir_shared: When True, the target directory itself will not be deleted.
        :return:
        """
        if not target.exists():
            self.logger.info("Target [%s] does not exist. No deletion to be performed" % target.path)
            return

        if not target.isDirectory():
            self.logger.info("Deleting [%s]" % target.path)
            target.delete()
            return

        assert source.isDirectory(), "Source [%s] is not a directory"

        remove_basedir = True
        for f in target.listFiles():
            if source.getFile(f.getName()).exists():
                if f.isDirectory():
                    self.logger.info("Recursively deleting directory [%s]" % f.path)
                    f.deleteRecursively()
                else:
                    self.logger.info("Deleting file [%s]" % f.path)
                    f.delete()
            else:
                remove_basedir = False

        if remove_basedir:
            if target_dir_shared:
                self.logger.info("Target directory [%s] is shared. Will not delete" % target.path)
            else:
                self.logger.info("Deleting directory [%s]" % target.path)
                target.delete()
        elif not target_dir_shared and not remove_basedir:
            self.logger.info("Target directory [%s] is not shared, but still has content from an external source. Will not delete" % target.path)

    def copy_text_to_file(self, content, target, mkdirs=True):
        """
        Copies the content to the specified file
        :param content: to write to file
        :param target: com.xebialabs.overthere.OverthereFile
        :param mkdirs: Automatically create target directory
        """
        parent = target.parentFile
        if mkdirs and not parent.exists():
            self.logger.info("Creating path " + parent.path)
            parent.mkdirs()
        OverthereUtils.write(str(content), target)

    def upload_text_content_to_work_dir(self, content, filename, executable=False):
        """
        Creates a file in the session's working directory with the specified content.
        :param content:  to write to file
        :param filename: relative path to file that will be created in session's working directory
        :param executable: True if file should be an executable file
        :return: com.xebialabs.overthere.OverthereFile
        """
        target = self.work_dir_file(filename)
        self.copy_text_to_file(str(content), target)
        if executable:
            target.setExecutable(executable)
        return target

    def upload_classpath_resource_to_work_dir(self, resource, executable=False):
        """
        Uploads the classpath resource to the session's working directory.
        :param resource: to find on the classpath to copy
        :param executable: True if the uploaded file should be made executable
        :return: com.xebialabs.overthere.OverthereFile
        """
        filename = posixpath.basename(resource)
        url = Thread.currentThread().contextClassLoader.getResource(resource)
        if url is None:
            raise Exception("Resource [%s] not found on classpath." % resource)
        target = self.work_dir_file(filename)
        outputstream = target.outputStream
        try:
            Resources.copy(url, outputstream)
        finally:
            outputstream.close()
        if executable:
            target.setExecutable(executable)
        return target

    def upload_file_to_work_dir(self, source_otfile, executable=False):
        """
        Uploads specified file to the session's working directory
        :param source_otfile: com.xebialabs.overthere.OverthereFile
        :param executable:
        :return:  com.xebialabs.overthere.OverthereFile
        """
        target = self.work_dir_file(source_otfile.name)
        source_otfile.copyTo(target)
        if executable:
            target.setExecutable(executable)
        return target

    def execute(self, cmd, check_success=True, suppress_streaming_output=False, wait_time=1):
        """
        Executes the command on the remote system and returns the result
        :param cmd: Command line as an Array of Strings or String.  A String is split by space.
        :param check_success: checks the return code is 0. On failure the output is printed to stdout and a system exit is performed
        :param suppress_streaming_output:  suppresses the output of the execution when the session is in streaming mode.
        :param wait_time:  wait time in second after launching the command and capture the result, default 1 second
        :return: CommandResponse
        """
        if isinstance(cmd, basestring):
            cmd = cmd.split()

        cmdline = CmdLine.build(cmd)
        capture_so_handler = CapturingOverthereExecutionOutputHandler.capturingHandler()
        capture_se_handler = CapturingOverthereExecutionOutputHandler.capturingHandler()

        if self._stream_command_output and not suppress_streaming_output:
            console_so_handler = PyLoggerExecutionOutputHandler.sysoutHandler(self.logger)
            console_se_handler = PyLoggerExecutionOutputHandler.syserrHandler(self.logger)
            so_handler = MultipleOverthereExecutionOutputHandler.multiHandler([capture_so_handler, console_so_handler])
            se_handler = MultipleOverthereExecutionOutputHandler.multiHandler([capture_se_handler, console_se_handler])
        else:
            so_handler = capture_so_handler
            se_handler = capture_se_handler

        rc = self.get_conn().execute(so_handler, se_handler, cmdline)
        #wait for output to drain
        time.sleep(wait_time)

        response = CommandResponse(rc=rc, stdout=capture_so_handler.outputLines, stderr=capture_se_handler.outputLines)

        if response.rc != 0 and check_success:
            if not self._stream_command_output and suppress_streaming_output:
                self.logger.error(StringUtils.concat(response.stdout))
                self.logger.error(StringUtils.concat(response.stderr))
            sys.exit(response.rc)

        return response
