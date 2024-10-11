import os
import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'PokeSearch.sqlite3')
    conn = sqlite3.connect(db_path)  # Usar la ruta absoluta del archivo de la base de datos
    conn.row_factory = sqlite3.Row  # Permite obtener resultados como diccionarios
    return conn

# Ruta para la página principal que servirá el archivo HTML
@app.route('/')
def index():
    return render_template('index.html')  # Asegúrate de que tu archivo HTML esté en la carpeta 'templates'

# Ruta para buscar el Pokémon y mostrar detalles
@app.route('/buscar')
def buscar_pokemon():
    query = request.args.get('query', '').lower()
    print(f"Consulta recibida: {query}")  # Para depuración
    if query:
        conn = get_db_connection()
        pokemon = conn.execute('SELECT name FROM pokemon WHERE lower(name) = ?', (query,)).fetchone()
        conn.close()

        if pokemon:
            print(f"Pokémon encontrado: {pokemon['name']}")  # Para depuración
            return jsonify({'name': pokemon['name']})
        else:
            print("Pokémon no encontrado")  # Para depuración
            return jsonify({'error': 'Pokémon no encontrado'}), 404
    print("Búsqueda vacía")  # Para depuración
    return jsonify({'error': 'Búsqueda vacía'}), 400



@app.route('/pokemon/<name>')
def mostrar_pokemon(name):
    conn = get_db_connection()
    pokemon = conn.execute('SELECT * FROM pokemon WHERE lower(name) = ?', (name.lower(),)).fetchone()
    conn.close()

    if pokemon:
        return render_template('pokemon.html', 
                               pokemon_name=pokemon['name'],
                               pokemon_weight=pokemon['weight'],
                               pokemon_height=pokemon['height'],
                               pokemon_hp=pokemon['hp'],
                               pokemon_atk=pokemon['atk'],
                               pokemon_def=pokemon['def'],
                               pokemon_satk=pokemon['satk'],
                               pokemon_sdef=pokemon['sdef'],
                               pokemon_spe=pokemon['spe'],
                               pokemon_total_stat=pokemon['total_stat'],
                               pokemon_sprite=pokemon['sprite']
                               )
    else:
        return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
