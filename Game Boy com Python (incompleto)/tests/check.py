#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Validacao rapida de instalacao - PyBoy Emulator
Verifica se o ambiente esta pronto para rodar o emulador
"""

import sys
import os

print("\n" + "="*60)
print("VALIDACAO DE INSTALACAO - PyBoy Emulator")
print("="*60 + "\n")

# 1. Verificar Python
print("1. Verificando Python...")
if sys.version_info >= (3, 10):
    print(f"   OK: Python {sys.version_info.major}.{sys.version_info.minor}")
else:
    print(f"   ERRO: Python {sys.version_info.major}.{sys.version_info.minor} (minimo: 3.10)")
    sys.exit(1)

# 2. Verificar ambiente virtual
print("\n2. Verificando ambiente virtual...")
in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
if in_venv:
    print("   OK: Ambiente virtual ativo")
else:
    print("   AVISO: Sem ambiente virtual (recomendado)")

# 3. Verificar packages
print("\n3. Verificando packages...")
packages = {
    'pyboy': 'PyBoy (emulador)',
    'PIL': 'Pillow (imagens)',
    'numpy': 'NumPy (calculos)',
}

missing = []
for module, name in packages.items():
    try:
        __import__(module)
        print(f"   OK: {name}")
    except ImportError:
        print(f"   ERRO: {name} nao instalado")
        missing.append(module)

if missing:
    print(f"\nERRO: Packages faltando: {', '.join(missing)}")
    print("Execute: pip install -r requirements.txt")
    sys.exit(1)

# 4. Verificar arquivos do projeto
print("\n4. Verificando arquivos do projeto...")
required_files = ['main.py', 'controls.py', 'utils.py', 'requirements.txt']
missing_files = []
for file in required_files:
    if os.path.exists(file):
        print(f"   OK: {file}")
    else:
        print(f"   ERRO: {file} nao encontrado")
        missing_files.append(file)

if missing_files:
    print(f"\nERRO: Arquivos faltando: {', '.join(missing_files)}")
    sys.exit(1)

# 5. Verificar diretórios
print("\n5. Verificando diretorios...")
required_dirs = ['assets', 'assets/screenshots', 'assets/states']
for dir_path in required_dirs:
    if os.path.exists(dir_path):
        print(f"   OK: {dir_path}/")
    else:
        os.makedirs(dir_path, exist_ok=True)
        print(f"   OK: {dir_path}/ (criado)")

print("\n" + "="*60)
print("VALIDACAO CONCLUIDA COM SUCESSO!")
print("="*60)

print("\nPROXIMOS PASSOS:")
print("\n1. Rodar o emulador:")
print("   python main.py path\\to\\game.gb")
print("\n2. Ou usar dialogo interativo:")
print("   python main.py")
print("\n3. Ver exemplos:")
print("   python examples.py")

print("\nCONTROLES:")
print("   Setas: D-Pad")
print("   Z: Botao A, X: Botao B")
print("   ENTER: Start, ESPACO: Select")
print("   ESC: Sair")

print("\n" + "="*60)
print("Emulador pronto para uso!")
print("="*60 + "\n")
