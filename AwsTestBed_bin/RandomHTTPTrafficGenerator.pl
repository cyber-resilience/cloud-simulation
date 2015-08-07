#!/usr/bin/perl -w


#  - HTTP traffic generators
#  ----  RandomHTTPTrafficGenerators(
#                                    min_wait_interval, 
#                                    max_wait_interval,
#                                    max_url_count_from_list
#                                    )  
#  Generates HTTP requests from a known list of URLs.  Minimum and maximum wait 
#  time between two successive requests are specified by the input parameters.


use strict;


BEGIN
{
  push(@INC, '/data/bin/');
#  $SIG{'__WARN__'} = sub { warn($_[0]) if ($_[0] !~ m/Subroutine Benchmark\:\:mytime redefined at/); };
}


use Carp;
#use Data::Dumper qw(Dumper); $Data::Dumper::Sortkeys = 1;
use Getopt::Long; Getopt::Long::Configure('bundling');
use LWP::Simple;
use Sys::Hostname;


my @COPY_ARGV        =                @ARGV;
my $HELP             =                    0;
my $HOSTNAME         =           hostname();
my $HOST_IP          =                'web';
my $HOST_PORT        =                 8888;
my $MINIMUM_FILES    =                    1;
my $MAXIMUM_FILES    =                    0;   #  NOTE: default is go forever
my $MINIMUM_INTERVAL =                    1;
my $MAXIMUM_INTERVAL =                    5;
my $OUTPUT_DIR       =      '/data/getfile';
my $OUTPUT_FILE      =                   '';
my $STOP_FILE        =  '/data/config/stop';
my $USERNAME         =         $ENV{'USER'};
my $PROG             =                   $0;


$PROG                =~             s#.*/##;


GetOptions(
            'f=i' => \$MINIMUM_FILES,
            'F=i' => \$MAXIMUM_FILES,
            'm=i' => \$MINIMUM_INTERVAL,
            'M=i' => \$MAXIMUM_INTERVAL,
            'h+'  => \$HELP,
            'o=s' => \$OUTPUT_DIR,
            'p=i' => \$HOST_PORT,
            's=s' => \$STOP_FILE,
            'w=s' => \$HOST_IP,
          ) || die("ERROR: command line arguments\n");;


sub get_hostip()
{
  $HOSTNAME          =~  s/\..*//g;

  if ($HOSTNAME      =~  m/^ip[-]\d+/)
  {
    #  NOTE: We are running on an AWS system
    my $ip           =  $HOSTNAME;
    $ip              =~ s/^ip[-]//;
    $ip              =~ s/[-]/./g;
    open(FH, '/etc/hosts') || croak("ERROR: Can't open /etc/hosts: $!\n");
    while (<FH>)
    {
      next unless (/^\s*\d+\.\d+\.\d+\.\d+\s+web/);
      my($ip, $hostname, @rest) = split(/\s+/, $_);
      if (length($hostname) > 2)
      {
        $HOST_IP     =  $ip;
        last;
      }
    }
    close(FH);
  }

  return($HOST_IP);
}


sub usage($)
{
  my($help)    = @_;

  print("\n$0 " . join(' ', @COPY_ARGV) . "\n") if (! $help);

  print("\n");
  print("  Usage: $0 [-h] | [-w web_server] [-o output_dir] [-f min_files] [-F max_files] [-m min_interval] [-M max_interval] [-p web_server_port]\n\n");
  print("    -h = Help\n");
  print("    -o = Output directory ($OUTPUT_DIR)\n");
  print("    -f = Minimum number of files ($MINIMUM_FILES)\n");
  print("    -F = Maximum number of files ($MAXIMUM_FILES)\n");
  print("    -m = Minimum interval in minutes ($MINIMUM_INTERVAL)\n");
  print("    -M = Maximum interval in minutes ($MAXIMUM_INTERVAL)\n");
  print("    -p = Web Server port ($HOST_PORT)\n");
  print("    -s = File to signal the program to stop ($STOP_FILE)\n");
  print("    -w = Web server name or IP address ($HOST_IP)\n");
  print("\n");
  print("\n");

  exit(0) if ($help);
}


sub get_random($$)
{
  my($x, $y) = @_;

  return(int(rand($y - $x) + 0.5) + $x);
}


sub main()
{
  $HOST_IP           = get_hostip();

  usage(1) if (1 == $HELP);
  usage(1) if ($MINIMUM_FILES    > $MAXIMUM_FILES && ($MAXIMUM_FILES != 0));
  usage(1) if ($MINIMUM_INTERVAL > $MAXIMUM_INTERVAL);
  usage(1) if (! -d $OUTPUT_DIR);

  $MINIMUM_INTERVAL *= 60;
  $MAXIMUM_INTERVAL *= 60;

  srand(scalar(time()));

  my $file_count     = 1;
  while ((! -f $STOP_FILE) && (($MAXIMUM_FILES == 0) || ($file_count <= $MAXIMUM_FILES)))
  {
    my $filelist = get("http://$HOST_IP:$HOST_PORT/get_filelist");   #  || die("ERROR: Unable to get page\n");
    if (length($filelist) > 0)
    {
      my @filelist = split(/\n/, $filelist);
      my $filename = $filelist[get_random(1, scalar(@filelist)) - 1];  #  NOTE: Hack to deal with 0 based index

      #print("FILENAME:$filename:\n");
      getstore("http://$HOST_IP:$HOST_PORT/get_file?name=$filename", "$OUTPUT_DIR/$filename.txt") || die("ERROR: Unable to get page\n");
      $file_count++;
    }
    sleep(get_random($MINIMUM_INTERVAL, $MAXIMUM_INTERVAL));
  }

  return;
}


main();


exit(0);
