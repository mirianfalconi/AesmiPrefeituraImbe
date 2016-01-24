from flask import Flask, json
from flaskext.mysql import MySQL

app = Flask(__name__)

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'adminzmRXBau'
app.config['MYSQL_DATABASE_PASSWORD'] = 'h8eE3gD_8Q4j'
app.config['MYSQL_DATABASE_DB'] = 'AESMI'
app.config['MYSQL_DATABASE_HOST'] = '127.7.29.130'
mysql.init_app(app)


def acessa_proc(nome, sql):
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.callproc(nome, sql)
        data = cursor.fetchall()

        if len(data) is 0:
            conn.commit()
        else:
            return data

    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        conn.close()


def acessa_sql(sql):
    try:
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
    except Exception as e:
        return json.dumps({'error': str(e)})
    finally:
        cursor.close()
        con.close()
    return data

