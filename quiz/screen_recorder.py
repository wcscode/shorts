import mss
import cv2
import numpy as np
import threading
import platform
import os
import time
from timeline import Timeline

#print(cv2.getBuildInformation())
#os.environ['PATH'] = r'C:\sqlite' + ";" + os.environ['PATH']

class ScreenRecorder:
    def __init__(self, window_geometry, directory="files"):
        self.geometry = window_geometry  # (x, y, width, height)
        self.directory = directory
        self.recording = False
        self.thread = None
        self.video_file_name = "output.avi"
        self.start_time = None
        self.fps = 30  # Taxa de quadros desejada
        self.timeline = Timeline()

    def start_recording(self):
        print("Iniciando a gravação...")
        self.timeline.start()
        self.recording = True
        self.thread = threading.Thread(target=self._record)
        self.thread.start()

    def stop_recording(self):
        self.recording = False
        if self.thread:
            self.thread.join()

        self.timeline.stop()
        print(f"Encerrando a gravação... Tempo total: {self.timeline.get_elapsed_time():.2f} segundos.")

    def get_file_name(self):
        return self.video_file_name
    
    def _record(self):
        top, left, width, height = self._geometry_adjustments()

        if not isinstance(width, int) or not isinstance(height, int):
            raise ValueError("Width and height must be integers.")

        output_width, output_height = 1080, 1920
        #output_width, output_height = 1440, 2560
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #fourcc = cv2.VideoWriter_fourcc(*'H264')

        try:
            out = cv2.VideoWriter(
                os.path.join(self.directory, self.video_file_name),
                fourcc,
                self.fps,
                (output_width, output_height),
                # Inverte width e height
                #isColor=True
            )
        except Exception as e:
            print(f"Erro ao criar VideoWriter: {e}")
            return

        with mss.mss() as sct:
            start_time = time.time()
            frame_count = 0
            while self.recording:
                elapsed_time = time.time() - start_time
                expected_frames = int(elapsed_time * self.fps)

                if frame_count < expected_frames:
                    screenshot = sct.grab({"top": top, "left": left, "width": width, "height": height})
                    frame = np.array(screenshot)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)                   
                    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
                    frame = cv2.resize(frame, (output_width, output_height))
                    out.write(frame)
                    frame_count += 1
                else:
                    time.sleep(1 / self.fps)  # Aguardar até o próximo quadro

        out.release()
        print("Gravação encerrada.")
    
    def _geometry_adjustments(self):
        system = platform.system()

        if system == "Windows":
            return self.geometry

        top, left, width, height = self.geometry
        return (top, left, width, height - 7)

   
