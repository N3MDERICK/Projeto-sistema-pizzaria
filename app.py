from flask import Flask, render_template, request, redirect, url_for
from models import db, Cliente, Pizza, Pedido, pedido_pizza

app = Flask(__name__)

#CONFIGURAÇÃO DO SQLITE
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)




#AQUI CRIA BANCO NA PRIMEIRA EXECUÇÃO
with app.app_context():
    db.create_all()




# PAGINA INCIAL ONDE APARECE PRIMEIRO
@app.route("/")
def index():
    return render_template("index.html")




#CLIENTES
@app.route("/clientes")
def clientes():
    lista = Cliente.query.all()
    return render_template("clientes.html", clientes=lista)

@app.route("/clientes/add", methods=["POST"])
def add_cliente():
    nome = request.form["nome"]
    email = request.form["email"]



    # ESSE IF IMPEDE EMAIL DUPLICADO
    if Cliente.query.filter_by(email=email).first():
        return "Erro: e-mail já cadastrado!"



    novo = Cliente(nome=nome, email=email)
    db.session.add(novo)
    db.session.commit()
    return redirect(url_for("clientes"))




#PIZZAS
@app.route("/pizzas")
def pizzas():
    lista = Pizza.query.all()
    return render_template("pizzas.html", pizzas=lista)

@app.route("/pizzas/add", methods=["POST"])
def add_pizza():
    sabor = request.form["sabor"]
    preco = request.form["preco"]

    nova = Pizza(sabor=sabor, preco=float(preco))
    db.session.add(nova)
    db.session.commit()
    return redirect(url_for("pizzas"))



#PEDIDOS 
@app.route("/pedidos")
def pedidos():
    lista = Pedido.query.all()
    return render_template("pedidos.html", pedidos=lista)

@app.route("/pedidos/add", methods=["POST"])
def add_pedido():
    cliente_id = request.form["cliente_id"]
    pizzas_ids = request.form.getlist("pizzas")

    novo = Pedido(cliente_id=cliente_id)


    # ADICIONA AS PIZZAS ESCOLHIDAS
    for i in pizzas_ids:
        pizza = Pizza.query.get(int(i))
        novo.pizzas.append(pizza)

    db.session.add(novo)
    db.session.commit()
    return redirect(url_for("pedidos"))

@app.route("/pedidos/update/<int:id>", methods=["POST"])
def update_pedido(id):
    pedido = Pedido.query.get(id)
    pedido.status = request.form["status"]
    db.session.commit()
    return redirect(url_for("pedidos"))




#RELATÓRIOS
@app.route("/relatorios")
def relatorios():
    total_pedidos = Pedido.query.count()

    # QUANTIDADE POR STATUS
    status_counts = db.session.query(Pedido.status, db.func.count(Pedido.id)).group_by(Pedido.status).all()

    # PIZZA MAIS PEDIDA
    from sqlalchemy import func
    pizza_mais_pedida = db.session.query(Pizza.sabor, func.count(pedido_pizza.c.pizza_id)) \
        .join(pedido_pizza, Pizza.id == pedido_pizza.c.pizza_id) \
        .group_by(Pizza.sabor) \
        .order_by(func.count(pedido_pizza.c.pizza_id).desc()) \
        .first()

    return render_template("relatorios.html", total=total_pedidos, status_counts=status_counts, pizza_mais=pizza_mais_pedida)


if __name__ =='__main__':
    app.run(debug=True)