from app.run_app import startCode

app = startCode()

# Start the server
if __name__ == '__main__':
    app.run(debug=True) #Debuggear y mirar errores
