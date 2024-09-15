from flask import Flask, request, jsonify, render_template, url_for, redirect
from openai import OpenAI

full_response = ""

app = Flask(__name__)

client = OpenAI(
    api_key="-",
    base_url="https://fridaplatform.com/v1"
)

"""Codigo prueba"""
"""@app.route('/respuesta') 
def respuesta(): 
    return render_template('index.html', texto=full_response)"""

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar', methods=['POST'])
def recibir_texto():
    data = request.get_json()
    promtext = data.get('promtext', '')
    print('Texto recibido:', promtext)  # Muestra el texto recibido en la terminal
    
    # Realiza la solicitud a OpenAI
    response = client.chat.completions.create(
        model="tgi",
        messages=[
            {"role": "system", "content": "Eres una asistente de reposteria"},
            {"role": "user", "content": promtext}
        ],
        stream=True
    )

    # Itera sobre el flujo para mostrar la respuesta
    for chunk in response:
        if hasattr(chunk.choices[0].delta, 'content'):
            content = chunk.choices[0].delta.content
            full_response += content

    print("\n\nRespuesta completa:")  # Muestra la respuesta completa en la terminal
    print(full_response)

    """return jsonify({'status': 'success', 'received_text': promtext, 'full_response': full_response})"""
    """return redirect(url_for('respuesta', texto=full_response))"""
    """return redirect(url_for('respuesta'))"""


if __name__ == '__main__':
    app.run(debug=True)
