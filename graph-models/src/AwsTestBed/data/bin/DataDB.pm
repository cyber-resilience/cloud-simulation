#!/usr/bin/perl -w


#use strict;


package DataDB;


#BEGIN
#{
#  $SIG{'__WARN__'} =  sub { warn($_[0]) if ($_[0] !~ m/Subroutine Benchmark\:\:mytime redefined at/); };
#}


use Carp;
use DBI;
#use Data::Dumper qw(Dumper); $Data::Dumper::Sortkeys = 1;


sub new
{
  my $proto        =  shift;
  my $class        =  ref($proto) || $proto;

  my $self         =
  {
    DATABASE       => 'awstestbed',
    HOST           => 'db',
    USERID         => 'root',
    PASSWD         => 'nothing',
    ISTMT          => shift || '',
    TABLENAME      => shift || '',
    DBH            => shift || '',
  };

  bless($self, $class);

  return($self);
}


sub connect_db()
{
  my $self         =  shift;
  #print("DATABASE:" .  $self->{'DATABASE'}  . ":\n");
  #print("HOST:" .  $self->{'HOST'}  . ":\n");
  #print("USERID:" .  $self->{'USERID'}  . ":\n");
  #print("PASSWD:" .  $self->{'PASSWD'}  . ":\n");
  my $dsn          =  'dbi:mysql:database=' . $self->{'DATABASE'} . ':host=' . $self->{'HOST'} . ':port=3306';
  #print("DSN:$dsn:\n");
  my %attr         =  (PrintError => 0, RaiseError => 1);

  $self->{'DBH'}   =  DBI->connect($dsn, $self->{'USERID'}, $self->{'PASSWD'}, \%attr) || croak("ERROR: Can't connect, " . $DBI::errstr . "\n");

  return;
}


sub table_exist($)
{
  my $self         =  shift;
  my($table_name)  =  @_;

  my $dbh          =  $self->{'DBH'};
  my $sth          =  $dbh->table_info(undef, undef, $table_name, 'TABLE') || croak("ERROR: Can't get table information for table, $table_name: " . $DBI::errstr . "\n");
  my @data;
  while (@data     =  $sth->fetchrow_array())
  {
#print("INFO:" . join(',', @data) . ":\n");
    return(1) if ($data[2] eq "$table_name");
  }

  $sth->finish();
  return(0);
}


sub create_table($)
{
  my $self         =  shift;
  my($INPUT_FILE)  =  @_;

  my $TABLENAME    =  $INPUT_FILE;
  $TABLENAME       =~ s#.*/##;
  $TABLENAME       =~ s#\..*##;

  open(FH, "$INPUT_FILE") || die("ERROR: Can't open input file, $INPUT_FILE: $!\n");
  my $line         =  <FH>;
  close(FH);

  my @columns;
  my $idx          =  1;
  foreach (split(',', $line))
  {
    push(@columns, "col_$idx");
    $idx++;
  }
  my $columns      =  join("  INTEGER NOT NULL, ", @columns) . "  INTEGER NOT NULL";

  my $sql;
  if ($self->table_exist($TABLENAME))
  {
    $sql           =  "DROP TABLE $TABLENAME";
    #print("SQL:$sql:\n");
    $self->{'DBH'}->do($sql);
  }

  if (! $self->table_exist('metadata'))
  {
    $sql           =  "CREATE TABLE metadata (filename VARCHAR(200) PRIMARY KEY, rows INTEGER, columns INTEGER)";
    #print("SQL:$sql:\n");
    $self->{'DBH'}->do($sql);
  }

  $sql             =  "CREATE TABLE $TABLENAME ($columns)";
  #print("SQL:$sql:\n");
  $self->{'DBH'}->do($sql);

  $self->{'ISTMT'} =  "INSERT INTO $TABLENAME (" . join(', ', @columns) . ') VALUES (' . ('?, ' x $#columns) . '?)';
  #print("\nSTMT:$ISTMT:\n");

  return($TABLENAME);
}


sub populate_table($$)
{
  my $self         =  shift;
  my $INPUT_FILE   =  shift;
  my $TABLENAME    =  shift;

  my @columns;
  my $rows         =  0;
  my $sth          =  $self->{'DBH'}->prepare(qq{$self->{'ISTMT'}}) || croak("ERROR: Can't prepare, " . $DBI::errstr . "\n");
  open(FH, "$INPUT_FILE") || die("ERROR: Can't open input file, $INPUT_FILE: $!\n");
  while(<FH>)
  {
    chomp();
    @columns       =  split(',', $_);
#print(join(', ', @columns) . "\n");
    $sth->execute(@columns);
    $rows++;
  }
  close(FH);
  my $columns      =  scalar(@columns);
  eval {
    $self->{'DBH'}->do("DELETE FROM metadata WHERE filename = \"$TABLENAME\"");
  };
  my $stmt         =  "INSERT INTO metadata (filename, rows, columns) VALUES (?, ?, ?)";
  $sth             =  $self->{'DBH'}->prepare(qq{$stmt}) || croak("ERROR: Can't prepare, " . $DBI::errstr . "\n");
  $sth->execute($TABLENAME, $rows, $columns) || croak("ERROR: Can't insert into metadata, " . $DBI::errstr . "\n");

  $sth->finish();
  return;
}


sub get_file($)
{
  my $self         =  shift;
  my($filename)    =  shift;

  my $sth          =  $self->{'DBH'}->prepare("SELECT * FROM $filename") || croak("ERROR: Couldn't prepare statement, SELECT * FROM $filename: " . $DBI::errstr . "\n");

  $sth->execute() ||  croak("ERROR: Couldn't execute statement: " . $sth->errstr . "\n");

  my $file         =  '';
  while (@data     =  $sth->fetchrow_array())
  {
    $file         .=  join(',', @data) . "\n";
  }

  $sth->finish();
  return($file);
}


sub get_filelist()
{
  my $self         =  shift;
  my @filelist;

  my $sth          =  $self->{'DBH'}->prepare('SELECT filename FROM metadata') || croak("ERROR: Couldn't prepare statement, SELECT filename FROM metadata: " . $DBI::errstr . "\n");

  $sth->execute() || croak("ERROR: Couldn't execute statement: " . $sth->errstr . "\n");

  # Read the matching records and print them out          
  while (@data     =  $sth->fetchrow_array())
  {
    push(@filelist, $data[0]);
  }

  $sth->finish();
#print("FILELIST:" . join(',', @filelist) . ":\n");
  return(@filelist);
}


sub disconnect_db()
{
  my $self         =  shift;
  $self->{'DBH'}->disconnect() || croak("ERROR: Can't disconnect, " . $DBI::errstr . "\n");
  return;
}


1;
