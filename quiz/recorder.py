import mss
import cv2
import numpy as np
import threading
import platform
import os

class Recorder:
    def __init__(self, window_geometry,directory="files"):
        self.geometry = window_geometry  # (x, y, width, height)
        self.directory = directory
        self.recording = False
        self.thread = None               
        self.video_file_name = "output.avi"

    def _record(self):
        # Ajuste da geometria
        top, left, width, height = self._geometry_adjustments()     
           
        if not isinstance(width, int) or not isinstance(height, int):
            raise ValueError("Width and height must be integers.")

        # Inverte dimensões para rotação de 90 graus
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        try:
            out = cv2.VideoWriter(os.path.join(self.directory, self.video_file_name), fourcc, 30, (height, width))  # Inverte width e height
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
   
    def start_recording(self):
        print('Iniciando a gravação...')
        self.recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop_recording(self):
        print('Encerrando a gravação...')
        self.recording = False
        if self.thread:
            self.thread.join()
    
    def get_file_name(self):
        return self.video_file_name