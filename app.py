from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

import  datetime

app = Flask(__name__)

# app konfigūracija
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db objektas
db = SQLAlchemy(app)

class Car(db.Model):
    __tablename__ = 'cars_create'
    id = db.Column(db.Integer, primary_key=True)
    automaker= db.Column(db.String)
    model = db.Column(db.String)
    color = db.Column(db.String)
    year = db.Column(db.Date)
    price = db.Column(db.Integer)

    def __init__(self, automaker, model, color, year, price):
        self.automaker = automaker
        self.model = model
        self.color = color
        self.year = year
        self.price = price

    def __str__(self):
        return f"{self.automaker} {self.model} {self.color} {self.year} "

# darbas su sql db failu
with app.app_context():
    db.create_all()

@app.route('/')
def home():
    search_text = request.args.get('paieskoslaukelis')
    if search_text:
        all_rows = Car.query.filter(Car.model.ilike(search_text + '%')).all()
    else:
        all_rows = Car.query.all()
    return render_template('index.html', all_rows=all_rows)

@app.route('/cars/<int:car_id>')
def one_car(car_id):
    one_row = Car.query.get(car_id)
    return render_template('one_car.html', one_row=one_row)

@app.route('/cars/new', methods=['GET', 'POST'])
def new_car():
    if request.method == 'GET':
        return  render_template('new_car.html')
    elif request.method == 'POST':
        automaker = request.form.get('automakerlaukas')
        model = request.form.get('modellaukas')
        color = request.form.get('colorlaukas')
        year = request.form.get('yearlaukas')
        price = request.form.get('pricelaukas')
        if automaker and model:
            new_row = Car(automaker, model, color,
                      datetime.datetime.fromisoformat(year),
                        int(price))
            db.session.add(new_row)
            db.session.commit()
    return redirect(url_for('home'))

@app.route('/cars/delete/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    row = Car.query.get(car_id)
    db.session.delete(row)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/cars/edit/<int:car_id>', methods=['GET', 'POST'])
def edite_car(car_id):
    row = Car.query.get(car_id)
    if not row:
        return "Nuoroda neegzistuoja"

    if request.method == 'GET':
        return render_template('update_car.html', row=row)

    elif request.method == 'POST':
        automaker = request.form.get('automakerlaukas')
        model = request.form.get('modellaukas')
        color = request.form.get('colorlaukas')
        year = request.form.get('yearlaukas')
        price = request.form.get('pricelaukas')
        if automaker and model and year and price:
            row.automaker = automaker
            row.model = model
            row.color = color
            row.year = datetime.datetime.fromisoformat(year)
            row.price = int(price)
            db.session.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(port=5001)
