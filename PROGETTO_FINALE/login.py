from flask import Flask, request, render_template, redirect, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Cambia questa chiave in produzione

# Configurazione database
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "nome_database"
}


def get_db_connection():
    return mysql.connector.connect(**DB_CONFIG)


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return "Credenziali errate!", 401

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return f"Benvenuto {session['user']}!"  # Qui puoi mostrare il contenuto dell'area riservata


@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
