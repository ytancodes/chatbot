import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, Toplevel
import pickle
import subprocess
import webbrowser  # Import the webbrowser module

# Initialize an empty knowledge dictionary
knowledge = {}

# Initialize the current mode (0 for Teach, 1 for Chat)
current_mode = 0

# Function to load knowledge from a file
def load_knowledge():
    try:
        with open('knowledge.pickle', 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

# Function to save knowledge to a file
def save_knowledge():
    with open('knowledge.pickle', 'wb') as f:
        pickle.dump(knowledge, f)

# Function to export tokens to a file
def export_tokens():
    try:
        with open('exported_tokens.txt', 'w') as f:
            for question, answer in knowledge.items():
                f.write(f"Question: {question}\nAnswer: {answer}\n\n")
        messagebox.showinfo("Export Successful", "Tokens exported to 'exported_tokens.txt'")
    except Exception as e:
        messagebox.showerror("Export Error", f"An error occurred while exporting tokens: {str(e)}")

# Function to update the chat log
def update_chat_log(message):
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, message + '\n')
    chat_log.config(state=tk.DISABLED)
    chat_log.see(tk.END)  # Scroll to the bottom of the chat log

# Function to import tokens from a file
def import_tokens():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            with open(file_path, 'r') as f:
                lines = f.read().split('\n\n')
                for line in lines:
                    if line.startswith("Question:") and "Answer:" in line:
                        parts = line.split('\n')
                        question = parts[0].replace("Question:", "").strip()
                        answer = parts[1].replace("Answer:", "").strip()
                        knowledge[question] = answer
            update_chat_log("Tokens imported successfully.")
            update_token_count()
        except Exception as e:
            messagebox.showerror("Import Error", f"An error occurred while importing tokens: {str(e)}")

# Function to toggle between Teach and Chat modes
def toggle_mode():
    global current_mode
    current_mode = 1 - current_mode  # Toggle between 0 and 1
    update_ui()

# Function to update the UI based on the current mode
def update_ui():
    if current_mode == 0:
        mode_label.config(text="Teaching Mode")
        chat_button.config(state=tk.DISABLED)
        teach_button.config(state=tk.NORMAL)
        question_entry.config(state=tk.NORMAL)
        answer_entry.config(state=tk.NORMAL)
    else:
        mode_label.config(text="Chat Mode")
        chat_button.config(state=tk.NORMAL)
        teach_button.config(state=tk.DISABLED)
        question_entry.config(state=tk.DISABLED)
        answer_entry.config(state=tk.DISABLED)

# Function to clear the chat log
def clear_chat_log():
    chat_log.config(state=tk.NORMAL)
    chat_log.delete(1.0, tk.END)
    chat_log.config(state=tk.DISABLED)

# Create a function to teach the chatbot
def teach():
    question = question_entry.get()
    answer = answer_entry.get()
    knowledge[question] = answer
    save_knowledge()  # Save the knowledge to a file
    update_chat_log(f"Teaching: {question} => {answer}")
    update_token_count()
    question_entry.delete(0, tk.END)
    answer_entry.delete(0, tk.END)

# Create a function to chat with the chatbot
def chat():
    user_input = user_input_entry.get()
    response = knowledge.get(user_input, "I don't know the answer to that.")
    
    if response == "I don't know the answer to that.":
        # If the bot doesn't have an answer, display a message and prompt an alert
        update_chat_log(f"User: {user_input}\nBot: I don't know the answer to that.")
        
        # Prompt an alert message with a "Lookup" button
        result = messagebox.askquestion("Lookup", "I don't know the answer to that.\nDo you want to perform a web search?")
        if result == "yes":
            # Open a web search in the default web browser
            search_url = f"https://www.google.com/search?q={user_input}"
            webbrowser.open_new_tab(search_url)
    else:
        # Otherwise, display the bot's response
        update_chat_log(f"User: {user_input}\nBot: {response}")

    user_input_entry.delete(0, tk.END)

# Function to launch TRES 2.0
def launch_tres():
    try:
        subprocess.Popen(["C:\\Projects\\Automation\\dist\\TRES0911.exe"])
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while launching TRES 2.0: {str(e)}")

# Function to update the token count
def update_token_count():
    tokens_label.config(text=f"Tokens Learned: {len(knowledge)}")

# Function to confirm app exit
def on_closing():
    result = messagebox.askquestion("Confirm Exit", "Please export Tokens before closing the app since Bot knowledge will not survive after PC is restarted.\nProceed Closing App?")
    if result == "yes":
        window.destroy()

# Function to open the Read Me window
def open_readme():
    readme_window = Toplevel(window)
    readme_window.title("Read Me")
    
    # Add labels or text widgets with your Read Me content
    readme_label = tk.Label(readme_window, text="Welcome to the Chatbot App!", font=("Helvetica", 16))
    readme_label.pack(padx=20, pady=10)
    
    readme_text = tk.Text(readme_window, wrap=tk.WORD, bg="black", fg="black", width=40, height=10)
    readme_text.insert(tk.END, "This app allows you to teach and chat with a chatbot.\n\n")
    readme_text.insert(tk.END, "In Teaching Mode, you can add questions and answers to train the chatbot.\n")
    readme_text.insert(tk.END, "In Chat Mode, you can chat with the chatbot using the knowledge you've provided.\n\n")
    readme_text.insert(tk.END, "Feel free to explore the features!\n\n")
    readme_text.pack(padx=20, pady=10)

# Create a GUI window
window = tk.Tk()

# Set the title of the window
window.title("SONI Ver09262023")

# Specify the icon file path
icon_path = "/Users/ytanmac/Downloads/soni9/Tesla1.png"  # Update with your actual path

# Use the iconbitmap method to set the icon
from tkinter import PhotoImage
icon = PhotoImage(file=icon_path)
window.iconphoto(True, icon)


# Set background color to black
window.configure(bg="black")

# Create frames to organize widgets
frame_top = tk.Frame(window, bg="black")
frame_top.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

frame_middle = tk.Frame(window, bg="black")
frame_middle.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

frame_bottom = tk.Frame(window, bg="black")
frame_bottom.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Mode label
mode_label = tk.Label(frame_top, text="Teaching Mode", font=("Helvetica", 14), bg="black", fg="yellow")
mode_label.pack(pady=10)

# Tokens learned label (in the upper part)
tokens_label = tk.Label(frame_top, text="Tokens Learned: 0", font=("Helvetica", 12), bg="black", fg="yellow")
tokens_label.pack(pady=10)

# Create a frame for the chat display
chat_frame = tk.Frame(frame_middle, bg="black")
chat_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Chat log
chat_log = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, bg="black", fg="yellow")
chat_log.pack(fill=tk.BOTH, expand=True)

# Create a frame for input
input_frame = tk.Frame(frame_bottom, bg="black")
input_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

# Entry field for chatting or teaching
user_input_entry = tk.Entry(input_frame, font=("Helvetica", 16), bg="black", fg="yellow")
user_input_entry.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

# Chat and Teach buttons
chat_button = tk.Button(input_frame, text="Chat", font=("Helvetica", 16), command=chat, bg="black", fg="yellow")
chat_button.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
teach_button = tk.Button(input_frame, text="Teach", font=("Helvetica", 16), command=teach, bg="black", fg="yellow")
teach_button.grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

# Entry fields for questions and answers during teaching
question_label = tk.Label(frame_bottom, text="Question:", font=("Helvetica", 16), bg="black", fg="yellow")
question_label.grid(row=1, column=0, padx=10, pady=(20, 5), sticky="w")
question_entry = tk.Entry(frame_bottom, font=("Helvetica", 16), bg="black", fg="yellow")
question_entry.grid(row=1, column=1, padx=10, pady=(20, 5), sticky="nsew")
answer_label = tk.Label(frame_bottom, text="Answer:", font=("Helvetica", 16), bg="black", fg="yellow")
answer_label.grid(row=2, column=0, padx=10, pady=(5, 20), sticky="w")
answer_entry = tk.Entry(frame_bottom, font=("Helvetica", 16), bg="black", fg="yellow")
answer_entry.grid(row=2, column=1, padx=10, pady=(5, 20), sticky="nsew")

# Create a frame for buttons in one row
button_frame = tk.Frame(frame_bottom, bg="black")
button_frame.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

# Clear button
clear_button = tk.Button(button_frame, text="Clear", font=("Helvetica", 12), command=clear_chat_log, bg="green", fg="yellow")
clear_button.grid(row=0, column=0, padx=5, sticky="nsew")

# Toggle Mode button
toggle_mode_button = tk.Button(button_frame, text="Toggle Mode", font=("Helvetica", 12), command=toggle_mode, bg="black", fg="yellow")
toggle_mode_button.grid(row=0, column=1, padx=5, sticky="nsew")

# Export Tokens button
export_tokens_button = tk.Button(button_frame, text="Export Tokens", font=("Helvetica", 12), command=export_tokens, bg="black", fg="yellow")
export_tokens_button.grid(row=0, column=2, padx=5, sticky="nsew")

# Import Tokens button
import_tokens_button = tk.Button(button_frame, text="Import Tokens", font=("Helvetica", 12), command=import_tokens, bg="black", fg="yellow")
import_tokens_button.grid(row=0, column=3, padx=5, sticky="nsew")

# TRES 2.0 button
launch_tres_button = tk.Button(button_frame, text="TRES 2.0", font=("Helvetica", 12), command=launch_tres, bg="black", fg="yellow")
launch_tres_button.grid(row=0, column=4, padx=5, sticky="nsew")

# Add a "Read Me" button to your main GUI
readme_button = tk.Button(button_frame, text="Read Me", font=("Helvetica", 12), command=open_readme, bg="black", fg="yellow")
readme_button.grid(row=0, column=5, padx=5, sticky="nsew")

# Load knowledge from a file if available
knowledge = load_knowledge()
update_token_count()

# Initial UI setup
update_ui()

# Bind the on_closing function to the window's close button
window.protocol("WM_DELETE_WINDOW", on_closing)

# Start the GUI main loop
window.mainloop()
