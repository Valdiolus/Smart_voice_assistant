import openai
import os

from gtts import gTTS
from recorder import Recorder

import re
import time

def audio_quickplayer(message):
  # Split message into parts
  part_message = re.split('[;|.|\n]', message)

  audio_names = []

  # Loop through parts
  for count in range(len(part_message)):

    # Check if part is empty
    if len(part_message[count]) == 0:
      continue

    #print(count, part_message[count])

    # Convert text to speech
    audio = gTTS(text=part_message[count], lang="en", slow=False)

    # Create file name
    current_name = "audio/assistant_record" + str(count) + ".mp3"
    
    # Add file name to list
    audio_names.append(current_name)

    # Save assistant response
    audio.save(current_name)

    # Play assistant response
    os.system("afplay -r 1.4 " + current_name)


def main():

  openai_key = open("OpenAI_key.txt", "r").read()

  openai.api_key = openai_key
  openai.Model.list()

  # List of chat messages
  chat_messages = [{"role": "system", "content": "You are a helpful voice assistant named Cookie, speak only in English, with sentences less than 10 words."}]

  recorder = Recorder()

  if not os.path.exists('audio'):
    os.makedirs('audio')

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
    print("assistant:", message)

    # Add assistant message to chat messages
    chat_messages.append({"role": "assistant", "content": message})
    
    audio_quickplayer(message)


if __name__ == "__main__":
  main()

