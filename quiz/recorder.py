import mss
import cv2
import numpy as np
import threading

class Recorder:
    def __init__(self, window_geometry):
        self.geometry = window_geometry  # (x, y, width, height)
        self.recording = False
        self.thread = None

    def _record(self):
        x, y, width, height = self._geometry_offset()     
           
        #print(f"Width: {width}, Height: {height}")  # Verifique os valores aqui
        if not isinstance(width, int) or not isinstance(height, int):
            raise ValueError("Width and height must be integers.")

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        try:
            out = cv2.VideoWriter('output.avi', fourcc, 120, (width, height))
        except Exception as e:
            print(f"Erro ao criar VideoWriter: {e}")
            return

        with mss.mss() as sct:
            while self.recording:
                screenshot = sct.grab({"top": y, "left": x, "width": width, "height": height})
                frame = np.array(screenshot)
                frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
                out.write(frame)

        out.release()

    def _geometry_offset(self):
        x, y, width, height = self.geometry
        return (x + 1, y + 25, width, height)

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
