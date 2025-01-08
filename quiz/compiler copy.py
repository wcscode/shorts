import ffmpeg
import os

class Compiler:
    def __init__(self, final_video_file_name="final_output.mp4", directory="files"):
        self.directory = directory
        self.final_video_file_name = final_video_file_name 
        self.video_file_name = []
        self.audios_files_names = []
        self.audios_starts_times = []

    def add_video(self, video_file_name):
        self.video_file_name.append(video_file_name)

    def add_audio(self, audios_files_names, start_time=0):
        self.audios_files_names.append(audios_files_names)
        self.audios_starts_times.append(start_time)

    def compile(self):        

        if not self.video_file_name:
            raise ValueError("A variável não pode ser nula, vazia ou conter apenas espaços em branco.")
 
        if not self.audios_files_names:
            raise ValueError("A variável não pode ser nula, vazia ou conter apenas espaços em branco.")
        
        input_video = ffmpeg.input(os.path.join(self.directory, self.video_file_name))
        
        # Prepara os streams de áudio com adelay
        audio_streams = []
        for audio_file_name, timestamp in zip(self.audios_files_names, self.audios_starts_times):           
            audio = ffmpeg.input(os.path.join(self.directory, audio_file_name))            
            delay_filter = f"{timestamp * 1000}|{timestamp * 1000}"  # Milissegundos
            audio = audio.filter("adelay", delay_filter)
            audio_streams.append(audio)

        # Mescla os streams de áudio usando amix
        if len(audio_streams) > 1:
            mixed_audio = ffmpeg.filter(audio_streams, 'amix', inputs=len(audio_streams), duration='longest')
        else:
            mixed_audio = audio_streams[0]  # Apenas um áudio, não precisa de amix

        # Gera a saída com vídeo e áudio combinados
        output_path = os.path.join(self.directory, self.final_video_file_name)
        
        ffmpeg_output = ffmpeg.output(
            input_video,
            mixed_audio,
            output_path,
            vcodec="libx264",
            acodec="aac",
            strict="experimental"
        ).overwrite_output().global_args('-hide_banner', '-loglevel', 'warning')

        # Executa o comando do ffmpeg
        ffmpeg_output.run()
        print(f"Arquivo gerado com sucesso: {self.final_video_file_name}")
