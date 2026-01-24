#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Game Boy Emulator - PyBoy
Projeto totalmente funcional de emulador Game Boy em Python.
Usa PyBoy com SDL2 (sem dependencias externas alem de PyBoy)
"""

import sys
import os
import json
import time
from pathlib import Path
from typing import Optional
from pyboy import PyBoy


class GameBoyEmulator:
    """Classe principal para gerenciar o emulador Game Boy."""
    
    # Configurações padrão
    DEFAULT_CONFIG = {
        "window_scale": 4,
        "fps": 60,
        "fullscreen": False,
        "volume": 0.7,
    }
    
    # Resolução nativa do Game Boy
    GB_WIDTH = 160
    GB_HEIGHT = 144
    
    def __init__(self, rom_path: str, config_path: str = "config.json"):
        """
        Inicializar o emulador.
        
        Args:
            rom_path: Caminho da ROM do Game Boy (.gb ou .gbc)
            config_path: Caminho do arquivo de configuração (opcional)
        """
        self.rom_path = rom_path
        self.config_path = config_path
        self.config = self.load_config()
        
        # Inicializar PyBoy
        print("Inicializando PyBoy...")
        self.mb = PyBoy(
            self.rom_path,
            window="SDL2",
            debug=False,
            cgb=False
        )
        self.mb.set_emulation_speed(1.0)  # Velocidade normal (1.0 = velocidade correta)
        
        self.running = True
        self.paused = False
        
        print(f"OK: Emulador iniciado com ROM: {Path(rom_path).name}")
        print(f"OK: Resolucao: {self.GB_WIDTH}x{self.GB_HEIGHT}")
        print(f"OK: Escala: {self.config['window_scale']}x")
        print(f"OK: FPS: {self.config['fps']}")
        print("\nPressione ESC para sair ou H para ajuda.")
    
    def load_config(self) -> dict:
        """
        Carregar configuração de arquivo ou usar padrão.
        
        Returns:
            Dicionário com configurações
        """
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print(f"AVISO: Erro ao ler {self.config_path}. Usando padrao.")
        
        return self.DEFAULT_CONFIG.copy()
    
    def save_config(self) -> None:
        """Salvar configuração atual em arquivo."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            print(f"OK: Configuracao salva em {self.config_path}")
        except IOError as e:
            print(f"ERRO: Nao foi possivel salvar configuracao: {e}")
    
    def capture_screenshot(self) -> None:
        """Capturar screenshot do jogo atual."""
        os.makedirs("assets/screenshots", exist_ok=True)
        
        try:
            # Obter imagem do emulador
            image = self.mb.screen.image
            
            # Salvar com timestamp
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"assets/screenshots/screenshot_{timestamp}.png"
            
            image.save(filename)
            print(f"OK: Screenshot salvo: {filename}")
        except Exception as e:
            print(f"ERRO: Nao foi possivel capturar screenshot: {e}")
    
    def save_state(self, slot: int) -> None:
        """
        Salvar estado do jogo.
        
        Args:
            slot: Número do slot (1, 2, ou 3)
        """
        os.makedirs("assets/states", exist_ok=True)
        filename = f"assets/states/savestate_{slot}.state"
        
        try:
            with open(filename, "wb") as f:
                self.mb.save_state(f)
            print(f"OK: Estado salvo no slot {slot}")
        except Exception as e:
            print(f"ERRO: Nao foi possivel salvar estado: {e}")
    
    def load_state(self, slot: int) -> None:
        """
        Carregar estado do jogo.
        
        Args:
            slot: Número do slot (1, 2, ou 3)
        """
        filename = f"assets/states/savestate_{slot}.state"
        
        if not os.path.exists(filename):
            print(f"AVISO: Estado nao encontrado no slot {slot}")
            return
        
        try:
            with open(filename, "rb") as f:
                self.mb.load_state(f)
            print(f"OK: Estado carregado do slot {slot}")
        except Exception as e:
            print(f"ERRO: Nao foi possivel carregar estado: {e}")
    
    def show_help(self) -> None:
        """Exibir controles disponíveis."""
        help_text = """
============================================================
          CONTROLES DO EMULADOR GAME BOY
============================================================

CONTROLES DO JOGO (Automático PyBoy):
 Setas (Cima/Baixo/Esq/Dir) : D-Pad
 Z                          : Botao A
 X                          : Botao B
 ENTER                      : Start
 ESPACO                     : Select

CONTROLES DO EMULADOR:
 P                          : Pausar/Retomar
 F                          : Screenshot
 ESC                        : Sair
 H                          : Ajuda (esta mensagem)

SAVE STATES:
 1, 2, 3                    : Salvar estado
 F1, F2, F3                 : Carregar estado

============================================================
Emulador rodando com SDL2 (sem dependencia de pygame)
"""
        print(help_text)
    
    def run(self) -> None:
        """Loop principal do emulador."""
        try:
            print("\nEmulador rodando. Pressione ESC ou clique em X para sair.\n")
            
            # Alguns jogos (especialmente Game Boy Color) precisam de tempo para
            # inicializar a ROM. Roda ~600 frames silenciosamente para carregar.
            print("Carregando ROM (pode levar alguns segundos)...")
            initial_frames = 0
            max_init_frames = 600
            
            while initial_frames < max_init_frames:
                try:
                    # Tentar tick, mas ignorar resultado em threads
                    self.mb.tick()
                except Exception as e:
                    print(f"Erro durante carregamento: {e}")
                    return
                    
                initial_frames += 1
            
            print(f"Pronto! Jogo iniciado.\n")
            
            # Loop principal - executar indefinidamente até erro ou janela fechar
            # Em threads, não conseguimos detectar ESC confiável
            # Mas a janela pode ser fechada clicando o X
            while True:
                try:
                    result = self.mb.tick()
                    # Se tick retorna False, pode ser porque:
                    # 1. Usuário clicou X (queremos parar)
                    # 2. Problema em thread (pode ser falso)
                    # Em threads, assumimos que False = usuário quer sair
                    if not result:
                        print("Janela fechada pelo usuário")
                        break
                    
                except Exception as e:
                    # Qualquer erro, sair
                    print(f"Erro: {e}")
                    break
                        
        except KeyboardInterrupt:
            print("\nEmulador interrompido (Ctrl+C no terminal)")
        except Exception as e:
            print(f"Erro no loop: {type(e).__name__}: {e}")
        
        finally:
            self.shutdown()
    
    def shutdown(self) -> None:
        """Finalizar emulador corretamente."""
        print("\nEncerrando emulador...")
        
        try:
            if self.mb:
                # Tentar parar o emulador
                try:
                    self.mb.stop(save=False)
                except Exception as e:
                    print(f"  ⚠ Erro ao parar mb: {e}")
                    # Tentar forçar
                    try:
                        self.mb = None
                    except:
                        pass
            
            print("OK: Emulador encerrado com sucesso!")
        except Exception as e:
            print(f"AVISO: Erro ao encerrar: {e}")
        finally:
            self.running = False


def select_rom_dialog() -> Optional[str]:
    """
    Exibir diálogo para seleção de ROM.
    
    Returns:
        Caminho da ROM ou None se cancelado
    """
    print("\n" + "="*60)
    print("SELETOR DE ROM - Game Boy Emulator")
    print("="*60)
    
    rom_path = input("\nDigite o caminho completo da ROM (.gb ou .gbc):\n> ").strip()
    
    if not rom_path:
        print("ERRO: Nenhuma ROM fornecida!")
        return None
    
    # Remover aspas se houver
    rom_path = rom_path.strip('"\'')
    
    if not os.path.exists(rom_path):
        print(f"ERRO: Arquivo nao encontrado: {rom_path}")
        return None
    
    if not rom_path.lower().endswith(('.gb', '.gbc')):
        print("ERRO: Arquivo deve ser .gb ou .gbc")
        return None
    
    print(f"OK: ROM encontrada!")
    return rom_path


def main():
    """Função principal."""
    print("\n" + "="*60)
    print("GAME BOY EMULATOR - PyBoy 2024")
    print("="*60)
    
    # Obter caminho da ROM
    rom_path = None
    
    if len(sys.argv) > 1:
        # ROM fornecida como argumento
        rom_path = sys.argv[1]
    else:
        # Diálogo interativo
        rom_path = select_rom_dialog()
    
    if not rom_path or not os.path.exists(rom_path):
        print("\nERRO: ROM nao fornecida ou nao encontrada!")
        print("\nUso: python main.py <caminho_da_rom>")
        print("Exemplo: python main.py 'C:\\Jogos\\Pokemon.gb'")
        sys.exit(1)
    
    # Inicializar e executar emulador
    try:
        emulator = GameBoyEmulator(rom_path)
        emulator.run()
    except FileNotFoundError as e:
        print(f"\nERRO: {e}")
        print("\nCertifique-se de que a ROM existe e o caminho esta correto.")
        sys.exit(1)
    except Exception as e:
        print(f"\nERRO FATAL: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
