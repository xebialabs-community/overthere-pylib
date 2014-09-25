#overthere-pylib
===============

Python wrapper for [Overthere](http://https://github.com/xebialabs/overthere) remoting library

## Basic Usage

### Setup connection settings

Depending on the target host, the following options are available :

* _overtherepy.SshConnectionOptions_
* _overtherepy.CifsConnectionOptions_
* _overtherepy.LocalConnectionOptions_

Please refer to the [Overthere](http://https://github.com/xebialabs/overthere) documentation for available options. Options are passed to the contructor as named parametes

<pre>
from overtherepy import LocalConnectionOptions, OverthereHost, OverthereHostSession
from com.xebialabs.overthere import OperatingSystemFamily
from com.xebialabs.overthere.cifs import CifsConnectionType

# Sample Local Connection Options
localOpts = LocalConnectionOptions(os=OperatingSystemFamily.UNIX)

# Sample SSH Connection options using custom port
sshOpts = SshConnectionOptions("myhost","myusername", port=2222 )

# Sample CIFS Connection options using TELNET for connection type
cifsOpts = CifsConnectionOptions("172.16.92.237", "Administrator", "secret",
            connectionType=CifsConnectionType.TELNET)

</pre>


Please refer to the [Overthere](http://https://github.com/xebialabs/overthere) documentation for available options. 

### Sample a session

<pre>
host = OverthereHost(cifsOpts)
session =  OverthereHostSession(host)

f = session.upload_classpath_resource_to_work_dir("testfiles/echo.sh", executable=True)
response = self._session.execute([f.path, "ping"])
if response['rc'] != 0:
	print "Failed to execute command"
	print response['stderr']
else:
	print "Response", str(response['stdout'])
	
session.close_conn()
</pre>

Current methods on OverthereHostSession

* is_windows(): Boolean
* get_conn(): OverthereConnection
* close_conn()
* work_dir(): OverthereFile
* work_dir_file(filepath: String): OverthereFile
* remote_file(filepath: String): OverthereFile
* local_file(filepath: String): OverthereFile
* read_file(filepath: String): String
* read_file_lines(filepath:String): String[]
* copy_to(source: OverthereFile, target: OverthereFile)
* upload_text_content_to_work_dir(content: String, filename: String, executable: Boolean)
* upload_classpath_resource_to_work_dir(resource:String, executable:Boolean)
* upload_file_to_work_dir(source:OverthereFile, executable:Boolean)
* execute(cmd:String[]): Dictionary with 'rc', 'stdout', 'stderr' keys