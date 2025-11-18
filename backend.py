from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI
import os
import base64

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/analise", methods=["POST"])
def analise():
    data = request.json

    # Se veio texto
    if "texto" in data:
        prompt = data["texto"]

    # Se veio imagem base64
    elif "imagem" in data:
        prompt = f"Descreva o conteúdo desta imagem em detalhes:\nIMAGEM(base64): {data['imagem']}"

    else:
        return jsonify({"erro": "Nenhum texto ou imagem enviado"}), 400

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        resultado = response.choices[0].message["content"]
        return jsonify({"resultado": resultado})

    except Exception as e:
        print(e)
        return jsonify({"erro": str(e)}), 500



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

