#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

from com.xebialabs.overthere import CmdLine, ConnectionOptions, Overthere, OperatingSystemFamily
from com.xebialabs.overthere.ssh import SshConnectionType
from com.xebialabs.overthere.cifs import CifsConnectionType, WinrmHttpsCertificateTrustStrategy, WinrmHttpsHostnameVerificationStrategy
from com.xebialabs.overthere.local import LocalFile
from com.xebialabs.overthere.util import OverthereUtils, MultipleOverthereExecutionOutputHandler, CapturingOverthereExecutionOutputHandler, ConsoleOverthereExecutionOutputHandler
from com.google.common.io import Resources
from java.lang import Thread, Integer
import posixpath
import time


class LocalConnectionOptions(object):
    def __init__(self, protocol="local", **kwargs):
        self.protocol = protocol
        self.tmpDeleteOnDisconnect = True
        self.tmpFileCreationRetries = 1000
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def build(self):
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
    def __init__(self, protocol, **kwargs):
        self.connectionTimeoutMillis=1200000
        super(LocalConnectionOptions, self).__init__(protocol, **kwargs)

class SshConnectionOptions(RemoteConnectionOptions):
    def __init__(self, address, username, **kwargs):
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
    def __init__(self, address, username, password, **kwargs):
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
    def __init__(self, options):
        self._options = options
        self.host = self
        self.os = options.os
        self.temporaryDirectoryPath = options.os.defaultTemporaryDirectoryPath


    def __getattr__(self, name):
        if name == "connection":
            return self.getConnection()
        raise AttributeError( "'OverthereHost' object has no attribute '%s'" % name)

    def getConnection(self):
        return Overthere.getConnection(self._options.protocol, self._options.build())


class OverthereHostSession(object):
    def __init__(self, host, stream_command_output=False):
        self.os = host.os
        self._host = host
        self._stream_command_output = stream_command_output
        self._conn = None
        self._work_dir = None

    def is_windows(self):
        return str(self.os) == 'WINDOWS'

    def get_conn(self):
        if self._conn is None:
            self._conn = self._host.connection
        return self._conn

    def close_conn(self):
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def work_dir(self):
        if self._work_dir is None:
            self._work_dir = self.get_conn().getTempFile("remote_plugin", ".tmp")
            self._work_dir.mkdir()
        return self._work_dir

    def work_dir_file(self, filepath):
        return self.work_dir().getFile(filepath)

    def remote_file(self, filepath):
        return self.get_conn().getFile(filepath)

    def local_file(self, filepath):
        return LocalFile.valueOf(filepath)

    def read_file(self, filepath):
        otfile = self.get_conn().getFile(filepath)
        if not otfile.exists():
            raise Exception("File [%s] does not exist" % filepath)
        return OverthereUtils.read(otfile, "UTF-8")

    def read_file_lines(self, filepath):
        return self.read_file(filepath).split(self.os.lineSeparator)

    def copy_to(self, source_otfile, target_otfile):
        source_otfile.copyTo(target_otfile)

    def upload_text_content_to_work_dir(self, content, filename, executable=False):
        target = self.work_dir_file(filename)
        if executable:
            target.setExecutable(executable)
        OverthereUtils.write(str(content), target)
        return target

    def upload_classpath_resource_to_work_dir(self, resource, executable=False):
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
        target = self.work_dir_file(source_otfile.name)
        source_otfile.copyTo(target)
        if executable:
            target.setExecutable(executable)
        return target

    ###
    # Some thing
    ###
    def execute(self, cmd):
        cmdline = CmdLine.build(cmd)
        capture_so_handler = CapturingOverthereExecutionOutputHandler.capturingHandler()
        capture_se_handler = CapturingOverthereExecutionOutputHandler.capturingHandler()

        if not self._stream_command_output:
            so_handler = capture_so_handler
            se_handler = capture_se_handler
        else:
            console_so_handler = ConsoleOverthereExecutionOutputHandler.sysoutHandler()
            console_se_hanlder = ConsoleOverthereExecutionOutputHandler.syserrHandler()
            so_handler = MultipleOverthereExecutionOutputHandler.multiHandler([capture_so_handler, console_so_handler])
            se_handler = MultipleOverthereExecutionOutputHandler.multiHandler([capture_se_handler, console_se_hanlder])

        rc = self.get_conn().execute(so_handler, se_handler, cmdline)
        #wait for output to drain
        time.sleep(1)

        return {'rc': rc, 'stdout': capture_so_handler.outputLines, 'stderr': capture_se_handler.outputLines}
