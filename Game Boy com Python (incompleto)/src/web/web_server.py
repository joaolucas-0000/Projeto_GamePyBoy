import os
import re
import sys
import threading
from flask import Flask, request, jsonify, render_template, send_from_directory
from werkzeug.utils import secure_filename

ALLOWED_EXT = {'.gb', '.gbc'}
# Caminho raiz do projeto (3 níveis acima: web -> src -> raiz)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
MEDIA_DIR = os.path.join(PROJECT_ROOT, 'media')
ROM_DIR = os.path.join(MEDIA_DIR, 'ROMs')
COVERS_DIR = os.path.join(MEDIA_DIR, 'assets', 'covers')
SCREENSHOTS_DIR = os.path.join(MEDIA_DIR, 'screenshots')
RECORDINGS_DIR = os.path.join(MEDIA_DIR, 'recordings')

def ensure_dirs():
    os.makedirs(ROM_DIR, exist_ok=True)
    os.makedirs(COVERS_DIR, exist_ok=True)
    os.makedirs(SCREENSHOTS_DIR, exist_ok=True)
    os.makedirs(RECORDINGS_DIR, exist_ok=True)

def generate_slug(path_or_name):
    name = os.path.splitext(os.path.basename(path_or_name))[0]
    slug = re.sub(r'[^A-Za-z0-9_\-]', '_', name)
    return slug

def get_game_media(rom_filename):
    """Retorna screenshots e gravações associados a um jogo."""
    rom_base = os.path.splitext(rom_filename)[0]
    # Remove caracteres especiais para matching mais flexível
    rom_base_normalized = re.sub(r'[^A-Za-z0-9]', '', rom_base).upper()
    
    screenshots = []
    recordings = []
    
    # Procura por screenshots
    if os.path.exists(SCREENSHOTS_DIR):
        for fname in os.listdir(SCREENSHOTS_DIR):
            if fname.lower().endswith(('.png', '.jpg', '.jpeg')):
                # Normaliza o nome do arquivo para comparação
                file_base_normalized = re.sub(r'[^A-Za-z0-9]', '', os.path.splitext(fname)[0]).upper()
                # Verifica se o arquivo contém o nome do jogo (procura por match parcial)
                if rom_base_normalized in file_base_normalized or file_base_normalized.startswith(rom_base_normalized[:10]):
                    screenshots.append(fname)
    
    # Procura por gravações
    if os.path.exists(RECORDINGS_DIR):
        for fname in os.listdir(RECORDINGS_DIR):
            if fname.lower().endswith(('.gif', '.mp4', '.avi', '.webm')):
                # Normaliza o nome do arquivo para comparação
                file_base_normalized = re.sub(r'[^A-Za-z0-9]', '', os.path.splitext(fname)[0]).upper()
                # Verifica se o arquivo contém o nome do jogo
                if rom_base_normalized in file_base_normalized or file_base_normalized.startswith(rom_base_normalized[:10]):
                    recordings.append(fname)
    
    return sorted(screenshots), sorted(recordings)

def generate_cover(rom_path, out_path=None):
    """
    Inicia PyBoy headless, avança ~120 frames, captura tela e salva PNG.
    Retorna o caminho do PNG salvo.
    """
    ensure_dirs()
    if out_path is None:
        slug = generate_slug(rom_path)
        out_path = os.path.join(COVERS_DIR, f"{slug}.png")

    from pyboy import PyBoy

    # Inicia PyBoy sem janela
    pyboy = PyBoy(rom_path, window='null')
    # Deixa o emulador rodar alguns frames (screen de título aparece rápido)
    # Donkey Kong CGB precisa de mais frames para inicializar (~600-800)
    for _ in range(800):
        pyboy.tick()

    # Tenta obter imagem PIL
    img = None
    try:
        img = pyboy.screen.image
    except (AttributeError, Exception):
        img = None

    if img is None:
        pyboy.stop(False)
        raise RuntimeError("Nao foi possivel obter imagem da tela do PyBoy")

    img.save(out_path, 'PNG')
    pyboy.stop(False)
    return out_path

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/upload', methods=['POST'])
def api_upload():
    ensure_dirs()
    if 'file' not in request.files:
        return jsonify({'ok': False, 'error': 'nenhum arquivo'}), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify({'ok': False, 'error': 'nome vazio'}), 400

    filename = secure_filename(f.filename)
    ext = os.path.splitext(filename)[1].lower()
    if ext not in ALLOWED_EXT:
        return jsonify({'ok': False, 'error': 'extensao invalida'}), 400

    rom_path = os.path.join(ROM_DIR, filename)
    f.save(rom_path)

    try:
        cover_path = generate_cover(rom_path)
        cover_url = '/covers/' + os.path.basename(cover_path)
    except Exception as e:
        print(f"Erro ao gerar capa: {e}")
        cover_url = ''
    return jsonify({'ok': True, 'filename': filename, 'cover': cover_url})

@app.route('/api/roms', methods=['GET'])
def api_roms():
    ensure_dirs()
    items = []
    for fname in sorted(os.listdir(ROM_DIR)):
        if os.path.splitext(fname)[1].lower() not in ALLOWED_EXT:
            continue
        slug = generate_slug(fname)
        cover_file = f"{slug}.png"
        cover_path = os.path.join(COVERS_DIR, cover_file)
        cover_url = '/covers/' + cover_file if os.path.exists(cover_path) else ''
        
        # Obtém screenshots e gravações
        screenshots, recordings = get_game_media(fname)
        
        items.append({
            'filename': fname,
            'cover': cover_url,
            'screenshots': screenshots,
            'recordings': recordings
        })
    return jsonify(items)

@app.route('/covers/<path:filename>')
def serve_cover(filename):
    ensure_dirs()
    return send_from_directory(COVERS_DIR, filename)

@app.route('/screenshots/<path:filename>')
def serve_screenshot(filename):
    ensure_dirs()
    return send_from_directory(SCREENSHOTS_DIR, filename)

@app.route('/recordings/<path:filename>')
def serve_recording(filename):
    ensure_dirs()
    return send_from_directory(RECORDINGS_DIR, filename)

@app.route('/api/delete/<filename>', methods=['DELETE'])
def api_delete(filename):
    """Deleta uma ROM do diretório."""
    try:
        filename = secure_filename(filename)
        rom_path = os.path.join(ROM_DIR, filename)
        
        if not os.path.exists(rom_path):
            return jsonify({'ok': False, 'error': 'ROM nao encontrada'}), 404
        
        # Remove a ROM
        os.remove(rom_path)
        
        # Tenta remover a capa associada
        slug = generate_slug(filename)
        cover_path = os.path.join(COVERS_DIR, f"{slug}.png")
        if os.path.exists(cover_path):
            os.remove(cover_path)
        
        return jsonify({'ok': True, 'message': 'ROM deletada com sucesso'})
    except Exception as e:
        print(f"Erro ao deletar: {e}")
        return jsonify({'ok': False, 'error': str(e)}), 500

@app.route('/api/play/<filename>', methods=['GET'])
def api_play(filename):
    """Inicia o emulador com a ROM especificada."""
    filename = secure_filename(filename)
    rom_path = os.path.join(ROM_DIR, filename)
    
    if not os.path.exists(rom_path):
        return jsonify({'ok': False, 'error': 'ROM nao encontrada'}), 404
    
    try:
        # Importa e executa o emulador em thread separada
        sys_path_backup = os.sys.path.copy()
        os.sys.path.insert(0, os.path.join(PROJECT_ROOT, 'src'))
        from emulator.main import GameBoyEmulator
        os.sys.path = sys_path_backup
        
        def run_emulator():
            try:
                emulator = GameBoyEmulator(rom_path)
                emulator.run()
            except Exception as e:
                print(f"Erro ao rodar emulador: {e}")
            finally:
                # Garantir que o emulador seja encerrado
                print("Thread do emulador finalizada")
        
        # Cria e inicia thread do emulador (não-daemon para permitir shutdown correto)
        emulator_thread = threading.Thread(target=run_emulator, daemon=False)
        emulator_thread.start()
        
        # Retorna imediatamente
        return jsonify({'ok': True, 'message': 'Emulador iniciado'})
    except Exception as e:
        print(f"Erro: {e}")
        return jsonify({'ok': False, 'error': str(e)}), 500

if __name__ == '__main__':
    ensure_dirs()
    app.run(host='127.0.0.1', port=5000, debug=True)
