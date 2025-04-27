import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QTextEdit, QLabel
)
from PyQt5.QtCore import Qt, QTimer

import socket
import Backend as be 
import frontend as fe
import webbrowser



class respond :
        
        def send_message_to(self , user_text):
            
            if "wish me" in user_text:
                be.Backend.wishMe()
                return
            
            elif "open" in user_text:
                if "erp portal" in user_text:
                    
                    webbrowser.open("https://erp.psit.ac.in/Student/")
                    return "Opening erp portal..."
                elif "leetcode" in user_text:
                    
                    webbrowser.open("https://leetcode.com/")
                    return "Opening leetcode..."
                
                else:
                    user_text = user_text.replace("open","")
                    fe.ChatBotApp.show_ai_response(self,"opening "+user_text)
                    be.Backend.open_taskbar_search(user_text)
                    return "opening "+user_text

            elif user_text == "shutdown" or user_text == "restart" or user_text == "sleep":
                task = user_text
                if task == "shutdown":
                    be.SystemTask.shutdown(self)
                    return "Shutting down..."
                elif task == "restart":
                    be.SystemTask.restart(self)
                    return "Restarting..."
                elif task == "sleep":
                    be.SystemTask.sleep(self)
                    return "Sleeping..."
                return  
              
            elif "send" in user_text:
                user_text= user_text.replace("send","")
                if "email" in user_text:
                    fe.ChatBotApp.show_ai_response(self,"Opening email...")
                    be.Backend.open_taskbar_search("email")
                    return "Opening email..."
                
                elif "whatsapp" in user_text:
                    whatsappSendText.send_message_to(self)
                    return "Sending message..."
                
                
            # elif  "set brightness to" or "brightness" in user_text:



                # return be.SystemTask.Setbrightness(self,user_text)

                # text = be.Backend.find_int_in_string(user_text)
                # persentage =text[0]
                # if(persentage>100 or persentage<0):
                #     fe.ChatBotApp.show_ai_response(self,"Please enter a valid number between 0 and 100")
                #     return "Please enter a valid number between 0 and 100"
                # sbc.set_brightness(int(persentage))
                # fe.ChatBotApp.show_ai_response(self,"Brightness set to "+str(user_text[0])+"%")
                # return "Brightness set to "+str(user_text[0])+"%"
            
            # elif "set volume to"or "volume" in user_text:
            #     text = be.Backend.find_int_in_string(user_text)
            #     persentage =text[0]
            #     if(persentage>100 or persentage<0):
            #         fe.ChatBotApp.show_ai_response(self,"Please enter a valid number between 0 and 100")
            #         return "Please enter a valid number between 0 and 100"
            #     be.SystemTask.set_volume(int(persentage))
            #     fe.ChatBotApp.show_ai_response(self,"Volume set to "+str(user_text[0])+"%")
            #     return "Volume set to "+str(user_text[0])+"%"
            
            elif 'play a song' in user_text: 
                fe.ChatBotApp.show_ai_response(self,'Which song would you like to listen to?')
                user_text = user_text.replace("play a song","")
                
                if user_text:
                    be.Backend.play_song_on_youtube(user_text)
            else :
                fe.ChatBotApp.show_ai_response(self,be.Backend.GeminiAi(user_text))
                return be.Backend.GeminiAi(user_text)
            





class whatsappSendText:
    def send_message_to(self):
        message=Nova_inter.ask(self,"what is the message")
        sender=Nova_inter.ask(self,"whom to send")
        be.Backend.send_whatsapp_message(sender,message)
    
class Nova_inter :
    def ask  (self, text) :

        Query=fe.ChatBotApp.send_message(self,text)  # return the query that shown in the chat history 
        return Query