# 🎮 GamePy 2.0

Um emulador de **Game Boy / Game Boy Color** em Python, construído como projeto educacional usando a biblioteca **PyBoy**. O objetivo do projeto é estudar emulação, arquitetura de sistemas clássicos, integração com SDL2 e gerenciamento de áudio/vídeo em tempo real.

> ⚠️ **Aviso importante**: este projeto é **experimental**. Alguns jogos (especialmente Game Boy Color) podem apresentar problemas de áudio conhecidos do PyBoy, como `CRITICAL Buffer overrun`.

---

## 📌 Funcionalidades

* Execução de jogos **Game Boy (GB)** e **Game Boy Color (GBC)**
* Janela gráfica via **SDL2**
* Sistema modular (main, emulator, config)
* Suporte a ROMs externas
* Estrutura pronta para expansão (input customizado, save states, etc.)

---

## 🧱 Estrutura do Projeto

```
GamePy 2.0/
│
├── main.py              # Ponto de entrada do programa
├── emulator.py          # Classe GameBoyEmulator
├── config.py            # Configurações do emulador
├── ROMs/                # Coloque suas ROMs aqui
│   └── exemplo.gb
└── README.md
```

---

## 🛠️ Requisitos

* Python **3.9+** (recomendado 3.10)
* Sistema operacional: Windows / Linux / macOS

### Bibliotecas Python

Instale as dependências com:

```bash
pip install pyboy pysdl2 pysdl2-dll pillow
```

> **Pillow** é opcional, mas recomendado para screenshots e screen recording.

---

## ▶️ Como Executar

1. Clone o repositório:

```bash
git clone https://github.com/SEU_USUARIO/GamePy-2.0.git
cd GamePy-2.0
```

2. Coloque suas ROMs na pasta `ROMs/`

3. Edite o caminho da ROM em `main.py`, por exemplo:

```python
rom_path = "ROMs/Super Mario Land.gb"
```

4. Execute:

```bash
python main.py
```

---

## 🧨 Problemas Conhecidos

### ❌ Buffer overrun (áudio)

Erro comum ao rodar jogos **Game Boy Color**, como Donkey Kong GBC:

```
pyboy.core.sound CRITICAL Buffer overrun! 1602 of 1602
```

📌 **Causa**:

* Limitação interna do sistema de áudio do PyBoy
* Eventos sonoros intensos (explosões, múltiplos efeitos)

📌 **Status**:

* ❗ Não é bug do código do projeto
* ❗ Ocorre também em projetos oficiais do PyBoy

📌 **Workarounds possíveis**:

* Rodar jogos **GB (não coloridos)**
* Reduzir FPS
* Executar sem áudio

---

## ⚖️ Aspectos Legais

* Este projeto **NÃO** inclui ROMs
* Projeto feito apenas para **estudo e aprendizado**

---

## 🚀 Próximos Passos (Ideias)

* Menu gráfico de seleção de ROMs
* Toggle de áudio em runtime
* Save/Load states
* Mapeamento de controles customizado
* Frontend em Tkinter ou PyQt

---

## 🤝 Contribuição

Pull requests são bem-vindos. Para mudanças maiores, abra uma issue antes para discutir o que você gostaria de alterar.

---

## 📄 Licença

Este projeto está sob a licença **MIT**.

---

## 🧠 Nota Final

Este projeto não é sobre perfeição — é sobre **aprender como sistemas clássicos funcionam**, quebrar a cabeça e entender limites reais de software.

Se você chegou até aqui: parabéns, você já sabe mais sobre emulação do que 90% das pessoas 😄
