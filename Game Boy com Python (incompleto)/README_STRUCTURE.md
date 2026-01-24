# Game Boy Emulator - PyBoy Web Interface

Um emulador Game Boy totalmente funcional com interface web moderna. Execute seus ROMs clássicos com uma UI elegante em preto e branco.

## 📋 Estrutura do Projeto

```
Game Boy com Python/
├── src/                          # Código-fonte
│   ├── emulator/                 # Lógica do emulador
│   │   ├── main.py               # Classe principal GameBoyEmulator
│   │   ├── controls.py           # Mapeamento de controles
│   │   └── __init__.py
│   ├── web/                      # Servidor web Flask
│   │   ├── web_server.py         # API REST e endpoints
│   │   ├── templates/            # Templates HTML/Jinja2
│   │   │   └── index.html        # Interface web moderna
│   │   └── __init__.py
│   └── utils/                    # Utilitários gerais
│       ├── utils.py
│       └── __init__.py
├── tests/                        # Testes e exemplos
│   ├── test_emulator.py
│   ├── check.py
│   └── examples.py
├── docs/                         # Documentação
│   └── README.md
├── config/                       # Configurações
│   └── config.example.json
├── media/                        # Mídia do projeto
│   ├── ROMs/                     # ✨ Coloque seus .gb/.gbc aqui
│   ├── screenshots/              # Screenshots automáticas
│   ├── recordings/               # Gravações de gameplay
│   └── assets/covers/            # Capas geradas
├── requirements.txt              # Dependências Python
├── __main__.py                   # Ponto de entrada
└── .gitignore
```

## 🚀 Como Usar

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o Servidor

```bash
python __main__.py
```

ou

```bash
python -m src.web.web_server
```

O servidor iniciará em: **http://127.0.0.1:5000**

### 3. Carregar ROMs

1. Coloque seus arquivos `.gb` ou `.gbc` na pasta `media/ROMs/`
2. Acesse o site e clique em "Carregar Jogo"
3. Selecione o arquivo e clique em "Enviar"

### 4. Jogar

- Clique em "▶ Jogar" para iniciar o emulador
- Use as **setas do teclado** para navegação (D-Pad)
- **A** = Botão A
- **S** = Botão B
- **Enter** = Start
- **Espaço** = Select
- **ESC** = Fechar o jogo

## 🎮 Recursos

✅ Suporte a ROMs Game Boy (`.gb`) e Game Boy Color (`.gbc`)
✅ Interface web moderna com tema preto e branco
✅ Upload de ROMs diretamente pelo navegador
✅ Visualização de screenshots e gravações
✅ Remover ROMs facilmente
✅ Emulador com precisão de hardware
✅ FPS estável (58-59 FPS)

## 📁 Mídia

### Screenshots
Automaticamente geradas na primeira execução da ROM. Armazenadas em `media/screenshots/`

### Gravações
Coloque seus arquivos `.gif` em `media/recordings/` com o nome começando com o nome da ROM.

**Exemplo:**
- ROM: `Super Mario Land (World).gb`
- Screenshot: `SUPER MARIO LAND-2026.01.20-12.12.35.png`
- Gravação: `SUPER MARIO LAND-2026.01.20-12.12.35.gif`

## 🛠️ Tecnologias

- **Backend**: Flask 3.1.2 + Python 3.10+
- **Emulador**: PyBoy 1.4.11 com SDL2 nativo
- **Frontend**: HTML5 + CSS3 + JavaScript vanilla
- **Ícones**: FontAwesome 6.5.1

## 📝 Notas Importantes

⚠️ **ROMs**: Este projeto é para fins educacionais. Você é responsável por possuir os ROMs que usar.

⚠️ **Debug Mode**: O servidor rodia em modo debug. Para produção, desabilitar em `src/web/web_server.py`

## 🐛 Solução de Problemas

**Janela do emulador não abre?**
- Certifique-se que SDL2 está instalado: `pip install pysdl2-dll`

**ROM não aparece no site?**
- Coloque o arquivo em `media/ROMs/`
- Recarregue a página

**Emulador não fecha?**
- Pressione **ESC** ou clique no botão X da janela

## 📚 Estrutura de Código

```python
# Usar o emulador diretamente
from src.emulator.main import GameBoyEmulator

emulator = GameBoyEmulator('media/ROMs/game.gb')
emulator.run()  # Abre janela SDL2
```

## 🤝 Contribuição

Melhorias são bem-vindas! Fork, modifique e abra um pull request.

---

**Desenvolvido com ❤️ usando PyBoy** | [PyBoy GitHub](https://github.com/Baekalfen/PyBoy)
