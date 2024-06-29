import pytube
from pytube import YouTube
import tkinter as tk
from tkinter import filedialog, messagebox
import requests
def baixarVideo(url, tipo, caminho=0): #Corrigir problema "Baixando vídeo em qualidade baixa"
    try:
        yt = YouTube(url)
        if tipo == "video":
            stream = yt.streams.get_highest_resolution()


        elif tipo == "audio":
            stream = yt.streams.filter(only_audio=True).first()

        else:
            print("Opção inválida.")
            return

        if caminho:
            stream.download(output_path=caminho)

        else:
            stream.download()
        label_status.config(text="Download concluído!")

    except pytube.exceptions.RegexMatchError:
        label_status.config(text="URL inválida.")
    except Exception as e:
        label_status.config(text=f"Ocorreu um erro: {e}")

def baixar_arquivo(url, tipo):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()

        if tipo == "audio":
            extensao = ".mp3"
        elif tipo == "video":
            extensao = ".mp4"
        else:
            return

        caminho_arquivo = filedialog.asksaveasfilename(defaultextension=extensao, filetypes=[("Todos os arquivos", f"*{extensao}")])
        if caminho_arquivo:
            with open(caminho_arquivo, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            label_status.config(text=f"{tipo.capitalize()} Download completo")
        else:
            label_status.config(text="Download cancelado.")
    except requests.exceptions.RequestException as e:
        label_status.config(text=f"Erro no download: {e}")

def baixarAudio(): #Corrigir problema "baixando apenas audio em mp4"
    url = entry_url.get()
    if url:
        if "youtube.com" in url or "youtu.be" in url:
            caminho = filedialog.askdirectory()
            if caminho:
                baixarVideo(url, "audio", caminho)
            else:
                label_status.config(text="Download cancelado.")
        else:
            baixar_arquivo(url, "audio")
    else:
        label_status.config(text="insira uma URL")

def baixar_video(): #Retorna o download
    url = entry_url.get()
    if url:
        if "youtube.com" in url or "youtu.be" in url:
            caminho = filedialog.askdirectory()
            if caminho:
                baixarVideo(url, "video", caminho)
            else:
                label_status.config(text="Download cancelado")
        else:
            baixar_arquivo(url, "video")
    else:
        label_status.config(text="Insira uma URL")


root = tk.Tk() #cria painel de download
root.title("Youtube Download")

# URL
label_url = tk.Label(root, text="URL:")
label_url.pack(pady=5)
entry_url = tk.Entry(root, width=50)
entry_url.pack(pady=5)

# Botões para baixar
btn_audio = tk.Button(root, text="Baixar Áudio", command=baixarAudio)
btn_audio.pack(pady=10)
btn_video = tk.Button(root, text="Baixar Vídeo", command=baixar_video)
btn_video.pack(pady=10)

label_status = tk.Label(root, text="")
label_status.pack(pady=5)

root.mainloop()
