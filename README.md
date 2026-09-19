# 🏷️ Desktop QR Code Generator

> **Language / Idioma:** [English](#english) | [Português](#português)

---

<a name="english"></a>
## 🇬🇧 English

A modern desktop application built with Python and CustomTkinter to automate QR Code creation for document sharing (e.g., SOPs). It features dynamic typography scaling to center labels neatly below the code, robust error correction, and standalone Windows `.exe` packaging.

### ✨ Key Features
- **Auto-Scaled Labels:** Automatically calculates text bounding boxes (`Pillow`) to fit labels without truncation.
- **High Error Correction:** Generates codes using `ERROR_CORRECT_H` (up to 30% recovery capability).
- **Standalone Executable:** Compiled via PyInstaller with embedded assets (icons, logo) and zero external runtime dependencies.
- **Modern Interface:** Dark theme UI built with CustomTkinter.

### 🛠️ Tech Stack
- **Python**
- **CustomTkinter** (GUI)
- **Pillow / PIL** (Typography & Image processing)
- **qrcode** (Matrix generation)
- **PyInstaller** (Executable compilation)

### 🚀 Quick Start
1. Clone & enter repository:
   git clone https://github.com/marcospaulogomez/QR_Genarator.exe/blob/main/app.py
   cd SEU_REPOSITORIO

2. Setup virtual environment:
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

3. Install requirements & run:
   pip install -r requirements.txt
   python app.py

---

<a name="português"></a>
## 🇧🇷 Português

Aplicação desktop moderna desenvolvida em Python e CustomTkinter para automatizar a geração de QR Codes voltados ao compartilhamento de documentos operacionais (como POPs). Conta com cálculo dinâmico de escala tipográfica para centralizar rótulos, alta correção de erros e distribuição em `.exe` nativo.

### ✨ Recursos Principais
- **Ajuste Dinâmico de Texto:** Dimensionamento automático da fonte via `Pillow` para garantir que o rótulo caiba na largura da imagem sem quebrar ou cortar.
- **Alta Tolerância a Falhas:** QR Codes gerados com `ERROR_CORRECT_H` (recuperação de até 30% em caso de avarias físicas).
- **Executável Portátil:** Empacotamento completo via PyInstaller contendo ícones e logotipo embutidos, sem exigir instalação prévia de Python na máquina final.
- **Interface Moderna:** Visual escuro nativo utilizando CustomTkinter.

### 🛠️ Tecnologias Utilizadas
- **Python**
- **CustomTkinter** (Interface gráfica)
- **Pillow / PIL** (Tratamento de imagem e medição tipográfica)
- **qrcode** (Geração da matriz 2D)
- **PyInstaller** (Compilação do executável)

### 🚀 Como Executar
1. Clonar e acessar a pasta:
   git clone https://github.com/marcospaulogomez/QR_Genarator.exe/blob/main/app.py
   cd SEU_REPOSITORIO

2. Criar e ativar o ambiente virtual:
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

3. Instalar dependências e iniciar:
   pip install -r requirements.txt
   python app.py

---

## 📄 License / Licença
This project is licensed under the [MIT License](LICENSE).
