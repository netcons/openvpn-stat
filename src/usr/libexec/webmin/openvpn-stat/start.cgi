#!/usr/bin/perl
# start.cgi
# Start the openvpn-statd daemon

require './openvpn-stat-lib.pl';
&ReadParse();
&error_setup($text{'start_err'});
$err = &start_openvpn_statd();
&error($err) if ($err);
&webmin_log("start");
&redirect("");
