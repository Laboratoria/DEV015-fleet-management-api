from flask import Flask

app = Flask(__name__)

# Aquí se define el endpoint y responde a la petición 'GET'
@app.route('/taxis', methods=['GET'])
def get_taxis():
    return "Hola mundo", 200

if __name__ == '__main__':
    app.run(debug=True)
