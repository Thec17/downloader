import yt_dlp
import flet as ft
import ssl
import certifi

ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())


def main(page: ft.Page):
    
    
    def my_hook(d):
        if d['status'] == 'downloading':
            try:
                progreso = float(d["downloaded_bytes"] / d["total_bytes"])
                progressBar.value = progreso
                text.value = ""
                text.value = f"Progreso: {str(progreso*100)[:4]}%"
                page.update()
            except Exception as e:
                print("No se pudo:", e)
        elif d['status'] == 'finished':
            pass

    def descargar_video(enlace):
        text.value = "Progreso: Esperando..."
        page.update()
        ydl_options = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best",
            "outtmpl": "%(title)s.%(ext)s",
            "merge_output_format": "mp4",
            "progress_hooks": [my_hook],
            "nocheckcertificate": True
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_options) as ydl:
                ydl.download([enlace])
                text.value = ""
                text.value = f"Progreso: ✅ Descarga completada"
                page.update()
        except Exception as e:
            text.value = ""
            text.value = f"Progreso: ❌ Error al descargar: {e}"
            page.update()
    
    page.title = "Descargar videos"
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.scroll = ft.ScrollMode.AUTO  
    
    content = ft.Column()
    
    textField = ft.TextField(label="Enlace del video")
    button = ft.Button(text="Descargar", on_click=lambda e: descargar_video(textField.value))
    text = ft.Text(value="Progreso: ")
    progressBar = ft.ProgressBar(value=0)
    
    
    content.controls.append(textField)
    content.controls.append(button)
    content.controls.append(text)
    content.controls.append(progressBar)
    
    page.add(ft.SafeArea(content))
    
ft.app(main)
