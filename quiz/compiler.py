import ffmpeg
import os

class Compiler:
    def __init__(self, final_video_file_name="final_output.mp4", directory="files"):
        self.directory = directory
        self.final_video_file_name = final_video_file_name 

    def merge_video_with_multiple_audios(self, video_file_name, audios_files_names, audios_timestamps):        
        input_video = ffmpeg.input(os.path.join(self.directory, video_file_name))
        
        # Prepara os streams de áudio com adelay
        audio_streams = []
        for audio_file_name, timestamp in zip(audios_files_names, audios_timestamps):           
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
            pix_fmt="yuv420p",
            strict="experimental"
        ).overwrite_output().global_args('-hide_banner', '-loglevel', 'warning')

        # Executa o comando do ffmpeg
        ffmpeg_output.run()
        print(f"Arquivo gerado com sucesso: {self.final_video_file_name}")
