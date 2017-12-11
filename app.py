from flask import Flask


app = Flask(__name__)


@app.route('/maps')
def maps():
    return 'ok'


@app.route('/find-thiefs-route')
def find_thief_route():
    return 'ok'


if __name__ == '__main__':
    app.run()
