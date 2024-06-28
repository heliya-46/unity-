import requests
import tkinter as tk
from tkinter import scrolledtext, messagebox


def fetch_competitions(api_key):
    url = 'https://api.football-data.org/v2/competitions'
    headers = {
        'X-Auth-Token': api_key
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data['competitions']
    else:
        raise Exception(f"Error: {response.status_code}, Message: {response.json().get('message', 'No message provided')}")


def on_button_click():
    api_key = api_key_entry.get()
    try:
        competitions = fetch_competitions(api_key)
        output_text.delete(1.0, tk.END) 
        for competition in competitions:
            output_text.insert(tk.END, f"Name: {competition['name']}, Country: {competition['area']['name']}\n")
    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Football Data API GUI")

api_key_label = tk.Label(root, text="API Key:")
api_key_label.pack(pady=5)
api_key_entry = tk.Entry(root, width=50)
api_key_entry.pack(pady=5)

fetch_button = tk.Button(root, text="Fetch Competitions", command=on_button_click)
fetch_button.pack(pady=10)


output_text = scrolledtext.ScrolledText(root, width=80, height=20)
output_text.pack(pady=10)

root.mainloop()
