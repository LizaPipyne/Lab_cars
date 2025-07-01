"""
Sis failas nera Flask dalis
juo pildome db duomenis
"""
import datetime

from app  import app, db, Car

with app.app_context():
    db.create_all()

    car1 = Car('Toyota', 'Avensis', 'blue',
                                  datetime.datetime.fromisoformat('2020-01-01'),
                                  16000)
    # elf.automaker = automaker
    # self.model = model
    # self.color = color
    # self.year = year
    # self.price = price

    car2 = Car('Skoda', 'Oktavia', 'green',
                                  datetime.datetime.fromisoformat('2023-01-01'),
                                  35000)


    cars = [car1, car2]
    db.session.add_all(cars)
    db.session.commit()








