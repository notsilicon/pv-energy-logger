<html>
<head><title>modbus-tk - Master HMI - Result of query {{name}}</title>
<link rel="stylesheet" type="text/css" href="/media/style.css" media="all" />
<script type="text/javascript" src="/media/jquery-1.3.2.min.js"></script>
</body>
<div id="main">
<h1>Results of request {{friendly_name}}</h1>
<table class="breadcrumbs"><tr>
	<td><a href="/masters">Masters</a></td>
	<td>></td>
	<td><a href="/master/{{master.id}}">{{master.address}}</a></td>
	<td>></td>
	<td><a href="{{url}}">{{friendly_name}}</a></td>
</tr></table>
<table class="results">
	<tr><th style="width:30px"> </th>
	%for i in range(16):
	<th style="width:50px;">{{i}}</th>
	%end
	</tr>
	%for l in lines:
	<tr><th>{{l+start}}</th>
		%for r in results[l:l+16]:
			<td style="text-align:center">{{r}}</td>
		%end
	</tr> 
	%end
</table>
</div></body>
</html>