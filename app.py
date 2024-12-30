from flask import Flask, request, jsonify
from impostos import calcular_impostos

app = Flask(__name__)

@app.route('/calcular_impostos', methods=['POST'])
def calcular_impostos_view():
    try:
        dados = request.get_json()
        
        valor_base = dados['valor_base']
        estado = dados['estado']
        tipo_produto = dados['tipo_produto']
        ncm = dados['ncm']

        resultados = calcular_impostos(valor_base, estado, tipo_produto, ncm)

        return jsonify(resultados)
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
