import os
import ctypes
import sys 
import qrcode
from PIL import Image, ImageDraw, ImageFont
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Garante que o ícone na barra de tarefas do Windows use o do programa, e não o do Python
try:
    myappid = "meuapp.geradorqrcode.versao1"
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except Exception:
    pass

def obter_caminho_recurso(caminho_relativo):
    #Retorna o caminho absoluto para recursos, funcionando tanto no VS Code quanto no executável do PyInstaller
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, caminho_relativo)

# Configuração visual do CustomTkinter
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


# Descobre o caminho da fonte uma única vez na inicialização
CAMINHO_FONTE_SISTEMA = None
for caminho in [
    "C:\\Windows\\Fonts\\arialbd.ttf",
    "C:\\Windows\\Fonts\\arial.ttf",
    "C:\\Windows\\Fonts\\segoeui.ttf",
]:
    if os.path.exists(caminho):
        CAMINHO_FONTE_SISTEMA = caminho
        break


def obter_fonte(tamanho):
    if CAMINHO_FONTE_SISTEMA:
        try:
            return ImageFont.truetype(CAMINHO_FONTE_SISTEMA, tamanho)
        except OSError:
            pass
    return ImageFont.load_default()


def criar_qrcode(url, texto, caminho_saida):
    # 1. Gera o QR Code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img_qr = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    largura_qr, altura_qr = img_qr.size

    # 2. Ajuste rápido de fonte (usando um único draw reutilizável)
    tamanho_fonte = 60
    margem_texto = 20
    largura_maxima = largura_qr - margem_texto

    # Reutiliza o mesmo objeto draw para não alocar memória em loop
    draw_medicao = ImageDraw.Draw(img_qr)
    fonte = obter_fonte(tamanho_fonte)

    while tamanho_fonte > 10:
        caixa = draw_medicao.textbbox((0, 0), texto, font=fonte)
        largura_texto = caixa[2] - caixa[0]

        if largura_texto <= largura_maxima:
            break

        tamanho_fonte -= 2
        fonte = obter_fonte(tamanho_fonte)

    # 3. Composição final da imagem
    padding_texto = tamanho_fonte + 25
    img_final = Image.new("RGB", (largura_qr, altura_qr + padding_texto), "white")
    img_final.paste(img_qr, (0, 0))

    draw_final = ImageDraw.Draw(img_final)
    caixa_final = draw_final.textbbox((0, 0), texto, font=fonte)
    largura_texto = caixa_final[2] - caixa_final[0]

    x_texto = (largura_qr - largura_texto) / 2
    y_texto = altura_qr + 5
    draw_final.text((x_texto, y_texto), texto, fill="black", font=fonte)

    # Salva no disco
    img_final.save(caminho_saida)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ícone da janela e da barra de tarefas (deve ser arquivo .ico)
        caminho_icone = obter_caminho_recurso("icone.ico")
        if os.path.exists(caminho_icone):
            self.iconbitmap(caminho_icone)

        self.title("Gerador de QR Code")
        self.geometry("520x460")
        self.resizable(False, False)

        # Título da tela
        self.lbl_titulo = ctk.CTkLabel(
            self, text="Gerador de QR Code", font=("Arial", 20, "bold")
        )
        self.lbl_titulo.pack(pady=(20, 15))

        # Campo 1: URL / Link do Drive
        self.lbl_url = ctk.CTkLabel(self, text="Link do Documento (Google Drive):")
        self.lbl_url.pack(anchor="w", padx=40)
        self.entry_url = ctk.CTkEntry(self, placeholder_text="https://drive.google.com/...")
        self.entry_url.pack(fill="x", padx=40, pady=(0, 10))

        # Campo 2: Texto de Identificação
        self.lbl_texto = ctk.CTkLabel(self, text="Texto Abaixo do QR Code (ex: relatório_final):")
        self.lbl_texto.pack(anchor="w", padx=40)
        self.entry_texto = ctk.CTkEntry(self, placeholder_text="relatório_final")
        self.entry_texto.pack(fill="x", padx=40, pady=(0, 10))

        # Campo 3: Pasta de Destino
        self.lbl_pasta = ctk.CTkLabel(self, text="Pasta onde salvar o QR Code:")
        self.lbl_pasta.pack(anchor="w", padx=40)
        
        self.frame_pasta = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_pasta.pack(fill="x", padx=40, pady=(0, 15))

        self.entry_pasta = ctk.CTkEntry(self.frame_pasta, placeholder_text="Selecione a pasta de destino...")
        self.entry_pasta.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.btn_buscar = ctk.CTkButton(
            self.frame_pasta, text="Procurar...", width=90, command=self.selecionar_pasta
        )
        self.btn_buscar.pack(side="right")

        # Botão Principal: Gerar
        self.btn_gerar = ctk.CTkButton(
            self,
            text="Gerar QR Code",
            height=40,
            font=("Arial", 15, "bold"),
            command=self.processar_geracao,
        )
        self.btn_gerar.pack(fill="x", padx=40, pady=(10, 10))

        # Carregamento e exibição da Logo na interface
        caminho_logo = obter_caminho_recurso("logo.png")
        if os.path.exists(caminho_logo):
            imagem_pil = Image.open(caminho_logo)
            # Ajuste o tamanho (largura, altura) conforme a proporção da sua logo:
            LARGURA_MAXIMA = 180
            ALTURA_MAXIMA = 70

            # Redimensiona mantendo o aspect ratio original
            imagem_pil.thumbnail((LARGURA_MAXIMA, ALTURA_MAXIMA), Image.Resampling.LANCZOS)
            largura_real, altura_real = imagem_pil.size

            self.img_logo = ctk.CTkImage(
                light_image=imagem_pil, 
                dark_image=imagem_pil, 
                size=(largura_real, altura_real)
                )

            self.lbl_logo = ctk.CTkLabel(self, image=self.img_logo, text="")
            self.lbl_logo.pack(pady=(35, 15))

        # Status
        self.lbl_status = ctk.CTkLabel(self, text="", text_color="gray")
        self.lbl_status.pack()

    def selecionar_pasta(self):
        caminho = filedialog.askdirectory()
        if caminho:
            self.entry_pasta.delete(0, "end")
            self.entry_pasta.insert(0, caminho)

    def processar_geracao(self):
        url = self.entry_url.get().strip()
        texto = self.entry_texto.get().strip()
        pasta = self.entry_pasta.get().strip()

        if not url or not texto or not pasta:
            messagebox.showwarning("Campos incompletos", "Por favor, preencha todos os campos e selecione a pasta.")
            return

        # Sanitiza o texto para virar o nome do arquivo PNG
        nome_arquivo = "".join(c for c in texto if c.isalnum() or c in (" ", "_", "-")).rstrip()
        nome_arquivo = f"qrcode_{nome_arquivo.replace(' ', '_').lower()}.png"
        caminho_final = os.path.join(pasta, nome_arquivo)

        try:
            criar_qrcode(url, texto, caminho_final)
            self.lbl_status.configure(text=f"Salvo: {nome_arquivo}", text_color="#2ecc71")
            messagebox.showinfo("Sucesso", f"QR Code gerado com sucesso em:\n{caminho_final}")
        except Exception as e:
            self.lbl_status.configure(text="Erro ao gerar QR Code", text_color="#e74c3c")
            messagebox.showerror("Erro", f"Ocorreu um erro ao gerar:\n{str(e)}")


if __name__ == "__main__":
    app = App()
    app.mainloop()