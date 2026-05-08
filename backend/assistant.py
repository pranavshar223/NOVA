import webbrowser
import yt_dlp
import wikipedia
import datetime

from ai_service import AIService
from system_tasks import SystemTasks


class Assistant:

    @staticmethod
    def wish_user():
        hour = datetime.datetime.now().hour

        if hour < 12:
            return "Good Morning!"
        elif hour < 18:
            return "Good Afternoon!"
        else:
            return "Good Evening!"

    @staticmethod
    def play_song_on_youtube(song_name):
        try:
            ydl_opts = {
                "format": "best",
                "noplaylist": True,
                "quiet": True,
                "default_search": "ytsearch1",
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                result = ydl.extract_info(song_name, download=False)

                if "entries" in result and result["entries"]:
                    video_url = result["entries"][0]["webpage_url"]
                else:
                    video_url = result["webpage_url"]

                webbrowser.open(video_url)

            return f"Playing {song_name} on YouTube."

        except Exception as e:
            print(f"[ERROR] YouTube play failed: {e}")
            return "Sorry, I could not play that on YouTube."

    @staticmethod
    def search_wikipedia(query):
        try:
            results = wikipedia.search(query)

            if not results:
                return "No Wikipedia results found."

            summary = wikipedia.summary(results[0], sentences=3)
            return summary

        except Exception as e:
            print(f"[ERROR] Wikipedia failed: {e}")
            return "Sorry, I could not get information from Wikipedia."

    @staticmethod
    def process_message(user_message):
        try:
            message = user_message.lower().strip()

            if not message:
                return "Please type something."

            if message in ["hello", "hi", "hey"]:
                return "Hello! I am NOVA. How can I help you?"

            if "good morning" in message or "good afternoon" in message or "good evening" in message:
                return Assistant.wish_user()

            if "volume" in message:
                return SystemTasks.set_volume_from_text(message)

            if "brightness" in message:
                return SystemTasks.set_brightness_from_text(message)

            if "shutdown" in message or "shut down" in message:
                return SystemTasks.shutdown()

            if "restart" in message:
                return SystemTasks.restart()

            if "sleep" in message or "hibernate" in message:
                return SystemTasks.sleep()

            if "play" in message and "youtube" in message:
                song_name = message.replace("play", "").replace("on youtube", "").replace("youtube", "").strip()
                if not song_name:
                    return "Which song should I play?"
                return Assistant.play_song_on_youtube(song_name)

            if message.startswith("play "):
                song_name = message.replace("play", "").strip()
                if not song_name:
                    return "Which song should I play?"
                return Assistant.play_song_on_youtube(song_name)

            if "wikipedia" in message:
                query = message.replace("wikipedia", "").replace("search", "").replace("about", "").strip()
                if not query:
                    return "What should I search on Wikipedia?"
                return Assistant.search_wikipedia(query)

            return AIService.ask_gemini(user_message)

        except Exception as e:
            print(f"[ERROR] Assistant process failed: {e}")
            return "Sorry, something went wrong while processing your request."