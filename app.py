import json

from peewee import DoesNotExist
from flask import Flask, request, abort

from graph import compute_routes, find_route, get_mapping
from models import db, City


app = Flask(__name__)


@app.route('/maps', methods=['POST'])
def maps():
    data = request.get_json()
    nodes = data['nodes']
    nodes_count = len(nodes)
    graph = [[-1 for j in range(nodes_count)] for i in range(nodes_count)]
    mapping = get_mapping(nodes)
    for street in data['streets']:
        graph[mapping[street['from']]][mapping[street['to']]] = 1
    for i in range(nodes_count):
        graph[i][i] = 0
    intermediary_info = compute_routes(graph)
    model_data = {
        'name': data['name'],
        'mapping': json.dumps(mapping),
        'graph': json.dumps(data['streets']),
        'intermediary_info': json.dumps(intermediary_info)
    }
    try:
        name = data['name']
        city = City.get(City.name == name)
        for k, v in model_data.items():
            setattr(city, k, v)
        city.save()
    except DoesNotExist:
        City.create(**model_data)
    return 'ok'


@app.route('/find-thiefs-route', methods=['POST'])
def find_thiefs_route():
    data = request.get_json()
    try:
        city = City.get(name=data['map'])
        mapping = dict((int(k), v) for k, v in json.loads(city.mapping).items())
        reverse_mapping = dict((v, k) for k, v in mapping.items())
        intermediaries = json.loads(city.intermediary_info)
        crime_checkpoints = list(map(lambda crime: crime[1], sorted(map(
            lambda crime: (crime['time'], crime['node'],),
            data['alerts']
        ))))
        victims_node = data['crime']['node']
        crime_trace = [victims_node, *crime_checkpoints]
        thief_route = [victims_node]
        for start_node, end_node in zip(crime_trace, crime_trace[1:]):
            intermediary_route = find_route(
                mapping[start_node], mapping[end_node], intermediaries
            )[1:]
            if intermediary_route is None:
                return f"Thief must have been using portals", 400
            thief_route.extend(map(lambda node: reverse_mapping[node], intermediary_route))
        return json.dumps({'route': thief_route})
    except DoesNotExist:
        return f"City with name `{data['map']}` does not exists", 404


if __name__ == '__main__':
    db.connect()
    db.create_tables([City], safe=True)
    app.run()
