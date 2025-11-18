from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI

app = Flask(__name__)
CORS(app)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/analise", methods=["POST"])
def analise():
    data = request.json

    print("=== JSON RECEBIDO ===")
    print(data)

    texto = data.get("texto")
    imagem = data.get("imagem")

    try:
        if texto:
            mensagens = [
                {"role": "user", "content": texto}
            ]

        elif imagem:
            print("=== TAMANHO DA IMAGEM BASE64 ===", len(imagem))

            mensagens = [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analise a imagem enviada."},
                        {"type": "image_url", "image_url": {"url": imagem}}
                    ]
                }
            ]

        else:
            return jsonify({"erro": "Nenhum texto ou imagem enviado"}), 400

        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=mensagens
        )

        return jsonify({"resultado": resp.choices[0].message["content"]})

    except Exception as e:
        print("=== ERRO OPENAI ===")
        print(e)
        return jsonify({"erro": str(e)}), 500


if __name__ == "__main__":
    app.run(port=5000)
