import nx

class TargetSelector:
    def __init__(self, graph, num_targets):
        self.graph = graph
        self.num_targets = num_targets

    def select_targets(self, targets, metrics):
        targets = choose_top_k_degree_nodes(num_targets)
        metrics = get_target_metrics(targets)
        
    def get_target_metrics(targets):

def load_nx_graph(path, is_directed):
    if is_directed:
      graph = nx.DiGraph()
    else:
      graph = nx.Graph()
    f = open(path)
    for line in f:
      graph.add_edge(...)
    f.close()

def probabilistic_graph_walk(graph, start, targets, max_hops,
        alpha, beta, patience):
    compromised_set = set()
    breach = False
    hop_count = 0
    current_node = start
    node_selector = BetaSelector(alpha, beta)

    for i in range(graph.number_of_nodes()):
      graph.node[i]['hardening_level'] = random.betavariate(alpha, beta)

    while (hop_count < max_hops):
        neighbor_count = graph.get_neighbor_count(current_node)
        next_node = selector.select(neighor_count)
        if next_node in compromised_set:
            continue
        hop_count += 1
        #cost = graph.get_node_weight(current_node, next_node)
        cost = graph.node[i]['hardening_level']
        if cost < patience:
            current_node = next_node
            if next_node in targets:
                breach = True
                break
            compromised_set.add(next_node)
        else:
            current_node = restart(compromised_set)
    return [breach, hop_count] 

def randomized_spread(graph, start, max_hops):
    hop_count = 0
    impact_count = 0
    visited = set()
    visit = queue()
    visit.push(start)
    while queue not empty:
        current = queue.front()
        neighbors = graph.get_neighbors(current)
        for nbr in neighbors:
            p = get_burn_probability()
            if p > threshold:
                visit.push(nbr)
                impact_count += 1
    return impact_count

#
# Teleportation 
#
# Attack1: Teleporation by physical network.
# Nodes grouped by same physical partition are removed from the network.
# Attack2: Teleportation by user access control.
# Instead of moving to the next node in the neighbor list, the attcker
# selects a node belonging to the same user. 

#def physical_teleportation(graph, physical_topology):
    #impact_count = 0
    #for segment in physical_topology:
        #for u in segment:
            # remove u
            # see how many edges in graph are lost as a consequence
            # for each lost_edge:
            #   p = edge.s
            #   q = edge.t
            # impact_count = randomized_spread(graph, p, max_hops) + 1
            # impact_count = randomized_spread(graph, q, max_hops) + 1
    #return impact_count

#def user_teleportation(graph, access_control_graph):
    #user = get_user(access_control_graph, node)
    #next_node = select_next(access_control_graph, user, node, visited)
    #move_to_next_node
