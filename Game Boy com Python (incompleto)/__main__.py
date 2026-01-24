#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Game Boy Emulator - Main Entry Point
Execute: python -m pyboy_emulator
"""

import sys
import os

# Adicionar diretório do projeto ao path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(project_root, 'src'))

# Importar Flask app do web server
from web.web_server import app

if __name__ == '__main__':
    print("=" * 60)
    print("  Game Boy Emulator - Web Interface")
    print("  Servidor rodando em: http://127.0.0.1:5000")
    print("=" * 60)
    print()
    app.run(host='127.0.0.1', port=5000, debug=False)
