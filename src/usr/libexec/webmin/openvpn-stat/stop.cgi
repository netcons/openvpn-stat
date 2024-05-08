#!/usr/bin/perl
# Stop the openvpn-statd daemon

require './openvpn-stat-lib.pl';
&ReadParse();
&error_setup($text{'stop_err'});
$err = &stop_openvpn_statd();
&error($err) if ($err);
&webmin_log("stop");
&redirect("");
