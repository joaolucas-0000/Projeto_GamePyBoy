#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modulo de controles - Mapeamento de teclado para botoes Game Boy
Versao simplificada sem dependencia de pygame
"""

from enum import Enum
from typing import Dict, List, Callable, Optional


class GameBoyButton(Enum):
    """Botoes do Game Boy."""
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"
    A = "a"
    B = "b"
    START = "start"
    SELECT = "select"


class ControlMapping:
    """Gerencia mapeamento de teclado para controles."""
    
    # Mapeamento padrão original (PyBoy)
    DEFAULT_MAPPING_INFO = {
        "UP": GameBoyButton.UP,
        "DOWN": GameBoyButton.DOWN,
        "LEFT": GameBoyButton.LEFT,
        "RIGHT": GameBoyButton.RIGHT,
        "Z": GameBoyButton.A,
        "X": GameBoyButton.B,
        "Return": GameBoyButton.START,
        "space": GameBoyButton.SELECT,
    }
    
    # Mapeamento customizado: Seta Cima para pular, S para segundo botão
    CUSTOM_MAPPING_INFO = {
        "UP": GameBoyButton.A,      # Seta Cima = Pular (Botão A)
        "DOWN": GameBoyButton.DOWN,
        "LEFT": GameBoyButton.LEFT,
        "RIGHT": GameBoyButton.RIGHT,
        "Z": GameBoyButton.B,       # Z = Botão B
        "S": GameBoyButton.B,       # S = Botão B
        "X": GameBoyButton.B,       # X = Botão B (opcional)
        "Return": GameBoyButton.START,
        "space": GameBoyButton.SELECT,
    }
    
    # Mapeamento alternativo (WASD)
    WASD_MAPPING_INFO = {
        "W": GameBoyButton.UP,
        "S": GameBoyButton.DOWN,
        "A": GameBoyButton.LEFT,
        "D": GameBoyButton.RIGHT,
        "Z": GameBoyButton.A,
        "X": GameBoyButton.B,
        "Return": GameBoyButton.START,
        "space": GameBoyButton.SELECT,
    }
    
    def __init__(self, mapping_type: str = "custom"):
        """
        Inicializar mapeamento de controles.
        
        Args:
            mapping_type: "default", "custom", ou "wasd"
        """
        if mapping_type == "wasd":
            self.mapping = self.WASD_MAPPING_INFO.copy()
        elif mapping_type == "custom":
            self.mapping = self.CUSTOM_MAPPING_INFO.copy()
        else:
            self.mapping = self.DEFAULT_MAPPING_INFO.copy()
        
        self.pressed_buttons: Dict[GameBoyButton, bool] = {
            button: False for button in GameBoyButton
        }
    
    def get_button_by_name(self, key_name: str) -> Optional[GameBoyButton]:
        """
        Obter botao Game Boy correspondente ao nome da tecla.
        
        Args:
            key_name: Nome da tecla (ex: "Up", "Z", "Return")
            
        Returns:
            GameBoyButton ou None
        """
        return self.mapping.get(key_name)
    
    def is_pressed(self, button: GameBoyButton) -> bool:
        """
        Verificar se um botao esta pressionado.
        
        Args:
            button: Botao Game Boy
            
        Returns:
            True se pressionado
        """
        return self.pressed_buttons.get(button, False)
    
    def set_pressed(self, button: GameBoyButton, pressed: bool) -> None:
        """
        Marcar botao como pressionado ou solto.
        
        Args:
            button: Botao Game Boy
            pressed: True para pressionar, False para soltar
        """
        if button in self.pressed_buttons:
            self.pressed_buttons[button] = pressed
    
    def remap_key(self, key_name: str, button: GameBoyButton) -> None:
        """
        Remapear uma tecla para um botao.
        
        Args:
            key_name: Nome da tecla
            button: Novo botao Game Boy
        """
        self.mapping[key_name] = button
    
    def reset_to_default(self, mapping_type: str = "custom") -> None:
        """
        Resetar mapeamento ao padrao.
        
        Args:
            mapping_type: "default", "custom", ou "wasd"
        """
        if mapping_type == "wasd":
            self.mapping = self.WASD_MAPPING_INFO.copy()
        elif mapping_type == "custom":
            self.mapping = self.CUSTOM_MAPPING_INFO.copy()
        else:
            self.mapping = self.DEFAULT_MAPPING_INFO.copy()
        
        self.pressed_buttons = {button: False for button in GameBoyButton}
    
    def get_active_buttons(self) -> List[GameBoyButton]:
        """
        Obter lista de botoes atualmente pressionados.
        
        Returns:
            Lista de GameBoyButton pressionados
        """
        return [btn for btn, pressed in self.pressed_buttons.items() if pressed]
    
    def print_mapping(self) -> None:
        """Imprimir mapeamento atual no console."""
        print("\n--- MAPEAMENTO DE CONTROLES ---")
        for key, button in sorted(self.mapping.items()):
            print(f"  {key:15} -> {button.value:10}")
        print("-------------------------------\n")


# Exemplo de uso
if __name__ == "__main__":
    # Criar mapeamento padrao
    controls = ControlMapping("default")
    print("Mapeamento PADRAO carregado:")
    controls.print_mapping()
    
    # Remapear uma tecla
    controls.remap_key("K", GameBoyButton.A)
    print("Remapeado: K -> Botao A")
    
    # Resetar
    print("Resetando para padrao...")
    controls.reset_to_default()
    controls.print_mapping()
