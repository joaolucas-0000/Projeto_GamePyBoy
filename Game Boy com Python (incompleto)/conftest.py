"""
Configuração de testes e resolução de imports para pytest e Pylance
"""

import sys
import os

# Adicionar src ao path de forma que o Pylance consiga resolver
project_root = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(project_root, 'src')

if src_path not in sys.path:
    sys.path.insert(0, src_path)
