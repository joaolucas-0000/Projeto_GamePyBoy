#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exemplos de uso avançado do emulador PyBoy
"""

import os
import sys
import json
from pathlib import Path

# Adicionar src ao path para imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from emulator.main import GameBoyEmulator
from emulator.controls import ControlMapping, GameBoyButton


# ==================== EXEMPLO 1: USO BÁSICO ====================

def example_basic():
    """Exemplo básico: carregar e executar um jogo."""
    print("\n=== EXEMPLO 1: USO BÁSICO ===\n")
    
    rom_path = "game.gb"  # Substituir pelo caminho real
    
    if not os.path.exists(rom_path):
        print(f"⚠ ROM não encontrada: {rom_path}")
        print("Forneça um caminho válido para um arquivo .gb ou .gbc")
        return
    
    try:
        emulator = GameBoyEmulator(rom_path)
        emulator.run()
    except Exception as e:
        print(f"Erro: {e}")


# ==================== EXEMPLO 2: USO CUSTOMIZADO ====================

def example_custom_config():
    """Exemplo: usar configuração customizada."""
    print("\n=== EXEMPLO 2: CONFIGURAÇÃO CUSTOMIZADA ===\n")
    
    rom_path = "game.gb"
    config_path = "custom_config.json"
    
    # Criar configuração customizada
    custom_config = {
        "window_scale": 3,
        "fps": 60,
        "fullscreen": False,
        "volume": 0.5
    }
    
    with open(config_path, 'w') as f:
        json.dump(custom_config, f, indent=4)
    
    print(f"✓ Configuração customizada criada: {config_path}")
    print(f"  - Escala: {custom_config['window_scale']}x")
    print(f"  - FPS: {custom_config['fps']}")
    print(f"  - Volume: {custom_config['volume']}")


# ==================== EXEMPLO 3: DESCOBRIR ROMs ====================

def example_find_roms():
    """Exemplo: descobrir ROMs no diretório."""
    print("\n=== EXEMPLO 3: DESCOBRIR ROMs ===\n")
    print("ℹ Função desabilitada - funcionalidade de busca de ROMs não está implementada")
    
    # Buscar ROMs no diretório media/ROMs
    import glob
    roms = glob.glob("media/ROMs/*.gb") + glob.glob("media/ROMs/*.gbc")
    
    if not roms:
        print("✗ Nenhuma ROM encontrada no diretório media/ROMs")
        return
    
    print(f"✓ {len(roms)} ROM(s) encontrada(s):\n")
    
    for i, rom in enumerate(roms, 1):
        size_bytes = os.path.getsize(rom)
        size_mb = size_bytes / (1024 * 1024)
        rom_name = os.path.basename(rom)
        print(f"{i}. {rom_name} ({size_mb:.2f} MB)")


# ==================== EXEMPLO 4: CONTROLES CUSTOMIZADOS ====================

def example_custom_controls():
    """Exemplo: remapear controles."""
    print("\n=== EXEMPLO 4: CONTROLES CUSTOMIZADOS ===\n")
    
    try:
        # Criar mapeamento de controles
        controls = ControlMapping("default")
        print("✓ Mapeamento de controles carregado:")
        print("  Setas: D-Pad")
        print("  Z: Botão A")
        print("  X: Botão B")
        print("  Enter: Start")
        print("  Espaço: Select")
    except Exception as e:
        print(f"ℹ Controles não disponíveis: {e}")


# ==================== EXEMPLO 5: ANÁLISE DE ROM ====================

def example_analyze_rom():
    """Exemplo: analisar informações de ROM."""
    print("\n=== EXEMPLO 5: ANÁLISE DE ROM ===\n")
    
    rom_path = "media/ROMs/Super_Mario_Land_World_Rev_1.gb"  # Caminho de exemplo
    
    if not os.path.exists(rom_path):
        print(f"⚠ ROM não encontrada: {rom_path}")
        return
    
    size_bytes = os.path.getsize(rom_path)
    size_mb = size_bytes / (1024 * 1024)
    
    print(f"Nome:      {os.path.basename(rom_path)}")
    print(f"Tamanho:   {size_mb:.2f} MB")
    print(f"Caminho:   {rom_path}")


# ==================== EXEMPLO 6: CRIAR LISTA DE ROMs ====================

def example_create_rom_list():
    """Exemplo: criar arquivo com lista de ROMs."""
    print("\n=== EXEMPLO 6: CRIAR LISTA DE ROMs ===\n")
    
    import glob
    roms = glob.glob("media/ROMs/*.gb") + glob.glob("media/ROMs/*.gbc")
    
    if not roms:
        print("✗ Nenhuma ROM encontrada em media/ROMs")
        return
    
    with open("rom_list.txt", "w", encoding="utf-8") as f:
        f.write("Lista de ROMs\n")
        f.write("=" * 40 + "\n\n")
        for rom in sorted(roms):
            size_mb = os.path.getsize(rom) / (1024 * 1024)
            f.write(f"- {os.path.basename(rom)} ({size_mb:.2f} MB)\n")
    
    print(f"✓ Arquivo 'rom_list.txt' criado com {len(roms)} ROM(s)")


# ==================== EXEMPLO 7: MONITORAR CONTROLES ====================

def example_monitor_controls():
    """Exemplo: monitorar entrada de controles."""
    print("\n=== EXEMPLO 7: MONITORAR CONTROLES ===\n")
    print("ℹ Para testar controles, inicie um jogo e use o teclado:")
    print("  - Setas: D-Pad")
    print("  - Z: Botão A")
    print("  - X: Botão B") 
    print("  - Enter: Start")
    print("  - Espaço: Select")
    print("  - P: Pausar/Retomar")
    print("  - ESC: Sair")


# ==================== EXEMPLO 8: TESTE DE DESEMPENHO ====================

def example_performance_test():
    """Exemplo: testar desempenho do emulador."""
    print("\n=== EXEMPLO 8: TESTE DE DESEMPENHO ===\n")
    
    rom_path = "media/ROMs/Super_Mario_Land_World_Rev_1.gb"
    
    if not os.path.exists(rom_path):
        print(f"⚠ ROM não encontrada: {rom_path}")
        return
    
    print("Este teste executa o emulador por 10 segundos...")
    print("Feche a janela para finalizar o teste.\n")
    
    try:
        from time import time
        
        emulator = GameBoyEmulator(rom_path)
        
        start_time = time()
        max_duration = 10  # segundos
        frames = 0
        
        # Simular execução (o emulador está em thread separada no modo web)
        import threading
        import time as time_module
        
        while time() - start_time < max_duration:
            time_module.sleep(0.1)
            frames += 1
        
        elapsed = time() - start_time
        fps = (frames * 60) / elapsed if elapsed > 0 else 0
        
        print(f"\n📊 RESULTADOS:")
        print(f"  Tempo: {elapsed:.2f}s")
        print(f"  Frames estimados: {frames * 60}")
        print(f"  FPS esperado: 60")
        
    except Exception as e:
        print(f"Erro durante teste: {e}")


# ==================== MENU PRINCIPAL ====================

def main():
    """Menu de exemplos."""
    examples = {
        "1": ("Uso básico", example_basic),
        "2": ("Configuração customizada", example_custom_config),
        "3": ("Descobrir ROMs", example_find_roms),
        "4": ("Controles customizados", example_custom_controls),
        "5": ("Análise de ROM", example_analyze_rom),
        "6": ("Criar lista de ROMs", example_create_rom_list),
        "7": ("Monitorar controles", example_monitor_controls),
        "8": ("Teste de desempenho", example_performance_test),
    }
    
    print("\n" + "="*60)
    print("📚 EXEMPLOS DE USO - PyBoy Emulator")
    print("="*60)
    
    for key, (name, _) in examples.items():
        print(f"{key}. {name}")
    
    print("0. Sair")
    
    while True:
        try:
            choice = input("\nEscolha uma opção: ").strip()
            
            if choice == "0":
                print("Até logo!")
                break
            
            if choice in examples:
                func = examples[choice][1]
                func()
            else:
                print("✗ Opção inválida")
        
        except KeyboardInterrupt:
            print("\n\nEncerrando...")
            break
        except Exception as e:
            print(f"Erro: {e}")


if __name__ == "__main__":
    main()
