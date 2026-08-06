#!/usr/bin/env python
import subprocess
import sys
import os

# Generar Prisma client si no existe
if not os.path.exists(".prisma/client"):
    print("⚙️ Generando cliente Prisma...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "prisma", "generate"],
            timeout=120,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print("❌ Error generando Prisma:", result.stderr)
        else:
            print("✓ Cliente Prisma generado")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

# Ejecutar la aplicación Flask
print("🚀 Iniciando Flask...")
os.execvp("python", ["python", "app.py"])
