#!/usr/bin/perl

do 'openvpn-stat-lib.pl';
&ReadParse();
use Tie::File;
use File::Basename;

&ui_print_header( "<img src=images/openvpn.png hspace=4>$text{'title_report'}", $text{'title'}, "" );

my $type = $in{'type'};
my $month = $in{'month'};
my $year = $in{'year'};
my $string = $in{'string'};

my @logs = glob("$config{'log_dir'}/*-$month-$year-session.log");
if (@logs) {
	for my $log (@logs) {
		my @sessions = &getsessions($log);

		my $tunnel = $log;
		$tunnel = &basename($log, ".log");
		$tunnel =~ s/-.*//;

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
		print "Session $type from $log";
		if( $string ne '' ) { print " containing <i>".&ui_text_color($string, 'info')."</i>"; }
		if( $type eq 'summary' ) { &showsummary($tundev,@sessions); }
		if( $type eq 'detail' ) { &showdetail($tundev,@sessions); }
	}
} else {
	&error($text{'error_log'}." ".$config{'log_dir'}." for ".$month." ".$year);
}

&ui_print_footer('report.cgi',$text{'report_return'});

#============================================================================

sub getsessions {

	my $log = shift;

	my @sessions = ();
	my @file_log_lines = ();
	my @log_lines = ();

	use Fcntl 'O_RDONLY';
	tie @file_log_lines, 'Tie::File', $log, mode => O_RDONLY;
		if( $string ne '' ) {
			@log_lines = grep(/$string/, @file_log_lines);
		} else {
			@log_lines = @file_log_lines;
		}
	untie @file_log_lines;

	foreach my $l (@log_lines) {

		my $cname = '';
		my $stime = '';
		my $etime = '';
		my $usage = '';
		my $vaddr4 = '';
		my $ccount = '';

		if( $l =~ /^(.*?),(.*?),(.*?),(.*?),(.*?),(.*?)/ ) {
			$cname = $1;
			$stime = $2;
			$etime = $3;
			$usage = $4;
			$vaddr4 = $5;
			$ccount = $6;
		}
		push @sessions, [$cname, $stime, $etime, $usage, $vaddr4, $ccount];
	}
	return @sessions;
}

sub showsummary {

	my $tundev = shift;
	my @sessions = @_;

  	my $sessiontotal = 0;
	my $sessioncount = @sessions;

	my @certs = ();
	foreach my $l (@sessions) {
	  	my ($cname, $stime, $etime, $usage, $vaddr4, $ccount) = @$l;
	  	push(@certs, $cname);
	}

	@certs = sort(@certs);
	my $prev = '***none***';
	@certs = grep($_ ne $prev && (($prev) = $_), @certs);

	my @summarysessions = ();

	foreach my $cert (@certs) {
	
		my $usagetotal = 0;
		my $certsessioncount = 0;
		my $addr4;

		my @certsessions = ();
		foreach my $l (@sessions) {
	  		my ($cname, $stime, $etime, $usage, $vaddr4, $ccount) = @$l;
			 	if ($cname eq $cert) {
					$addr4 = $vaddr4;
					$usagetotal = $usagetotal + $usage;
					$certsessioncount++;
				}
	 	}

		my @summarysession = ($cert, $addr4, $certsessioncount, $usagetotal);
		push(@summarysessions, \@summarysession);

		$sessiontotal = $sessiontotal + $usagetotal;
	}

	my @summarysessions = sort { $b->[3] <=> $a->[3] } @summarysessions;

	@tds = ( "" ,"" ,"" ,"width=1% style=text-align:right;white-space:nowrap" );

        print &ui_columns_start([
                          "<b>$text{'head_cname'}</b>",
                          "<b>$text{'head_vaddr4'}</b>",
                          "<b>$text{'head_scount'}</b>",
                          "<b>$text{'head_bytes'}</b>" ], 100, 0, \@tds);

	foreach my $l (@summarysessions) {
		local @cols;
		my ($cname, $vaddr4, $scount, $usage) = @$l;

		push(@cols, &ui_text_color($cname, 'info'));
		push(@cols, &ui_text_color($vaddr4, 'info'));
		push(@cols, &ui_text_color($scount, 'info'));
		push(@cols, &ui_text_color(&roundbytes($usage), 'info'));
	        print &ui_columns_row(\@cols, \@tds);
	}
	print &ui_columns_row(["<b> Total :</b>", undef, "<b>".$sessioncount."</b>", "<b>".&roundbytes($sessiontotal)."</b>"], \@tds);

	print &ui_columns_end();
}

sub showdetail {

	my $tundev = shift;
	my @sessions = @_;

  	my $sessiontotal = 0;
	my $sessioncount = @sessions;

	my @sessions = sort { $b->[3] <=> $a->[3] } @sessions;

	@tds = ( "" ,"" ,"" ,"" ,"", "", "width=1% style=text-align:right;white-space:nowrap" );

        print &ui_columns_start([
                          "<b>$text{'head_cname'}</b>",
                          "<b>$text{'head_vaddr4'}</b>",
                          "<b>$text{'head_sdate'}</b>",
                          "<b>$text{'head_stime'}</b>",
                          "<b>$text{'head_edate'}</b>",
                          "<b>$text{'head_etime'}</b>",
                          "<b>$text{'head_bytes'}</b>" ], 100, 0, \@tds);

	foreach my $l (@sessions) {
		local @cols;
	  	my ($cname, $stime, $etime, $usage, $vaddr4, $ccount) = @$l;

		my @stimefields = split(/_/, $stime);
		my @sdatefields = split(/-/, $stimefields[0]);
		my $sdate = "$sdatefields[2]-$sdatefields[1]-$sdatefields[0]";
		my @stimes = split(/:/, $stimefields[1]);
		my $stime = "$stimes[0]:$stimes[1]";

		my @etimefields = split(/_/, $etime);
		my @edatefields = split(/-/, $etimefields[0]);
		my $edate = "$edatefields[2]-$edatefields[1]-$edatefields[0]";
		my @etimes = split(/:/, $etimefields[1]);
		my $etime = "$etimes[0]:$etimes[1]";

		push(@cols, &ui_text_color($cname, 'info'));
		push(@cols, &ui_text_color($vaddr4, 'info'));
		push(@cols, &ui_text_color($sdate, 'info'));
		push(@cols, &ui_text_color($stime, 'info'));
		push(@cols, &ui_text_color($edate, 'info'));
		push(@cols, &ui_text_color($etime, 'info'));
		push(@cols, &ui_text_color(&roundbytes($usage), 'info'));
	        print &ui_columns_row(\@cols, \@tds);

		$sessiontotal = $sessiontotal + $usage;
	}
	print &ui_columns_row(["<b> Sessions : ".$sessioncount."</b>", undef, undef, undef, undef, undef, "<b>".&roundbytes($sessiontotal)."</b>"], \@tds);

	print &ui_columns_end();
}
