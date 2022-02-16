from flask import render_template, redirect, request
from flask_app import app
from flask_app.models.email import Email


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/emails')
def emails():
    return render_template("emails.html", all_emails=Email.get_all())


@app.route('/create_email', methods=['POST'])
def create_email():
    if not Email.validate_email(request.form):
        return redirect('/')
    Email.create(request.form)
    return redirect('/emails')


@app.route("/delete/<int:num>")
def delete_email(num):
    data = {
        "id": num
    }
    Email.delete(data)
    return redirect("/emails")
