from flask import Flask, request, jsonify, abort, flash
from flaskext.mysql import MySQL
import sys

# App Initialization
app = Flask(__name__)

# Instantiate Object From MYSQL-DB
mysql = MySQL()

# # Localhost MySQL configurations
# app.config['MYSQL_DATABASE_USER'] = "root"
# app.config["MYSQL_DATABASE_PASSWORD"] = ""
# app.config["MYSQL_DATABASE_DB"] = "flask_app"
# app.config["MYSQL_DATABASE_HOST"] = "localhost"

# Initialization For Global DB
app.config['MYSQL_DATABASE_USER'] = "sql12342103"
app.config["MYSQL_DATABASE_PASSWORD"] = "lAsAiiDHNT"
app.config["MYSQL_DATABASE_DB"] = "sql12342103"
app.config["MYSQL_DATABASE_HOST"] = "sql12.freemysqlhosting.net"

# MySQL initialization
mysql.init_app(app)


# GET Whole DBcontent
@app.route('/users', methods=['GET'])
def get():
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = str("SELECT * from users")
        cursor.execute(query)
        data = cursor.fetchall()
    except:
        return jsonify({'All Data is': data}), 404
    finally:
        cursor.close()
        connection.close()
    return jsonify({'All Data is': data}), 200


# GET One Entry From MysqlDB By ID
@app.route('/users/<task_id>', methods=['GET'])
def get_task(task_id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = str("SELECT * from users where uid=%s")
        cursor.execute(query, (task_id))
        dbData = cursor.fetchone()
        data = [data for data in dbData if str(dbData[0]) == task_id]
        if len(data) == 0 or dbData is None:
            abort(404)
        return jsonify({'data for id ' + task_id + " is": data}), 200
    except:
        return sys.exc_info()
    finally:
        cursor.close()
        connection.close()
    return jsonify({'finally': "done!"}), 200


# POST New Entry To DBcontent
@app.route('/users', methods=['POST'])
def create_task():
    try:
        name = request.args.get('name')
        email = str(request.args.get('email'))
        password = str(request.args.get('password'))
        connection = mysql.connect()
        cursor = connection.cursor()
        query = 'INSERT INTO `users` (`name`, `email` , `password`) VALUES (%s,%s, %s)'
        cursor.execute(query, (name, email, password))
        connection.commit()
        return jsonify({'Post': True}), 201
    except:
        return sys.exc_info()
    finally:
        cursor.close()
        connection.close()


# PUT Modified Entry
@app.route('/users/<task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = str("SELECT * from users where `uid`=%s")
        cursor.execute(query, (task_id))
        data = cursor.fetchone()
        print(data)
        name = str(request.args.get('name'))
        email = str(request.args.get('email'))
        password = str(request.args.get('password'))
        query = str(
            'UPDATE `users` SET `name` = %s, `email` = %s, `password` = %s WHERE `users`.`uid`=%s')
        cursor.execute(query, (name, email, password, task_id))
        connection.commit()
        return jsonify({'updated task': True}), 201
    except:
        return sys.exc_info()
    finally:
        cursor.close()
        connection.close()


# DELETE One Entry From Myusers List
@app.route('/users/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        connection = mysql.connect()
        cursor = connection.cursor()
        query = str("DELETE FROM users WHERE `uid`=%s")
        cursor.execute(query, task_id)
        connection.commit()
        return jsonify({'result': True}), 200
    except:
        return sys.exc_info()
    finally:
        cursor.close()
        connection.close()

if __name__ == '__main__':
    app.run(debug=True)
