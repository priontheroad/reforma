# routes/impostos.py
from flask import Blueprint, request, jsonify
from impostos import calcular_impostos_anteriores

# Cria o Blueprint
impostos_bp = Blueprint('impostos', __name__)

@impostos_bp.route('/calcular-impostos', methods=['POST'])
def calcular_impostos():
    try:
        dados = request.get_json()
        
        estado = dados.get('estado')
        tipo_produto = dados.get('tipo_produto')
        ncm = dados.get('ncm')
        valor_base = dados.get('valor_base')

        if not all([estado, tipo_produto, ncm, valor_base]):
            return jsonify({"erro": "Todos os dados são obrigatórios!"}), 400

        valor_base = float(valor_base)
        
        impostos_anteriores = calcular_impostos_anteriores(
            valor_base, estado, tipo_produto, ncm,
            "data/aliquotas_estado.csv", "data/aliquotas_ncm.csv"
        )
        
        return jsonify(impostos_anteriores), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 400
