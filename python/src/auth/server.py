import jwt, datetime, os
from flask import Flask, request, jsonify, make_response
from flask_mysqldb import MySQL

server = Flask(__name__)
mysql = MySQL(server)

# config
server.config["MYSQL_HOST"] = os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"] = os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"] = os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"] = os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"] = os.environ.get("MYSQL_PORT")


@server.route("/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth:
        return "Missing credentials", 401

    # check db for username and password
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE username = %s",
        (auth.username),
    )
    if res:
        user_row = cur.fetchone()
        email = user_row[0]
        password = user_row[1]

        if auth.username != email or auth.password != password:
            return "Invalid credentials", 401
        else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "Invalid credentials", 401


def createJWT(username, secret, is_admin):
    payload = {
        "username": username,
        "is_admin": is_admin,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
    }
    token = jwt.encode(payload, secret, algorithm="HS256")
    return jsonify({"token": token.decode("UTF-8")})