from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy # ORM

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://wtpmaglj:DUTH-x9j2NFD-v5Z7tsJOom79kU5PzxX@kesavan.db.elephantsql.com/wtpmaglj'

db = SQLAlchemy(app)

class Carro(db.Model): # Carro se tornará a tabela carro quando eu criar o banco de dados
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome = db.Column(db.String(150), nullable=False)
    marca = db.Column(db.String(150), nullable=False)
    imagem = db.Column(db.String(500), nullable=False)
    valor = db.Column(db.Float, nullable=False)
    
    def __init__(self, nome, marca, imagem, valor):
        self.nome = nome
        self.marca = marca
        self.imagem = imagem
        self.valor = valor

@app.route('/')
def index():
    catalogo = Carro.query.all()
    return render_template('index.html', listaCatalogo=catalogo)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        carro = Carro(
            request.form['nome'],
            request.form['marca'],
            request.form['imagem'],
            request.form['valor']
        )
        db.session.add(carro)
        db.session.commit()
        return redirect('/')

@app.route("/<id>")
def get_by_id(id):
    carro = Carro.query.get(id)
    return render_template('delete.html', carro=carro)

@app.route('/delete/<id>')
def delete(id):
    carro = Carro.query.get(id)
    db.session.delete(carro)
    db.session.commit()
    return redirect('/')

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    carro = Carro.query.get(id)
    if request.method == 'POST':
        carro.nome = request.form['nome']
        carro.marca = request.form['marca']
        carro.imagem = request.form['imagem']
        carro.valor = request.form['valor']
        db.session.commit()
        return redirect('/')
    return render_template('edit.html', carro=carro)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True, port=3000)