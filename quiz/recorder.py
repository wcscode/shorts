import mss
import cv2
import numpy as np
import threading
import platform
from gtts import gTTS
import ffmpeg
import os

class Recorder:
    def __init__(self, window_geometry, text_to_speech=None):
        self.geometry = window_geometry  # (x, y, width, height)
        self.recording = False
        self.thread = None
        self.text_to_speech = text_to_speech
        self.audio_file = "audio.mp3"
        self.video_file = "output.avi"
        self.final_output = "final_output.mp4"

    def _record(self):
        # Ajuste da geometria
        top, left, width, height = self._geometry_adjustments()     
           
        if not isinstance(width, int) or not isinstance(height, int):
            raise ValueError("Width and height must be integers.")

        # Inverte dimensões para rotação de 90 graus
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        try:
            out = cv2.VideoWriter(self.video_file, fourcc, 30, (height, width))  # Inverte width e height
        except Exception as e:
            print(f"Erro ao criar VideoWriter: {e}")
            return

        # Captura de tela e gravação
        with mss.mss() as sct:
            while self.recording:
                screenshot = sct.grab({"top": top, "left": left, "width": width, "height": height})
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                out.write(frame)

        out.release()
        print("Gravação encerrada.")

    def _geometry_adjustments(self):
        system = platform.system()

        if system == "Windows":
            return self.geometry

        # Ajuste da geometria para compensar bordas ou deslocamentos
        top, left, width, height = self.geometry
        return (top, left, width, height)

    def _convert_text_to_audio(self):
        if self.text_to_speech:
            tts = gTTS(self.text_to_speech, lang="pt")
            #tts = gTTS(self.text_to_speech, lang="en")
            tts.save(self.audio_file)
            print("Áudio gerado com sucesso.")

    def _merge_audio_video(self):

        if not os.path.exists(self.video_file):
            print(f"Arquivo de vídeo não encontrado: {self.video_file}")
            return

        if not os.path.exists(self.audio_file):
            print(f"Arquivo de áudio não encontrado: {self.audio_file}")
            return

        try:
            input_video = ffmpeg.input(self.video_file)
            input_audio = ffmpeg.input(self.audio_file)
            ffmpeg.output(
                input_video,
                input_audio,
                self.final_output,
                vcodec="libx264",
                acodec="aac",
                strict="experimental",
                #audio_bitrate="192k", 
                #map="0:v",  # Mapeia o vídeo da primeira entrada (input_video)
                #map="1:a"   # Mapeia o áudio da segunda entrada (input_audio)
            ).run()
            print(f"Vídeo finalizado com áudio: {self.final_output}")
        except Exception as e:
            print(f"Erro ao mesclar áudio e vídeo: {e}")

    def start_recording(self):
        print('Iniciando a gravação...')
        self.recording = True

        # Converter texto em áudio antes de iniciar a gravação
        self._convert_text_to_audio()

        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop_recording(self):
        print('Encerrando a gravação...')
        self.recording = False
        if self.thread:
            self.thread.join()

        # Mesclar áudio e vídeo
        self._merge_audio_video()
