import os
import random 
import sqlite3
from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Función para conectar a la base de datos
def get_db_connection():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'PokeSearch.sqlite3')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Permite obtener resultados como diccionarios
    return conn

# Diccionario que mapea los tipos a colores pastel
tipo_colores = {
    'electric': '#FFEB3B',  # amarillo pastel
    'fire': '#FF8A65',  # rojo pastel
    'water': '#64B5F6',  # azul pastel
    'grass': '#81C784',  # verde claro pastel
    'ice': '#81D4FA',  # azul claro pastel
    'fighting': '#FFAB91',  # marrón claro pastel
    'poison': '#CE93D8',  # púrpura pastel
    'ground': '#D7CCC8',  # beige pastel
    'flying': '#B3E5FC',  # celeste pastel
    'psychic': '#FFC1E3',  # rosa pastel
    'bug': '#C5E1A5',  # verde pastel
    'rock': '#A1887F',  # marrón claro pastel
    'ghost': '#B39DDB',  # índigo pastel
    'dragon': '#7986CB',  # azul oscuro pastel
    'dark': '#90A4AE',  # gris claro pastel
    'steel': '#CFD8DC',  # gris muy claro
    'fairy': '#F48FB1',  # rosa claro pastel
}

# Diccionario que mapea los tipos a emojis
tipo_emojis = {
    'electric': '⚡',  
    'fire': '🔥',  
    'water': '💧',  
    'grass': '🌿',  
    'ice': '❄️',  
    'fighting': '🥊',  
    'poison': '☠️',  
    'ground': '🌍',  
    'flying': '🌬️',  
    'psychic': '🔮',  
    'bug': '🐛',  
    'rock': '🪨',  
    'ghost': '👻',  
    'dragon': '🐉',  
    'dark': '🌑',  
    'steel': '🔩',  
    'fairy': '✨',
}

# Ruta para la página principal que muestra 6 Pokémon aleatorios
@app.route('/')
def index():
    conn = get_db_connection()
    
    # Seleccionar 6 IDs aleatorios de Pokémon en el rango de 1 a 905
    random_ids = random.sample(range(1, 906), 6)
    
    # Obtener la información de los 6 Pokémon seleccionados
    random_pokemon = conn.execute(
        'SELECT * FROM pokemon WHERE id IN (?, ?, ?, ?, ?, ?)',
        random_ids
    ).fetchall()
    
    # Crear una lista para almacenar la información de los Pokémon
    pokemon_list = []
    for pokemon in random_pokemon:
        # Obtener los tipos del Pokémon
        tipos_pokemon = conn.execute('''
            SELECT tipe.name FROM pok_typ
            JOIN tipe ON pok_typ.id_type = tipe.id
            WHERE pok_typ.id_pokemon = ?
        ''', (pokemon['id'],)).fetchall()
        
        # Convertir los tipos en una lista
        tipos = [tipo['name'] for tipo in tipos_pokemon]
        
        # Tomar el color basado en el primer tipo
        pokemon_card_color = tipo_colores.get(tipos[0], '#FFF')
        
        # Añadir la información del Pokémon a la lista
        pokemon_list.append({
            'name': pokemon['name'],
            'id': pokemon['id'],
            'weight': pokemon['weight'],
            'height': pokemon['height'],
            'hp': pokemon['hp'],
            'atk': pokemon['atk'],
            'def': pokemon['def'],
            'satk': pokemon['satk'],
            'sdef': pokemon['sdef'],
            'spe': pokemon['spe'],
            'total_stat': pokemon['total_stat'],
            'sprite': pokemon['sprite'],
            'types': tipos,
            'card_color': pokemon_card_color
        })
    
    conn.close()

    return render_template('index.html', 
                            pokemon_list=pokemon_list, 
                            tipo_emojis=tipo_emojis,
                            tipo_colores=tipo_colores,)

# Ruta para buscar un Pokémon y mostrar los detalles
@app.route('/pokemon/<name>')
def detalle_pokemon(name):
    conn = get_db_connection()
    pokemon = conn.execute('SELECT * FROM pokemon WHERE lower(name) = ?', (name.lower(),)).fetchone()
    
    # Obtener tipos del Pokémon
    tipos_pokemon = conn.execute('''
        SELECT tipe.name FROM pok_typ
        JOIN tipe ON pok_typ.id_type = tipe.id
        WHERE pok_typ.id_pokemon = ?
    ''', (pokemon['id'],)).fetchall()

    conn.close()

    # Convertir los tipos en una lista
    tipos = [tipo['name'] for tipo in tipos_pokemon]

    # Tomar el color basado en el primer tipo
    pokemon_card_color = tipo_colores.get(tipos[0], '#FFF')

    return render_template('pokemon.html',
                           pokemon_name=pokemon['name'],
                           pokemon_id=pokemon['id'],
                           pokemon_weight=pokemon['weight'],
                           pokemon_height=pokemon['height'],
                           pokemon_hp=pokemon['hp'],
                           pokemon_atk=pokemon['atk'],
                           pokemon_def=pokemon['def'],
                           pokemon_satk=pokemon['satk'],
                           pokemon_sdef=pokemon['sdef'],
                           pokemon_spe=pokemon['spe'],
                           pokemon_total_stat=pokemon['total_stat'],
                           pokemon_sprite=pokemon['sprite'],
                           pokemon_types=tipos,
                           pokemon_card_color=pokemon_card_color,
                           tipo_emojis=tipo_emojis
                           )

# Ruta para buscar Pokémon por nombre
@app.route('/buscar')
def buscar_pokemon():
    query = request.args.get('query', '').lower()
    if query:
        conn = get_db_connection()
        pokemon = conn.execute('SELECT name FROM pokemon WHERE lower(name) = ?', (query,)).fetchone()
        conn.close()

        if pokemon:
            return jsonify({'name': pokemon['name']})
        else:
            return jsonify({'error': 'Pokémon no encontrado'}), 404
    return jsonify({'error': 'Búsqueda vacía'}), 400


# Ruta para obtener 6 Pokémon adicionales de forma aleatoria
@app.route('/mas_pokemon')
def random_pokemon():
    conn = get_db_connection()
    
    # Seleccionar 6 Pokémon aleatorios
    random_ids = random.sample(range(1, 906), 6)
    
    # Obtener la información de los 6 Pokémon seleccionados
    random_pokemon = conn.execute(
        'SELECT * FROM pokemon WHERE id IN (?, ?, ?, ?, ?, ?)',
        random_ids
    ).fetchall()
    
    # Crear una lista para almacenar la información de los Pokémon
    pokemon_list = []
    for pokemon in random_pokemon:
        # Obtener los tipos del Pokémon
        tipos_pokemon = conn.execute('''
            SELECT tipe.name FROM pok_typ
            JOIN tipe ON pok_typ.id_type = tipe.id
            WHERE pok_typ.id_pokemon = ?
        ''', (pokemon['id'],)).fetchall()
        
        # Convertir los tipos en una lista
        tipos = [tipo['name'] for tipo in tipos_pokemon]
        
        # Tomar el color basado en el primer tipo
        pokemon_card_color = tipo_colores.get(tipos[0], '#FFF')
        
        # Añadir la información del Pokémon a la lista
        pokemon_list.append({
            'name': pokemon['name'],
            'id': pokemon['id'],
            'weight': pokemon['weight'],
            'height': pokemon['height'],
            'hp': pokemon['hp'],
            'atk': pokemon['atk'],
            'def': pokemon['def'],
            'satk': pokemon['satk'],
            'sdef': pokemon['sdef'],
            'spe': pokemon['spe'],
            'total_stat': pokemon['total_stat'],
            'sprite': pokemon['sprite'],
            'types': tipos,
            'card_color': pokemon_card_color
        })
    
    conn.close()
    
    # Retornar los datos en formato JSON
    return jsonify(pokemon_list)


if __name__ == '__main__':
    app.run(debug=True)
