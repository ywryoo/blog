# you need to make db_info.py to connect db
# there are 4 variables to define which is
# dbuser = sth
# dbpass = sth
# dbhost = sth
# dbname = sth
import MySQLdb as mdb
import db_info


def conn():
    try:
        con = mdb.connect(db_info.dbhost, db_info.dbuser,
                          db_info.dbpass, db_info.dbname, charset='utf8')
        return con
    except mdb.Error, e:
        print "Error %d: %s" % (e.args[0], e.args[1])
        return None
