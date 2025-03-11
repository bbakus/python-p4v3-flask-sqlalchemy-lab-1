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

# Add views here

@app.route('/earthquakes/<int:id>')
def earthquakes_view(id):

    earthquake = Earthquake.query.get(id)
    
    if earthquake is None:
        return jsonify({"message": f"Earthquake {id} not found."}), 404
        
    return jsonify({
        "id": earthquake.id,
        "location": earthquake.location,
        "magnitude": earthquake.magnitude,
        "year": earthquake.year
    })


@app.route('/earthquakes/magnitude/<float:magnitude>')
def earthquakes_by_magnitude(magnitude):

    quakes = Earthquake.query.filter(Earthquake.magnitude >= magnitude).all()
    
    response = {
        "count": len(quakes),
        "quakes": [quake.to_dict() for quake in quakes]
    }
    
    return jsonify(response)


if __name__ == '__main__':
    app.run(port=5555, debug=True)
