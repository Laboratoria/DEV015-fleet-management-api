from flask import Flask



# Crear la aplicación Flask
app = Flask(__name__)

# Definir el primer endpoint
@app.route('/')
def home():
    return "Servidor funcionando"

@app.route('/taxis', methods=['GET'])
def taxis():
    return "Hola Mundo"

# Iniciar la aplicación Flask
if __name__ == "__main__":
    app.run(debug=True)
