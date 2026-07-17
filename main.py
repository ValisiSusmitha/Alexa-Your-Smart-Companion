from tkinter import *
from PIL import Image, ImageTk

import speech_to_text
import action

# ---------------- Window ---------------- #

root = Tk()
root.title("Alexa - Your Smart Companion")
root.geometry("550x675")
root.resizable(False, False)

# ---------------- Background ---------------- #

try:
    bg_image = Image.open("w.jpeg")
except Exception:
    # fallback to a plain background if file not found
    bg_image = Image.new("RGB", (550, 675), color=(0, 22, 35))
bg_image = bg_image.resize((550, 675), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = Canvas(root, width=550, height=675)
canvas.pack(fill="both", expand=True)

canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# ---------------- Ask Function ---------------- #

def ask():

    try:
        user_val = speech_to_text.speech_to_text()
    except Exception as e:
        print("Error during speech input:", e)
        text.insert(END, "ERROR: Could not capture voice input: " + str(e) + "\n")
        return

    if user_val == "":
        return

    try:
        bot_val = action.Action(user_val)
    except Exception as e:
        print("Error in Action:", e)
        text.insert(END, "User ---> " + user_val + "\n")
        text.insert(END, "ERROR: Action failed: " + str(e) + "\n\n")
        return

    text.insert(END, "User ---> " + user_val + "\n")

    if bot_val is not None:
        text.insert(END, "BOT <--- " + str(bot_val) + "\n\n")

    if bot_val == "ok sir":
        root.destroy()


# ---------------- Send Function ---------------- #

def send(event=None):

    send_val = entry.get()

    if send_val == "":
        return

    try:
        bot_val = action.Action(send_val)
    except Exception as e:
        print("Error in Action:", e)
        text.insert(END, "User ---> " + send_val + "\n")
        text.insert(END, "ERROR: Action failed: " + str(e) + "\n\n")
        entry.delete(0, END)
        return

    text.insert(END, "User ---> " + send_val + "\n")

    if bot_val is not None:
        text.insert(END, "BOT <--- " + str(bot_val) + "\n\n")

    if bot_val == "ok sir":
        root.destroy()

    entry.delete(0, END)


# ---------------- Clear Chat ---------------- #

def del_text():

    text.delete("1.0", END)


# ---------------- Images ---------------- #

try:
    top_left_image = Image.open("Va.jpg")
except Exception:
    top_left_image = Image.new("RGBA", (60, 60), color=(255, 255, 255, 0))
top_left_photo = ImageTk.PhotoImage(top_left_image)

canvas.create_image(
    20,
    20,
    image=top_left_photo,
    anchor="nw"
)

try:
    second_image = Image.open("hello.jpeg")
except Exception:
    second_image = Image.new("RGBA", (60, 60), color=(255, 255, 255, 0))
second_photo = ImageTk.PhotoImage(second_image)

canvas.create_image(
    20,
    80,
    image=second_photo,
    anchor="nw"
)

# ---------------- Chat Box ---------------- #

text = Text(
    root,
    font=("Courier", 10, "bold"),
    bg="#000E1E",
    fg="white",
    bd=0,
    highlightthickness=0
)

canvas.create_window(
    275,
    350,
    window=text,
    width=350,
    height=200
)

# ---------------- Entry ---------------- #

entry = Entry(
    root,
    justify=CENTER,
    font=("Arial", 12)
)

canvas.create_window(
    275,
    520,
    window=entry,
    width=350,
    height=30
)

# ---------------- Button Images ---------------- #

try:
    ask_image = Image.open("v.jpg")
    ask_image = ask_image.resize((50, 50), Image.LANCZOS)
except Exception:
    ask_image = Image.new("RGBA", (50, 50), color=(255, 255, 255, 0))
ask_photo = ImageTk.PhotoImage(ask_image)

try:
    send_image = Image.open("send.png")
    send_image = send_image.resize((50, 50), Image.LANCZOS)
except Exception:
    send_image = Image.new("RGBA", (50, 50), color=(255, 255, 255, 0))
send_photo = ImageTk.PhotoImage(send_image)

try:
    delete_image = Image.open("del.jpg")
    delete_image = delete_image.resize((50, 50), Image.LANCZOS)
except Exception:
    delete_image = Image.new("RGBA", (50, 50), color=(255, 255, 255, 0))
delete_photo = ImageTk.PhotoImage(delete_image)

# ---------------- Buttons ---------------- #

ask_button = Button(
    root,
    image=ask_photo,
    bg="#001623",
    borderwidth=0,
    relief=SOLID,
    command=ask,
    highlightthickness=0
)

canvas.create_window(
    100,
    600,
    window=ask_button
)

send_button = Button(
    root,
    image=send_photo,
    bg="#001623",
    borderwidth=0,
    relief=SOLID,
    command=send,
    highlightthickness=0
)

canvas.create_window(
    450,
    600,
    window=send_button
)

delete_button = Button(
    root,
    image=delete_photo,
    bg="#001623",
    borderwidth=0,
    relief=SOLID,
    command=del_text,
    highlightthickness=0
)

canvas.create_window(
    275,
    600,
    window=delete_button
)

# ---------------- Enter Key ---------------- #

root.bind("<Return>", send)

# ---------------- Run ---------------- #

root.mainloop()