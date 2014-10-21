#overthere-pylib
===============

Python wrapper for [Overthere](http://https://github.com/xebialabs/overthere) remoting library

## Basic Usage

### Setup connection settings

Depending on the target host, the following options are available :

* _overtherepy.SshConnectionOptions_
* _overtherepy.CifsConnectionOptions_
* _overtherepy.LocalConnectionOptions_

Please refer to the [Overthere](http://https://github.com/xebialabs/overthere) documentation for available options. Options are passed to the contructor as named parameters

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



### Sample a session and execution of remote os command

<pre>
...
host = OverthereHost(cifsOpts)
session =  OverthereHostSession(host)

f = session.upload_classpath_resource_to_work_dir("testfiles/echo.sh", executable=True)
response = self._session.execute([f.path, "ping"], check_success=False)
if response.rc != 0:
	print "Failed to execute command"
	print response.stderr
else:
	print "Response", str(response.stdout)
	
session.close_conn()
</pre>

### Sample session using 'with'

The session supports the 'with' statement.  You must first import the statement from the `___futures___` package. The session's connection is automatically closed at the end of the 'with' body.

<pre>
from __futures__ import with
...
with session:
	# do stuff
</pre>

### API Reference

Refer to  [Overtherepy Module Api Documentation](./api-docs/overtherepy.md) for a complete API reference.
Below is a description of the main _OverthereHostSession_ class.

<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ffc8d8">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#000000" face="helvetica, arial"><a name="OverthereHostSession">class <strong>OverthereHostSession</strong></a>(<a href="__builtin__.html#object">__builtin__.object</a>)</font></td></tr>
    
<tr bgcolor="#ffc8d8"><td rowspan=2><tt>&nbsp;&nbsp;&nbsp;</tt></td>
<td colspan=2><tt>Session&nbsp;with&nbsp;a&nbsp;target&nbsp;host<br>&nbsp;</tt></td></tr>
<tr><td>&nbsp;</td>
<td width="100%">Methods defined here:<br>
<dl><dt><a name="OverthereHostSession-__enter__"><strong>__enter__</strong></a>(self)</dt></dl>

<dl><dt><a name="OverthereHostSession-__exit__"><strong>__exit__</strong></a>(self, type, value, traceback)</dt></dl>

<dl><dt><a name="OverthereHostSession-__init__"><strong>__init__</strong></a>(self, host, enable_logging<font color="#909090">=True</font>, stream_command_output<font color="#909090">=False</font>)</dt><dd><tt>:param&nbsp;host:&nbsp;to&nbsp;connect&nbsp;to.&nbsp;Can&nbsp;either&nbsp;be&nbsp;an&nbsp;<a href="#OverthereHost">OverthereHost</a>&nbsp;or&nbsp;an&nbsp;XL&nbsp;Deploy's&nbsp;HostContainer&nbsp;class<br>
:param&nbsp;enable_logging:&nbsp;Enables&nbsp;info&nbsp;logging&nbsp;to&nbsp;console.<br>
:param&nbsp;stream_command_output:&nbsp;True&nbsp;when&nbsp;remote&nbsp;command&nbsp;execution&nbsp;output&nbsp;is&nbsp;to&nbsp;be&nbsp;send&nbsp;to&nbsp;stdout&nbsp;and&nbsp;stderr</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-close_conn"><strong>close_conn</strong></a>(self)</dt><dd><tt>Close&nbsp;connection&nbsp;to&nbsp;target&nbsp;host</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-copy_diff"><strong>copy_diff</strong></a>(self, target_path, diff)</dt><dd><tt>Apply&nbsp;the&nbsp;changes&nbsp;represented&nbsp;by&nbsp;the&nbsp;<a href="#Diff">Diff</a>&nbsp;<a href="__builtin__.html#object">object</a>&nbsp;to&nbsp;the&nbsp;target&nbsp;path.<br>
:param&nbsp;target_path:&nbsp;absolute&nbsp;path&nbsp;to&nbsp;folder&nbsp;on&nbsp;target&nbsp;system<br>
:param&nbsp;diff:&nbsp;<a href="#Diff">Diff</a>&nbsp;containing&nbsp;all&nbsp;changes&nbsp;to&nbsp;be&nbsp;applied&nbsp;to&nbsp;target&nbsp;path</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-copy_text_to_file"><strong>copy_text_to_file</strong></a>(self, content, target, mkdirs<font color="#909090">=True</font>)</dt><dd><tt>Copies&nbsp;the&nbsp;content&nbsp;to&nbsp;the&nbsp;specified&nbsp;file<br>
:param&nbsp;content:&nbsp;to&nbsp;write&nbsp;to&nbsp;file<br>
:param&nbsp;target:&nbsp;com.xebialabs.overthere.OverthereFile<br>
:param&nbsp;mkdirs:&nbsp;Automatically&nbsp;create&nbsp;target&nbsp;directory</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-copy_to"><strong>copy_to</strong></a>(self, source, target, mkdirs<font color="#909090">=True</font>)</dt><dd><tt>Copy&nbsp;the&nbsp;source&nbsp;file&nbsp;to&nbsp;the&nbsp;target&nbsp;file<br>
:param&nbsp;source:&nbsp;com.xebialabs.overthere.OverthereFile<br>
:param&nbsp;target:&nbsp;com.xebialabs.overthere.OverthereFile<br>
:param&nbsp;mkdirs:&nbsp;Automatically&nbsp;create&nbsp;target&nbsp;directory<br>
:return:</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-delete_from"><strong>delete_from</strong></a>(self, source, target, target_dir_shared<font color="#909090">=False</font>)</dt><dd><tt>Uses&nbsp;the&nbsp;source&nbsp;directory&nbsp;to&nbsp;determine&nbsp;the&nbsp;files&nbsp;to&nbsp;delete&nbsp;from&nbsp;the&nbsp;target&nbsp;directory.<br>
Only&nbsp;the&nbsp;immediate&nbsp;sub-directories&nbsp;and&nbsp;files&nbsp;in&nbsp;the&nbsp;source&nbsp;directory&nbsp;base&nbsp;are&nbsp;used.<br>
If&nbsp;the&nbsp;target&nbsp;is&nbsp;a&nbsp;file,&nbsp;then&nbsp;it&nbsp;is&nbsp;deleted&nbsp;without&nbsp;analysing&nbsp;the&nbsp;source.<br>
When&nbsp;there&nbsp;are&nbsp;files&nbsp;present&nbsp;in&nbsp;the&nbsp;target&nbsp;directory&nbsp;after&nbsp;deleting&nbsp;source&nbsp;files&nbsp;from&nbsp;it,&nbsp;the&nbsp;target&nbsp;is&nbsp;not&nbsp;deleted.<br>
:param&nbsp;source:&nbsp;directory&nbsp;of&nbsp;files&nbsp;to&nbsp;be&nbsp;deleted.<br>
:param&nbsp;target:&nbsp;directory&nbsp;or&nbsp;file&nbsp;to&nbsp;be&nbsp;deleted.<br>
:param&nbsp;target_dir_shared:&nbsp;When&nbsp;True,&nbsp;the&nbsp;target&nbsp;directory&nbsp;itself&nbsp;will&nbsp;not&nbsp;be&nbsp;deleted.<br>
:return:</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-execute"><strong>execute</strong></a>(self, cmd, check_success<font color="#909090">=True</font>)</dt><dd><tt>Executes&nbsp;the&nbsp;command&nbsp;on&nbsp;the&nbsp;remote&nbsp;system&nbsp;and&nbsp;returns&nbsp;the&nbsp;result<br>
:param&nbsp;cmd:&nbsp;Command&nbsp;line&nbsp;as&nbsp;an&nbsp;Array&nbsp;of&nbsp;Strings<br>
:param&nbsp;check_success:&nbsp;checks&nbsp;the&nbsp;return&nbsp;code&nbsp;is&nbsp;0.&nbsp;On&nbsp;failure&nbsp;the&nbsp;output&nbsp;is&nbsp;printed&nbsp;to&nbsp;stdout&nbsp;and&nbsp;a&nbsp;system&nbsp;exit&nbsp;is&nbsp;performed<br>
:return:&nbsp;<a href="#CommandResponse">CommandResponse</a></tt></dd></dl>

<dl><dt><a name="OverthereHostSession-get_conn"><strong>get_conn</strong></a>(self)</dt><dd><tt>Get&nbsp;connection&nbsp;to&nbsp;host.&nbsp;&nbsp;Create&nbsp;new&nbsp;connection&nbsp;if&nbsp;one&nbsp;does&nbsp;not&nbsp;exist.<br>
:return:&nbsp;com.xebialabs.overthere.OverthereConnection.</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-is_windows"><strong>is_windows</strong></a>(self)</dt><dd><tt>:return:&nbsp;True&nbsp;if&nbsp;target&nbsp;host&nbsp;is&nbsp;a&nbsp;Windows&nbsp;machine</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-local_file"><strong>local_file</strong></a>(self, file)</dt><dd><tt>Get&nbsp;reference&nbsp;to&nbsp;local&nbsp;file&nbsp;as&nbsp;an&nbsp;OverthereFile<br>
:param&nbsp;file:&nbsp;java.util.File<br>
:return:&nbsp;com.xebialabs.overthere.OverthereFile</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-read_file"><strong>read_file</strong></a>(self, filepath, encoding<font color="#909090">='UTF-8'</font>)</dt><dd><tt>Reads&nbsp;the&nbsp;content&nbsp;of&nbsp;a&nbsp;remote&nbsp;file&nbsp;as&nbsp;a&nbsp;string<br>
:param&nbsp;filepath:&nbsp;absolute&nbsp;path&nbsp;on&nbsp;target&nbsp;system<br>
:param&nbsp;encoding:&nbsp;target&nbsp;file&nbsp;encoding<br>
:return:&nbsp;String</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-read_file_lines"><strong>read_file_lines</strong></a>(self, filepath, encoding<font color="#909090">='UTF-8'</font>)</dt><dd><tt>Reads&nbsp;the&nbsp;content&nbsp;of&nbsp;a&nbsp;remote&nbsp;file&nbsp;split&nbsp;by&nbsp;newline<br>
:param&nbsp;filepath:&nbsp;absolute&nbsp;path&nbsp;on&nbsp;target&nbsp;system<br>
:param&nbsp;encoding:&nbsp;target&nbsp;file&nbsp;encoding<br>
:return:&nbsp;Array&nbsp;of&nbsp;String</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-remote_file"><strong>remote_file</strong></a>(self, filepath)</dt><dd><tt>Get&nbsp;reference&nbsp;to&nbsp;remote&nbsp;file<br>
:param&nbsp;filepath:&nbsp;absolute&nbsp;path&nbsp;on&nbsp;target&nbsp;system<br>
:return:&nbsp;com.xebialabs.overthere.OverthereFile</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-upload_classpath_resource_to_work_dir"><strong>upload_classpath_resource_to_work_dir</strong></a>(self, resource, executable<font color="#909090">=False</font>)</dt><dd><tt>Uploads&nbsp;the&nbsp;classpath&nbsp;resource&nbsp;to&nbsp;the&nbsp;session's&nbsp;working&nbsp;directory.<br>
:param&nbsp;resource:&nbsp;to&nbsp;find&nbsp;on&nbsp;the&nbsp;classpath&nbsp;to&nbsp;copy<br>
:param&nbsp;executable:&nbsp;True&nbsp;if&nbsp;the&nbsp;uploaded&nbsp;file&nbsp;should&nbsp;be&nbsp;made&nbsp;executable<br>
:return:&nbsp;com.xebialabs.overthere.OverthereFile</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-upload_file_to_work_dir"><strong>upload_file_to_work_dir</strong></a>(self, source_otfile, executable<font color="#909090">=False</font>)</dt><dd><tt>Uploads&nbsp;specified&nbsp;file&nbsp;to&nbsp;the&nbsp;session's&nbsp;working&nbsp;directory<br>
:param&nbsp;source_otfile:&nbsp;com.xebialabs.overthere.OverthereFile<br>
:param&nbsp;executable:<br>
:return:&nbsp;&nbsp;com.xebialabs.overthere.OverthereFile</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-upload_text_content_to_work_dir"><strong>upload_text_content_to_work_dir</strong></a>(self, content, filename, executable<font color="#909090">=False</font>)</dt><dd><tt>Creates&nbsp;a&nbsp;file&nbsp;in&nbsp;the&nbsp;session's&nbsp;working&nbsp;directory&nbsp;with&nbsp;the&nbsp;specified&nbsp;content.<br>
:param&nbsp;content:&nbsp;&nbsp;to&nbsp;write&nbsp;to&nbsp;file<br>
:param&nbsp;filename:&nbsp;relative&nbsp;path&nbsp;to&nbsp;file&nbsp;that&nbsp;will&nbsp;be&nbsp;created&nbsp;in&nbsp;session's&nbsp;working&nbsp;directory<br>
:param&nbsp;executable:&nbsp;True&nbsp;if&nbsp;file&nbsp;should&nbsp;be&nbsp;an&nbsp;executable&nbsp;file<br>
:return:&nbsp;com.xebialabs.overthere.OverthereFile</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-work_dir"><strong>work_dir</strong></a>(self)</dt><dd><tt>Get&nbsp;the&nbsp;temporary&nbsp;working&nbsp;directory&nbsp;on&nbsp;the&nbsp;target&nbsp;system&nbsp;for&nbsp;the&nbsp;current&nbsp;session.<br>
:return:&nbsp;com.xebialabs.overthere.OverthereFile</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-work_dir_file"><strong>work_dir_file</strong></a>(self, filepath)</dt><dd><tt>Create&nbsp;a&nbsp;file&nbsp;in&nbsp;the&nbsp;session's&nbsp;working&nbsp;directory<br>
:param&nbsp;filepath:&nbsp;relative&nbsp;path&nbsp;to&nbsp;working&nbsp;directory<br>
:return:&nbsp;com.xebialabs.overthere.OverthereFile</tt></dd></dl>

</td></tr></table> 
