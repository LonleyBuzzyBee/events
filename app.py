from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Event(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(200), nullable=False)
  description = db.Column(db.String(200), nullable=False)
  price = db.Column(db.Integer, default=0)
  img = db.Column(db.String(400), nullable=True)
  date = db.Column(db.String(8), nullable=False)

  def __repr__(self):
    return '<Event %r>' % self.id
    
@app.route('/', methods=['POST', 'GET'])
def index():
    events = Event.query.order_by(Event.price).all()
    return render_template('index.html', events=events)
@app.route('/about', methods=['GET'])
def about():
  return render_template('about.html')

@app.route('/delete/<int:id>')
def delete(id):
  event_to_delete = Event.query.get_or_404(id)
  try:
    db.session.delete(event_to_delete)
    db.session.commit()
    return redirect('/')
  except:
    return 'There was a problem deleting that event'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
  event = Event.query.get_or_404(id)
  if request.method == "POST":
    event.title = request.form['title']
    event.description = request.form['description']
    event.price = request.form['price']
    event.img = request.form['img']
    event.date = request.form['date']
    try:
      db.session.commit()
      return redirect('/')
    except:
      return 'Unable update event, something went wrong'
  else:
    return render_template('update.html', event=event)

@app.route('/details/<int:id>', methods=['GET'])
def details(id):
  this_event = Event.query.get_or_404(id)
  return render_template('event_details.html', event=this_event)

@app.route('/create', methods=['POST','GET'])
def create_event():
  if request.method == 'POST':
    event_title = request.form['title']
    event_description = request.form['description']
    event_price = request.form['price']
    event_img = request.form['img']
    event_date = request.form['date']
    new_event = Event(title=event_title, description=event_description, price=event_price, img=event_img, date=event_date)
    try:
      db.session.add(new_event)
      db.session.commit()
      return redirect('/')
    except:
      return 'Unable add new task, something went wrong'
  else:
     return render_template('create.html')

if __name__ == "__main__":
  app.run(debug=True)