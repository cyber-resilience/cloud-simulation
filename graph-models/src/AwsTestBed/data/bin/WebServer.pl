#!/usr/bin/perl


use strict;


BEGIN
{
  push(@INC, '/data/bin/');
#  $SIG{'__WARN__'} = sub { warn($_[0]) if ($_[0] !~ m/Subroutine Benchmark\:\:mytime redefined at/); };
}


{
  package MyWebServer;
 
  use DataDB;
  use HTTP::Server::Simple::CGI;
  use base qw(HTTP::Server::Simple::CGI);
 
  my $DATABASE       =  'awstestbed';
  my $HOST           =  'bedstone';
  my $USERID         =  'd3c572';
  my $PASSWD         =  'Gaypig23';
  my %dispatch       = (
                        '/hello'        => \&resp_hello,
                        '/get_filelist' => \&resp_filelist,
                        '/get_file'     => \&resp_file,
                        # ...
                       );
 
  sub handle_request
  {
    my $self = shift;
    my $cgi  = shift;
   
    my $path = $cgi->path_info();
    my $handler = $dispatch{$path};
 
    if (ref($handler) eq "CODE")
    {
      print "HTTP/1.0 200 OK\r\n";
      $handler->($cgi);
    }
    else
    {
      print "HTTP/1.0 404 Not found\r\n";
      print $cgi->header, $cgi->start_html('Not found'), $cgi->h1('Not found'), $cgi->end_html;
    }
  }
 

  sub resp_hello
  {
    my $cgi  = shift;   # CGI.pm object
    return if !ref $cgi;
     
    my $who = $cgi->param('name');
     
    print $cgi->header, $cgi->start_html("Hello"), $cgi->h1("Hello $who!"), $cgi->end_html;

    return;
  }
 

  sub resp_filelist
  {
    my $cgi  = shift;   # CGI.pm object
    return if !ref $cgi;
     
    my $db = new DataDB($DATABASE, $HOST, $USERID, $PASSWD);
    $db->connect_db();
    my @filelist = $db->get_filelist();
    $db->disconnect_db();

    print $cgi->header('text/plain'), join("\n", @filelist);

    return;
  }
 

  sub resp_file
  {
    my $cgi  = shift;   # CGI.pm object
    return if !ref $cgi;
     
    my $filename       = $cgi->param('name');
     
    my $db = new DataDB($DATABASE, $HOST, $USERID, $PASSWD);
    $db->connect_db();
    my @filelist = $db->get_filelist();
    my $found = 0;
    foreach my $file (@filelist)
    {
      if ($file eq $filename)
      {
        $found = 1;
      }
    }
    if ($found)
    {
      print $cgi->header('text/plain'), $db->get_file($filename);
    }
    else
    {
      print $cgi->header('text/plain'), "FILE, $filename, NOT FOUND";
    }
    $db->disconnect_db();

    return;
  }
 
} 
 
# start the server on port 8888
my $pid = MyWebServer->new(8888)->background();
print "Use 'kill $pid' to stop server.\n";
