#!/usr/bin/perl

do 'openvpn-stat-lib.pl';
use Tie::File;
use POSIX qw(strftime);

&ui_print_header( $text{'title_report'}, $text{'title'}, "" );

my $type = 'summary';
my $month = lc(&strftime('%b', localtime));
my $year = &strftime('%Y', localtime);
my $string = '';

my $options_type = '';
my @types = ('summary','detail');
for my $k (@types) {
	$options_type .= '<option'.($k eq $type ? ' selected' : '').'>'.$k.'</option>';
}

my $options_month = '';
my @months = ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec');
for my $k (@months) {
	$options_month .= '<option'.($k eq $month ? ' selected' : '').'>'.$k.'</option>';
}

$td = "width=20% style='white-space: nowrap;'";
print qq~<br><br>
	<form action=\"report_stats.cgi\">
	<table border width=\"100%\">
		<tr $tb>
			<th>$text{'edit_report_title_create'}</th>
		</tr>
		<tr $cb>
			<td>
			<table width=\"100%\">
			<tr>
				<td $td><b>$text{'edit_report_type'}</b></td>
				<td><select name="type">$options_type</select></td>
			</tr>
  			<tr>
				<td $td><b>$text{'edit_report_month'}</b></td>
				<td><select name="month">$options_month</select></td>
			</tr>
			<tr>
				<td><b>$text{'edit_report_year'}</b></td>
				<td><input type="text" size="4" name="year" value="$year"></td>
			</tr>
			<tr>
				<td><b>$text{'edit_report_string'}</b></td>
				<td><input type="text" size="60" name="string" value="$string"></td>
			</tr>
			</table>
			</td>
		</tr>
	</table>~;

print "<table width=\"100%\"><tr>";
print '<td>'.&ui_submit( $text{'button_create'}, "create").'</td>';
print "</tr></table>";
print "</form>";

print "<br><br>";
&ui_print_footer('index.cgi',$text{'index_return'});
