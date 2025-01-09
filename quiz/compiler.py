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

    def add_background_music(self, music_file_name, start_time=0, volume=0.5, loop=True):
        """Adiciona uma música de fundo à lista."""
        self.background_tracks.append({
            "file": music_file_name,
            "volume": volume,
            "start_time": start_time,
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
        video_duration = float(ffmpeg.probe(os.path.join(self.directory, self.video_file_name))['format']['duration'])

        # Preparar streams de áudio
        audio_streams = []
        for i, track in enumerate(self.audio_tracks):
            audio_path = os.path.join(self.directory, track["file"])
            audio = ffmpeg.input(audio_path)

            # Dividir o fluxo de áudio para múltiplas saídas
            audio_split = audio.filter('asplit', outputs=2)

            # Ajustar o volume (usar o rótulo 'a0' da saída do asplit)
            audio_volume = audio_split['a0'].filter('volume', volume=track["volume"])

            # Adicionar atraso ao áudio
            delay_filter = f"{int(track['start_time'] * 1000)}|{int(track['start_time'] * 1000)}"  # Em milissegundos
            delayed_audio = audio_volume.filter("adelay", delay_filter)

            audio_streams.append(delayed_audio)

        # Processar músicas de fundo
        for i, track in enumerate(self.background_tracks):
            bg_audio_path = os.path.join(self.directory, track["file"])
            bg_audio = ffmpeg.input(bg_audio_path)

            # Dividir o fluxo de áudio
            bg_audio_split = bg_audio.filter('asplit', outputs=2)

            # Ajustar o volume (usar o rótulo 'a0')
            bg_audio_volume = bg_audio_split['a0'].filter('volume', volume=track["volume"])

            # Repetir o áudio, se necessário
            if track["loop"]:
                bg_audio_volume = bg_audio_volume.filter('aloop', loop=-1, size=video_duration * 44100)

            # Adicionar atraso para o início da música
            delay_filter = f"{int(track['start_time'] * 1000)}|{int(track['start_time'] * 1000)}"  # Em milissegundos
            delayed_bg_audio = bg_audio_volume.filter("adelay", delay_filter)

            audio_streams.append(delayed_bg_audio)

        # Mesclar os áudios
        if len(audio_streams) > 1:
            mixed_audio = ffmpeg.filter(audio_streams, 'amix', inputs=len(audio_streams), duration='longest')
        else:
            mixed_audio = audio_streams[0]

        # Gera a saída final
        output_path = os.path.join(self.directory, self.final_video_file_name)
        ffmpeg_output = ffmpeg.output(
            input_video,
            mixed_audio,
            output_path,
            vcodec="libx264",
            acodec="aac",
            strict="experimental"
        ).overwrite_output().global_args('-hide_banner', '-loglevel', 'warning')

        ffmpeg_output.run()
        print(f"Arquivo gerado com sucesso: {self.final_video_file_name}")
