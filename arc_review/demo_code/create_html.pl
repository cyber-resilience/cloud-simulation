#!/usr/bin/perl -w

use POSIX;

print("<!DOCTYPE html>\n");
print("<html>\n");
print("<head>\n");
print("<link rel='icon' type='image/png' href='data:image/png;base64,iVBORw0KGgo='>\n");
print("<meta http-equiv='cache-control' content='max-age=0'>\n");
print("<meta http-equiv='cache-control' content='no-cache'>\n");
print("<meta http-equiv='expires' content='-1'>\n");
print("<meta http-equiv='expires' content='Tue, 01 Jan 1980 11:00:00 GMT'>\n");
print("<meta http-equiv='pragma' content='no-cache'>\n");
print("<meta http-equiv='refresh' content='30'>\n");
print("<script>\n");
print("  function getDate() {\n");
print("    var x = new Date(document.lastModified);\n");
print("    document.getElementById('demo').innerHTML = x;\n");
print("}\n");
print("  var last_mod = document.lastModified;\n");
print("</script>\n");
print("<style>\n");
print("table, td, th {\n");
print("  border: 1px solid green;\n");
print("}\n");
print("\n");
print("th {\n");
print("  background-color: green;\n");
print("  color: white;\n");
print("}\n");
print("td {\n");
print("  text-align: right;\n");
print("}\n");
print("</style>\n");
print("</head>\n");
print("<body onload='getDate()'>\n");
print("<h4 id='demo'>\n");
print("</h4>\n");
print("<p>\n");
print("<table>\n");
print("<tr><th>Mission</th><th>% Confidence</th><th>Recommended Action</th></tr>\n");
while (<STDIN>)
{
  s#^\s+##;
  s#\s+$##;
  my $letter = 'd';
  my $style  = '';
  my($mission, $value) = split(/\s+/, $_);
  if (int($value + 0.5) == 0)
  {
    $recommend = '&nbsp;';
  }
  else
  {
    $recommend = 'Shutdown';
    $letter    = 'h';
    $style     = 'style="background-color: red; text-align: right"';
  }
  $value = sprintf("%0.1f", $value);
  print("<tr><t$letter $style>$mission</t$letter><t$letter $style>$value</t$letter><t$letter $style>$recommend</t$letter></tr>\n");
}
print("</table>\n");
print("</p>\n");
print("<p>\n");
print("<img src='https://s3-us-west-2.amazonaws.com/mnms4graphs/data/latency_window.png'>\n");
print("</p>\n");
print("</body>\n");
print("</html>\n");

exit(0);
