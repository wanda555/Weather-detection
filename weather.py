import requests
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

API_KEY = "2240e10488abbb2ea37884d12801f4bd"

def get_weather_data(city, unit):
    unit_param = 'metric' if unit == 'C' else 'imperial'
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units={unit_param}"
    try:
        response = requests.get(url)
        data = response.json()
        if data['cod'] != 200:
            raise ValueError(data['message'])
        return data
    except Exception as e:
        raise e

def update_weather():
    city = city_entry.get()
    unit = unit_var.get()
    if not city:
        messagebox.showwarning("Input Error", "Please enter a city.")
        return
    try:
        weather = get_weather_data(city, unit)
        temp = weather['main']['temp']
        desc = weather['weather'][0]['description'].title()
        icon_code = weather['weather'][0]['icon']
        wind_speed = weather['wind']['speed']
        humidity = weather['main']['humidity']

        temp_label.config(text=f"{temp} °{unit}")
        desc_label.config(text=desc)
        wind_label.config(text=f"Wind: {wind_speed} {'km/h' if unit == 'C' else 'mph'}")
        humidity_label.config(text=f"Humidity: {humidity}%")
        load_icon(icon_code)

    except Exception as e:
        messagebox.showerror("Error", f"Could not retrieve weather:\n{e}")

def load_icon(icon_code):
    try:
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        img_data = requests.get(icon_url).content
        with open("weather_icon.png", "wb") as f:
            f.write(img_data)
        img = Image.open("weather_icon.png")
        img = img.resize((100, 100))
        photo = ImageTk.PhotoImage(img)
        icon_label.config(image=photo)
        icon_label.image = photo
    except:
        icon_label.config(text="🌦")

# GUI setup
root = tk.Tk()
root.title("Weather App")
root.geometry("400x450")
root.configure(bg="#222")

# Fonts & Colors
style = {"bg": "#222", "fg": "#fff", "font": ("Segoe UI", 14)}

tk.Label(root, text="Enter City:", **style).pack(pady=(20, 5))
city_entry = tk.Entry(root, font=("Segoe UI", 14), width=25)
city_entry.pack(pady=5)

unit_var = tk.StringVar(value='C')
unit_frame = tk.Frame(root, bg="#222")
tk.Radiobutton(unit_frame, text="°C", variable=unit_var, value='C', bg="#222", fg="#fff").pack(side='left')
tk.Radiobutton(unit_frame, text="°F", variable=unit_var, value='F', bg="#222", fg="#fff").pack(side='left')
unit_frame.pack()

tk.Button(root, text="Get Weather", command=update_weather, font=("Segoe UI", 12), bg="#0f0", fg="#000").pack(pady=10)

icon_label = tk.Label(root, bg="#222")
icon_label.pack(pady=10)

temp_label = tk.Label(root, text="Temperature", **style)
temp_label.pack()

desc_label = tk.Label(root, text="Condition", **style)
desc_label.pack()

wind_label = tk.Label(root, text="Wind", **style)
wind_label.pack()

humidity_label = tk.Label(root, text="Humidity", **style)
humidity_label.pack()

root.mainloop()
