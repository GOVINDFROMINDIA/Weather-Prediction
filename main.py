import tkinter as tk
from tkinter import messagebox
import joblib
from tkinter.font import Font
from PIL import Image, ImageTk
import geocoder

classifier = joblib.load('dtm.joblib')

window = tk.Tk()
window.title("Weather")
window.geometry("800x500")
window.configure(bg="#396285")

def predict_weather(event=None):
    precipitation = float(entry_precipitation.get())
    temp_max = float(entry_temp_max.get())
    temp_min = float(entry_temp_min.get())
    wind = float(entry_wind.get())

    if wind > 10:
        messagebox.showinfo("Alert", "Cyclone Alert: Heavy wind above 10")
    elif precipitation > 8:
        messagebox.showinfo("Alert", "Flood Alert: Heavy precipitation above 8")
    elif temp_max < 10:
        messagebox.showinfo("Alert", "Snowfall Alert: Max temperature below 10")
    elif temp_min > 40:
        messagebox.showinfo("Alert", "Drought Alert: Min temperature above 40")
    else:
        prediction = classifier.predict([[precipitation, temp_max, temp_min, wind]])
        label_result.configure(text="Predicted weather: " + prediction[0])

heading_font = Font(family="Helvetica", size=20, weight="bold")
label_title = tk.Label(window, text="WEATHER PREDICTION USING DECISION TREE", font=heading_font, bg="#396285", fg="white")
label_title.pack(pady=(10, 20))

frame_inputs = tk.Frame(window, bg="#396285")
frame_inputs.pack(padx=50, pady=20, anchor="w")

label_precipitation = tk.Label(frame_inputs, text="Precipitation", bg="#396285", fg="white")
label_precipitation.grid(row=0, column=0, padx=10, sticky="w")
entry_precipitation = tk.Entry(frame_inputs)
entry_precipitation.grid(row=0, column=1)
entry_precipitation.bind('<Return>', lambda e: entry_temp_max.focus())

label_temp_max = tk.Label(frame_inputs, text="Maximum Temperature", bg="#396285", fg="white")
label_temp_max.grid(row=1, column=0, padx=10, sticky="w")
entry_temp_max = tk.Entry(frame_inputs)
entry_temp_max.grid(row=1, column=1)
entry_temp_max.bind('<Return>', lambda e: entry_temp_min.focus())

label_temp_min = tk.Label(frame_inputs, text="Minimum Temperature", bg="#396285", fg="white")
label_temp_min.grid(row=2, column=0, padx=10, sticky="w")
entry_temp_min = tk.Entry(frame_inputs)
entry_temp_min.grid(row=2, column=1)
entry_temp_min.bind('<Return>', lambda e: entry_wind.focus())

label_wind = tk.Label(frame_inputs, text="Wind Speed", bg="#396285", fg="white")
label_wind.grid(row=3, column=0, padx=10, sticky="w")
entry_wind = tk.Entry(frame_inputs)
entry_wind.grid(row=3, column=1)
entry_wind.bind('<Return>', predict_weather)

predict_image = Image.open("predict.png")
predict_image = predict_image.resize((150, 50), Image.LANCZOS)
predict_photo = ImageTk.PhotoImage(predict_image)

button_predict = tk.Button(window, image=predict_photo, command=predict_weather, bd=0, bg="#396285", activebackground="#396285")
button_predict.pack(pady=(0, 20), anchor="w", padx=155)

label_result = tk.Label(window, text="", bg="#396285", fg="white", font=("Helvetica", 12))
label_result.pack(anchor="w")

frame_black = tk.Frame(window, bg="black", height=250)
frame_black.pack(fill="both", expand=True)

g = geocoder.ip('me')
current_location = g.city + ', ' + g.country
country = g.country

if country == 'IN':
    country = 'India'

label_location = tk.Label(frame_black, text=country, bg="black", fg="white", font=("Helvetica", 36, "bold", "italic"))
label_location.pack(side="bottom", pady=(20, 10))

label_location = tk.Label(frame_black, text=current_location, bg="black", fg="white", font=("Helvetica", 24, "bold", "italic"))
label_location.pack(side="bottom", pady=(20, 10))

window.mainloop()
