#!/share/apps/python/3.2.2/bin/python3
import errno, os, sys
import argparse

def mkdir_p(path):
    try:
        print('INFO Creating directory: ' + path)
        os.makedirs(path)
    except os.error: 
        pass

def compare_shortest_paths():

    flat_results = '/pic/projects/mnms4graphs/nccdc/2013/apsp/nccdc-filtered-t_0/Uniform/Flat/ALL.txt'
    L1_results = '/pic/projects/mnms4graphs/nccdc/2013/apsp/nccdc-filtered-t_0/Uniform/1L/ALL.txt'

    f_flat = open(flat_results, 'r')
    flat_dist = dict() 
    for line in f_flat:
        tokens = line.strip().split(' ')
        edge_key = tokens[1] + '_' + tokens[3]
        dist = float(tokens[4])
        if dist <= 0:
            continue
        else:
            flat_dist[edge_key] = dist
    f_flat.close()

    print('Finished reading flat file ...')

    f_L1 = open(L1_results, 'r')
    f_out = open('shortest_path_ratios.csv', 'w')
    num_ratios = 0
    for line in f_L1:
        tokens = line.strip().split(' ')
        edge_key = tokens[1] + '_' + tokens[3]
        if edge_key in flat_dist:
            d_flat = flat_dist[edge_key]
            if d_flat != 0:
                d_L1 = float(tokens[4])
                ratio = d_L1/d_flat
                f_out.write(str(ratio) + '\n')
                num_ratios += 1
    f_out.close()
    f_L1.close()
    print('Number of output ratios: ' + str(num_ratios))

def aggregate_pagerank():
    
    pagerank_data = []
    dir = '/pic/projects/mnms4graphs/nccdc/2013/mods/num_edges-10000/graphlab_logs/pagerank/'
    file = 'nccdc-filtered-none.tsv'
    for i in range(1, 5):
        logpath = dir + file + '_pagerank_' + str(i) + '_of_4'
        f = open(logpath, 'r')
        for line in f:
            tokens = line.strip().split('\t')
            # format: vertex_id \t pagerank
            pagerank_data.append((int(tokens[0]), float(tokens[-1])))
        f.close()

    pagerank_data.sort() # sort by vertex id
    
    outpath = dir + file + '.aggr_pagerank.csv'
    f_out = open(outpath, 'w')
    for tuple in pagerank_data:
        f_out.write(str(tuple[0]) + ',' + str(tuple[1]) + '\n') 
    f_out.close()

def parse_pagerank_data(path):

    log_id_list = []
    pagerank_dir = path + '/pagerank/'
    logs = os.listdir(path)
    for log in logs:
        pos = log.find('pagerank.log')
        if pos == -1:
            continue
        prefix = log[0:pos-1]
        log_id_list.append(prefix)
    
    for log in log_id_list:
        pagerank_vector = []
        for i in range(1,5):
            logpath = pagerank_dir + log + '_pagerank_' + str(i) + '_of_4'
            f = open(logpath, 'r')
            for line in f:
                tokens = line.strip().split('\t')
                pagerank_vector.append(float(tokens[-1]))
                #fout.write(str(tokens[-1]) + '\n')
            f.close()
        pagerank_vector.sort()
        outpath = pagerank_dir + log + '_pagerank.csv'
        print('Aggregating pagerank data to: ' + outpath)
        fout = open(outpath, 'w')
        for rank in pagerank_vector:
            fout.write(str(rank) + '\n')
        fout.close()

def parse_kcore_data(path):
    
    log_list = []
    in_dir = ''
    out_dir = ''
    if os.path.isdir(path) == True:
        in_dir = path
        out_dir = path + '/kcore'
        mkdir_p(out_dir)
        files = os.listdir(path)
        for file in files:
            if file.find('kcore.log') != -1:
                log_list.append(file)
    else:
        log_list.append(path)

    for log in log_list:
        if in_dir != '':
            logpath = in_dir + '/' + log
            log_summary = out_dir + '/' + log[0:-4] + '_summary.csv'
        else:
            logpath = log
            log_summary = log[0:-4] + '_summary.csv'
        f = open(logpath, 'r')
        print('Writing: ' + log_summary)
        fout = open(log_summary, 'w')
        k = 0
        for line in f:
            if line.find('K=', 0) != -1:
                tokens = line.strip().split(' ')
                num_vertices = tokens[4]
                num_edges = tokens[9]
                fout.write(str(k) + ',' + str(num_vertices) + ',' + str(num_edges) + '\n')
                k += 1
        f.close()
        fout.close()

def get_approx_diam(path, logdir):
    file = ''
    approx_diam = ''
    f = open(path, 'r')
    for line in f:
        line = line.strip()
        tokens = line.split()
        if line.find('Loading graph from file:') != -1:
            file = tokens[-1]
        elif line.find('The approximate diameter is') != -1:
            approx_diam = tokens[-1]
    f.close()
    #approx_diam_log = '/pic/projects/mnms4graphs/nccdc/2013/logs/approx_diam.csv'
    if os.path.dirname(path) == '':
        approx_diam_log = 'approx_diam.csv'
    else:
        approx_diam_log = os.path.dirname(path) + '/approx_diam.csv'
    f = open(approx_diam_log, 'a')
    f.write(path + ',approx_diameter,' + approx_diam + '\n')
    f.close() 

def compute_metrics(path):
    print('INFO processing: ' + path)
    if os.path.dirname(path) == '':
        logdir = 'graphlab'
    else:
        logdir = os.path.dirname(path) + '/graphlab'
    if logdir[-1] != '/':
        logdir = logdir + '/'
    mkdir_p(logdir)
    args = ' --format=tsv --graph=' + path + ' >& '

    logfile = logdir + os.path.basename(path) + '.diam.log'
    cmd = 'approximate_diameter' + args + logfile
    print('Running: ' + cmd)
    os.system(cmd)
    get_approx_diam(logfile, logdir)

    logfile = logdir + os.path.basename(path) + '.kcore.log'
    cmd = 'kcore --kmax=20' + args + logfile
    print('Running: ' + cmd)
    os.system(cmd)

    logfile = logdir + os.path.basename(path) + '.connected_comp.log'
    cmd = 'connected_component' + args + logfile
    print('Running: ' + cmd)
    os.system(cmd)

    logfile = logdir + os.path.basename(path) + '.pagerank.log'
    args = ' --saveprefix=' + logdir + 'pagerank/' + \
            os.path.basename(path) + '_pagerank' + args
    cmd = 'pagerank' + args + logfile
    mkdir_p(logdir + 'pagerank')
    print('Running: ' + cmd)
    os.system(cmd)

    return

def compute_partition(path):
    args = ' --format=weight -partitions=4 --graph=' + path + ' >& '
    if os.path.dirname(path) == '':
        logdir = 'graphlab'
    else:
        logdir = os.path.dirname(path) + '/graphlab'
    mkdir_p(logdir)
    args = ' --format=tsv --graph=' + path + ' >& '

    logfile = logdir + os.path.basename(path) + '.partitioning.log'
    cmd = 'partitioning' + args + logfile
    print('Running: ' + cmd)
    os.system(cmd)

def process_list(listfile):
    flist = open(listfile, 'r')
    for line in flist:
        path = line.strip()
        if path.find('.tsv') != -1:
            compute_metrics(path)
        elif path.find('.weight') != -1:
            compute_partition(path)
        else:
            print('File with unknown extension: ' + path)
    flist.close()

#parse_pagerank_data('/pic/projects/mnms4graphs/nccdc/2013/mods/num_edges-10000/graphlab_logs')
#aggregate_pagerank()
#compare_shortest_paths()
parser = argparse.ArgumentParser()
parser.add_argument('--metrics', \
        help='GraphLab file with .tsv or .weight extension or .list file')
parser.add_argument('--aggr_kcore', help='kcore log or directory with kcore logs')
parser.add_argument('--aggr_pagerank', help='Directory with GraphLab logs')
args = parser.parse_args()

if args.metrics != None:
#if len(sys.argv) < 2:
    #print('USAGE: ' + sys.argv[0] + ' [input-file]')
    #print('     [input-file]: graphlab file with .tsv or .weight extension')
    #print('                   or file with a graphlab file path on each line')
    #sys.exit(1)
    #input = sys.argv[1]
    input = args.metrics
    
    if input.find('.list') == -1:
        compute_metrics(input)
    else:
         process_list(input)
elif args.aggr_kcore != None:
    parse_kcore_data(args.aggr_kcore)
elif args.aggr_pagerank != None:
    parse_pagerank_data(args.aggr_pagerank)
else:
    parser.print_help()
