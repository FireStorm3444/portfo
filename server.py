from flask import Flask, render_template as render, request, redirect
import csv

app = Flask(__name__)


@app.route("/")
def index():
    return render('index.html')


@app.route("/<string:page_name>")
def html_page(page_name):
    return render(page_name)


def update_database_text(data_dict):
    with open('./database.txt', mode='a+') as database:
        email = data_dict['email']
        subject = data_dict['subject']
        message = data_dict['message']
        if database.tell() != 0:
            database.write(f'\nemail: {email}\nsubject: {subject}\nmessage: {message}\n')
        else:
            database.write(f'email: {email}\nsubject: {subject}\nmessage: {message}\n')


def update_database_csv(data_dict):
    with open('./database.csv', newline='', mode='a') as database:
        email = data_dict['email']
        subject = data_dict['subject']
        message = data_dict['message']
        if database.tell() == 21:
            csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            database.write('\n')
            csv_writer.writerow([email, subject, message])
        else:
            csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([email, subject, message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            update_database_csv(data)
            return redirect('./thankyou.html')
        except:
            return 'Could not save to Database!!'
    else:
        return 'Something went wrong. Try Again!'
