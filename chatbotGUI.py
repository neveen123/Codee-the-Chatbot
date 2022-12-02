
import tkinter
from tkinter import *
from chatbot import chatbot_response


def bot_greeting():
    print("hello there")


def greeting():

    msg2 = ChatLog.get("1.0", 'end-1c').strip()
    ChatLog.delete("0.0", END)
    ChatLog.config(state=NORMAL)
    response = bot_greeting(msg2)
    ChatLog.insert(END, "Codee: " + response + '\n\n')
    ChatLog.config(state=DISABLED)
    ChatLog.xview(END)


def send():
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)
    if msg != '':
        ChatLog.config(state=NORMAL)
       #response = bot_greeting(msg2)
        #ChatLog.insert(END, "Codee: " + response + '\n\n')
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 11, 'bold'))
        res = chatbot_response(msg)
        ChatLog.insert(END, "Codee: " + res + '\n\n')
        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


base = Tk()
base.title("Codee Chatbot")  # title of window

# width of window at y-axis*height of window at y-axis+ width at x-axis+height at x-axis
base.geometry("500x700+100+30")

# Create Chat window
ChatLog = Text(base, bd=0, bg="white",
               font="Arial",)
# ChatLog.config(state=DISABLED)

# upload logo codee image for chatbot
LogoPic = PhotoImage(file='Codeehappy.png')

# adding logo image on chat window
LogoPicLabel = Label(base, image=LogoPic)
LogoPicLabel.pack(pady=5)

centerFrame = Frame(base)
centerFrame.pack()

# create scrollbar
scrollbar = Scrollbar(centerFrame)
scrollbar.pack(side=RIGHT)

ChatLog = Text(centerFrame, font=('Verdana', 10, 'bold'),
               height=15, yscrollcommand=scrollbar.set, wrap='word')
ChatLog.pack(side=LEFT)

# Bind scrollbar to Chat window
scrollbar.config(command=ChatLog.yview)

# Create Button to send message
SendButton = Button(base, font=("Verdana", 12, 'bold'), text="Send", width="12", height=5,
                    bd=0, bg="#BF3EFF", activebackground="#3c9d9b", fg='#ffffff', command=send)
# Create the box to enter message
EntryBox = Text(base, bd=0, bg="white", width="50",
                height="50", font="Verdana",  wrap='word')

# bind the return/enter key to the send button
EntryBox.bind("<Return>", lambda e: send())

# Place all components on the screen
EntryBox.place(x=128, y=601, height=90, width=355)
SendButton.place(x=6, y=601, height=90)
base.mainloop()
