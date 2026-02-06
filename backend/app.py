from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app) # Allows your mobile apps to talk to the API

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///returns.db'
db = SQLAlchemy(app)

# The Return Model
class ReturnRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), default='Pending') # Pending, Approved, Shipped
    reason = db.Column(db.String(200))

# Create the database file
with app.app_context():
    db.create_all()

@app.route('/submit_return', methods=['POST'])
def create_return():
    data = request.json
    new_return = ReturnRequest(
        order_number=data['order_number'],
        reason=data.get('reason', '')
    )
    db.session.add(new_return)
    db.session.commit()
    return jsonify({"message": "Return submitted!", "id": new_return.id}), 201

@app.route('/returns', methods=['GET'])
def get_returns():
    all_returns = ReturnRequest.query.all()
    output = []
    for r in all_returns:
        output.append({"id": r.id, "order": r.order_number, "status": r.status})
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001) # host='0.0.0.0' lets your phone find the server