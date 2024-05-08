#!/usr/bin/perl
# restart.cgi
# Restart with a HUP signal

require './openvpn-stat-lib.pl';
&ReadParse();
$err = &restart_openvpn_statd();
&error($err) if ($err);
sleep(2);	# wait to come back up
&webmin_log("restart");
&redirect("");
