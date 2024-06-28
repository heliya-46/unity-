import requests

import tkinter as tk

from tkinter import scrolledtext, messagebox, ttk




API_KEY = '7c8b154f9c034867a3c3f30c38b8e9d3' 



def jls_extract_def():
    return API_KEY


def fetch_competitions():

    url = 'https://api.football-data.org/v2/competitions'

    headers = {

        'X-Auth-Token': jls_extract_def()

    }

    try:

        response = requests.get(url, headers=headers)

        response.raise_for_status()  

        data = response.json()

        print("Fetched competitions successfully")  

        return data['competitions']

    except requests.exceptions.HTTPError as http_err:

        messagebox.showerror("HTTP error", f"HTTP error occurred: {http_err}\nStatus Code: {response.status_code}")

    except Exception as err:

        messagebox.showerror("Error", f"Other error occurred: {err}")

    return []




def fetch_competition_details(competition_id):

    url = f'https://api.football-data.org/v2/competitions/{competition_id}'

    headers = {

        'X-Auth-Token': API_KEY

    }

    try:

        response = requests.get(url, headers=headers)

        response.raise_for_status() 

        print("Fetched competition details successfully") 

        return response.json()

    except requests.exceptions.HTTPError as http_err:

        messagebox.showerror("HTTP error", f"HTTP error occurred: {http_err}\nStatus Code: {response.status_code}")

    except Exception as err:

        messagebox.showerror("Error", f"Other error occurred: {err}")

    return {}



def on_fetch_and_show_button_click():

    try:

        global competitions

        competitions = fetch_competitions()

        competition_names = [comp['name'] for comp in competitions]

        competition_dropdown['values'] = competition_names
        

        selected_competition = competition_dropdown.get()

        if selected_competition:

            competition_id = next(comp['id'] for comp in competitions if comp['name'] == selected_competition)

            details = fetch_competition_details(competition_id)

            output_text.delete(1.0, tk.END) 

            output_text.insert(tk.END, f"Name: {details['name']}\n")

            output_text.insert(tk.END, f"Area: {details['area']['name']}\n")

            output_text.insert(tk.END, f"Start Date: {details['currentSeason']['startDate']}\n")

            output_text.insert(tk.END, f"End Date: {details['currentSeason']['endDate']}\n")

            output_text.insert(tk.END, f"Current Matchday: {details['currentSeason']['currentMatchday']}\n")

            output_text.insert(tk.END, f"Number of Available Seasons: {details['numberOfAvailableSeasons']}\n")

            output_text.insert(tk.END, f"Last Updated: {details['lastUpdated']}\n")

        else:

            messagebox.showwarning("Warning", "Please select a competition from the dropdown.")

    except Exception as e:

        messagebox.showerror("Error", str(e))




root = tk.Tk()

root.title("Football Data API GUI")


competition_dropdown = ttk.Combobox(root, width=50)

competition_dropdown.pack(pady=10)



fetch_and_show_button = tk.Button(root, text="Fetch and Show Competition Details", command=on_fetch_and_show_button_click)

fetch_and_show_button.pack(pady=10)



output_text = scrolledtext.ScrolledText(root, width=80, height=20)

output_text.pack(pady=10)



root.mainloop()

