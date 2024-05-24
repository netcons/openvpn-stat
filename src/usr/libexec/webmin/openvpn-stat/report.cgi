#!/usr/bin/perl

do 'openvpn-stat-lib.pl';
use Tie::File;
use POSIX qw(strftime);

&ui_print_header( "<img src=images/openvpn.png hspace=4>$text{'edit_report_title_create'}", $text{'title'}, "" );

my $type = 'summary';
my $month = lc(&strftime('%b', localtime));
my $year = &strftime('%Y', localtime);
my $string = '';

my @types = ('summary','detail');

my @months = ('jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec');

print &ui_subheading("<img src=images/openvpn.png hspace=4>$text{'edit_report_title_create'}");
print &ui_form_start("report_stats.cgi", "post");
my @tds = ( "width=20% style=white-space:nowrap ", "width=80%" );
print &ui_columns_start(undef, 100, 0, \@tds);
my $col = '';
$col = &ui_select("type", $type, \@types);
print &ui_columns_row([ "<b>$text{'edit_report_type'}</b>", $col ], \@tds);
$col = &ui_select("month", $month, \@months);
print &ui_columns_row([ "<b>$text{'edit_report_month'}</b>", $col ], \@tds);
$col = &ui_textbox("year", $year, 4, 0, 4);
print &ui_columns_row([ "<b>$text{'edit_report_year'}</b>", $col ], \@tds);
$col = &ui_textbox("string", $string, 60, 0, 60);
print &ui_columns_row([ "<b>$text{'edit_report_string'}</b>", $col ], \@tds);
print &ui_columns_end();

print "<table width=100%><tr>";
print '<td>'.&ui_submit( $text{'button_create'}, "create").'</td>';
print "</tr></table>";
print &ui_form_end();

print "<br><br>";
&ui_print_footer('index.cgi',$text{'index_return'});
