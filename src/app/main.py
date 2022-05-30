#from aiohttp import BasicAuth
from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth
from textblob import TextBlob
from sklearn.linear_model import LinearRegression
import pickle
import os

colunas = ['tamanho', 'ano', 'garagem']
modelo = pickle.load(open('../../models/modelo.sav', 'rb'))

app = Flask(__name__) # Definindo nome do app
app.config['BASIC_AUTH_USERNAME'] = os.environ.get('BASIC_AUTH_USERNAME')
app.config['BASIC_AUTH_PASSWORD'] = os.environ.get('BASIC_AUTH_PASSWORD')

basic_auth = BasicAuth(app)

@app.route('/') # Rota home, colocou / para não precisar passar mais nenhum caminho adicional
def home(): # Criando função para executar uma ação quando uma pessoa acessar API
    return 'Minha primeira API'

@app.route('/sentimento/<frase>') # end point,<> para colocar frase
@basic_auth.required
def sentimento(frase):
    tb = TextBlob(frase)
    polaridade = tb.sentiment.polarity
    return 'Polaridade: {}'.format(polaridade)

@app.route('/cotacao/', methods=['POST'])
@basic_auth.required
def cotacao():
    dados = request.get_json()
    dados_input = [dados[col] for col in colunas]
    preco = modelo.predict([dados_input])
    return jsonify(preco=preco[0])
    
app.run(debug=True, host='0.0.0.0')

# Debug serve para quando alterar algo, o  flask identificar e restartar o processo
# Depois, é só ir no terminal e executar o arquivo
# Vai retornar um link com o IP da máquina e a porta de acesso, ex http://127.0.0.1:5000/ , temos o
# IP 127.0.0.1 e porta 5000
# Além dos Flask, outros frameworks são utilizados, como é o caso do Django e Pyramid