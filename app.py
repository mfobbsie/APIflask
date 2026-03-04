from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import ValidationError
from sqlalchemy import DateTime, Float, String, Table, Column, Integer, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

#Initialize Flask app
app = Flask(__name__)

#Configure MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:ellietteGrace22@localhost/flask_api_db'   

#Create base Model class
class Base(DeclarativeBase):
    pass
#Initialize extensions
db = SQLAlchemy(app, model_class=Base)
ma = Marshmallow(app)

#Association Table for many orders and products
order_product = Table(
    'order_product',
    Base.metadata,
    Column('order_id', Integer, ForeignKey('orders.id'), primary_key=True),
    Column('product_id', Integer, ForeignKey('products.id'), primary_key=True)
)

#Models
class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    address: Mapped[str] = mapped_column(String(200), nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    
    #One-to-many relationship with orders
    orders: Mapped[list["Order"]] = relationship('Order', back_populates='user', lazy=True)
    
class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    order_date: Mapped[DateTime] = mapped_column(DateTime, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('users.id'), nullable=False)
    #Many-to-one relationship with user
    user: Mapped["User"] = relationship('User', back_populates='orders')
    #Many-to-many relationship with products
    products: Mapped[list["Product"]] = relationship('Product', secondary=order_product, back_populates='orders')
    
class Product(Base):
    __tablename__ = 'products'
    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)
    
    #Many-to-many relationship with orders
    orders: Mapped[list["Order"]] = relationship('Order', secondary=order_product, back_populates='products')

#User Schema for serialization
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = False
        
#Order Schema for serialization
class OrderSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Order
        load_instance = False
        include_fk = True
        
#Product Schema for serialization
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = False  
                
#Initialize schema instances
user_schema = UserSchema()
users_schema = UserSchema(many=True)
order_schema = OrderSchema()
orders_schema = OrderSchema(many=True)
product_schema = ProductSchema()
products_schema = ProductSchema(many=True)   


def load_payload(schema, *, partial=False):
    try:
        return schema.load(request.json, partial=partial), None
    except ValidationError as e:
        db.session.rollback()
        return None, (jsonify(e.messages), 400)


def apply_updates(model, data, allowed_fields):
    for field in allowed_fields:
        if field in data:
            setattr(model, field, data[field])


def commit_session():
    db.session.commit()


def persist_instance(instance):
    db.session.add(instance)
    commit_session()
    return instance


def delete_instance(instance, message):
    db.session.delete(instance)
    commit_session()
    return jsonify({'message': message}), 200

#Helper function to get order-product link data with user, order, and product details
def get_order_product_rows(order_id=None):
    statement = (
        db.select(
            Order.user_id.label('user_id'),
            Order.id.label('order_id'),
            Product.id.label('product_id'),
            Product.name.label('product_name'),
            Product.price.label('product_price')
        )
        .select_from(Order)
        .join(order_product, order_product.c.order_id == Order.id)
        .join(Product, Product.id == order_product.c.product_id)
    )

    if order_id is not None:
        statement = statement.where(Order.id == order_id)

    rows = db.session.execute(statement).mappings().all()
    return [dict(row) for row in rows]

# User Endpoints

@app.route('/api/users', methods=['POST'])
def create_user():
    user_data, error_response = load_payload(user_schema)
    if error_response:
        return error_response
    
    new_user = User(
        name=user_data['name'],
        address=user_data['address'],
        email=user_data['email']
    )
    persist_instance(new_user)
    return user_schema.jsonify(new_user), 201

#Get all users 
@app.route('/api/users', methods=['GET'])
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    return users_schema.jsonify(users), 200

#Get user by ID
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.get_or_404(User, user_id)
    return user_schema.jsonify(user), 200

#Update user by ID
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = db.get_or_404(User, user_id)
    user_data, error_response = load_payload(user_schema, partial=True)
    if error_response:
        return error_response

    apply_updates(user, user_data, ('name', 'address', 'email'))

    commit_session()
    return user_schema.jsonify(user), 200       

#Delete user by ID
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.get_or_404(User, user_id)
    return delete_instance(user, 'User deleted successfully')

#Product Endpoints
@app.route('/api/products', methods=['POST'])
def create_product():
    product_data, error_response = load_payload(product_schema)
    if error_response:
        return error_response
    
    new_product = Product(
        name=product_data['name'],
        price=product_data['price']
    )
    persist_instance(new_product)
    return product_schema.jsonify(new_product), 201

#Get all products
@app.route('/api/products', methods=['GET'])
def get_products():
    products = db.session.execute(db.select(Product)).scalars().all()
    return products_schema.jsonify(products), 200

#Get product by ID
@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = db.get_or_404(Product, product_id)
    return product_schema.jsonify(product), 200

#Update product by ID
@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = db.get_or_404(Product, product_id)
    product_data, error_response = load_payload(product_schema, partial=True)
    if error_response:
        return error_response

    apply_updates(product, product_data, ('name', 'price'))

    commit_session()
    return product_schema.jsonify(product), 200     

#Delete product by ID
@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = db.get_or_404(Product, product_id)
    return delete_instance(product, 'Product deleted successfully')

# Order Endpoints
@app.route('/api/orders', methods=['POST'])
def create_order():
    order_data, error_response = load_payload(order_schema)
    if error_response:
        return error_response
    
    new_order = Order(
        order_date=order_data['order_date'],
        user_id=order_data['user_id']
    )
    persist_instance(new_order)
    return order_schema.jsonify(new_order), 201

#Add products to order
@app.route('/api/orders/<int:order_id>/products', methods=['PUT'])
def add_products_to_order(order_id):
    order = db.get_or_404(Order, order_id)
    request_data = request.get_json(silent=True) or {}
    product_ids = request_data.get('products')

    if not isinstance(product_ids, list) or not product_ids:
        return jsonify({'message': 'products must be a non-empty list of product IDs'}), 400

    for product_id in product_ids:
        product = db.get_or_404(Product, product_id)
        if product not in order.products:
            order.products.append(product)
    commit_session()
    return order_schema.jsonify(order), 200

#Get all orders for a user
@app.route('/api/orders', methods=['GET'])
def get_orders():
    orders = db.session.execute(db.select(Order)).scalars().all()
    return orders_schema.jsonify(orders), 200

#Get order by ID
@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = db.get_or_404(Order, order_id)
    return order_schema.jsonify(order), 200

#Get all products in an order
@app.route('/api/orders/<int:order_id>/products', methods=['GET'])
def get_order_products(order_id):
    order = db.get_or_404(Order, order_id)
    products = order.products
    return products_schema.jsonify(products), 200


@app.route('/api/order-products', methods=['GET'])
def get_order_product_links():
    return jsonify(get_order_product_rows()), 200


@app.route('/api/orders/<int:order_id>/order-products', methods=['GET'])
def get_order_product_links_by_order(order_id):
    db.get_or_404(Order, order_id)
    return jsonify(get_order_product_rows(order_id=order_id)), 200

#Delete product from order
@app.route('/api/orders/<int:order_id>', methods=['DELETE'])
def delete_product_from_order(order_id):
    order = db.get_or_404(Order, order_id)
    product_id = request.json.get('product_id')
    if not product_id:
        return jsonify({'message': 'Product ID is required'}), 400
    product = db.get_or_404(Product, product_id)
    if product not in order.products:
        return jsonify({'message': 'Product not found in order'}), 404
    order.products.remove(product)
    commit_session()
    return jsonify({'message': 'Product removed from order successfully'}), 200

# Health Check Endpoint

@app.route('/')
def home():
    return {'message': 'Flask API is running'}, 200


@app.route('/health')
def health():
    return {'status': 'ok'}, 200
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables in the database
    app.run(debug=True, port=5050)