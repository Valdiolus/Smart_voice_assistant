import openai
import os

from gtts import gTTS
from recorder import Recorder

openai_key = open("OpenAI_key.txt", "r").read()

openai.api_key = openai_key
openai.Model.list()

# List of chat messages
chat_messages = [{"role": "system", "content": "You are a helpful voice assistant named Cookie, speak only in English, with sentences less than 10 words."}]

recorder = Recorder()

print("Say something!")

while(True):

  file_path = recorder.listen()

  print("Recording finished ")

  # Convert audio to text
  audio_file= open(file_path, "rb")
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