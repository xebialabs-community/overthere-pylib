#
# THIS CODE AND INFORMATION ARE PROVIDED "AS IS" WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY AND/OR FITNESS
# FOR A PARTICULAR PURPOSE. THIS CODE AND INFORMATION ARE NOT SUPPORTED BY XEBIALABS.
#

"""
    Module to wrap the Overthere (https://github.com/xebialabs/overthere) library
"""
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


class OverthereHostSession(object):
    """ Session with a target host """
    def __init__(self, host, stream_command_output=False):
        """
        :param host: to connect to. Can either be an OverthereHost or an XL Deploy's HostContainer class
        :param stream_command_output: True when remote command execution output is to be send to stdout and stderr
        """
        self.os = host.os
        self._host = host
        self._stream_command_output = stream_command_output
        self._conn = None
        self._work_dir = None

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
            self._work_dir = self.get_conn().getTempFile("remote_plugin", ".tmp")
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

    def local_file(self, filepath):
        """
        Get reference to local file
        :param filepath: absolute path on local system
        :return: com.xebialabs.overthere.OverthereFile
        """
        return LocalFile.valueOf(filepath)

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

    def copy_to(self, source_otfile, target_otfile):
        """
        Copy the source file to the target file
        :param source_otfile: com.xebialabs.overthere.OverthereFile
        :param target_otfile: com.xebialabs.overthere.OverthereFile
        """
        source_otfile.copyTo(target_otfile)

    def upload_text_content_to_work_dir(self, content, filename, executable=False):
        """
        Creates a file in the session's working directory with the specified content.
        :param content:  to write to file
        :param filename: relative path to file that will be created in session's working directory
        :param executable: True if file should be an executable file
        :return: com.xebialabs.overthere.OverthereFile
        """
        target = self.work_dir_file(filename)
        if executable:
            target.setExecutable(executable)
        OverthereUtils.write(str(content), target)
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

    def execute(self, cmd):
        """
        Executes the command on the remote system and returns the result
        :param cmd: Command line as an Array of Strings
        :return: CommandResponse
        """
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

        return CommandResponse(rc=rc, stdout=capture_so_handler.outputLines, stderr=capture_se_handler.outputLines)
