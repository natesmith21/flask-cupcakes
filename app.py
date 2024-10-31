from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

"""Flask app for Cupcakes"""

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"
app.app_context().push()

connect_db(app)


# **** API BELOW ***** 

@app.route('/api/cupcakes')
def get_all_cupcakes():
    """returns JSON w/ all cupcakes"""
    
    all_cupcakes = [cc.serialize() for cc in Cupcake.query.all()] 
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:cc_id>')
def get_cupcake(cc_id):
    '''returns JSON for 1 cupcake'''

    cc = Cupcake.query.get_or_404(cc_id)
    return jsonify(cupcake=cc.serialize())

@app.route('/api/cupcakes', methods=['POST'])
def post_cupcake():
    '''creates cupcake and returns JSON'''

    new_cc = Cupcake(flavor = request.json['flavor'], 
                     size = request.json['size'],
                     rating = request.json['rating'],
                     image = request.json.get('image')
                     )
    db.session.add(new_cc)
    db.session.commit()
    response = jsonify(cupcake=new_cc.serialize())
    return (response, 201)


