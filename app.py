import os
import db
from flask import Flask, render_template, send_from_directory, g


# initialization
app = Flask(__name__)
app.config.from_object(__name__)
app.debug = True


@app.before_request
def before_request():
    g.db = db.conn()


@app.teardown_request
def teardown_request(exception):
    g.db.close()


# controllers
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'ico/favicon.ico')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
def index():
    cur = g.db.cursor()
    cur.execute("SELECT title, text FROM post ORDER BY id DESC")
    main = dict(title=cur.fetchone()[0], text=cur.fetchone()[1])
    entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return render_template('index.html', main=main, entries=entries)


@app.route("/list")
def list():
    return render_template('list.html')


@app.route("/search")
def search():
    return render_template('search.html')


@app.route("/post")
def post():
    return render_template('post.html')


# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    app.run(host='0.0.0.0', port=port)
