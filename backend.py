from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)  # permite requisições de qualquer origem (front-end)

# Configure sua chave como variável de ambiente
# export OPENAI_API_KEY="sua_chave_aqui"
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/analise", methods=["POST"])
def analise():
    data = request.json
    texto = data.get("texto", "")

    if not texto:
        return jsonify({"erro": "Nenhum texto enviado"}), 400

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": texto}]
        )
        resultado = response.choices[0].message.content
        return jsonify({"resultado": resultado})
    except Exception as e:
        print(e)
        return jsonify({"erro": "Erro ao chamar a API"}), 500

if __name__ == "__main__":
    app.run(port=5000)
