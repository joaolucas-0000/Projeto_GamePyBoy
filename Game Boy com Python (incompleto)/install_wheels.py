#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de instalação rápida - Evita problemas de compilação no Windows
Usa apenas wheels pré-compilados (--only-binary)
"""

import subprocess
import sys
import platform


def run_command(cmd):
    """Executar comando e retornar resultado."""
    print(f"→ {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0


def install_with_wheels():
    """Instalar dependências usando apenas wheels pré-compilados."""
    
    print("\n" + "="*60)
    print("🎮 INSTALADOR RÁPIDO - PyBoy Emulator")
    print("Usando apenas wheels (sem compilação)")
    print("="*60 + "\n")
    
    # Atualizar pip
    print("📦 Atualizando pip...")
    if not run_command(f"{sys.executable} -m pip install --upgrade pip"):
        print("⚠ Erro ao atualizar pip (continuando...)")
    
    print("\n📦 Instalando dependências com wheels...\n")
    
    # Instalar cada package com --only-binary para evitar compilação
    packages = [
        "pygame==2.5.2",
        "pyboy==1.4.11",
        "pillow==10.1.0",
        "numpy==1.26.0",
    ]
    
    for package in packages:
        print(f"  Instalando {package}...")
        cmd = f'{sys.executable} -m pip install --only-binary :all: "{package}"'
        if not run_command(cmd):
            print(f"  ⚠ Falha ao instalar {package}, tentando sem --only-binary...")
            cmd = f'{sys.executable} -m pip install "{package}"'
            if not run_command(cmd):
                print(f"  ✗ ERRO: Não foi possível instalar {package}")
                return False
    
    print("\n✅ Todas as dependências instaladas com sucesso!\n")
    return True


def main():
    """Função principal."""
    success = install_with_wheels()
    
    if success:
        print("="*60)
        print("✅ INSTALAÇÃO COMPLETA!")
        print("="*60)
        print("\nPróximas etapas:\n")
        print("1. Testar instalação:")
        print(f"   {sys.executable} validate.py\n")
        print("2. Rodar emulador:")
        print(f"   {sys.executable} main.py path/to/game.gb\n")
        print("3. Ver exemplos:")
        print(f"   {sys.executable} examples.py\n")
        sys.exit(0)
    else:
        print("="*60)
        print("❌ ERRO NA INSTALAÇÃO")
        print("="*60)
        print("\nTente os seguintes passos manual:")
        print("1. pip install --upgrade pip")
        print("2. pip install pygame==2.5.2 --only-binary :all:")
        print("3. pip install -r requirements.txt")
        sys.exit(1)


if __name__ == "__main__":
    main()
