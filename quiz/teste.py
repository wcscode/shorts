from compiler import Compiler

compiler = Compiler()
   
compiler.add_video("output.avi")    
compiler.add_audio("audio_file_1", 1) 
compiler.add_audio("audio_file_2", 8) 
compiler.add_background_music("free-stile.mp3")

compiler.compile()