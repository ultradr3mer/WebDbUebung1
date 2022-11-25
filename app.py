from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.exceptions import BadRequest

from data.customer import Customer

app = Flask(__name__)
app.secret_key = 'd1d3d823-c9a1-496e-9f04-a8f264470a20'
customers = []

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        data = request.form
        forename = data.get('forename')
        surname = data.get('surname')
        email = data.get('email')
        password = data.get('password')
        passwordconfirm = data.get('passwordconfirm')
        is_agb = data.get('checkagb') == 'on'
        is_newsletter = data.get('checknewsletter') == 'on'
        customer = Customer(forename, surname, email, password, is_agb, is_newsletter)

        try:
            if len(forename) == 0:
                raise BadRequest('Vorname nicht angegeben')

            if len(surname) == 0:
                raise BadRequest('Nachname nicht angegeben')

            if len(email) == 0:
                raise BadRequest('Email nicht angegeben')

            if len(password) == 0:
                raise BadRequest('Passwort nicht angegeben')

            if len(passwordconfirm) == 0:
                raise BadRequest('Passwort Wiederholung nicht angegeben')
            if password != passwordconfirm:
                raise BadRequest('Passwort Wiederholung stimmt nicht überein')

            if not is_agb:
                raise BadRequest('AGB nicht bestätigt')

            if any(c.email == email for c in customers):
                raise BadRequest('Benutzer bereits registriert')

            customers.append(customer)

        except BadRequest as e:
            return render_template('register.html',
                                   customer=customer,
                                   passwordconfirm=passwordconfirm,
                                   message=e.description)

        return redirect(url_for('index'))

    return render_template('register.html',
                           customer=Customer())


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.form
        email = data.get('email')
        password = data.get('password')
        matching_customers = [c for c in customers if c.email == email and c.password == password]

        if not matching_customers:
            return render_template('login.html', message="Fehlerhafte E-Mail oder Passwort")

        session["customer_signed_in"] = matching_customers[0].email
        return redirect(url_for('profile'))

    return render_template('login.html');


@app.route('/profile', methods=['GET'])
def profile():
    customer_signed_in = session["customer_signed_in"]
    if not customer_signed_in:
        return redirect(url_for('index'))

    customer = [c for c in customers if c.email == customer_signed_in][0]

    return render_template('profile.html', customer=customer)


@app.route('/logout', methods=['GET'])
def logout():
    session["customer_signed_in"] = None
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
