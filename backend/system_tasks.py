import os
import re
import screen_brightness_control as sbc

from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class SystemTasks:

    @staticmethod
    def find_int_in_string(input_string):
        numbers = re.findall(r"\d+", input_string)
        return list(map(int, numbers))

    @staticmethod
    def set_volume_from_text(user_text):
        numbers = SystemTasks.find_int_in_string(user_text)

        if not numbers:
            return "Please provide a volume level between 0 and 100."

        level = numbers[0]

        if level < 0 or level > 100:
            return "Please enter a volume number between 0 and 100."

        try:
            devices = AudioUtilities.GetSpeakers()
            interface = devices.Activate(
                IAudioEndpointVolume._iid_,
                CLSCTX_ALL,
                None
            )
            volume = cast(interface, POINTER(IAudioEndpointVolume))
            volume.SetMasterVolumeLevelScalar(level / 100.0, None)

            return f"Volume set to {level}%"

        except Exception as e:
            print(f"[ERROR] Volume change failed: {e}")
            return "Sorry, I could not change the volume."

    @staticmethod
    def set_brightness_from_text(user_text):
        numbers = SystemTasks.find_int_in_string(user_text)

        if not numbers:
            return "Please provide a brightness level between 0 and 100."

        percentage = numbers[0]

        if percentage < 0 or percentage > 100:
            return "Please enter a brightness number between 0 and 100."

        try:
            sbc.set_brightness(percentage)
            return f"Brightness set to {percentage}%"

        except Exception as e:
            print(f"[ERROR] Brightness change failed: {e}")
            return "Sorry, I could not change the brightness."

    @staticmethod
    def shutdown():
        try:
            os.system("shutdown /s /t 5")
            return "Shutting down the system in 5 seconds."
        except Exception as e:
            print(f"[ERROR] Shutdown failed: {e}")
            return "Sorry, I could not shut down the system."

    @staticmethod
    def restart():
        try:
            os.system("shutdown /r /t 5")
            return "Restarting the system in 5 seconds."
        except Exception as e:
            print(f"[ERROR] Restart failed: {e}")
            return "Sorry, I could not restart the system."

    @staticmethod
    def sleep():
        try:
            os.system("shutdown /h")
            return "Putting the system to sleep."
        except Exception as e:
            print(f"[ERROR] Sleep failed: {e}")
            return "Sorry, I could not put the system to sleep."