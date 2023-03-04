import openai
import os

import sounddevice as sd
from scipy.io.wavfile import write
from gtts import gTTS

openai_key = open("OpenAI_key.txt", "r").read()

openai.api_key = openai_key
openai.Model.list()

# List of chat messages
chat_messages = [{"role": "system", "content": "You are a helpful voice assistant, speak only in English, with sentences less than 10 words."}]

while(True):
  seconds = input("Press Enter number of seconds to record: ")

  if seconds == "q":
    print("Exiting")
    break
  
  print("Recording for", seconds, "seconds")

  freq = 44100
  
  duration = int(seconds)
  
  # Recording audio
  user_recording = sd.rec(int(duration * freq),
                    samplerate=freq, channels=1)

  print("Recording Audio")
  # Record audio for the given number of seconds
  sd.wait()
  print("Audio recording complete")
  
  # Save user recording
  write("user_record.mp3", freq, user_recording)

  # Convert audio to text
  audio_file= open("user_record.mp3", "rb")
  user_transcript = openai.Audio.transcribe("whisper-1", audio_file).text
  print("User:", user_transcript)

  # Add user message to chat messages
  chat_messages.append({"role": "user", "content": user_transcript})

  # Get assistant response
  completions = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=chat_messages
  )

  # Get assistant message
  message = completions.choices[0].message.content
  print("assistant", message)

  # Add assistant message to chat messages
  chat_messages.append({"role": "assistant", "content": message})
  
  # Convert text to speech
  audio = gTTS(text=message, lang="en", slow=False)

  # Save assistant response
  audio.save("assistant_record.mp3")

  # Play audio
  os.system("afplay -r 1.4 assistant_record.mp3")