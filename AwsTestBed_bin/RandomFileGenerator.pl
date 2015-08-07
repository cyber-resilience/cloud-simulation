#!/usr/bin/perl


#  - Data generators
#  ----  RadomFileGenerator(
#                           generate_interval_in_minutes,  
#                           min_rows,
#                           max_rows,
#                           num_cols,
#                           output_dir,
#                           output_prefix
#                          )

#  ----  Script produces CSV files with random data and randomly set file size.  
#  Appends a checksum column, so the number of output column is num_cols+1.
#  ----  Writes out files named as : 
#  output_dir/hostname_username_output_prefix_YYYYMMDDhhmm.csv


use strict;


BEGIN
{
  push(@INC, '/data/bin/');
#  $SIG{'__WARN__'}   =  sub { warn($_[0]) if ($_[0] !~ m/Subroutine Benchmark\:\:mytime redefined at/); };
}


use Carp;
#use Data::Dumper qw(Dumper); $Data::Dumper::Sortkeys = 1;
use Getopt::Long; Getopt::Long::Configure('bundling');
use POSIX qw(strftime);
use Sys::Hostname;


my @COPY_ARGV        =         @ARGV;
my $HELP             =             0;
my $HOSTNAME         =    hostname();
my $MINIMUM_FILES    =             1;
my $MAXIMUM_FILES    =             0;   #  NOTE: default is go forever
my $MINIMUM_INTERVAL =             1;
my $MAXIMUM_INTERVAL =             3;
my $MINIMUM_ROWS     =         50000;
my $MAXIMUM_ROWS     =         80000;
my $MINIMUM_VALUE    =            25;
my $MAXIMUM_VALUE    =            75;
my $NUMBER_COLS      =            49;   #  NOTE: The $NUMBER_COLS+1 column will be the sum of the values in the $NUMBER_COLS columns
my $OUTPUT_DIR       =   '/data/genfile';
my $OUTPUT_PREFIX    =       '_TEST';
my $OUTPUT_FILE      =            '';
my $STOP_FILE        =  '/data/config/stop';
my $TIMESTAMP        =  strftime("%Y%m%d%H%M", localtime());
my $USERNAME         =  $ENV{'USER'};
my $PROG             =  $0;


$PROG                =~ s#.*/##;


GetOptions(
            'f=i'    => \$MINIMUM_FILES,
            'F=i'    => \$MAXIMUM_FILES,
            'm=i'    => \$MINIMUM_INTERVAL,
            'M=i'    => \$MAXIMUM_INTERVAL,
            'r=i'    => \$MINIMUM_ROWS,
            'R=i'    => \$MAXIMUM_ROWS,
            'c=i'    => \$NUMBER_COLS,
            'h+'     => \$HELP,
            'o=s'    => \$OUTPUT_DIR,
            'p=s'    => \$OUTPUT_PREFIX,
            's=s'    => \$STOP_FILE,
            'v=i'    => \$MINIMUM_VALUE,
            'V=i'    => \$MAXIMUM_VALUE,
          );


sub get_hostname()
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
      next unless (/^\s*$ip\s+/);
      my($ip, $hostname, @rest) = split(/\s+/, $_);
      if (length($hostname) > 2)
      {
        $HOSTNAME    =  $hostname;
        last;
      }
    }
    close(FH);
  }

  return($HOSTNAME);
}


sub get_output_filename()
{
  $TIMESTAMP         =  strftime("%Y%m%d%H%M", localtime());
  $OUTPUT_FILE       =  $OUTPUT_DIR . '/' . $HOSTNAME . '_' . $USERNAME . $OUTPUT_PREFIX . '_' . $TIMESTAMP . '.csv';

  return($OUTPUT_FILE);
}


sub usage($)
{
  my($help)          =  @_;

  $OUTPUT_FILE       =  get_output_filename();

  print("\n$PROG " . join(' ', @COPY_ARGV) . "\n") if (! $help);

  print("\n");
  print("  Usage: $PROG [-h] | [-o output_dir] [-f min_files] [-F max_files] [-m min_interval] [-M max_interval] [-r min_rows] [-R max_rows] [-v min_value] [-V max_value] [-c num_cols] [-p output_prefix]\n\n");
  print("    -h = Help\n");
  print("    -o = Output directory ($OUTPUT_DIR)\n");
  print("    -f = Minimum number of files ($MINIMUM_FILES)\n");
  print("    -F = Maximum number of files ($MAXIMUM_FILES)\n");
  print("    -m = Minimum interval in minutes ($MINIMUM_INTERVAL)\n");
  print("    -M = Maximum interval in minutes ($MAXIMUM_INTERVAL)\n");
  print("    -r = Minimum number of rows ($MINIMUM_ROWS)\n");
  print("    -R = Maximum number of rows ($MAXIMUM_ROWS)\n");
  print("    -s = File to signal the program to stop ($STOP_FILE)\n");
  print("    -v = Minimum random value in a row ($MINIMUM_VALUE)\n");
  print("    -V = Maximum random value in a row ($MAXIMUM_VALUE)\n");
  print("    -c = Number of columns ($NUMBER_COLS)\n");
  print("    -p = Output prefix ($OUTPUT_PREFIX)\n");
  print("\n");
  print("    HOSTNAME:    $HOSTNAME\n");
  print("    USERNAME:    $USERNAME\n");
  print("    TIMESTAMP:   $TIMESTAMP\n");
  print("\n");
  print("    OUTPUT_FILE: $OUTPUT_FILE\n");
  print("\n");

  exit(0) if ($help);
}


sub get_random($$)
{
  my($x, $y)         =  @_;

  return(int(rand($y - $x)) + $x);
}


sub get_row()
{
  my @rand           =  map { get_random($MINIMUM_VALUE, $MAXIMUM_VALUE) } (1 .. $NUMBER_COLS);
  my $sum;
  $sum              +=  $_ for @rand;

  return(join(',', @rand) . ",$sum\n");
}


sub create_file($)
{
  my($file)          =  @_;

  if (-f $file)
  {
    carp("ERROR: Can't overwrite output OUTPUT_FILE, $OUTPUT_FILE: $!\n");
  }

  open(FH, ">$file.tmp") || carp("ERROR: Can't create file, $file.tmp: $!\n");
  foreach (1 .. get_random($MINIMUM_ROWS, $MAXIMUM_ROWS))
  {
    print(FH get_row());
  }
  close(FH);
  rename("$file.tmp", $file);

  return;
}


sub main()
{
  $HOSTNAME          =  get_hostname();

  usage(1) if (1 == $HELP);
  usage(1) if ($MINIMUM_FILES    > $MAXIMUM_FILES && ($MAXIMUM_FILES != 0));
  usage(1) if ($MINIMUM_INTERVAL > $MAXIMUM_INTERVAL);
  usage(1) if ($MINIMUM_ROWS     > $MAXIMUM_ROWS);
  usage(1) if ($MINIMUM_VALUE    > $MAXIMUM_VALUE);
  usage(1) if (-z $HOSTNAME);
  usage(1) if (12 <length($TIMESTAMP));
  if (! -d $OUTPUT_DIR)
  {
    usage(0);
    croak("ERROR: Can't find output directory, $OUTPUT_DIR: $!\n");
  }
  if (! -w $OUTPUT_DIR)
  {
    usage(0);
    croak("ERROR: Can't create files in output directory, $OUTPUT_DIR: $!\n");
  }

  $MINIMUM_INTERVAL *= 60;
  $MAXIMUM_INTERVAL *= 60;

  srand(scalar(time()));

  my $file_count     = 1;
  while ((! -f $STOP_FILE) && (($MAXIMUM_FILES == 0) || ($file_count <= $MAXIMUM_FILES)))
  {
    my $filename     = get_output_filename();
    #print("FILE:$file_count:$filename:\n");
    create_file($filename);
    $file_count++;
    sleep(get_random($MINIMUM_INTERVAL, $MAXIMUM_INTERVAL));
  }

  return;
}


main();


exit(0);
