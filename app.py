import db
import os
import time
import json
from flask import Flask, render_template, send_from_directory, g, request


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


@app.route("/save", methods=['POST'])
def save():
    cur = g.db.cursor()
    title = request.form["title"]
    text = request.form["text"]
    date = time.strftime('%Y-%m-%d %H:%M:%S')
    writer = request.form["writer"]
    cur.execute("set names utf8")
    cur.execute("INSERT INTO notice(title, text, date, writer) VALUES\
                 ('%s', '%s', '%s', '%s')" % (title, text, date, writer))
    g.db.commit()
    return "done!"


@app.route("/noty_load")
def load():
    cur = g.db.cursor()
    cur.execute("SELECT title, text FROM notice ORDER BY date DESC")
    result = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
    return json.dumps(result)


@app.route("/noty_load2", methods=['POST'])
def load2():
    cur = g.db.cursor()
    writer = request.form["writer"]
    cur.execute("SELECT title, text, date FROM notice\
                WHERE writer = %s ORDER BY date DESC" % writer)
    result = [dict(title=row[0], text=row[1], date=row[2], writer=row[3])
              for row in cur.fetchall()]
    return json.dumps(result)


@app.route("/test")
def test():
    return render_template('test.html')

# launch
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 4000))
    app.run(host='0.0.0.0', port=port)
