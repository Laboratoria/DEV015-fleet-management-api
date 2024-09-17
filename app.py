from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Configurar conexión a la base de datos PostgreSQL en Vercel
def get_db_connection():
    return psycopg2.connect(
        host='ep-proud-scene-a1ctqxby-pooler.ap-southeast-1.aws.neon.tech',
        database='verceldb', 
        user='default',  
        password='LNpT4n5jdOBf', 
        port='5432'  
    )

@app.route('/api/taxis', methods=['GET'])
def get_taxis():
    """
    Endpoint para obtener taxis filtrados por placa y paginados.
    ---
    parameters:
      - name: plate
        in: query
        type: string
        required: false
        description: Patrón para filtrar taxis por placa
      - name: page
        in: query
        type: integer
        required: false
        default: 1
        description: Número de página
      - name: limit
        in: query
        type: integer
        required: false
        default: 10
        description: Número de taxis por página
    responses:
      200:
        description: Lista de taxis
        schema:
          type: array
          items:
            properties:
              id:
                type: integer
              plate:
                type: string
        examples:
          application/json: [
            {"id": 974, "plate": "FNDF-2678"},
            {"id": 8935, "plate": "GAJG-2446"}
            {"id": 6772, "plate": "NOCB-3788"}

          ]
      400:
        description: Parámetros de página o límite no válidos
        schema:
          properties:
            error:
              type: string
        examples:
          application/json: { "error": "page or limit is not valid" }

    """
    plate = request.args.get('plate', '')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    offset = (page - 1) * limit

    # Validación de los parámetros
    if page < 1 or limit < 1:
        return jsonify({"error": "page or limit is not valid"}), 400

    try:
        # Conexión a la base de datos
        conn = get_db_connection()
        cur = conn.cursor()

        # Consulta SQL con filtro por 'plate' y paginación
        query = """
        SELECT id, plate
        FROM taxis
        WHERE plate ILIKE %s
        LIMIT %s OFFSET %s
        """
        cur.execute(query, (f'%{plate}%', limit, offset))
        taxis = cur.fetchall()

        cur.close()
        conn.close()

        # Formatear la respuesta
        taxi_list = [{'id': taxi[0], 'plate': taxi[1]} for taxi in taxis]
        return jsonify(taxi_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Iniciar servidor
if __name__ == '__main__':
    app.run(debug=True)
