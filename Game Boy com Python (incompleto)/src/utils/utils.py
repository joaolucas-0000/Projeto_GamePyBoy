#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilitários - Funções auxiliares para o emulador
"""

import os
import json
from pathlib import Path
from datetime import datetime
import hashlib


def find_roms(directory: str = ".") -> list:
    """
    Procurar por arquivos ROM no diretório.
    
    Args:
        directory: Diretório a buscar
        
    Returns:
        Lista de caminhos de ROMs encontradas
    """
    roms = []
    valid_extensions = ('.gb', '.gbc')
    
    for root, dirs, files in os.walk(directory):
        # Ignorar pastas do sistema
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        for file in files:
            if file.lower().endswith(valid_extensions):
                roms.append(os.path.join(root, file))
    
    return sorted(roms)


def get_rom_info(rom_path: str) -> dict:
    """
    Obter informações sobre uma ROM.
    
    Args:
        rom_path: Caminho da ROM
        
    Returns:
        Dicionário com informações
    """
    if not os.path.exists(rom_path):
        return {}
    
    stat = os.stat(rom_path)
    
    # Calcular hash MD5
    md5_hash = hashlib.md5()
    with open(rom_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            md5_hash.update(chunk)
    
    return {
        "name": os.path.basename(rom_path),
        "path": rom_path,
        "size": stat.st_size,
        "size_mb": stat.st_size / (1024 * 1024),
        "md5": md5_hash.hexdigest(),
        "is_color": rom_path.lower().endswith('.gbc'),
        "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
    }


def format_rom_info(rom_info: dict) -> str:
    """
    Formatar informações de ROM para exibição.
    
    Args:
        rom_info: Dicionário com info da ROM
        
    Returns:
        String formatada
    """
    if not rom_info:
        return "Nenhuma informação disponível"
    
    text = f"""
╔════════════════════════════════════════════════════════════╗
║                   INFORMAÇÕES DA ROM                       ║
╚════════════════════════════════════════════════════════════╝

Nome:        {rom_info.get('name', 'N/A')}
Caminho:     {rom_info.get('path', 'N/A')}
Tamanho:     {rom_info.get('size_mb', 0):.2f} MB ({rom_info.get('size', 0)} bytes)
Tipo:        {'Game Boy Color (GBC)' if rom_info.get('is_color') else 'Game Boy (GB)'}
MD5:         {rom_info.get('md5', 'N/A')}
Modificado:  {rom_info.get('modified', 'N/A')}
"""
    return text


def list_screenshots() -> list:
    """
    Listar screenshots capturados.
    
    Returns:
        Lista de caminhos de screenshots
    """
    screenshots_dir = "assets/screenshots"
    if not os.path.exists(screenshots_dir):
        return []
    
    files = []
    for file in os.listdir(screenshots_dir):
        if file.lower().endswith('.png'):
            files.append(os.path.join(screenshots_dir, file))
    
    return sorted(files, reverse=True)


def list_savestates() -> list:
    """
    Listar save states salvos.
    
    Returns:
        Lista de caminhos de savestates
    """
    states_dir = "assets/states"
    if not os.path.exists(states_dir):
        return []
    
    files = []
    for file in os.listdir(states_dir):
        if file.lower().endswith('.state'):
            stat = os.stat(os.path.join(states_dir, file))
            files.append({
                "path": os.path.join(states_dir, file),
                "name": file,
                "size": stat.st_size,
                "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
            })
    
    return sorted(files, key=lambda x: x['modified'], reverse=True)


def cleanup_old_screenshots(max_files: int = 100) -> int:
    """
    Limpar screenshots antigos mantendo apenas os últimos.
    
    Args:
        max_files: Número máximo de screenshots a manter
        
    Returns:
        Número de arquivos deletados
    """
    screenshots = list_screenshots()
    if len(screenshots) <= max_files:
        return 0
    
    deleted = 0
    for file in screenshots[max_files:]:
        try:
            os.remove(file)
            deleted += 1
        except OSError:
            pass
    
    return deleted


def create_rom_list(directory: str = ".") -> None:
    """
    Criar arquivo com lista de ROMs encontradas.
    
    Args:
        directory: Diretório a buscar
    """
    roms = find_roms(directory)
    
    with open("rom_list.txt", "w", encoding="utf-8") as f:
        f.write("LISTA DE ROMs ENCONTRADAS\n")
        f.write("=" * 60 + "\n\n")
        
        for rom in roms:
            info = get_rom_info(rom)
            f.write(f"Nome: {info.get('name', 'N/A')}\n")
            f.write(f"Caminho: {rom}\n")
            f.write(f"Tamanho: {info.get('size_mb', 0):.2f} MB\n")
            f.write(f"Tipo: {'Game Boy Color' if info.get('is_color') else 'Game Boy'}\n")
            f.write("-" * 60 + "\n\n")
    
    print(f"✓ Lista criada: rom_list.txt ({len(roms)} ROMs encontradas)")


# Exemplo de uso
if __name__ == "__main__":
    print("Procurando ROMs...")
    roms = find_roms(".")
    
    if roms:
        print(f"\n✓ {len(roms)} ROM(s) encontrada(s):\n")
        for rom in roms:
            info = get_rom_info(rom)
            print(format_rom_info(info))
    else:
        print("\n✗ Nenhuma ROM encontrada")
    
    print("\n📸 Screenshots:")
    screenshots = list_screenshots()
    for ss in screenshots[:5]:
        print(f"  • {os.path.basename(ss)}")
    
    if len(screenshots) > 5:
        print(f"  ... e mais {len(screenshots) - 5}")
    
    print("\n💾 Save States:")
    savestates = list_savestates()
    for ss in savestates:
        print(f"  • {ss['name']} ({ss['size']} bytes)")
