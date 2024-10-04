import os
import pytubefix
import ffmpeg
import google.generativeai as genai
import sys
genai.configure(api_key="AIzaSyBf7nGW5QwUiTWcZt-5EUliIDZvysmLunQ")
url = sys.argv[1]
filename = "audio.wav"

try:
    yt = pytubefix.YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    
    if audio_stream:
        print("Baixando o áudio...")
        audio_stream.download(filename="temp_audio.mp4")
        print("Download concluído.")

        print("Convertendo o áudio para WAV...")
        ffmpeg.input("temp_audio.mp4").output(filename, format='wav', loglevel="error").run()
        print("Conversão concluída.")
        print(filename)

        audio_file = genai.upload_file(filename)

        model = genai.GenerativeModel(model_name="gemini-1.5-flash")

        prompt = "transcription de music"

        response = model.generate_content([prompt, audio_file])

        with open("jorge.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
        print(response.text)

    else:
        print("Nenhum stream de áudio disponível.")
except Exception as e:
    print("Ocorreu um erro:", str(e))
