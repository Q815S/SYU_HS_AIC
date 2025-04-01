import tkinter as tk
from tkinter import scrolledtext
import google.generativeai as genai
import textwrap
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SYU_HS = os.getenv('SYU_HS')
NEW = os.getenv('NEW')
SSK = os.getenv('SSK')
BLUE = os.getenv('BLUE')
INJ = os.getenv('INJ')
End = os.getenv('END')

genai.configure(api_key=GOOGLE_API_KEY)
Fan = input('사용자 이름을 입력해주세요: ')

system_instruction = SYU_HS + NEW + SSK + BLUE
model = genai.GenerativeModel(model_name="gemini-2.5-pro-exp-03-25", system_instruction=system_instruction)

def to_markdown(text):
    text = text.replace('•', ' *')
    return textwrap.indent(text, '> ', predicate=lambda _: True)

def send_message():
    user_message = user_input.get()
    user_input.set("")

    CL.config(state=tk.NORMAL)
    CL.tag_configure("user_right", justify='right')
    CL.insert(tk.END, Fan + f": {user_message}\n", ("user", "user_right"))
    CL.tag_config("user", foreground="black", font=default_font)
    CL.config(state=tk.DISABLED)
    CL.see(tk.END)

    try:
        if user_message == 'F':
            response = model.generate_content(End)
        else:
            response = model.generate_content(user_message)

        ai_response = response.text
        markdown_response = to_markdown(ai_response)

        CL.config(state=tk.NORMAL)
        CL.tag_configure("ai_left", justify='left')
        CL.insert(tk.END, f"수야 SUYA: {markdown_response}\n", ("ai", "ai_left"))
        CL.tag_config("ai", foreground="blue", font=default_font)
        CL.config(state=tk.DISABLED)
        CL.see(tk.END)
    except Exception as e:
        error_message = f"Error: {e}"
        CL.config(state=tk.NORMAL)
        CL.insert(tk.END, f"Error: {error_message}\n", "error")
        CL.tag_config("error", foreground="red", font=default_font)
        CL.config(state=tk.DISABLED)
        CL.see(tk.END)

root = tk.Tk()
root.title("SYU_HS_SUYA")

default_font = ("LG Smart UI Regular", 12)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

window_width = int(screen_width * 0.8)
window_height = int(screen_height * 0.8)
root.geometry(f"{window_width}x{window_height}")

CL = scrolledtext.ScrolledText(root, wrap=tk.WORD, state=tk.DISABLED, font=default_font)
CL.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

input_frame = tk.Frame(root)
input_frame.pack(padx=10, pady=5, fill=tk.X)

user_input = tk.StringVar()
input_box = tk.Entry(input_frame, textvariable=user_input, font=default_font)
input_box.pack(side=tk.LEFT, fill=tk.X, expand=True)

send_button = tk.Button(input_frame, text="보내기", command=send_message, font=default_font)
send_button.pack(side=tk.RIGHT)

root.bind('<Return>', lambda event=None: send_button.invoke())

root.mainloop()
