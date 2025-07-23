from flask import Flask, render_template
from flask_cors import CORS
import os
import sys

# Adicionar o diretório raiz ao path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Criar a aplicação Flask
app = Flask(__name__, static_folder='static', template_folder='static')
CORS(app)

# Importar as rotas
from routes.mercos_v3 import mercos_v3_bp

# Registrar blueprints
app.register_blueprint(mercos_v3_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

