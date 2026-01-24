#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de instalação do projeto PyBoy Emulator
Configura ambiente virtual e instala dependências
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def run_command(cmd: str, description: str = "") -> bool:
    """
    Executar comando no shell.
    
    Args:
        cmd: Comando a executar
        description: Descrição do que está sendo feito
        
    Returns:
        True se sucesso, False se erro
    """
    if description:
        print(f"\n📦 {description}...")
    
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Erro: {e.stderr}")
        return False


def setup_venv() -> bool:
    """
    Criar ambiente virtual.
    
    Returns:
        True se sucesso
    """
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print("✓ Ambiente virtual já existe")
        return True
    
    return run_command(f"{sys.executable} -m venv .venv", "Criando ambiente virtual")


def get_activation_command() -> str:
    """
    Obter comando para ativar venv baseado no SO.
    
    Returns:
        Comando de ativação
    """
    if platform.system() == "Windows":
        return r".\\.venv\\Scripts\\Activate.ps1"
    else:
        return "source .venv/bin/activate"


def install_requirements() -> bool:
    """
    Instalar dependências.
    
    Returns:
        True se sucesso
    """
    if platform.system() == "Windows":
        activate_cmd = r".\\.venv\\Scripts\\pip"
    else:
        activate_cmd = ".venv/bin/pip"
    
    # Upgrade pip
    if not run_command(f"{activate_cmd} install --upgrade pip", "Atualizando pip"):
        return False
    
    # Instalar requirements
    if not run_command(f"{activate_cmd} install -r requirements.txt", "Instalando dependências"):
        return False
    
    return True


def create_directories() -> None:
    """Criar estrutura de diretórios necessária."""
    directories = [
        "assets/screenshots",
        "assets/states",
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
    
    print("✓ Diretórios criados")


def copy_config() -> None:
    """Copiar arquivo de configuração exemplo."""
    if not Path("config.json").exists() and Path("config.example.json").exists():
        import shutil
        shutil.copy("config.example.json", "config.json")
        print("✓ Arquivo config.json criado (baseado em config.example.json)")


def run_tests() -> bool:
    """
    Executar testes.
    
    Returns:
        True se sucesso
    """
    if platform.system() == "Windows":
        cmd = r".\\.venv\\Scripts\\python test_emulator.py"
    else:
        cmd = ".venv/bin/python test_emulator.py"
    
    return run_command(cmd, "Executando testes")


def print_next_steps() -> None:
    """Imprimir próximos passos."""
    system = platform.system()
    
    if system == "Windows":
        activate_cmd = r".\\.venv\\Scripts\\Activate.ps1"
        run_cmd = r".\\.venv\\Scripts\\python main.py"
    else:
        activate_cmd = "source .venv/bin/activate"
        run_cmd = ".venv/bin/python main.py"
    
    print("\n" + "="*60)
    print("✓ INSTALAÇÃO CONCLUÍDA!")
    print("="*60)
    print(f"""
Próximos passos:

1. Ativar ambiente virtual:
   {activate_cmd}

2. Executar o emulador:
   {run_cmd} path\\\\to\\\\game.gb

   Ou usar o diálogo interativo:
   {run_cmd}

3. Listar controles:
   Pressione 'H' dentro do emulador

4. Ver informações de ROMs:
   {'.venv\\\\Scripts\\\\python' if system == 'Windows' else '.venv/bin/python'} utils.py

Documentação: Veja README.md para mais detalhes
""")


def main():
    """Função principal de instalação."""
    print("\n" + "="*60)
    print("🎮 INSTALADOR - Game Boy Emulator com PyBoy")
    print("="*60)
    
    # Verificar Python version
    if sys.version_info < (3, 10):
        print("✗ Python 3.10+ é necessário")
        sys.exit(1)
    
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detectado")
    
    # Passos de instalação
    steps = [
        ("setup_venv", "Ambiente virtual", setup_venv),
        ("install_requirements", "Dependências", install_requirements),
        ("create_directories", "Diretórios", create_directories),
        ("copy_config", "Configuração", copy_config),
    ]
    
    for step_id, step_name, step_func in steps:
        try:
            if not step_func():
                print(f"✗ Erro em: {step_name}")
                sys.exit(1)
        except Exception as e:
            print(f"✗ Erro inesperado em {step_name}: {e}")
            sys.exit(1)
    
    # Executar testes (opcional)
    print("\n" + "-"*60)
    response = input("Deseja executar os testes? (s/n): ").lower()
    if response in ('s', 'sim', 'y', 'yes'):
        run_tests()
    
    # Próximos passos
    print_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Instalação cancelada pelo usuário")
        sys.exit(1)
