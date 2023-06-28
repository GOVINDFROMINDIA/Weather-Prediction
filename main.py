import tkinter as tk
from tkinter import messagebox
import joblib
from tkinter.font import Font
from PIL import Image, ImageTk
import geocoder
from datetime import datetime

classifier = joblib.load('dtm.joblib')

window = tk.Tk()
window.title("Weather")
window.geometry("700x580")
window.configure(bg="#396285")

def predict_weather(event=None):
    precipitation = float(entry_precipitation.get())
    temp_max = float(entry_temp_max.get())
    temp_min = float(entry_temp_min.get())
    wind = float(entry_wind.get())

    if wind > 15:
        messagebox.showwarning("Alert", "Cyclone Alert: Heavy wind \n National Disaster Response Force (NDRF): 011-26107953")
    elif precipitation > 10:
        messagebox.showwarning("Alert", "Flood Alert: Heavy precipitation (cm) \n National Emergency Response Center (NERC): 011-26701728, 011-26701729")
    elif temp_max < -5:
        messagebox.showwarning("Alert", "Heavy Snowfall Alert: Very Low Temperature (°C) \n Tip: Stay Away from Remote Locations")
    elif temp_min > 38:
        messagebox.showwarning("Alert", "Drought Alert: Very High temperature (°C) \n Tip: Save Enough Water, don't waste it")
    else:
        prediction = classifier.predict([[precipitation, temp_max, temp_min, wind]])
        label_result.configure(text="                    Predicted weather for today is  " + prediction[0], font=("Helvetica", 20), justify="center")

def update_time():
    current_time = datetime.now().strftime("%I:%M %p")
    current_date = datetime.now().strftime("%d %B %Y")
    current_day = datetime.now().strftime("%A")
    label_datetime.config(text=f"{current_time}\n{current_date}\n{current_day}")
    window.after(1000, update_time)

heading_font = Font(family="Helvetica", size=20, weight="bold")
label_title = tk.Label(window, text="WEATHER FORECAST AND ALERT SYSTEM", font=heading_font, bg="#396285", fg="white")
label_title.pack(pady=(10, 20))

frame_inputs = tk.Frame(window, bg="#396285")
frame_inputs.pack(padx=50, pady=20, anchor="w")

label_font = Font(family="Helvetica", size=14, weight="bold")

label_precipitation = tk.Label(frame_inputs, text="Precipitation", bg="#396285", fg="white", font=label_font)
label_precipitation.grid(row=0, column=0, padx=10, sticky="w")
entry_precipitation = tk.Entry(frame_inputs)
entry_precipitation.grid(row=0, column=1)
label_unit_precipitation = tk.Label(frame_inputs, text="cm", bg="#396285", fg="white", font=label_font)
label_unit_precipitation.grid(row=0, column=2)
entry_precipitation.bind('<Return>', lambda e: entry_temp_max.focus())

label_temp_max = tk.Label(frame_inputs, text="Maximum Temperature", bg="#396285", fg="white", font=label_font)
label_temp_max.grid(row=1, column=0, padx=10, sticky="w")
entry_temp_max = tk.Entry(frame_inputs)
entry_temp_max.grid(row=1, column=1)
label_unit_temp_max = tk.Label(frame_inputs, text="°C", bg="#396285", fg="white", font=label_font)
label_unit_temp_max.grid(row=1, column=2)
entry_temp_max.bind('<Return>', lambda e: entry_temp_min.focus())

label_temp_min = tk.Label(frame_inputs, text="Minimum Temperature", bg="#396285", fg="white", font=label_font)
label_temp_min.grid(row=2, column=0, padx=10, sticky="w")
entry_temp_min = tk.Entry(frame_inputs)
entry_temp_min.grid(row=2, column=1)
label_unit_temp_min = tk.Label(frame_inputs, text="°C", bg="#396285", fg="white", font=label_font)
label_unit_temp_min.grid(row=2, column=2)
entry_temp_min.bind('<Return>', lambda e: entry_wind.focus())

label_wind = tk.Label(frame_inputs, text="Wind Speed", bg="#396285", fg="white", font=label_font)
label_wind.grid(row=3, column=0, padx=10, sticky="w")
entry_wind = tk.Entry(frame_inputs)
entry_wind.grid(row=3, column=1)
label_unit_wind = tk.Label(frame_inputs, text="mph", bg="#396285", fg="white", font=label_font)
label_unit_wind.grid(row=3, column=2)
entry_wind.bind('<Return>', predict_weather)

predict_image = Image.open("predict.png")
predict_image = predict_image.resize((150, 50), Image.LANCZOS)
predict_photo = ImageTk.PhotoImage(predict_image)

button_predict = tk.Button(window, image=predict_photo, command=predict_weather, bd=0, bg="#396285", activebackground="#396285")
button_predict.pack(pady=(0, 20), anchor="w", padx=155)

label_result = tk.Label(window, text="", bg="#396285", fg="white", font=("Helvetica", 12, "bold"), justify="center")
label_result.pack(anchor="w")

frame_black = tk.Frame(window, bg="black", height=250)
frame_black.pack(fill="both", expand=True)

g = geocoder.ip('me')

country = g.country

if country == 'IN':
    country = 'India'
current_location = g.city + ', ' + country

label_location = tk.Label(frame_black, text=current_location, bg="black", fg="white", font=("Helvetica", 36, "bold", "italic"))
label_location.pack(side="top", padx=(60, 0), pady=(0, 4))

label_datetime = tk.Label(frame_black, text="", bg="black", fg="white", font=("Helvetica", 35))
label_datetime.pack(side="top", pady=(0, 20))

update_time()

window.mainloop()
