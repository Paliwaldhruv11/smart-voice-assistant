import speech_recognition as sr
import pyttsx3
import datetime
import pywhatkit
import wikipedia
import pyautogui
import webbrowser
import customtkinter as ctk
import threading
import keyboard
import smtplib
from email.mime.text import MIMEText

# Initialize Text to Speech Engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine.setProperty('rate', 170)

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio)
        print(f"User said: {query}")
    except Exception as e:
        print("Sorry, say that again.")
        return ""
    return query.lower()

def send_email(to, subject, message):
    # Enter your app password and email here
    user_email = 'paliwaldhruv11@gmail.com'
    app_password = 'Dpa@96958716'

    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = user_email
    msg['To'] = to

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(user_email, app_password)
        server.sendmail(user_email, to, msg.as_string())
        server.quit()
        speak("Email has been sent successfully.")
    except Exception as e:
        print(e)
        speak("Sorry, I could not send the email.")

def perform_task(command):
    if 'open chrome' in command:
        speak('Opening Chrome')
        webbrowser.open('https://www.google.com')
    elif 'open notepad' in command:
        speak('Opening Notepad')
        pyautogui.hotkey('win', 'r')
        pyautogui.write('notepad')
        pyautogui.press('enter')
    elif 'open spotify' in command:
        speak('Opening Spotify')
        webbrowser.open('https://open.spotify.com/')
    elif 'search' in command:
        speak('Searching Google...')
        query = command.replace('search', '')
        pywhatkit.search(query)
    elif 'send whatsapp' in command:
        speak('Who is the recipient?')
        recipient = listen()
        speak('What is the message?')
        message = listen()
        pywhatkit.sendwhatmsg_instantly(f"+91{recipient}", message)
        speak('Message sent.')
    elif 'email' in command:
        speak('Who should I send it to? (give email)')
        to = listen()
        speak('What is the subject?')
        subject = listen()
        speak('What should be the message?')
        message = listen()
        send_email(to, subject, message)
    elif 'time' in command:
        time = datetime.datetime.now().strftime('%I:%M %p')
        speak('Current time is ' + time)
    elif 'exit' in command:
        speak("Goodbye, see you soon!")
        exit()
    else:
        try:
            result = wikipedia.summary(command, sentences=2)
            speak(result)
        except:
            speak('Sorry, could not find information.')

def run_assistant():
    while True:
        command = listen()
        if "hello" in command:
            speak("How can I help you?")
            command = listen()
            perform_task(command)

# GUI Part
def start_gui():
    app = ctk.CTk()
    app.geometry("400x300")
    app.title("Backbencher AI Assistant")

    ctk.set_appearance_mode("dark")  # Dark Mode
    ctk.set_default_color_theme("blue")

    label = ctk.CTkLabel(master=app, text="Backbencher AI Assistant", font=("Arial", 24))
    label.pack(pady=20)

    start_button = ctk.CTkButton(master=app, text="Start Listening", command=lambda: threading.Thread(target=run_assistant).start())
    start_button.pack(pady=20)

    app.mainloop()

# Main Execution
if __name__ == "__main__":
    start_gui()
