from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

# IN TERMINAL (ctrl + `) TYPE THE FOLLOWING: 
# pip install flask
# pip install flask_sqlalchemy
# flask run

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///outfits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Outfit(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  top = db.Column(db.String(100), nullable=False)
  bottom = db.Column(db.String(100))
  shoes = db.Column(db.String(100))  # NEW!!! look at HTML form
  weather = db.Column(db.Boolean)  # NEW!!! look at HTML form

  def __repr__(self):
    return f'<Outfit {self.top}>'


@app.route('/')
def index():
  outfits = Outfit.query.all()
  return render_template('index.html', outfits=outfits)


# Define ROUTE and FUNCTION for adding an outfit
@app.route('/add', methods=['POST'])
def add_outfit():
  # Retrieve input data from HTML form
  top = request.form['top']
  bottom = request.form['bottom']
  shoes = request.form['shoes']
  weather = True if request.form['weather'] == 'Warm' else False  # NEW!!!

  # Create an Outfit object based on form data
  new_outfit = Outfit(top=top, bottom=bottom, shoes=shoes, weather=weather)

  # Commit new object to database
  db.session.add(new_outfit)
  db.session.commit()

  # Refresh the page with new data
  return redirect(url_for('index'))


# Define a route and function for deleting an outfit
@app.route('/delete/<int:outfit_id>')
def delete_outfit(outfit_id):
  outfit = Outfit.query.get(outfit_id)
  if outfit:
    db.session.delete(outfit)
    db.session.commit()
  return redirect(url_for('index'))


if __name__ == '__main__':
  with app.app_context():
    db.create_all()
  app.run(host='0.0.0.0', port=5421, debug=True)

# FIX FOUND for "sqlite3 OperationalError: no such table"
# in the Shell window, enter: python main.py
# then press Run & your program should work
