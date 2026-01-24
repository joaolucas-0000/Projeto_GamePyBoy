# Game Boy Emulator com PyBoy

Projeto totalmente funcional de um emulador Game Boy usando PyBoy em Python.

## Requisitos

- Python 3.10+
- Windows 10+ (ou macOS/Linux com SDL2)

## Instalação

### 1. Clonar ou preparar o repositório

```powershell
cd "c:\Users\joaosouz\Desktop\Projetos do GitHub\Game Boy com Python"
```

### 2. Criar ambiente virtual

```powershell
python -m venv .venv
```

### 3. Ativar ambiente virtual (Windows PowerShell)

```powershell
.\\.venv\\Scripts\\Activate.ps1
```

Se receber erro de permissão, execute:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 4. Instalar dependências

```powershell
pip install --upgrade pip
pip install -r requirements.txt
```

## Como usar

### Executar o emulador

```powershell
python main.py path\to\your\game.gb
```

Ou use o diálogo interativo:

```powershell
python main.py
```

### Controles do jogo

| Tecla         | Botão Game Boy |
|---------------|----------------|
| **Arrow Keys** | D-Pad          |
| **Z**         | Botão A        |
| **X**         | Botão B        |
| **Enter**     | Start          |
| **Space**     | Select         |
| **F**         | Capturar screenshot |
| **Esc**       | Sair           |

### Salvar e carregar estado

- **Ctrl+S**: Salvar estado atual
- **Ctrl+L**: Carregar último estado salvo

## Estrutura do projeto

```
.
├── main.py              # Entrypoint principal
├── controls.py          # Mapeamento de controles
├── config.example.json  # Configuração de exemplo
├── requirements.txt     # Dependências Python
├── assets/              # Pasta para screenshots e dados
│   └── screenshots/     # Screenshots capturados
└── README.md            # Este arquivo
```

## Aviso Legal

Este projeto é um emulador educacional. ROMs de jogos são propriedade intelectual de seus respectivos donos. 

**NÃO incluir ROMs no repositório.** Use apenas:
- ROMs legalmente adquiridas
- ROMs de jogos homebrew
- ROMs de domínio público

As ROMs devem ser fornecidas localmente pelo usuário.

## Troubleshooting

### Erro: "No module named 'pyboy'"

Verifique se o ambiente virtual está ativado:
```powershell
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
```

### Erro: "No module named 'pygame'"

**RESOLVIDO**: O projeto agora usa PyBoy com SDL2 nativo (sem pygame)!

Se receber esse erro, significa que você tem um arquivo main.py antigo. Atualize o repositório:

```powershell
git pull origin main
```

Ou reinstale as dependências:
```powershell
pip install -r requirements.txt
python main.py path\to\game.gb
```

### Erro de SSL ao instalar dependências

Se receber: `ssl.SSLCertVerificationError`

Tente:
```powershell
pip install --trusted-host pypi.python.org -r requirements.txt
```

## Contribuindo

Este é um projeto educacional. Sinta-se livre para fazer fork e contribuir!

## Licença

MIT License - veja LICENSE.md para detalhes.
