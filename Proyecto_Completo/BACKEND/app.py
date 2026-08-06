import os
import subprocess
import sys

# Generar Prisma client si no existe
if not os.path.exists(".prisma/client"):
    print("⚙️ Generando cliente Prisma...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "prisma", "generate"],
            timeout=120
        )
        if result.returncode != 0:
            print("❌ Error generando Prisma")
            sys.exit(1)
        print("✓ Cliente Prisma generado")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

# Ahora importar Flask y otros módulos
from flask import Flask
from flask_cors import CORS

from db import db
from routes.transaccion_routes import transaccion_bp

app = Flask(__name__)
CORS(app)

db.connect()

app.register_blueprint(transaccion_bp, url_prefix="/api/transacciones")


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
