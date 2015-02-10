from flask import Flask, jsonify, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return 'Flask is running!'


@app.route('/data')
def names():
    data = {"first_names": ["John", "Jacob", "Julie", "Jennifer"],
            "last_names": ["Connor", "Johnson", "Cloud", "Ray"]}
    return jsonify(data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run()
