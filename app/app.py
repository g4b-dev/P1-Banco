from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://<postgres>:<116440>@<localhost>:5432/<db.p1>'
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Product {self.name}>'

@app.route('/products', methods=['GET', 'POST'])
def products():
    if request.method == 'GET':
        products = Product.query.all()
        output = []
        for product in products:
            product_data = {'id': product.id, 'name': product.name, 'description': product.description}
            output.append(product_data)
        return jsonify({'products': output})
    elif request.method == 'POST':
        data = request.json
        new_product = Product(name=data['name'], description=data['description'])
        db.session.add(new_product)
        db.session.commit()
        return jsonify({'message': 'Product created successfully'})

@app.route('/products/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def product(id):
    product = Product.query.get_or_404(id)
    if request.method == 'GET':
        product_data = {'id': product.id, 'name': product.name, 'description': product.description}
        return jsonify({'product': product_data})
    elif request.method == 'PUT':
        data = request.json
        product.name = data['name']
        product.description = data['description']
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})
    elif request.method == 'DELETE':
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
