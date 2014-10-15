<html><head><title>Python: package overtherepy</title>
</head><body bgcolor="#f0f0f8">

<p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ee77aa">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#ffffff" face="helvetica, arial"><big><strong>Classes</strong></big></font></td></tr>
    
<tr><td bgcolor="#ee77aa"><tt>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</tt></td><td>&nbsp;</td>
<td width="100%"><dl>
<dt><font face="helvetica, arial"><a href="__builtin__.html#object">__builtin__.object</a>
</font></dt><dd>
<dl>
<dt><font face="helvetica, arial"><a href="#CommandResponse">CommandResponse</a>
</font></dt><dt><font face="helvetica, arial"><a href="#LocalConnectionOptions">LocalConnectionOptions</a>
</font></dt><dd>
<dl>
<dt><font face="helvetica, arial"><a href="#RemoteConnectionOptions">RemoteConnectionOptions</a>
</font></dt><dd>
<dl>
<dt><font face="helvetica, arial"><a href="#CifsConnectionOptions">CifsConnectionOptions</a>
</font></dt><dt><font face="helvetica, arial"><a href="#SshConnectionOptions">SshConnectionOptions</a>
</font></dt></dl>
</dd>
</dl>
</dd>
<dt><font face="helvetica, arial"><a href="#OverthereHost">OverthereHost</a>
</font></dt><dt><font face="helvetica, arial"><a href="#OverthereHostSession">OverthereHostSession</a>
</font></dt></dl>
</dd>
</dl>
 <p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ffc8d8">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#000000" face="helvetica, arial"><a name="CifsConnectionOptions">class <strong>CifsConnectionOptions</strong></a>(<a href="#RemoteConnectionOptions">RemoteConnectionOptions</a>)</font></td></tr>
    
<tr bgcolor="#ffc8d8"><td rowspan=2><tt>&nbsp;&nbsp;&nbsp;</tt></td>
<td colspan=2><tt>CIFS&nbsp;Connection&nbsp;options.&nbsp;&nbsp;See&nbsp;https://github.com/xebialabs/overthere#cifs<br>
Defaults&nbsp;settings:<br>
connectionType&nbsp;=&nbsp;CifsConnectionType.WINRM_INTERNAL<br>
os&nbsp;=&nbsp;OperatingSystemFamily.WINDOWS<br>
cifsPort&nbsp;=&nbsp;445<br>
winrmEnableHttps&nbsp;=&nbsp;False<br>
winrsAllowDelegate&nbsp;=&nbsp;False<br>
winrmContext&nbsp;=&nbsp;"/wsman"<br>
winrmEnvelopSize&nbsp;=&nbsp;153600<br>
winrmLocale&nbsp;=&nbsp;"en-US"<br>
winrmTimeout&nbsp;=&nbsp;"PT60.000S"<br>
winrmHttpsCertificateTrustStrategy&nbsp;=&nbsp;WinrmHttpsCertificateTrustStrategy.STRICT<br>
winrmHttpsHostnameVerificationStrategy&nbsp;=&nbsp;WinrmHttpsHostnameVerificationStrategy.STRICT<br>
winrmKerberosDebug&nbsp;=&nbsp;False<br>
winrmKerberosAddPortToSpn&nbsp;=&nbsp;False<br>
winrmKerberosUseHttpSpn&nbsp;=&nbsp;False<br>
winrsCompression&nbsp;=&nbsp;False<br>
winrsNoecho&nbsp;=&nbsp;False<br>
winrsNoprofile&nbsp;=&nbsp;False<br>
winrsUnencrypted&nbsp;=&nbsp;False<br>&nbsp;</tt></td></tr>
<tr><td>&nbsp;</td>
<td width="100%"><dl><dt>Method resolution order:</dt>
<dd><a href="#CifsConnectionOptions">CifsConnectionOptions</a></dd>
<dd><a href="#RemoteConnectionOptions">RemoteConnectionOptions</a></dd>
<dd><a href="#LocalConnectionOptions">LocalConnectionOptions</a></dd>
<dd><a href="__builtin__.html#object">__builtin__.object</a></dd>
</dl>
<hr>
Methods defined here:<br>
<dl><dt><a name="CifsConnectionOptions-__init__"><strong>__init__</strong></a>(self, address, username, password, **kwargs)</dt><dd><tt>Constructor<br>
:param&nbsp;address:&nbsp;ip&nbsp;or&nbsp;address&nbsp;of&nbsp;target&nbsp;machine<br>
:param&nbsp;username:&nbsp;user&nbsp;to&nbsp;login&nbsp;as<br>
:param&nbsp;kwargs:&nbsp;See&nbsp;https://github.com/xebialabs/overthere#ssh&nbsp;for&nbsp;options</tt></dd></dl>

<hr>
Methods inherited from <a href="#LocalConnectionOptions">LocalConnectionOptions</a>:<br>
<dl><dt><a name="CifsConnectionOptions-build"><strong>build</strong></a>(self)</dt><dd><tt>:return:&nbsp;com.xebialabs.overthere.ConnectionOptions</tt></dd></dl>

<hr>
Data descriptors inherited from <a href="#LocalConnectionOptions">LocalConnectionOptions</a>:<br>
<dl><dt><strong>__dict__</strong></dt>
<dd><tt>dictionary&nbsp;for&nbsp;instance&nbsp;variables&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
<dl><dt><strong>__weakref__</strong></dt>
<dd><tt>list&nbsp;of&nbsp;weak&nbsp;references&nbsp;to&nbsp;the&nbsp;object&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
</td></tr></table> <p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ffc8d8">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#000000" face="helvetica, arial"><a name="CommandResponse">class <strong>CommandResponse</strong></a>(<a href="__builtin__.html#object">__builtin__.object</a>)</font></td></tr>
    
<tr bgcolor="#ffc8d8"><td rowspan=2><tt>&nbsp;&nbsp;&nbsp;</tt></td>
<td colspan=2><tt>Response&nbsp;from&nbsp;the&nbsp;execution&nbsp;of&nbsp;a&nbsp;remote&nbsp;os&nbsp;command<br>&nbsp;</tt></td></tr>
<tr><td>&nbsp;</td>
<td width="100%">Methods defined here:<br>
<dl><dt><a name="CommandResponse-__getitem__"><strong>__getitem__</strong></a>(self, name)</dt></dl>

<dl><dt><a name="CommandResponse-__init__"><strong>__init__</strong></a>(self, rc<font color="#909090">=-1</font>, stdout<font color="#909090">=[]</font>, stderr<font color="#909090">=[]</font>)</dt><dd><tt>Constructor<br>
:param&nbsp;rc:&nbsp;&nbsp;the&nbsp;return&nbsp;code&nbsp;from&nbsp;the&nbsp;executed&nbsp;remote&nbsp;command<br>
:param&nbsp;stdout:&nbsp;Array&nbsp;containing&nbsp;the&nbsp;standard&nbsp;output&nbsp;from&nbsp;the&nbsp;executed&nbsp;remote&nbsp;command<br>
:param&nbsp;stderr:&nbsp;Array&nbsp;containing&nbsp;the&nbsp;standard&nbsp;output&nbsp;from&nbsp;the&nbsp;executed&nbsp;remote&nbsp;command<br>
:return:</tt></dd></dl>

<hr>
Data descriptors defined here:<br>
<dl><dt><strong>__dict__</strong></dt>
<dd><tt>dictionary&nbsp;for&nbsp;instance&nbsp;variables&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
<dl><dt><strong>__weakref__</strong></dt>
<dd><tt>list&nbsp;of&nbsp;weak&nbsp;references&nbsp;to&nbsp;the&nbsp;object&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
</td></tr></table> <p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ffc8d8">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#000000" face="helvetica, arial"><a name="LocalConnectionOptions">class <strong>LocalConnectionOptions</strong></a>(<a href="__builtin__.html#object">__builtin__.object</a>)</font></td></tr>
    
<tr bgcolor="#ffc8d8"><td rowspan=2><tt>&nbsp;&nbsp;&nbsp;</tt></td>
<td colspan=2><tt>Local&nbsp;connection&nbsp;settings<br>&nbsp;</tt></td></tr>
<tr><td>&nbsp;</td>
<td width="100%">Methods defined here:<br>
<dl><dt><a name="LocalConnectionOptions-__init__"><strong>__init__</strong></a>(self, protocol<font color="#909090">='local'</font>, **kwargs)</dt><dd><tt>Constructor<br>
:param&nbsp;protocol:&nbsp;https://github.com/xebialabs/overthere#protocols<br>
:param&nbsp;kwargs:&nbsp;See&nbsp;https://github.com/xebialabs/overthere#local&nbsp;available&nbsp;options</tt></dd></dl>

<dl><dt><a name="LocalConnectionOptions-build"><strong>build</strong></a>(self)</dt><dd><tt>:return:&nbsp;com.xebialabs.overthere.ConnectionOptions</tt></dd></dl>

<hr>
Data descriptors defined here:<br>
<dl><dt><strong>__dict__</strong></dt>
<dd><tt>dictionary&nbsp;for&nbsp;instance&nbsp;variables&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
<dl><dt><strong>__weakref__</strong></dt>
<dd><tt>list&nbsp;of&nbsp;weak&nbsp;references&nbsp;to&nbsp;the&nbsp;object&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
</td></tr></table> <p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ffc8d8">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#000000" face="helvetica, arial"><a name="OverthereHost">class <strong>OverthereHost</strong></a>(<a href="__builtin__.html#object">__builtin__.object</a>)</font></td></tr>
    
<tr bgcolor="#ffc8d8"><td rowspan=2><tt>&nbsp;&nbsp;&nbsp;</tt></td>
<td colspan=2><tt>Represents&nbsp;an&nbsp;Overthere&nbsp;host.&nbsp;&nbsp;Compatible&nbsp;with&nbsp;XL&nbsp;Deploy's&nbsp;HostContainer&nbsp;class.<br>&nbsp;</tt></td></tr>
<tr><td>&nbsp;</td>
<td width="100%">Methods defined here:<br>
<dl><dt><a name="OverthereHost-__getattr__"><strong>__getattr__</strong></a>(self, name)</dt></dl>

<dl><dt><a name="OverthereHost-__init__"><strong>__init__</strong></a>(self, options)</dt><dd><tt>:param&nbsp;options:&nbsp;an&nbsp;instance&nbsp;of&nbsp;either&nbsp;<a href="#SshConnectionOptions">SshConnectionOptions</a>,&nbsp;<a href="#CifsConnectionOptions">CifsConnectionOptions</a>&nbsp;or&nbsp;<a href="#LocalConnectionOptions">LocalConnectionOptions</a></tt></dd></dl>

<dl><dt><a name="OverthereHost-getConnection"><strong>getConnection</strong></a>(self)</dt><dd><tt>:return:&nbsp;a&nbsp;new&nbsp;com.xebialabs.overthere.OverthereConnection</tt></dd></dl>

<hr>
Data descriptors defined here:<br>
<dl><dt><strong>__dict__</strong></dt>
<dd><tt>dictionary&nbsp;for&nbsp;instance&nbsp;variables&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
<dl><dt><strong>__weakref__</strong></dt>
<dd><tt>list&nbsp;of&nbsp;weak&nbsp;references&nbsp;to&nbsp;the&nbsp;object&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
</td></tr></table> <p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ffc8d8">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#000000" face="helvetica, arial"><a name="OverthereHostSession">class <strong>OverthereHostSession</strong></a>(<a href="__builtin__.html#object">__builtin__.object</a>)</font></td></tr>
    
<tr bgcolor="#ffc8d8"><td rowspan=2><tt>&nbsp;&nbsp;&nbsp;</tt></td>
<td colspan=2><tt>Session&nbsp;with&nbsp;a&nbsp;target&nbsp;host<br>&nbsp;</tt></td></tr>
<tr><td>&nbsp;</td>
<td width="100%">Methods defined here:<br>
<dl><dt><a name="OverthereHostSession-__init__"><strong>__init__</strong></a>(self, host, stream_command_output<font color="#909090">=False</font>)</dt><dd><tt>:param&nbsp;host:&nbsp;to&nbsp;connect&nbsp;to.&nbsp;Can&nbsp;either&nbsp;be&nbsp;an&nbsp;<a href="#OverthereHost">OverthereHost</a>&nbsp;or&nbsp;an&nbsp;XL&nbsp;Deploy's&nbsp;HostContainer&nbsp;class<br>
:param&nbsp;stream_command_output:&nbsp;True&nbsp;when&nbsp;remote&nbsp;command&nbsp;execution&nbsp;output&nbsp;is&nbsp;to&nbsp;be&nbsp;send&nbsp;to&nbsp;stdout&nbsp;and&nbsp;stderr</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-close_conn"><strong>close_conn</strong></a>(self)</dt><dd><tt>Close&nbsp;connection&nbsp;to&nbsp;target&nbsp;host</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-copy_to"><strong>copy_to</strong></a>(self, source_otfile, target_otfile)</dt><dd><tt>Copy&nbsp;the&nbsp;source&nbsp;file&nbsp;to&nbsp;the&nbsp;target&nbsp;file<br>
:param&nbsp;source_otfile:&nbsp;com.xebialabs.overthere.OverthereFile<br>
:param&nbsp;target_otfile:&nbsp;com.xebialabs.overthere.OverthereFile</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-execute"><strong>execute</strong></a>(self, cmd)</dt><dd><tt>Executes&nbsp;the&nbsp;command&nbsp;on&nbsp;the&nbsp;remote&nbsp;system&nbsp;and&nbsp;returns&nbsp;the&nbsp;result<br>
:param&nbsp;cmd:&nbsp;Command&nbsp;line&nbsp;as&nbsp;an&nbsp;Array&nbsp;of&nbsp;Strings<br>
:return:&nbsp;<a href="#CommandResponse">CommandResponse</a></tt></dd></dl>

<dl><dt><a name="OverthereHostSession-get_conn"><strong>get_conn</strong></a>(self)</dt><dd><tt>Get&nbsp;connection&nbsp;to&nbsp;host.&nbsp;&nbsp;Create&nbsp;new&nbsp;connection&nbsp;if&nbsp;one&nbsp;does&nbsp;not&nbsp;exist.<br>
:return:&nbsp;com.xebialabs.overthere.OverthereConnection.</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-is_windows"><strong>is_windows</strong></a>(self)</dt><dd><tt>:return:&nbsp;True&nbsp;if&nbsp;target&nbsp;host&nbsp;is&nbsp;a&nbsp;Windows&nbsp;machine</tt></dd></dl>

<dl><dt><a name="OverthereHostSession-local_file"><strong>local_file</strong></a>(self, filepath)</dt><dd><tt>Get&nbsp;reference&nbsp;to&nbsp;local&nbsp;file<br>
:param&nbsp;filepath:&nbsp;absolute&nbsp;path&nbsp;on&nbsp;local&nbsp;system<br>
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

<hr>
Data descriptors defined here:<br>
<dl><dt><strong>__dict__</strong></dt>
<dd><tt>dictionary&nbsp;for&nbsp;instance&nbsp;variables&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
<dl><dt><strong>__weakref__</strong></dt>
<dd><tt>list&nbsp;of&nbsp;weak&nbsp;references&nbsp;to&nbsp;the&nbsp;object&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
</td></tr></table> <p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ffc8d8">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#000000" face="helvetica, arial"><a name="RemoteConnectionOptions">class <strong>RemoteConnectionOptions</strong></a>(<a href="#LocalConnectionOptions">LocalConnectionOptions</a>)</font></td></tr>
    
<tr bgcolor="#ffc8d8"><td rowspan=2><tt>&nbsp;&nbsp;&nbsp;</tt></td>
<td colspan=2><tt>Base&nbsp;class&nbsp;for&nbsp;remote&nbsp;connection&nbsp;options<br>&nbsp;</tt></td></tr>
<tr><td>&nbsp;</td>
<td width="100%"><dl><dt>Method resolution order:</dt>
<dd><a href="#RemoteConnectionOptions">RemoteConnectionOptions</a></dd>
<dd><a href="#LocalConnectionOptions">LocalConnectionOptions</a></dd>
<dd><a href="__builtin__.html#object">__builtin__.object</a></dd>
</dl>
<hr>
Methods defined here:<br>
<dl><dt><a name="RemoteConnectionOptions-__init__"><strong>__init__</strong></a>(self, protocol, **kwargs)</dt></dl>

<hr>
Methods inherited from <a href="#LocalConnectionOptions">LocalConnectionOptions</a>:<br>
<dl><dt><a name="RemoteConnectionOptions-build"><strong>build</strong></a>(self)</dt><dd><tt>:return:&nbsp;com.xebialabs.overthere.ConnectionOptions</tt></dd></dl>

<hr>
Data descriptors inherited from <a href="#LocalConnectionOptions">LocalConnectionOptions</a>:<br>
<dl><dt><strong>__dict__</strong></dt>
<dd><tt>dictionary&nbsp;for&nbsp;instance&nbsp;variables&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
<dl><dt><strong>__weakref__</strong></dt>
<dd><tt>list&nbsp;of&nbsp;weak&nbsp;references&nbsp;to&nbsp;the&nbsp;object&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
</td></tr></table> <p>
<table width="100%" cellspacing=0 cellpadding=2 border=0 summary="section">
<tr bgcolor="#ffc8d8">
<td colspan=3 valign=bottom>&nbsp;<br>
<font color="#000000" face="helvetica, arial"><a name="SshConnectionOptions">class <strong>SshConnectionOptions</strong></a>(<a href="#RemoteConnectionOptions">RemoteConnectionOptions</a>)</font></td></tr>
    
<tr bgcolor="#ffc8d8"><td rowspan=2><tt>&nbsp;&nbsp;&nbsp;</tt></td>
<td colspan=2><tt>SSH&nbsp;Connection&nbsp;options.&nbsp;&nbsp;See&nbsp;https://github.com/xebialabs/overthere#ssh<br>
Defaults&nbsp;settings:<br>
connectionType&nbsp;=&nbsp;SshConnectionType.SFTP<br>
os&nbsp;=&nbsp;OperatingSystemFamily.UNIX<br>
address&nbsp;=&nbsp;address<br>
port&nbsp;=&nbsp;22<br>
username&nbsp;=&nbsp;username<br>
allocateDefaultPty&nbsp;=&nbsp;False<br>
interactiveKeyboardAuthRegex&nbsp;=&nbsp;".*Password:[&nbsp;]?"<br>
sudoCommandPrefix&nbsp;=&nbsp;"sudo&nbsp;-u&nbsp;{0}"<br>
sudoQuoteCommand&nbsp;=&nbsp;False<br>
sudoPreserveAttributesOnCopyFromTempFile&nbsp;=&nbsp;True<br>
sudoPreserveAttributesOnCopyToTempFile&nbsp;=&nbsp;True<br>
sudoPasswordPromptRegex&nbsp;=&nbsp;".*[Pp]assword.*:"<br>
sudoOverrideUmask&nbsp;=&nbsp;True<br>
suCommandPrefix&nbsp;=&nbsp;"su&nbsp;-&nbsp;{0}&nbsp;-c"<br>
suQuoteCommand&nbsp;=&nbsp;True<br>
suPreserveAttributesOnCopyFromTempFile&nbsp;=&nbsp;True<br>
suPreserveAttributesOnCopyToTempFile&nbsp;=&nbsp;True<br>
suPasswordPromptRegex&nbsp;=&nbsp;".*[Pp]assword.*:"<br>
suOverrideUmask&nbsp;=&nbsp;True<br>&nbsp;</tt></td></tr>
<tr><td>&nbsp;</td>
<td width="100%"><dl><dt>Method resolution order:</dt>
<dd><a href="#SshConnectionOptions">SshConnectionOptions</a></dd>
<dd><a href="#RemoteConnectionOptions">RemoteConnectionOptions</a></dd>
<dd><a href="#LocalConnectionOptions">LocalConnectionOptions</a></dd>
<dd><a href="__builtin__.html#object">__builtin__.object</a></dd>
</dl>
<hr>
Methods defined here:<br>
<dl><dt><a name="SshConnectionOptions-__init__"><strong>__init__</strong></a>(self, address, username, **kwargs)</dt><dd><tt>Constructor<br>
:param&nbsp;address:&nbsp;ip&nbsp;or&nbsp;address&nbsp;of&nbsp;target&nbsp;machine<br>
:param&nbsp;username:&nbsp;user&nbsp;to&nbsp;login&nbsp;as<br>
:param&nbsp;kwargs:&nbsp;See&nbsp;https://github.com/xebialabs/overthere#ssh&nbsp;for&nbsp;options</tt></dd></dl>

<hr>
Methods inherited from <a href="#LocalConnectionOptions">LocalConnectionOptions</a>:<br>
<dl><dt><a name="SshConnectionOptions-build"><strong>build</strong></a>(self)</dt><dd><tt>:return:&nbsp;com.xebialabs.overthere.ConnectionOptions</tt></dd></dl>

<hr>
Data descriptors inherited from <a href="#LocalConnectionOptions">LocalConnectionOptions</a>:<br>
<dl><dt><strong>__dict__</strong></dt>
<dd><tt>dictionary&nbsp;for&nbsp;instance&nbsp;variables&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
<dl><dt><strong>__weakref__</strong></dt>
<dd><tt>list&nbsp;of&nbsp;weak&nbsp;references&nbsp;to&nbsp;the&nbsp;object&nbsp;(if&nbsp;defined)</tt></dd>
</dl>
</td></tr></table></td></tr></table>
</body></html>