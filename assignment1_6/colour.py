
import tkinter as tk
from tkinter import Scale, Label, Canvas
from machinevisiontoolbox import colorspace_convert

def update_color(red, green, blue):
    hex_color = "#{:02x}{:02x}{:02x}".format(red, green, blue)
    color_display.config(bg=hex_color)
    color_label.config(text=hex_color)

    r = red / (red + green + blue)
    g = green / (red + green + blue)
    chromaticity_label.config(text="Chromaticity (r, g): ({:.2f}, {:.2f})".format(r, g))

    hsv = colorspace_convert([red/255, green/255, blue/255], "RGB", "HSV")
    hsv_label.config(text="HSV: ({:.2f}, {:.2f}, {:.2f})".format(hsv[0], hsv[1], hsv[2]))
    
app = tk.Tk()
app.title("RGB Color Mixer")
font_settings = ("Arial", 30) # Change the font and size as needed

# Sliders for Red, Green, and Blue
red_slider = Scale(app, from_=0, to=255, orient="horizontal", fg="red",
label="Red", command=lambda x: update_color(red_slider.get(), green_slider.get(),
blue_slider.get()), font=font_settings)
red_slider.pack(fill="x", padx=20, pady=10)

green_slider = Scale(app, from_=0, to=255, orient="horizontal", fg="green",
label="Green", command=lambda x: update_color(red_slider.get(), green_slider.get(),
blue_slider.get()), font=font_settings)
green_slider.pack(fill="x", padx=20, pady=10)

blue_slider = Scale(app, from_=0, to=255, orient="horizontal", fg="blue",
label="Blue", command=lambda x: update_color(red_slider.get(), green_slider.get(),
blue_slider.get()), font=font_settings)
blue_slider.pack(fill="x", padx=20, pady=10)

# Display for resulting color
color_display = Canvas(app, bg="white", height=100, width=300)
color_display.pack(pady=20)
color_label = Label(app, text="#ffffff", font=font_settings)
color_label.pack(pady=10)

# Chromaticity display
chromaticity_label = Label(app, text="", font=font_settings)
chromaticity_label.pack(pady=10)

# HSV display
hsv_label = Label(app, text="", font=font_settings)
hsv_label.pack(pady=10)

app.mainloop()
