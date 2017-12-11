INF = 1000000


def compute_routes(graph_matrix):
    """
    Computes intermediary matrix:
    matrix that would allow us to find shortest path between any two nodes
    See: Floyd–Warshall algorithm
    """
    nodes_amount = len(graph_matrix)
    distances = [
        [graph_matrix[i][j] if graph_matrix[i][j] >= 0 else INF
         for j in range(nodes_amount)]
        for i in range(nodes_amount)
    ]
    intermediaries = [
        [i if graph_matrix[i][j] >= 0 else None
         for j in range(nodes_amount)]
        for i in range(nodes_amount)
    ]
    for k in range(nodes_amount):
        for i in range(nodes_amount):
            for j in range(nodes_amount):
                should_update_distance = (
                    (distances[i][k] < INF) and
                    (distances[k][j] < INF)
                )
                if should_update_distance:
                    intermediary_distance = distances[i][k] + distances[k][j]
                    can_optimize = intermediary_distance < distances[i][j]
                    if can_optimize:
                        distances[i][j] = intermediary_distance
                        intermediaries[i][j] = k
    return intermediaries


def find_route(start_node, end_node, intermediaries):
    """
    Finds the shortest path between two nodes
    """
    intermediary_node = intermediaries[start_node][end_node]
    if intermediary_node is None:
        return None
    if start_node == intermediary_node:
        return [start_node, end_node]
    path_to_intermediary = find_route(start_node, intermediary_node, intermediaries)
    path_from_intermediary = find_route(intermediary_node, end_node, intermediaries)
    if (not path_to_intermediary) or (not path_from_intermediary[1:]):
        return None
    return path_to_intermediary + path_from_intermediary[1:]


def get_mapping(nodes_list):
    """
    Maps arbitrary node indexes to 0..n range
    """
    return dict(zip(nodes_list, range(len(nodes_list))))
