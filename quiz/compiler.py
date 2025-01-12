import ffmpeg
import os

class Compiler:
    def __init__(self, final_video_file_name="final_output.mp4", directory="files"):
        self.directory = directory
        self.final_video_file_name = final_video_file_name
        self.video_file_name = None
        self.audio_tracks = []  # Lista para áudios adicionados
        self.background_tracks = []  # Lista para músicas de fundo

    def add_video(self, video_file_name):
        self.video_file_name = video_file_name

    def add_audio(self, audio_file_name, start_time=0, volume=1.0):
        """Adiciona um áudio com tempo de início e volume."""
        self.audio_tracks.append({
            "file": audio_file_name,
            "start_time": start_time,
            "volume": volume
        })

    def add_background_music(self, music_file_name, start_time=0, end_time=None, volume=0.5, loop=True):
        """Adiciona uma música de fundo à lista."""
        self.background_tracks.append({
            "file": music_file_name,
            "volume": volume,
            "start_time": start_time,
            "end_time": end_time,
            "loop": loop
        })

    def compile(self):
        if not self.video_file_name:
            raise ValueError("Nenhum vídeo foi adicionado.")

        if not self.audio_tracks and not self.background_tracks:
            raise ValueError("Nenhum áudio foi adicionado.")

        # Carregar o vídeo principal
        input_video = ffmpeg.input(os.path.join(self.directory, self.video_file_name))

        # Obter a duração do vídeo
        #video_duration = float(ffmpeg.probe(os.path.join(self.directory, self.video_file_name))['format']['duration'])

        # Preparar streams de áudio
        audio_streams = []
        for track in self.audio_tracks:
            audio = ffmpeg.input(os.path.join(self.directory, track["file"]))                        
            audio_volume = audio.filter('volume', track["volume"])            
            delay_filter = f"{int(track['start_time'] * 1000)}|{int(track['start_time'] * 1000)}"  # Em milissegundos
            delayed_audio = audio_volume.filter("adelay", delay_filter)

            audio_streams.append(delayed_audio)

        # Processar músicas de fundo
        for track in self.background_tracks:
            bg_audio = ffmpeg.input(os.path.join(self.directory, track["file"]))                        
            bg_audio_volume = bg_audio.filter('volume', track["volume"])            

            # Obter informações da música de fundo
            bg_audio_info = ffmpeg.probe(os.path.join(self.directory, track["file"]))
            bg_audio_duration = float(bg_audio_info['format']['duration'])
            #sample_rate = int(bg_audio_info['streams'][0]['sample_rate'])  # Taxa de amostragem

            # Ajustar a duração do áudio com base no end_time
            start_time = track["start_time"]  # Padrão 0 se não definido
            end_time = bg_audio_duration if track["end_time"] is None else track["end_time"]# Padrão para a duração total do áudio

            # Certifique-se de que o end_time não excede a duração total do áudio
            end_time = min(end_time, bg_audio_duration)

            # Aplicar o filtro atrim para ajustar a duração do áudio
            trimmed_bg_audio = bg_audio_volume.filter('atrim', start=start_time, end=end_time).filter('asetpts', 'PTS-STARTPTS')

            # Adicionar atraso ao áudio ajustado
            delay_filter = f"{int(start_time * 1000)}|{int(start_time * 1000)}"  # Em milissegundos
            delayed_bg_audio = trimmed_bg_audio.filter("adelay", delay_filter)

            audio_streams.append(delayed_bg_audio)

        # Mesclar os áudios
        if len(audio_streams) > 1:
            mixed_audio = ffmpeg.filter(audio_streams, 'amix', inputs=len(audio_streams), duration='longest')
        else:
            mixed_audio = audio_streams[0]

        output_directory = os.path.join(self.directory, "output")
        
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)

        # Gera a saída final
        output_path = os.path.join(output_directory, self.final_video_file_name)
        ffmpeg_output = ffmpeg.output(
            input_video,
            mixed_audio,
            output_path,
            vcodec="libx264",
            acodec="aac",
            strict="experimental"
        ).overwrite_output().global_args('-hide_banner', '-loglevel', 'warning')

        print("Processando...")
        response = ffmpeg_output.run()
        print(f"Arquivo gerado com sucesso: {self.final_video_file_name} {response}")

        return response[1] is None
