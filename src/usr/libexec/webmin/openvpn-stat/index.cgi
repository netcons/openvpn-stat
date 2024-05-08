#!/usr/bin/perl

do 'openvpn-stat-lib.pl';

&ui_print_header(undef , $text{'title'}, "", undef, 1, 1, 0,
        &help_search_link("openvpn", "man", "doc"));

my @links = ('monitor.cgi',
	     'report.cgi');
my @titles = ($text{'index_icon_monitor'},
              $text{'index_icon_report'});
my @icons = ('images/monitor.png',
	     'images/report.png');

&icons_table(\@links, \@titles, \@icons, 2);

# Check if openvpn_statd is running
$pid = &get_openvpn_statd_pid();
print &ui_hr();
print &ui_buttons_start();
if ($pid) {
	# Running .. offer to restart and stop
	print &ui_buttons_row("restart.cgi",
			      $text{'index_restart'}, $text{'index_restartmsg'});

	print &ui_buttons_row("stop.cgi",
			      $text{'index_stop'}, $text{'index_stopmsg'});
	}
else {
	# Not running .. offer to start
	print &ui_buttons_row("start.cgi", $text{'index_start'},
			      $text{'index_startmsg'});
	}
print &ui_buttons_end();

&ui_print_footer("/", $text{'index'});
