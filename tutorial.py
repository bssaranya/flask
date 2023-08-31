from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
import  sqlalchemy

app = Flask(__name__)
app.secret_key = "nandu"
app.permanent_session_lifetime = timedelta(minutes=5)

a = False
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/login", methods=["POST","GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        user = request.form["nm"]
        session["user"] = user
        flash("Login successful")
        flash(f"Welcome {user}")
        return redirect(url_for("user"))
    else:
        if "user" in session:
            flash("Already logged in")
            return redirect(url_for("user"))
        return render_template("login.html")

@app.route("/user", methods=["GET", "POST"])
def user():
    email = None
    if "user" in session:
        user = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
            flash("Email was saved")
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        flash("You are not logged in")
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    if "user" in session:
        user= session["user"]
        flash(f"You have been logged out {user}", "info")

    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
