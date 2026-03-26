from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os

sys.path.append(os.path.dirname(__file__))
from puzzle_lineal import buscar_solucion_DFS

app = Flask(__name__)
CORS(app)

@app.route('/resolver', methods=['POST'])
def resolver_puzzle():
    try:
        data = request.get_json()
        estado_inicial = data.get('estado_inicial', [4, 2, 3, 1])
        solucion = data.get('solucion', [1, 2, 3, 4])
        
        print(f" Resolviendo: {estado_inicial} -> {solucion}")
        
        nodo_solucion = buscar_solucion_DFS(estado_inicial, solucion)
        
        if nodo_solucion is None:
            return jsonify({
                'success': False,
                'error': 'No se encontró solución'
            }), 404
        
        resultado = []
        nodo = nodo_solucion
        while nodo.get_padre() is not None:
            resultado.append(nodo.get_datos())
            nodo = nodo.get_padre()
        resultado.append(estado_inicial)
        resultado.reverse()
        
        return jsonify({
            'success': True,
            'estado_inicial': estado_inicial,
            'estado_final': solucion,
            'ruta': resultado,
            'pasos': len(resultado) - 1
        })
        
    except Exception as e:
        print(f" Error: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print(" Servidor iniciado en http://localhost:5000")
    app.run(debug=True, port=5000)