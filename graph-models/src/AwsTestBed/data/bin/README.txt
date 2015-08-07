AWS Testbed specs 12/01/2014

/**********************
 * Data generation:
 **********************

- Data generators
----  RadomFileGenerator(generate_interval_in_minutes,  
min_rows, max_rows, num_cols, output_dir, output_prefix)
----  Script produces CSV files with random data and randomly set file size.  
Appends a checksum column, so the number of output column is num_cols+1.
----  Writes out files named as : 
output_dir/hostname.output_prefix.YYYY-MM-DD.csv

- HTTP traffic generators
----  RandomHTTPTrafficGenerators(min_wait_interval, 
    max_wait_interval, max_url):  
Generates HTTP requests from a known list of URLs.  Minimum and maximum wait 
time between two successive requests are specified by the input parameters.

/**********************************
 * Supporting data infrastructure:
 **********************************

- Data Ingest
----  CheckSumVerifier(csv_path, out_path):  Script reads in the CSV files, 
verifies checksum.  
----  Updates processing summary in database (see below)

- Database server (PostgreSQL/MySQL or any NoSQL key-value store)
----  Stores, timestamp, data_source_prefix, num_rows
----  Provides UPDATE and QUERY mechanism.
----  Example queries:
-------- GetFileCountByHostName()
-------- GetRowCountByHostName()
-------- GetFileCount()
-------- GetRowCount()

- Web server (Python/PHP/Tomcat, take your pick)
----  Provides a HTTP interface to the the above queries
----  Querying the following URL should provide answers
----  our_aws_server.com/SummaryApp/GetFileCountByHostName?host=some_host
----  our_aws_server.com/SummaryApp/GetFileCount


Need a database:
  - A table for each filename
  - A table with the metadata about each filename
