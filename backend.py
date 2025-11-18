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

    # Verifica se veio arquivo
    if "image" not in request.files:
        return jsonify({"erro": "Nenhuma imagem enviada"}), 400

    image_file = request.files["image"]
    img_bytes = image_file.read()
    img_b64 = base64.b64encode(img_bytes).decode("utf-8")

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "input_image", "image_url": f"data:image/jpeg;base64,{img_b64}"},
                        {
                            "type": "text",
                            "text": "Analise esta estrutura e descreva possíveis danos."
                        },
                    ],
                }
            ],
        )

        resultado = response.choices[0].message["content"]

        return jsonify({"resultado": resultado})

    except Exception as e:
        print("ERRO:", e)
        return jsonify({"erro": "Falha ao chamar a API OpenAI"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
