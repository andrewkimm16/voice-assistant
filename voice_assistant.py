import speech_recognition as sr
import openai
from gtts import gTTS
import os

openai.api_key = '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'

r = sr.Recognizer()

messages = [
    {"role": "system", "content": "You are a tutor named Judie that teaches in the Socratic Style of learning. You don't usually just give the student the answer at the first prompt, but try at first to ask just the right question to help them learn to think for themselves. You should always try to tune your question to the interest & knowledge of the student, breaking down the problem into simpler parts until it's at just the right level for them. If after asking a question the student does not get it you give them the answer and explain how you got there.  Never just give the answer, answers must come with explanations. Respond using proper markdown"},
]

kill_phrases = ["bye judie", "bye judy", "terminate"]

while True:
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)  # Listen for audio through the microphone

    try:
        print("Recognizing...")
        text = r.recognize_google(audio)
        print("You said: " + text)

        if text.lower() in kill_phrases:
            print("Kill phrase detected, stopping...")
            bye_message = "Goodbye, Andrew!"
            tts = gTTS(text=bye_message, lang='en')
            tts.save("response.mp3")
            os.system("mpg321 response.mp3")
            break

        messages.append({"role": "user", "content": text})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        chatGPT_response = response['choices'][0]['message']['content']
        print("ChatGPT says: " + chatGPT_response)

        messages.append({"role": "assistant", "content": chatGPT_response})

        tts = gTTS(text=chatGPT_response, lang='en')
        tts.save("response.mp3")
        os.system("mpg321 response.mp3")

    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
