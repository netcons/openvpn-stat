#!/usr/bin/perl

do 'openvpn-stat-lib.pl';
&ReadParse();
use Tie::File;
use POSIX qw(strftime);

print "Refresh: 15\r\n";
&ui_print_header( "<img src=images/openvpn.png hspace=4>$text{'title_monitor'}", $text{'title'}, "" );

my @logs = glob("$config{'live_log_dir'}/*.log");
if (@logs) {
	for my $log (@logs) {
		my @sessions = &getsessions($log);

		my $tunnel = $log;
		$tunnel =~ s/^[^_]*status-//;
		$tunnel	=~ s/\.log//;

      		my $tunconf = "/etc/openvpn/server/$tunnel.conf";
		my $tundev = '----';

		if( -e $tunconf ) {
			my @file_conf_lines = ();
			my @conf_line = ();

			use Fcntl 'O_RDONLY';
			tie @file_conf_lines, 'Tie::File', $tunconf, mode => O_RDONLY;
				@conf_line = grep(/^dev/, @file_conf_lines);
			untie @file_conf_lines;

			$tundev = $conf_line[0];
			$tundev =~ s/^[^_]* //;
			if( $tundev eq 'tun' ) { $tundev = 'tun0'; }
		       	if( $tundev eq 'tap' ) { $tundev = 'tap0'; }
		}

		print &ui_hr();
		my $now = &strftime('%d-%m-%Y %H:%M', localtime);
		print "Sessions from $log ( <b>".&ui_text_color($now, 'info')."</b> )";
		&showsessions($tundev,@sessions);
	}
} else {
	&error($text{'error_log'}." ".$config{'live_log_dir'});
}

&ui_print_footer('index.cgi',$text{'index_return'});

#============================================================================

sub getsessions {

	my $log = shift;

	my @sessions = ();
	my @file_log_lines = ();
	my @log_lines = ();

	use Fcntl 'O_RDONLY';
	tie @file_log_lines, 'Tie::File', $log, mode => O_RDONLY;
		@log_lines = grep(/^CLIENT_LIST/, @file_log_lines);
	untie @file_log_lines;

	foreach my $l (@log_lines) {

		my $cname = '';
		my $raddr = '';
		my $vaddr4 = '';
		my $vaddr6 = '';
		my $rbytes = '';
		my $sbytes = '';
		my $connd = '';
		my $connt = '';
		my $username = '';
		my $cid = '';
		my $pid = '';
		my $cipher = '';

		if( $l =~ /^CLIENT_LIST,(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)/ ) {
			$cname = $1;
			$raddr = $2;
			$vaddr4 = $3;
			$vaddr6 = $4;
			$rbytes = $5;
			$sbytes = $6;
			$connd = $7;
			$connt = $8;
			$username = $9;
			$cid = $10;
			$pid = $11;
			$cipher = $12;
		}
		push @sessions, [$cname, $raddr, $vaddr4, $vaddr6, $rbytes, $sbytes, $connd, $connt, $username, $cid, $pid, $cipher];
	}
	return @sessions;
}

sub showsessions {

	my $tundev = shift;
	my @sessions = @_;

  	my $sessiontotal = 0;
	my $sessioncount = @sessions;

	@tds = ( "" ,"" ,"" ,"" ,"" ,"" ,"width=1% style=text-align:right;white-space:nowrap" );

        print &ui_columns_start([
                          "<b>$text{'head_cname'}</b>",
                          "<b>$text{'head_vaddr4'}</b>",
                          "<b>$text{'head_tundev'}</b>",
                          "<b>$text{'head_raddr'}</b>",
                          "<b>$text{'head_sdate'}</b>",
                          "<b>$text{'head_stime'}</b>",
                          "<b>$text{'head_bytes'}</b>" ], 100, 0, \@tds);

	foreach my $l (@sessions) {
		local @cols;
		my ($cname, $raddr, $vaddr4, $vaddr6, $rbytes, $sbytes, $connd, $connt, $username, $cid, $pid, $cipher) = @$l;

		my @raddrfields = split(/:/, $raddr);
		my @conndfields = split(/ /, $connd);

		my @datefields = split(/-/, $conndfields[0]);
		my $sdate = "$datefields[2]-$datefields[1]-$datefields[0]";
		my @timefields = split(/:/, $conndfields[1]);
		my $stime = "$timefields[0]:$timefields[1]";

		$sessiontotal = ($sessiontotal + $rbytes + $sbytes);

		push(@cols, &ui_text_color($cname, 'info'));
		push(@cols, &ui_text_color($vaddr4, 'info'));
		push(@cols, &ui_text_color($tundev, 'info'));
		push(@cols, &ui_text_color($raddrfields[0], 'info'));
		push(@cols, &ui_text_color($sdate, 'info'));
		push(@cols, &ui_text_color($stime, 'info'));
		push(@cols, &ui_text_color(&roundbytes($rbytes + $sbytes), 'info'));
	        print &ui_columns_row(\@cols, \@tds);
	}
	print &ui_columns_row(["<b> Sessions : ".$sessioncount."</b>", undef, undef, undef, undef, undef, "<b> Total : ".&roundbytes($sessiontotal)."</b>"], \@tds);

	print &ui_columns_end();
}
