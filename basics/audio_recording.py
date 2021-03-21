# # Beep on Windows
# import winsound
# winsound.Beep(500, 1000)  # Beep at 500 Hz for 1000 ms

# import webbrowser
# webbrowser.open("sample.mp3")

## Docs: http://www.pygame.org/docs/ref/music.html
# from pygame import mixer  # Load the popular external library
# import time

# mixer.init()
# mixer.music.load("sample.mp3")
# mixer.music.play()  # loops=-1)

# while mixer.music.get_busy():
#     time.sleep(1)
# #mixer.music.stop()

# import sounddevice as sd
# from scipy.io.wavfile import write

# fs = 44100  # Sample rate
# seconds = 3  # Duration of recording

# myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
# sd.wait()  # Wait until recording is finished
# write('output.wav', fs, myrecording)  # Save as WAV file 

