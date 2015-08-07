import sqlite3
import csv
import numpy as np
import networkx as nx

#read a given Silk flow file to database and store in given table
def read_to_db(tbl_name, filename):
	with open('{}.txt'.format(filename), 'r') as f:
		names = ['sIP', 'dIP', 'sPort', 'dPort', 'pro', 'packets', 'bytes', 'flags', 'sTime', 'dur', 'eTime', 'sen', '']
		f.readline()
		dr = csv.DictReader(f, fieldnames=names, delimiter='|')
		to_db = [(int(i['sIP'].translate(None, '.')), int(i['dIP'].translate(None, '.')), str(i['sPort']).strip(), str(i['dPort']).strip(), str(i['pro']).strip(), str(i['packets']).strip(), str(i['bytes']).strip(), str(i['flags']).strip(), str(i['sTime']).strip(), str(i['dur']).strip(), str(i['eTime']).strip(), str(i['sen']).strip(), i['']) for i in dr]
	f.close()
	conn = sqlite3.connect("ISCX.db")
	curse = conn.cursor()
	curse.executemany("INSERT INTO {} ('sIP', 'dIP', 'sPort', 'dPort', 'pro', 'packets', 'bytes', 'flags', 'sTime', 'dur', 'eTime', 'sen', '') VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?);".format(tbl_name), to_db)
	conn.commit()
	curse.close()
	conn.close()

#compile list of unique IP addresses present in a given table
def unique_IPs(tbl_name):
	#connect to database and initialize cursor
	conn = sqlite3.connect("ISCX.db")
	curse = conn.cursor()
	#get distinct source IPs and store to array
	curse.execute("SELECT DISTINCT sIP FROM {};".format(tbl_name))
	srcs = np.array(curse.fetchall())
	src_ips = [ip for src in srcs for ip in src]
	curse.close()
	#re-initialize cursor
	curse = conn.cursor()
	#get distinct destination IPs and store to array
	curse.execute("SELECT DISTINCT dIP FROM {};".format(tbl_name))
	dsts = np.array(curse.fetchall())
	dst_ips = [ip for dst in dsts for ip in dst]
	#close cursor and connection
	curse.close()
	conn.close()
	#combine lists of source and destination IPs and remove duplicates
	return list(set(np.concatenate((src_ips,dst_ips))))

#calculate in degree for an IP in a given table
def in_degree(tbl_name, ip):
	#connect to database and initialize cursor
	conn = sqlite3.connect("ISCX.db")
	curse = conn.cursor()
	#get count of all source IPs connecting to given IP
	curse.execute("SELECT sIP FROM {0} WHERE dIP={1};".format(tbl_name, ip))
	weighted = len(curse.fetchall())
	curse.close()
	#re-initialize cursor
	curse = conn.cursor()
	#get count of distince source IPs connecting to a given IP
	curse.execute("SELECT DISTINCT sIP FROM {0} WHERE dIP={1};".format(tbl_name, ip))
	unweighted = len(curse.fetchall())
	#close cursor and database connection
	curse.close()
	conn.close()
	return unweighted, weighted

#same as in_degree, but gathering destination IP info instead of source
def out_degree(tbl_name, ip):
	conn = sqlite3.connect("ISCX.db")
	curse = conn.cursor()
	curse.execute("SELECT dIP FROM {0} WHERE sIP={1};".format(tbl_name, ip))
	weighted = len(curse.fetchall())
	curse.close()
	curse = conn.cursor()
	curse.execute("SELECT DISTINCT dIP FROM {0} WHERE sIP={1};".format(tbl_name, ip))
	unweighted = len(curse.fetchall())
	curse.close()
	conn.close()
	return unweighted, weighted

#get total length of all interactions for a given IP
def get_total_dur(tbl_name, ip):
	#connect to database and initialize cursor
	conn = sqlite3.connect("ISCX.db")
	curse = conn.cursor()
	#sum duration column of records with given IP as either source or destination
	curse.execute("SELECT SUM(dur) FROM {0} WHERE sIP={1} OR dIP={2};".format(tbl_name,ip,ip))
	dur = curse.fetchone()[0]
	#close cursor and connection
	curse.close()
	conn.close()
	return dur

#get total number of interactions for a given IP
def count_interactions(tbl_name, ip):
	#connect to database and initialize cursor
	conn = sqlite3.connect("ISCX.db")
	curse = conn.cursor()
	#count records with given IP as either source or destination
	curse.execute("SELECT COUNT(*) FROM {0} WHERE sIP={1} OR dIP={2};".format(tbl_name,ip,ip))
	count = curse.fetchone()[0]
	#close cursor and connection
	curse.close()
	conn.close()
	return count

#get total number of ports a given IP talks to
def count_ports(tbl_name, ip):
	#connect to database and initialize cursor
	conn = sqlite3.connect("ISCX.db")
	curse = conn.cursor()
	#count the distinct destination ports where the given IP is the source IP
	curse.execute("SELECT COUNT(DISTINCT dPort) FROM {0} WHERE sIP={1};".format(tbl_name,ip,ip))
	count = curse.fetchone()[0]
	#close cursor and connection
	curse.close()
	conn.close()
	return count

#gets number of different protocols associated with a given IP
def count_protocols(tbl_name, ip):
	#connect to database and initialize cursor
	conn = sqlite3.connect("ISCX.db")
	curse = conn.cursor()
	#count distinct protocols from records where the given IP is either the source or destination
	curse.execute("SELECT COUNT(DISTINCT pro) FROM {0} WHERE sIP={1} OR dIP={2};".format(tbl_name,ip,ip))
	count = curse.fetchone()[0]
	#close cursor and connection
	curse.close()
	conn.close()
	return count

#gets the total number of packets transmitted in interactions involving a given IP
def count_packets(tbl_name, ip):
	#connect to database and initialize cursor
	conn = sqlite3.connect("ISCX.db")
	curse = conn.cursor()
	#sum the packets column for records with the given IP as either the source or destination
	curse.execute("SELECT SUM(packets) FROM {0} WHERE sIP={1} OR dIP={2};".format(tbl_name,ip,ip))
	pkts = curse.fetchone()[0]
	#close cursor and connection
	curse.close()
	conn.close()
	return pkts

#gets the total number of bytes transmitted in interactions involving a given IP
def count_bytes(tbl_name, ip):
	#connect to database and initialize cursor
	conn = sqlite3.connect("ISCX.db")
	curse = conn.cursor()
	#sum bytes column for records with the given IP as either the source or destination
	curse.execute("SELECT SUM(bytes) FROM {0} WHERE sIP={1} OR dIP={2};".format(tbl_name,ip,ip))
	bytez = curse.fetchone()[0]
	#close cursor and connection
	curse.close()
	conn.close()
	return bytez

#returns a list of all source destination pairs to be used as edges in graph
def get_edges(tbl_name):
	#connect to database and initialize cursor
	conn = sqlite3.connect("ISCX.db")
	curse = conn.cursor()
	#get list of distinct pairs for use as unweighted edges
	curse.execute("SELECT DISTINCT sIP, dIP FROM {};".format(tbl_name))
	unweighted = np.array(curse.fetchall())
	curse.close()
	#find number of instances of each distinct pair to add as weight to each edge
	weighted = []
	for edge in unweighted:
		#re-initialize cursor
		curse = conn.cursor()
		#get weight
		curse.execute("SELECT COUNT(*) FROM {0} WHERE sIP={1} AND dIP={2};".format(tbl_name,edge[0],edge[1]))
		w = curse.fetchone()[0]
		#close cursor
		curse.close()
		#append weighted edge to new list
		weighted.append((edge[0],edge[1],w))
	#close connection
	conn.close()
	return unweighted, weighted

#define path to files
path = '/home/ubuntu/share_folder/MnMs/ISCX_Silk/'
#define list of filenames
filenames = ['testbed16jun', 'testbed17jun']

#consider each file individually
for f_name in filenames:
	#connect to database and initialize cursor
	con = sqlite3.connect("ISCX.db")
	cur = con.cursor()
	#create table with Silk flow headers
	cur.execute("DROP TABLE IF EXISTS {}".format(f_name))
	cur.execute("CREATE TABLE {} ('sIP', 'dIP', 'sPort', 'dPort', 'pro', 'packets', 'bytes', 'flags', 'sTime', 'dur', 'eTime', 'sen', '');".format(f_name))
	#close cursor and connection
	cur.close()
	con.close()
	print "Reading {} to database.".format(f_name)
	read_to_db(f_name, path+f_name)
	#get list of unique IPs
	master_IPs = unique_IPs(f_name)
	print len(master_IPs), "IPs total."
	#for each IP 12 features will be collected
	features = []
	print "Gathering Netflow and node degree features for each IP..."
	j = 0
	for IP in master_IPs:
		if (j%100) == 0 and j != 0:
			print str(j) + ' of '+ str(len(master_IPs)) + ' IPs complete.'
		j = j + 1
		in_deg, weighted_in_deg = in_degree(f_name, IP)
		out_deg, weighted_out_deg = out_degree(f_name, IP)
		features.append([IP, get_total_dur(f_name, IP), count_interactions(f_name, IP), count_ports(f_name, IP), count_protocols(f_name, IP), count_packets(f_name, IP), count_bytes(f_name, IP), in_deg, out_deg, in_deg + out_deg, weighted_in_deg, weighted_out_deg, weighted_in_deg + weighted_out_deg])
	print "Writing feature matrix to .csv file..."
	with open('ISCX-{}-feature_matrix.csv'.format(f_name), 'w') as fm:
	    feature_matrix_writer = csv.writer(fm)
	    for x in features:
	        feature_matrix_writer.writerow(x)
	fm.close()

