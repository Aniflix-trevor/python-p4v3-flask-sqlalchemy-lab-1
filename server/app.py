# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here;
@app.post('/earthquakes/<int:id>')
def add_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        body = {'message': 'Earthquake already exists', 'earthquake': earthquake.to_dict()}
        return make_response(body, 400)

    # Assuming we have some data to create a new earthquake
    new_earthquake = Earthquake(id=id, magnitude=5.0, location='Unknown', year=2023)
    db.session.add(new_earthquake)
    db.session.commit()

    body = {'message': 'Earthquake added successfully', 'earthquake': new_earthquake.to_dict()}
    return make_response(body, 201)

@app.get('/earthquakes/<int:id>')
def get_earthquake(id):
    earthquake = Earthquake.query.get(id)
    if earthquake:
        return make_response(jsonify(earthquake.to_dict()), 200)
    else:
        body = {'error': 'Earthquake not found'}
        return make_response(jsonify(body), 404)

if __name__ == '__main__':
    app.run(port=5555, debug=True)