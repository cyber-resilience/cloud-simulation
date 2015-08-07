for i in range(num_graphs):
    graph = gen_graph()
    m1 = get_metrics(graph)
    for j in range(num_attacks):
        new_graph = sim_attack(graph)
        m2 = get_metrics(new_graph)
        delta_metrics.append(get_delta(m2, m1))
    save(m1, delta_metrics)
