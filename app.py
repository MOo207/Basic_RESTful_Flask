from flask import Flask, request, jsonify, abort, flash
import unicodedata as unicode
from flaskext.mysql import MySQL

#App Initialization
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
@app.route('/tasks', methods=['GET'])
def get():
    connection = mysql.connect()
    cursor = connection.cursor()
    query = str("SELECT * from users")
    cursor.execute(query)
    dbData = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({'All Data is': dbData}) , 200

# GET One Entry From MysqlDB By ID
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    connection = mysql.connect()
    cursor = connection.cursor()
    query = str("SELECT * from users where uid=%s")
    cursor.execute(query,(str(task_id)))
    dbData = cursor.fetchone()
    cursor.close()
    connection.close()
    data = [data for data in dbData if dbData[0] == task_id]
    if len(data) == 0 or dbData is None:
        abort(404)
    return jsonify({'data for id '+str(task_id)+" is": data}) , 200

# POST New Entry To DBcontent
@app.route('/tasks', methods=['POST'])
def create_task():
    name = request.args.get('name')
    email = str(request.args.get('email'))
    password = str(request.args.get('password'))
    connection = mysql.connect()
    cursor = connection.cursor()
    query = 'INSERT INTO `users` (`name`, `email` , `password`) VALUES (%s,%s, %s)'
    cursor.execute(query,(name,email,password))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'Post': True}), 201

# PUT Modified Entry
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    connection = mysql.connect()
    cursor = connection.cursor()
    query = str("SELECT * from users where `uid`=%s")
    cursor.execute(query,(str(task_id)))
    data = cursor.fetchone()
    print(data)
    name = str(request.args.get('name'))
    email = str(request.args.get('email'))
    password = str(request.args.get('password'))
    query = str('UPDATE `users` SET `name` = %s, `email` = %s, `password` = %s WHERE `users`.`uid`=%s')
    cursor.execute(query,(name,email,password,task_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'updated task': True}), 201

# DELETE One Entry From MyTasks List
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    connection = mysql.connect()
    cursor = connection.cursor()
    query = str("DELETE FROM users WHERE `uid`=%s")
    cursor.execute(query,str(task_id))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({'result': True}) , 200

if __name__ == '__main__':
    app.run(debug=True)
