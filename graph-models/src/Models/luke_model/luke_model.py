import networkx as nx
import random, csv, statistics, glob
from collections import defaultdict

class CyberGraph:

    def __init__(self):
        self.G = nx.MultiDiGraph()
        self.blocked_users = defaultdict(list)

    #label: url-like identifier for the machine
    def add_machine_node(self, label):
        self.G.add_node(label, type='machine')

    #label: identifier for the user (e.g. Admin1)
    def add_user_node(self, label):
        self.G.add_node(label, type='user')

    #label: identifier for the application in question
    def add_application_node(self, label): #label should be a service (ETR)
        self.G.add_node(label, type='application')

    #machine1: first of the two machines that are physically connected
    #machine2: second machine
    #start_time: time (in seconds) at which this connection was established
    #end_time: time (in seconds) at which this connection was removed
    def add_physical_edge(self, machine1, machine2, start_time, end_time='none'): #src and dst should both be machines
        self.G.add_edge(machine1, machine2, type='are_connected', start=start_time, end=end_time)
        self.G.add_edge(machine2, machine1, type='are_connected', start=start_time, end=end_time)

    #user: the user who has access to a machine
    #machine: the machine that the user has access to
    #access_type: the level of access that the user holds on this machine (e.g. 'sudo')
    #start_time: time (in seconds) at which this connection was established
    #end_time: time (in seconds) at which this connection was removed
    def add_access_edge(self, user, machine, access_type, start_time, end_time='none'):
        self.G.add_edge(user, machine, type='has_access', level=access_type, start=start_time, end=end_time)

    #user_or_application: the entity requesting the data
    #application: the app that the data is coming from
    #num_bytes: the number of bytes in this flow
    #total_duration: the total duration of this flow
    #start_time: time (in seconds) at which this connection was established
    #end_time: time (in seconds) at which this connection was removed
    def add_dataflow_edge(self, user_or_application, application, num_bytes, start_time, end_time):
        self.G.add_edge(user_or_application, application, type='gets_data', bytes=num_bytes, start=start_time, end=end_time)

    #Utility function for simulation
    def create_dataflow_edges(self, user_or_application, application, num_flows, mean_bytes, earliest_time, latest_time):
        for i in range(0, num_flows):
            start = random.uniform(earliest_time, latest_time)
            end = start + random.gauss(1, 0.05)
            self.add_dataflow_edge(user_or_application, application, random.gauss(mean_bytes,mean_bytes/4), start, end)

    #Utility function for simulation
    def create_disrupted_dataflow_edges(self, user_or_application, application, num_flows, mean_bytes, earliest_time, latest_time):
        for i in range(0, num_flows):
            start = random.uniform(earliest_time, latest_time)
            end = start + random.gauss(1, 0.05) + random.gauss(10,2)
            self.add_dataflow_edge(user_or_application, application, random.gauss(mean_bytes,mean_bytes/4), start, end)

    #Utility function for simulation
    #This function will assign the duration of the this particular dataflow edge according to the number of
    #requests currently being processed by the system.
    def create_modeled_dataflow_edge(self, user_or_application, application, start_time, num_bytes):
        if user_or_application in self.blocked_users[application]:
            return
        start_time = float(start_time)
        ## These paramters control the function used: f(r) = a*r^4
        a = 0.0001      #slope of the linear function
        b = 4           #Exponent of the steep increase
        c = 0.1         #Constant multiplier of the power component
        d = 0.1         #y-intercept
        p = 100          #Cricital point (number of flows at which it starts to fail
        ## This is the minimum duration of a netflow.
        min_duration = 0.1

        ## First we need to decide the number of requests currently being processed by the system that hosts the application
        #What machine is this hosted on?
        machine = ''
        for edge in self.G.edges(data=True):
            if edge[0] == application and edge[2]['type'] == 'hosted_on_port' and edge[2]['start'] <= start_time and (edge[2]['end'] == 'none' or edge[2]['end'] >= start_time):
                machine=edge[1]
                break
        #What are all of the applications hosted on this machine?
        all_applications = set()
        for edge in self.G.edges(data=True):
            if edge[1] == machine and edge[2]['type'] == 'hosted_on_port' and edge[2]['start'] <= start_time and (edge[2]['end'] == 'none' or edge[2]['end'] >= start_time):
                all_applications.add(edge[0])

        #How many requests are currently being processed by this machine?
        r = 0
        for edge in self.G.edges(data=True):
            if edge[2]['type'] == 'gets_data' and edge[1] in all_applications and edge[2]['start'] <= start_time and (edge[2]['end'] == 'none' or edge[2]['end'] >= start_time):
                r += 1
        #Calculate the mean of the normal distribution to use to assign duration based on f(r).
        if r <= p:
            mean = a*r+d
        else:
            mean = c*((r-p)**b)+a*r+d
        mean = max(mean, min_duration)
        duration = random.gauss(mean, mean/10)
        self.add_dataflow_edge(user_or_application, application, num_bytes, start_time, start_time + duration)



    #application: the app that is hosted on a machine
    #machine: the machine hosting the app
    #start_time: time (in seconds) at which this connection was established
    #end_time: time (in seconds) at which this connection was removed
    def add_hosting_edge(self, application, machine, port_number, start_time, end_time='none'):
        self.G.add_edge(application, machine, type='hosted_on_port', port=port_number, start=start_time, end=end_time)

    #machine1/2: The machines to disconnect
    #time: The time at which they should become disconnected
    ####NOTE: This is intended for use for edges that include a machine as one of the two nodes - not dataflow edges! #####
    def disconnect_edge(self, node1, node2, time):
        if not self.G.has_edge(node1, node2):
            print('No edge to disconnect')
            return
        for edge in self.G.edge[node1][node2]:
            if self.G.edge[node1][node2][edge]['start'] <= time and (self.G.edge[node1][node2][edge]['end'] == 'none' or self.G.edge[node1][node2][edge]['end'] >= time):
                self.G.edge[node1][node2][edge]['end'] = time

    def get_edge_sets(self, start_time, end_time):
        physical = []
        dataflow = []
        access = []
        hosting = []
        for edge in self.G.edges(data=True):
 #           if edge[2]['type'] == 'gets_data':
 #               if edge[2]['start'] >= start_time and edge[2]['end'] <= end_time:
 #                   dataflow.append(edge)
            if edge[2]['type'] == 'gets_data':
                if edge[2]['end'] > start_time and edge[2]['end'] <= end_time:
                    dataflow.append(edge)
            elif edge[2]['start'] <= start_time and (edge[2]['end'] == 'none' or edge[2]['end'] >= end_time):
                if edge[2]['type'] == 'are_connected':
                    physical.append(edge)
                elif edge[2]['type'] == 'has_access':
                    access.append(edge)
                elif edge[2]['type'] == 'hosted_on_port':
                    hosting.append(edge)
                else:
                    print('Some edge is weirdly typed. What did you do?')
        return [physical, dataflow, access, hosting]

    def get_physical_graph(self):
        Gphys = nx.Graph()
        edge_set = self.get_physical_edges()
        for edge in edge_set:
            Gphys.add_edge(edge[0], edge[1])
        return Gphys

    def get_dataflow_graph(self):
        Gapp = nx.DiGraph()
        edge_set = self.get_dataflow_edges()
        for edge in edge_set:
            Gapp.add_edge(edge[0], edge[1], bytes=edge[2]['bytes'], duration=edge[2]['duration'])
        return Gapp

    def get_access_graph(self):
        Gacc = nx.DiGraph()
        edge_set = self.get_access_edges()
        for edge in edge_set:
            Gacc.add_edge(edge[0], edge[1])
        return Gacc

    def get_hosting_graph(self):
        Ghost = nx.DiGraph()
        edge_set = self.get_hosting_edges()
        for edge in edge_set:
            Ghost.add_edge(edge[0], edge[1])
        return Ghost

    def build_sample_graph(self):

####### Things that happen at system boot ########
        #Users
        self.add_user_node('HR1')
        self.add_user_node('HR2')
        self.add_user_node('HR3')
        self.add_user_node('HR4')
        self.add_user_node('HR5')
        self.add_user_node('CEO')
        self.add_user_node('Dev1')
        self.add_user_node('Dev2')
        self.add_user_node('Dev3')
        self.add_user_node('Intern')
        self.add_user_node('External')

        #Machines
        self.add_machine_node('HR-laptop1.company.com')
        self.add_machine_node('HR-laptop2.company.com')
        self.add_machine_node('HR-laptop3.company.com')
        self.add_machine_node('HR-laptop4.company.com')
        self.add_machine_node('HR-laptop5.company.com')
        self.add_machine_node('HR-front-desk.company.com')
        self.add_machine_node('CEO-laptop.company.com')
        self.add_machine_node('CEO-desktop.company.com')
        self.add_machine_node('Dev-laptop1.company.com')
        self.add_machine_node('Dev-laptop2.company.com')
        self.add_machine_node('Dev-laptop3.company.com')
        self.add_machine_node('Dev-desktop1.company.com')
        self.add_machine_node('Dev-desktop2.company.com')
        self.add_machine_node('Dev-desktop3.company.com')
        self.add_machine_node('extra-computer1.company.com')
        self.add_machine_node('extra-computer2.company.com')
        self.add_machine_node('server.company.com')
        self.add_machine_node('database.company.com')
        self.add_machine_node('use-cluster.company.com')
        self.add_machine_node('sandbox-cluster.company.com')
        self.add_machine_node('R1')
        self.add_machine_node('R2')
        self.add_machine_node('R3')

        #Applications
        self.add_application_node('ETR')
        self.add_application_node('payroll-app')
        self.add_application_node('website-host')
        self.add_application_node('email-host')
        self.add_application_node('website-backup')
        self.add_application_node('employee-database')

        #Physical Topology
        self.add_physical_edge('R1', 'R2',0,20)
        self.add_physical_edge('R1', 'R3',0)
        self.add_physical_edge('HR-laptop1.company.com', 'R3',0)
        self.add_physical_edge('HR-laptop2.company.com', 'R3',0)
        self.add_physical_edge('HR-laptop3.company.com', 'R3',0)
        self.add_physical_edge('HR-laptop4.company.com', 'R3',0)
        self.add_physical_edge('HR-laptop5.company.com', 'R3',0)
        self.add_physical_edge('HR-front-desk.company.com', 'R3',0)
        self.add_physical_edge('CEO-laptop.company.com', 'R3',0)
        self.add_physical_edge('CEO-desktop.company.com', 'R3',0)
        self.add_physical_edge('Dev-laptop1.company.com', 'R3',0)
        self.add_physical_edge('Dev-laptop2.company.com', 'R3',0)
        self.add_physical_edge('Dev-laptop3.company.com', 'R3',0)
        self.add_physical_edge('Dev-desktop1.company.com', 'R3',0)
        self.add_physical_edge('Dev-desktop2.company.com', 'R3',0)
        self.add_physical_edge('Dev-desktop3.company.com', 'R3',0)
        self.add_physical_edge('extra-computer1.company.com', 'R3',0)
        self.add_physical_edge('extra-computer2.company.com', 'R3',0)
        self.add_physical_edge('server.company.com', 'R2',0)
        self.add_physical_edge('database.company.com', 'R2',0)
        self.add_physical_edge('use-cluster.company.com', 'R2',0)
        self.add_physical_edge('sandbox-cluster.company.com', 'R2',0)

        #Access Control
        self.add_access_edge('HR1', 'HR-laptop1.company.com', 'standard',0)
        self.add_access_edge('Dev1', 'HR-laptop1.company.com', 'sudo',0)
        self.add_access_edge('Dev2', 'HR-laptop1.company.com', 'sudo',0)
        self.add_access_edge('Dev3', 'HR-laptop1.company.com', 'sudo',0)
        self.add_access_edge('HR2', 'HR-laptop2.company.com', 'standard',0)
        self.add_access_edge('Dev1', 'HR-laptop2.company.com', 'sudo',0)
        self.add_access_edge('Dev2', 'HR-laptop2.company.com', 'sudo',0)
        self.add_access_edge('Dev3', 'HR-laptop2.company.com', 'sudo',0)
        self.add_access_edge('HR3', 'HR-laptop3.company.com', 'standard',0)
        self.add_access_edge('Dev1', 'HR-laptop3.company.com', 'sudo',0)
        self.add_access_edge('Dev2', 'HR-laptop3.company.com', 'sudo',0)
        self.add_access_edge('Dev3', 'HR-laptop3.company.com', 'sudo',0)
        self.add_access_edge('HR4', 'HR-laptop4.company.com', 'standard',0)
        self.add_access_edge('Dev1', 'HR-laptop4.company.com', 'sudo',0)
        self.add_access_edge('Dev2', 'HR-laptop4.company.com', 'sudo',0)
        self.add_access_edge('Dev3', 'HR-laptop4.company.com', 'sudo',0)
        self.add_access_edge('HR5', 'HR-laptop5.company.com', 'standard',0)
        self.add_access_edge('Dev1', 'HR-laptop5.company.com', 'sudo',0)
        self.add_access_edge('Dev2', 'HR-laptop5.company.com', 'sudo',0)
        self.add_access_edge('Dev3', 'HR-laptop5.company.com', 'sudo',0)
        self.add_access_edge('HR1', 'HR-front-desk.company.com', 'standard',0)
        self.add_access_edge('HR2', 'HR-front-desk.company.com', 'standard',0)
        self.add_access_edge('HR3', 'HR-front-desk.company.com', 'standard',0)
        self.add_access_edge('HR4', 'HR-front-desk.company.com', 'standard',0)
        self.add_access_edge('HR5', 'HR-front-desk.company.com', 'standard',0)
        self.add_access_edge('Dev1', 'HR-front-desk.company.com', 'sudo',0)
        self.add_access_edge('Dev2', 'HR-front-desk.company.com', 'sudo',0)
        self.add_access_edge('Dev3', 'HR-front-desk.company.com', 'sudo',0)
        self.add_access_edge('CEO', 'CEO-laptop.company.com', 'sudo',0)
        self.add_access_edge('Dev1', 'CEO-laptop.company.com', 'sudo',0)
        self.add_access_edge('CEO', 'CEO-desktop.company.com', 'sudo',0)
        self.add_access_edge('Dev1', 'CEO-desktop.company.com', 'sudo',0)
        self.add_access_edge('Dev1', 'Dev-laptop1.company.com', 'sudo',0)
        self.add_access_edge('Dev1', 'Dev-desktop1.company.com', 'sudo',0)
        self.add_access_edge('Dev2', 'Dev-laptop2.company.com', 'sudo',0)
        self.add_access_edge('Dev2', 'Dev-desktop2.company.com', 'sudo',0)
        self.add_access_edge('Dev3', 'Dev-laptop3.company.com', 'sudo',0)
        self.add_access_edge('Dev3', 'Dev-desktop3.company.com', 'sudo',0)
        self.add_access_edge('HR1', 'extra-computer1.company.com', 'standard',0)
        self.add_access_edge('HR2', 'extra-computer1.company.com', 'standard',0)
        self.add_access_edge('HR3', 'extra-computer1.company.com', 'standard',0)
        self.add_access_edge('HR4', 'extra-computer1.company.com', 'standard',0)
        self.add_access_edge('HR5', 'extra-computer1.company.com', 'standard',0)
        self.add_access_edge('CEO', 'extra-computer1.company.com', 'standard',0)
        self.add_access_edge('Intern', 'extra-computer1.company.com', 'standard',0)
        self.add_access_edge('Dev1', 'extra-computer1.company.com', 'sudo',0)
        self.add_access_edge('Dev2', 'extra-computer1.company.com', 'sudo',0)
        self.add_access_edge('Dev3', 'extra-computer1.company.com', 'sudo',0)
        self.add_access_edge('HR1', 'extra-computer2.company.com', 'standard',0)
        self.add_access_edge('HR2', 'extra-computer2.company.com', 'standard',0)
        self.add_access_edge('HR3', 'extra-computer2.company.com', 'standard',0)
        self.add_access_edge('HR4', 'extra-computer2.company.com', 'standard',0)
        self.add_access_edge('HR5', 'extra-computer2.company.com', 'standard',0)
        self.add_access_edge('CEO', 'extra-computer2.company.com', 'standard',0)
        self.add_access_edge('Intern', 'extra-computer2.company.com', 'standard',0)
        self.add_access_edge('Dev1', 'extra-computer2.company.com', 'sudo',0)
        self.add_access_edge('Dev2', 'extra-computer2.company.com', 'sudo',0)
        self.add_access_edge('Dev3', 'extra-computer2.company.com', 'sudo',0)
        self.add_access_edge('Dev1', 'server.company.com', 'sudo',0)
        self.add_access_edge('Dev2', 'server.company.com', 'standard',0)
        self.add_access_edge('Dev1', 'database.company.com', 'sudo',0)
        self.add_access_edge('Dev3', 'database.company.com', 'standard',0)
        self.add_access_edge('CEO', 'use-cluster.company.com', 'standard',0)
        self.add_access_edge('Intern', 'use-cluster.company.com', 'standard',0)
        self.add_access_edge('Dev1', 'use-cluster.company.com', 'sudo',0)
        self.add_access_edge('Dev2', 'use-cluster.company.com', 'sudo',0)
        self.add_access_edge('Dev3', 'use-cluster.company.com', 'sudo',0)
        self.add_access_edge('Dev1', 'sandbox-cluster.company.com', 'sudo',0)
        self.add_access_edge('Dev2', 'sandbox-cluster.company.com', 'standard',0)
        self.add_access_edge('Dev3', 'sandbox-cluster.company.com', 'standard',0)

        #Systems
        self.add_hosting_edge('ETR', 'use-cluster.company.com', 880,0)
        self.add_hosting_edge('payroll-app', 'use-cluster.company.com', 50,0)
        self.add_hosting_edge('website-host', 'server.company.com', 10,0)
        self.add_hosting_edge('email-host', 'server.company.com', 80,0)
        self.add_hosting_edge('website-backup', 'database.company.com', 880,0)
        self.add_hosting_edge('employee-database', 'database.company.com', 62,0)

####### Set times ############
        random.seed(456357)
        flows = []
        for i in range(200):
            flows.append((random.uniform(0,200),'HR1', 'payroll-app'))
            flows.append((random.uniform(0,200),'HR2', 'payroll-app'))
            flows.append((random.uniform(0,200),'HR3', 'payroll-app'))
            flows.append((random.uniform(0,200),'HR4', 'payroll-app'))
            flows.append((random.uniform(0,200),'HR5', 'payroll-app'))
            flows.append((random.uniform(0,200),'HR1', 'ETR'))
            flows.append((random.uniform(0,200),'HR2', 'ETR'))
            flows.append((random.uniform(0,200),'HR3', 'ETR'))
            flows.append((random.uniform(0,200),'HR5', 'ETR'))
            flows.append((random.uniform(0,200),'CEO', 'ETR'))
            flows.append((random.uniform(0,200),'Dev1', 'ETR'))
            flows.append((random.uniform(0,200),'Dev2', 'ETR'))
            flows.append((random.uniform(0,200),'Dev3', 'ETR'))
            flows.append((random.uniform(0,200),'Intern', 'ETR'))
            flows.append((random.uniform(0,200),'HR1', 'email-host'))
            flows.append((random.uniform(0,200),'HR2', 'email-host'))
            flows.append((random.uniform(0,200),'HR3', 'email-host'))
            flows.append((random.uniform(0,200),'HR4', 'email-host'))
            flows.append((random.uniform(0,200),'HR5', 'email-host'))
            flows.append((random.uniform(0,200),'CEO', 'email-host'))
            flows.append((random.uniform(0,200),'Dev1', 'email-host'))
            flows.append((random.uniform(0,200),'Dev2', 'email-host'))
            flows.append((random.uniform(0,200),'Dev3', 'email-host'))
            flows.append((random.uniform(0,200),'Intern', 'email-host'))
            flows.append((random.uniform(0,200),'Dev2', 'website-host'))
            flows.append((random.uniform(0,200),'Dev3', 'employee-database'))
            flows.append((random.uniform(0,200),'payroll-app', 'ETR'))
            flows.append((random.uniform(0,200),'website-backup', 'website-host'))

        ##External user is the weird one##
        for i in range(800):
            flows.append((random.uniform(0,200),'External', 'website-host'))
        for i in range(5000):
            flows.append((50+i/1000, 'External', 'website-host'))

####### Loop through the time windows and add flows/perform actions ############
        i = 1
        for flow in sorted(flows):
            if flow[0] >= i: #We have hit the next time window
                print(i)
                if i > 10:
                    self.print_steady_state_with_snapshot(i-1,i)
                #if i == 52:
                #    self.blocked_users['website-host'].append('External')
                #    self.remove_pending_requests(54,'External','website-host')
                #    self.remove_pending_requests(54,'External','email-host')
                i += 1
            self.create_modeled_dataflow_edge(flow[1], flow[2], flow[0], random.gauss(50,5))

    def remove_pending_requests(self, time, user, application):
        for edge in self.G.edges(data=True, keys=True):
            if edge[0]==user and edge[1]==application and edge[3]['end'] > time:
            #if edge[1]==application and edge[3]['end']>time:
                self.G.remove_edge(edge[0], application, edge[2])

    def print_snapshot(self, start_time, end_time, folder):
        edgesets = self.get_edge_sets(start_time, end_time)
        prefix = 'output/'+folder+'/' + str(start_time) + "-" + str(end_time) + "_"
        with open(prefix+'node_list.csv', mode='w', newline='')  as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['identifier', 'node type'])
            for node in self.G.nodes(data=True):
                writer.writerow([node[0], node[1]['type']])
        with open(prefix+'physical_graph.csv', mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['node1', 'node2'])
            for edge in edgesets[0]:
                writer.writerow([edge[0], edge[1]])
        with open(prefix+'application_graph.csv', mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['src', 'dst', 'bytes', 'duration', 'num_flows'])
            durations = defaultdict(list)
            sizes = defaultdict(list)
            for edge in edgesets[1]:
                durations[(edge[0], edge[1])].append(edge[2]['end'] - edge[2]['start'])
                sizes[(edge[0], edge[1])].append(edge[2]['bytes'])
            for pair in durations:
        #QUICK HACK FOR PLOTTING:
        #        for duration in durations[pair]:
        #            writer.writerow([pair[0], pair[1], duration])
                writer.writerow([pair[0], pair[1], statistics.median(sizes[pair]), statistics.median(durations[pair]), len(durations[pair])])
        with open(prefix+'access_graph.csv', mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['src', 'dst', 'access_type'])
            for edge in edgesets[2]:
                writer.writerow([edge[0], edge[1], edge[2]['level']])
        with open(prefix+'hosting_graph.csv', mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow(['src', 'dst', 'port_number'])
            for edge in edgesets[3]:
                writer.writerow([edge[0], edge[1], edge[2]['port']])

    def print_steady_state_with_snapshot(self, start_time, end_time):
        duration = end_time - start_time
        steady_start = start_time - 10*duration
        self.print_snapshot(steady_start, start_time, 'steady')
        self.print_snapshot(start_time, end_time, 'test')


def print_throughput():
    files = glob.glob('output/test/*application*.csv')
    times = []
    for file in files:
        with open(file) as f:
            reader = csv.reader(f)
            printzero = True
            for row in reader:
                if row[1] == 'website-host':
                    num_bytes = float(row[2])
                    duration = float(row[3])
                    times.append((float(file.split('\\')[1].split('-')[0]), num_bytes/duration))
                    printzero = False
            if printzero: times.append((float(file.split('\\')[1].split('-')[0]), num_bytes/duration))
    temp = ''
    tempnum = 0
    tempthrough = 0
    for time in sorted(times):
        if time[0] == temp:
            tempnum += 1
            tempthrough += time[1]
        else:
            if not temp == '':
                print(tempthrough/tempnum)
            temp = time[0]
            tempthrough = time[1]
            tempnum = 1
    print(tempthrough/tempnum)



if __name__ == "__main__":
    a = CyberGraph()
    a.build_sample_graph()


# NOTES:
# talk about the fact that other users are effected by the reduction in QOS due to DOS
# plot durations of all flows that finish
