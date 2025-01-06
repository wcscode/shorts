from gtts import gTTS
import ffmpeg
import os

class Audio:
    def __init__(self,lang="en", directory="files"):
        self.lang=lang
        self.directory = directory
        self.audios_files_names = []      

    def create(self, text_to_speech, audio_file_name):
        self.audios_files_names.append(audio_file_name)

        if text_to_speech:
            tts = gTTS(text_to_speech, lang=self.lang)            
            tts.save(os.path.join(self.directory, audio_file_name))
            print("Áudio gerado com sucesso.")
        return self._get_duration(audio_file_name)
    
    def get_files_names(self):
        return self.audios_files_names
    
    def _get_duration(self, audio_file_name):       
        try:
            probe = ffmpeg.probe(os.path.join(self.directory, audio_file_name))
            duration = float(probe['format']['duration'])
            return duration
        except Exception as e:
            print(f"Erro ao obter duração do áudio: {e}")
            return None
    
   