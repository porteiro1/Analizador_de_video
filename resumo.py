import pytubefix
import ffmpeg
import openai
import sys

openai.api_key = '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'

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
        
        with open(filename, "rb") as audio_file:
            transcript = openai.Audio.transcribe(
                model="whisper-1",
                file=audio_file
            )
        
        transcription_text = transcript["text"]
        print("Transcrição completa:\n", transcription_text)

        summary_response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Por favor, forneça um resumo para o seguinte texto:\n\n{transcription_text}",
            max_tokens=200,
            temperature=0.5
        )

        summary = summary_response.choices[0].text.strip()
        print("\nResumo:\n", summary)

    else:
        print("Nenhum stream de áudio disponível.")
except Exception as e:
    print("Ocorreu um erro:", str(e))
