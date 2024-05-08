#!/usr/bin/perl

BEGIN { push(@INC, ".."); };
use WebminCore;
&init_config();

sub restart_openvpn_statd {
	if ($config{'restart_cmd'}) {
        	local $out = `$config{'restart_cmd'} 2>&1 </dev/null`;
	        return "<pre>$out</pre>" if ($?);
	} else {
	        local $pid = &get_openvpn_statd_pid();
	        $pid || return $text{'apply_epid'};
	        &kill_logged('HUP', $pid);
	}
	return undef;
}

sub stop_openvpn_statd {
if ($config{'stop_cmd'}) {
        	local $out = `$config{'stop_cmd'} 2>&1 </dev/null`;
	        return "<pre>$out</pre>" if ($?);
	} else {
        	local $pid = &get_openvpn_statd_pid();
	        $pid || return $text{'apply_epid'};
        	&kill_logged('TERM', $pid);
        }
	return undef;
}

sub start_openvpn_statd {
	if (-f $config{'pid_file'} && !&check_pid_file($config{'pid_file'})) {
	        &unlink_file($config{'pid_file'});
        }
	if ($config{'start_cmd'}) {
        	$out = &backquote_logged("$config{'start_cmd'} 2>&1 </dev/null");
	        if ($?) { return "<pre>$out</pre>"; }
	} else {
        	$out = &backquote_logged("$config{'openvpn_statd_bin'} 2>&1 </dev/null");
	        if ($?) { return "<pre>$out</pre>"; }
        }
	return undef;
}

sub get_openvpn_statd_pid {
	local $file = $config{'pid_file'};
	if ($file) {
        	return &check_pid_file($file);
	} else {
        	local ($rv) = &find_byname("openvpn-statd");
	        return $rv;
        }
}

sub roundbytes {
	my $bytes = shift;
	my $n = 0;
	++$n and $bytes /= 1024 until $bytes < 1024;
	return sprintf "%.1f %s", $bytes, ( qw[ B KB MB GB TB ] )[ $n ];
}

1;
