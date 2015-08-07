#!/usr/bin/perl -w


use strict;


BEGIN
{
  push(@INC, '/data/bin/');
#  $SIG{'__WARN__'} = sub { warn($_[0]) if ($_[0] !~ m/Subroutine Benchmark\:\:mytime redefined at/); };
}


use Carp;
#use Data::Dumper qw(Dumper); $Data::Dumper::Sortkeys = 1;
use DataDB;
use Getopt::Long; Getopt::Long::Configure('bundling');


my @COPY_ARGV      =  @ARGV;
my $HELP           =  0;
my $DATABASE       =  '{{ mysql_db }}';
my $HOST           =  'db';
my $USERID         =  '{{ mysql_user }}';
my $PASSWD         =  '{{ mysql_password }}';
my $INPUT_DIR      =  '/data/genfile';    #  $ENV{'HOME'};  #  '/people/d3c572  olympus_d3c572_PREFIX_201412072208.csv';
my $STOP_FILE      =  '/data/config/stop';
my $SLEEP          =  30;
my $PROG           =  $0;


$PROG              =~ s#.*/##;


GetOptions(
            'd=s'  => \$DATABASE,
            'h+'   => \$HELP,
            'H=s'  => \$HOST,
            'i=s'  => \$INPUT_DIR,
            'u=s'  => \$USERID,
            'p=s'  => \$PASSWD,
            's=s'  => \$STOP_FILE,
            'S=i'  => \$SLEEP,
          );


sub usage($)
{
  my($help)        =  @_;

  print("\n$PROG " . join(' ', @COPY_ARGV) . "\n") if (! $help);

  print("\n");
  print("  Usage: $0 [-h] | [-d database] [-H host] [-i input_dir] [-u userid] [-p password] [-s stop_file] [-S sleep]\n\n");
  print("    -h = Help\n");
  print("    -d = Database name ($DATABASE)\n");
  print("    -H = Hostname where database resides ($HOST)\n");
  print("    -i = Input directory to monitor for new files ($INPUT_DIR)\n");
  print("    -u = UserId to connect to database ($USERID)\n");
  print("    -p = Password for UserId (" . ('*' x length($PASSWD)) . ")\n");
  print("    -s = File to signal the program to stop ($STOP_FILE)\n");
  print("    -S = Time to sleep between looking for files ($SLEEP)\n");
  print("\n");

  exit(0) if ($help);

  return;
}


sub main()
{
  usage(1) if (1 == $HELP);

  if (! -d "$INPUT_DIR")
  {
    usage(0);
    croak("ERROR: Can't find input directory, $INPUT_DIR: $!\n");
  }

  my $db = new DataDB($DATABASE, $HOST, $USERID, $PASSWD);
  $db->connect_db();

  while (! -f $STOP_FILE)
  {
    opendir(DIR, $INPUT_DIR);
    my @files = grep { /\.csv$/ } readdir(DIR);
    closedir(DIR);

    foreach my $file (@files)
    {
      my $input_file = $INPUT_DIR . '/' . $file;
      $db->populate_table($input_file, $db->create_table($input_file));
      rename($input_file, "$input_file.done");
    }

    sleep($SLEEP);
  }

  $db->disconnect_db();

  return;
}


main();


exit(0);
