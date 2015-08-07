#!/usr/bin/perl -w

package IngestFile;

BEGIN
{
  push(@INC, '/data/bin/');
#  $SIG{'__WARN__'} = sub { warn($_[0]) if ($_[0] !~ m/Subroutine Benchmark\:\:mytime redefined at/); };
}

use strict;
use warnings;
use Carp;
use DataDB;
 
use Exporter qw(import);
our @EXPORT = qw(ingest);
 

sub ingest($)
{
  my($file) = @_;
  if (! -f "$file")
  {
    croak("ERROR: IngestFile Can't find input file, $file: $!\n");
  }

  my $db = new DataDB();
  $db->connect_db();

  $db->populate_table($file, $db->create_table($file));
  rename($file, "$file.done");

  $db->disconnect_db();

  return;
}


1;
