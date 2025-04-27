import pyttsx3
import speech_recognition as sr
import datetime
import time
import pyautogui
import google.generativeai as genai
from IPython.display import display
import os
import wikipedia
import frontend as fe
import yt_dlp
import webbrowser
import re 
import screen_brightness_control as sbc

class Backend :
    # Function to speak the text
    def speak(text):
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[0].id)
        engine.setProperty('rate', 193)
        engine.setProperty('volume', 1)
        print(f"NOVA {text}")  # Debugging statement
        engine.say(text)
        engine.runAndWait()


    # Function to wish the user according to the time of the day
    def wishMe():
        hour = datetime.datetime.now().hour
        print(hour)
        if hour < 12:
            Backend.speak("Good Morning!")
        elif hour < 18:
            Backend.speak("Good Afternoon!")
        else:
            Backend.speak("Good Evening!")

    # Function to send a message on WhatsApp        
    def whatsappSendText(sender,text):
    # open the whatsapp
        Backend.open_taskbar_search("whatsapp")
    # time.sleep(1)
        time.sleep(1)
        pyautogui.typewrite(sender)
        time.sleep(1)
        pyautogui.press('down')
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.typewrite(text)
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(2)
        pyautogui.hotkey('alt', 'f4')
        Backend.speak("Message sent successfully")

    # Function to open the search bar and search for a query
    def open_taskbar_search(query):
    # Simulate 'Win + S' to open the search bar
        pyautogui.hotkey('win', 's')
        time.sleep(1)  # Wait for the search bar to open
    
    # Type the query
        pyautogui.typewrite(query)
        pyautogui.press('enter')

        time.sleep(1)  # Optional: Wait before performing further actions

    
    # Gemini AI function
    def GeminiAi(text):

        # Set up the API key
        os.environ["API_KEY"] = 'AIzaSyBkPNNj4QODv69jYFBguNKQWB7RXgScNxY'
        genai.configure(api_key=os.environ["API_KEY"])
    
        # Define model and generation function
        model = genai.GenerativeModel('gemini-1.5-flash-latest')
        # Generate content using the model
        response = model.generate_content(text)
    
        # Extract the response text (assuming it's in 'response.text' or similar)
        response_text = response.text  # Adjust this based on your response structure

        # 1. Remove unwanted characters like '*'
        response_text = response_text.replace('*', '')  # Removes all occurrences of '*'

        # 2. Format the response to make it more readable

        # Assuming we want to break the response into multiple lines for readability
        # We can split based on newlines or other logic depending on the response format
        formatted_response = response_text.replace('. ', '.\n')  # This adds a newline after each sentence (adjust as needed)

        return formatted_response


    def search_wikipedia(query):
        results = wikipedia.search(query)
        if not results:
            print("No results found.")
            return
        print(f"Found {len(results)} results. Which one would you like to read?")
        for i, result in enumerate(results):
            print(f"{i + 1}. {result}")
        choice = int(input("Enter the number of the article you want to read: "))
        if 1 <= choice <= len(results):
            print("Reading the article...")
            page = wikipedia.page(results[choice - 1])
            print(page.content)
        else:
            return "Invalid choice."



    def lisen(self):
        count=0
        r = sr.Recognizer()
        with sr.Microphone() as source:
            fe.ChatBotApp.show_ai_response(self,"Listening...")
            r.pause_threshold = 1
            audio = r.listen(source)
        try:
            fe.ChatBotApp.show_ai_response(self,"Recognizing...")
            query = r.recognize_google(audio, language='en-in')
            fe.ChatBotApp.show_ai_response(self,f"User said: {query}")
            return query.lower()
        
        except Exception:
            Backend.speak(" please repeat !!")
            count += 1
            if count == 3:
                return None
            else:
                return Backend.lisen(self)
            
        
        
    
    # def lisen():
    #     r = sr.Recognizer()
    #     with sr.Microphone() as source:
            
    #         r.pause_threshold = 1
    #         audio = r.listen(source)
    #     try:
    #         print("Recognizing...")
    #         query = r.recognize_google(audio, language='en-in')
    #         print(f"User said: {query}")
            
    #     except Exception:
    #         Backend.speak("i don,t understand")
    #         Backend.lisen()
    #         return None
        
    #     return query.lower()
    

    def play_song_on_youtube(song_name):
        ydl_opts = {
            'format': 'best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch1',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(song_name, download=False)
            video_url = result['entries'][0]['webpage_url']
            webbrowser.open(video_url)
            return"Playing"



    def find_int_in_string(input_string) :
        # Find all numbers in the string using regular expressions
        numbers = re.findall(r'\d+', input_string)
        # Convert them to integers
        integers = list(map(int, numbers))
        return integers



from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
import screen_brightness_control as sbc


class SystemTask :
    def set_volume(level):
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(level / 100.0, None)
         


    def set_brightness(level):
        sbc.set_brightness(level)



    def Setbrightness(self,user_text):
        text = Backend.find_int_in_string(user_text)
        persentage =text[0]
        if(persentage>100 or persentage<0):
            # fe.ChatBotApp.show_ai_response(self,"Please enter a valid number between 0 and 100")
            return "Please enter a valid number between 0 and 100"
        sbc.set_brightness(int(persentage))
        # fe.ChatBotApp.show_ai_response(self,"Brightness set to "+str(user_text[0])+"%")
        return "Brightness set to "+str(user_text[0])+"%"





        

    def shutdown(self):
        Backend.speak("Shutting down the system... Goodbye! Have a great day.")
        fe.ChatBotApp.show_ai_response(self,"Goodbye! Have a great day.")
        os.system('cmd /k "shutdown /s"')

    def restart(self):
        Backend.speak("Restarting the system...")
        fe.ChatBotApp.show_ai_response(self,"Restarting the system...")
        os.system('cmd /k "shutdown /r"')
    def sleep(self):
        Backend.speak("its time to take a nap...")
        Backend.speak("Putting the system to sleep...")
        os.system('cmd /k "shutdown /h"')




# if __name__ == "__main__" :
#     result=Backend.lisen()