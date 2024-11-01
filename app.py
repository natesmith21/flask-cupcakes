from flask import Flask, request, jsonify, render_template
from models import db, connect_db, Cupcake

"""Flask app for Cupcakes"""

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"
app.app_context().push()

connect_db(app)

#***** APP ROUTES BELOW ***** 

@app.route('/')
def get_home():

    ccs = Cupcake.query.all()
    return render_template('home.html', ccs=ccs)


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

@app.route('/api/cupcakes/<int:cc_id>', methods=['PATCH'])
def update_cupcake(cc_id):
    '''updates 1 particular cupcake'''

    cc = Cupcake.query.get_or_404(cc_id)
    cc.flavor = request.json.get('flavor', cc.flavor)
    cc.size = request.json.get('size', cc.size)
    cc.rating = request.json.get('rating', cc.rating)
    cc.image = request.json.get('image', cc.image)
    db.session.commit()
    return jsonify(cupcakes=cc.serialize())

@app.route('/api/cupcakes/<int:cc_id>', methods=['DELETE'])
def delete_cupcake(cc_id):
    '''deletes a particular cupcake'''

    cc = Cupcake.query.get_or_404(cc_id)
    db.session.delete(cc)
    db.session.commit()
    return jsonify(message='deleted')



