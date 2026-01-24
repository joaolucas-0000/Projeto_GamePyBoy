#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Validação de instalação - Verifica se tudo está configurado corretamente
"""

import sys
import os
import json
from pathlib import Path


class InstallationValidator:
    """Validar instalação do projeto."""
    
    def __init__(self):
        """Inicializar validador."""
        self.errors = []
        self.warnings = []
        self.info = []
        self.checks_passed = 0
        self.checks_total = 0
    
    def check_python_version(self) -> bool:
        """Verificar versão do Python."""
        self.checks_total += 1
        
        required = (3, 10)
        current = sys.version_info[:2]
        
        if current >= required:
            self.checks_passed += 1
            self.info.append(f"✓ Python {current[0]}.{current[1]} (mínimo: {required[0]}.{required[1]})")
            return True
        else:
            self.errors.append(f"Python {current[0]}.{current[1]} é muito antigo (mínimo: {required[0]}.{required[1]})")
            return False
    
    def check_virtual_env(self) -> bool:
        """Verificar se está em um ambiente virtual."""
        self.checks_total += 1
        
        in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
        
        if in_venv:
            self.checks_passed += 1
            self.info.append("✓ Ambiente virtual ativo")
            return True
        else:
            self.warnings.append("⚠ Nenhum ambiente virtual detectado (recomendado)")
            return False
    
    def check_required_packages(self) -> bool:
        """Verificar se packages necessários estão instalados."""
        self.checks_total += 1
        
        required = {
            'pyboy': 'PyBoy',
            'pygame': 'Pygame',
            'PIL': 'Pillow',
            'numpy': 'NumPy',
        }
        
        missing = []
        for module, name in required.items():
            try:
                __import__(module)
            except ImportError:
                missing.append(name)
        
        if not missing:
            self.checks_passed += 1
            self.info.append(f"✓ Todos os packages instalados ({len(required)} packages)")
            return True
        else:
            self.errors.append(f"Packages faltando: {', '.join(missing)}")
            return False
    
    def check_project_files(self) -> bool:
        """Verificar estrutura de arquivos."""
        self.checks_total += 1
        
        required_files = [
            'main.py',
            'controls.py',
            'utils.py',
            'examples.py',
            'test_emulator.py',
            'setup.py',
            'requirements.txt',
            'config.example.json',
            'README.md',
            'LICENSE',
            '.gitignore',
        ]
        
        missing = []
        for file in required_files:
            if not Path(file).exists():
                missing.append(file)
        
        if not missing:
            self.checks_passed += 1
            self.info.append(f"✓ Estrutura de arquivos OK ({len(required_files)} arquivos)")
            return True
        else:
            self.errors.append(f"Arquivos faltando: {', '.join(missing)}")
            return False
    
    def check_directories(self) -> bool:
        """Verificar diretórios necessários."""
        self.checks_total += 1
        
        required_dirs = [
            'assets',
            'assets/screenshots',
            'assets/states',
        ]
        
        missing = []
        for dir_path in required_dirs:
            if not Path(dir_path).exists():
                missing.append(dir_path)
        
        if not missing:
            self.checks_passed += 1
            self.info.append(f"✓ Diretórios criados ({len(required_dirs)} dirs)")
            return True
        else:
            self.warnings.append(f"Diretórios faltando: {', '.join(missing)} (serão criados automaticamente)")
            return False
    
    def check_config_file(self) -> bool:
        """Verificar arquivo de configuração."""
        self.checks_total += 1
        
        config_exists = Path('config.example.json').exists()
        config_valid = False
        
        if config_exists:
            try:
                with open('config.example.json', 'r', encoding='utf-8') as f:
                    config = json.load(f)
                
                required_keys = ['window_scale', 'fps', 'volume']
                if all(key in config for key in required_keys):
                    config_valid = True
            except json.JSONDecodeError:
                pass
        
        if config_valid:
            self.checks_passed += 1
            self.info.append("✓ Arquivo de configuração válido")
            return True
        else:
            self.warnings.append("⚠ Arquivo config.example.json não encontrado ou inválido")
            return False
    
    def check_requirements_file(self) -> bool:
        """Verificar arquivo requirements.txt."""
        self.checks_total += 1
        
        if not Path('requirements.txt').exists():
            self.errors.append("requirements.txt não encontrado")
            return False
        
        try:
            with open('requirements.txt', 'r', encoding='utf-8') as f:
                lines = [l.strip() for l in f if l.strip() and not l.startswith('#')]
            
            if len(lines) >= 4:  # mínimo de packages
                self.checks_passed += 1
                self.info.append(f"✓ requirements.txt válido ({len(lines)} packages)")
                return True
            else:
                self.errors.append("requirements.txt com muito poucos packages")
                return False
        except Exception as e:
            self.errors.append(f"Erro ao ler requirements.txt: {e}")
            return False
    
    def run_all_checks(self) -> None:
        """Executar todas as verificações."""
        self.check_python_version()
        self.check_virtual_env()
        self.check_required_packages()
        self.check_project_files()
        self.check_directories()
        self.check_config_file()
        self.check_requirements_file()
    
    def print_report(self) -> None:
        """Imprimir relatório de validação."""
        print("\n" + "="*60)
        print("✅ VALIDAÇÃO DE INSTALAÇÃO")
        print("="*60)
        
        # Informações
        if self.info:
            print("\n📋 INFORMAÇÕES:")
            for msg in self.info:
                print(f"  {msg}")
        
        # Aviso
        if self.warnings:
            print("\n⚠️  AVISOS:")
            for msg in self.warnings:
                print(f"  {msg}")
        
        # Erros
        if self.errors:
            print("\n❌ ERROS:")
            for msg in self.errors:
                print(f"  {msg}")
        
        # Resumo
        print("\n" + "-"*60)
        print(f"RESUMO: {self.checks_passed}/{self.checks_total} verificações passaram")
        
        if self.checks_passed == self.checks_total and not self.errors:
            print("\n✅ INSTALAÇÃO COMPLETA E FUNCIONAL!")
            print("\nPróximos passos:")
            print("  1. python main.py            (executar emulador)")
            print("  2. python examples.py        (ver exemplos)")
            print("  3. python test_emulator.py   (rodar testes)")
            print("  4. Ler README.md ou QUICKSTART.md")
        
        elif not self.errors:
            print("\n⚠️  AVISOS CORRIGÍVEIS - Tudo funcionará, mas recomenda-se resolver avisos")
        else:
            print("\n❌ ERROS CRÍTICOS - Instale dependências com:")
            print("  pip install -r requirements.txt")
        
        print("="*60 + "\n")


def main():
    """Função principal."""
    validator = InstallationValidator()
    validator.run_all_checks()
    validator.print_report()
    
    # Retornar código de saída apropriado
    if validator.errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
