from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#AQUI É CLIENTE
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    pedidos = db.relationship("Pedido", backref="cliente", lazy=True)

#ENTIDADE PIZZA
class Pizza(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sabor = db.Column(db.String(100), nullable=False)
    preco = db.Column(db.Float, nullable=False)

#ENTIDADE PEDIDO,UM PEDIDO PERTENCE A UM CLIENTE MAS PODE TER VARIAS PIZZA
pedido_pizza = db.Table('pedido_pizza',
                        db.Column('pedido_id', db.Integer, db.ForeignKey('pedido.id')),
                        db.Column('pizza_id', db.Integer, db.ForeignKey('pizza.id'))

)

class Pedido(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"), nullable=False)
    status = db.Column(db.String(50), default="Em preparo")  # STATUS INICIAL

    # RELACIONAMENTO N PRA N ENTRE PEDIDO E PIZZA
    pizzas = db.relationship("Pizza", secondary=pedido_pizza, backref="pedidos")
#NAO SEI DIREITO O QUE TO FAZENDO TAMO FUDIDO