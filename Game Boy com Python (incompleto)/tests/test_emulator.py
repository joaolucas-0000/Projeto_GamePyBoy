#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes unitários para o emulador Game Boy
"""

import unittest
import os
import json
import tempfile
from pathlib import Path

# Importar módulos do projeto
import utils
from controls import ControlMapping, GameBoyButton, InputHandler
import pygame


class TestUtils(unittest.TestCase):
    """Testes para funções utilitárias."""
    
    def test_find_roms(self):
        """Testar busca de ROMs."""
        # Criar diretório temporário
        with tempfile.TemporaryDirectory() as tmpdir:
            # Criar arquivo ROM falso
            rom_path = os.path.join(tmpdir, "game.gb")
            Path(rom_path).touch()
            
            roms = utils.find_roms(tmpdir)
            self.assertEqual(len(roms), 1)
            self.assertTrue(roms[0].endswith(".gb"))
    
    def test_get_rom_info(self):
        """Testar obtenção de informações da ROM."""
        with tempfile.TemporaryDirectory() as tmpdir:
            rom_path = os.path.join(tmpdir, "game.gb")
            with open(rom_path, 'wb') as f:
                f.write(b"TEST" * 256)
            
            info = utils.get_rom_info(rom_path)
            self.assertEqual(info['name'], "game.gb")
            self.assertFalse(info['is_color'])
            self.assertIn('md5', info)
    
    def test_get_rom_info_gbc(self):
        """Testar detecção de ROM Color."""
        with tempfile.TemporaryDirectory() as tmpdir:
            rom_path = os.path.join(tmpdir, "game.gbc")
            Path(rom_path).touch()
            
            info = utils.get_rom_info(rom_path)
            self.assertTrue(info['is_color'])


class TestControlMapping(unittest.TestCase):
    """Testes para mapeamento de controles."""
    
    def setUp(self):
        """Configurar antes de cada teste."""
        pygame.init()
        self.controls = ControlMapping("default")
    
    def tearDown(self):
        """Limpar após cada teste."""
        pygame.quit()
    
    def test_default_mapping(self):
        """Testar mapeamento padrão."""
        button = self.controls.get_button(pygame.K_z)
        self.assertEqual(button, GameBoyButton.A)
        
        button = self.controls.get_button(pygame.K_UP)
        self.assertEqual(button, GameBoyButton.UP)
    
    def test_press_button(self):
        """Testar pressionar botão."""
        self.assertFalse(self.controls.is_pressed(GameBoyButton.A))
        
        self.controls.set_pressed(GameBoyButton.A, True)
        self.assertTrue(self.controls.is_pressed(GameBoyButton.A))
        
        self.controls.set_pressed(GameBoyButton.A, False)
        self.assertFalse(self.controls.is_pressed(GameBoyButton.A))
    
    def test_remap_key(self):
        """Testar remapeamento de tecla."""
        self.controls.remap_key(pygame.K_k, GameBoyButton.A)
        
        button = self.controls.get_button(pygame.K_k)
        self.assertEqual(button, GameBoyButton.A)
        
        # Z não deve mais estar mapeado
        button = self.controls.get_button(pygame.K_z)
        self.assertIsNone(button)
    
    def test_reset_mapping(self):
        """Testar reset de mapeamento."""
        self.controls.remap_key(pygame.K_k, GameBoyButton.A)
        self.controls.reset_to_default()
        
        button = self.controls.get_button(pygame.K_z)
        self.assertEqual(button, GameBoyButton.A)
    
    def test_wasd_mapping(self):
        """Testar mapeamento WASD."""
        wasd_controls = ControlMapping("wasd")
        
        button = wasd_controls.get_button(pygame.K_w)
        self.assertEqual(button, GameBoyButton.UP)
        
        button = wasd_controls.get_button(pygame.K_a)
        self.assertEqual(button, GameBoyButton.LEFT)
    
    def test_get_active_buttons(self):
        """Testar obtenção de botões ativos."""
        self.controls.set_pressed(GameBoyButton.A, True)
        self.controls.set_pressed(GameBoyButton.B, True)
        
        active = self.controls.get_active_buttons()
        self.assertEqual(len(active), 2)
        self.assertIn(GameBoyButton.A, active)
        self.assertIn(GameBoyButton.B, active)


class TestInputHandler(unittest.TestCase):
    """Testes para o manipulador de entrada."""
    
    def setUp(self):
        """Configurar antes de cada teste."""
        pygame.init()
        self.controls = ControlMapping("default")
        self.handler = InputHandler(self.controls)
        self.callback_called = False
    
    def tearDown(self):
        """Limpar após cada teste."""
        pygame.quit()
    
    def test_register_callback(self):
        """Testar registro de callback."""
        def callback(button):
            self.callback_called = True
        
        self.handler.register_key_down(GameBoyButton.A, callback)
        
        # Simular evento de tecla
        event = pygame.event.Event(pygame.KEYDOWN, {'key': pygame.K_z})
        self.handler.process_event(event)
        
        self.assertTrue(self.callback_called)


class TestConfiguration(unittest.TestCase):
    """Testes para configuração."""
    
    def test_config_json(self):
        """Testar arquivo de configuração."""
        config_path = "config.example.json"
        
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            self.assertIn('window_scale', config)
            self.assertIn('fps', config)
            self.assertIn('volume', config)
            self.assertGreater(config['fps'], 0)


def run_tests():
    """Executar todos os testes."""
    unittest.main(argv=[''], exit=False, verbosity=2)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("🧪 EXECUTANDO TESTES")
    print("="*60 + "\n")
    
    run_tests()
