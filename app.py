from flask import Flask, render_template, request, redirect, url_for
from werkzeug.exceptions import BadRequest

from data.customer import Customer

app = Flask(__name__)
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


if __name__ == '__main__':
    app.run()
