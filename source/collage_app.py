from PIL import Image, ImageDraw, ExifTags
import os

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk

import webbrowser

padding = 5         # Space between images in the collage
corner_radius = 20  # Radius for rounded corners
min_dimension = 10  # Minimum width or height to prevent resizing errors

def rotate_image_based_on_exif(img):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = img._getexif()
        if exif is not None:
            orientation_value = exif.get(orientation)
            if orientation_value == 3:
                img = img.rotate(180, expand=True)
            elif orientation_value == 6:
                img = img.rotate(270, expand=True)
            elif orientation_value == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass
    return img

def resize_image_proportionally(img, target_height):
    aspect_ratio = img.width / img.height
    new_width = int(target_height * aspect_ratio)
    resized_img = img.resize((new_width, target_height), Image.LANCZOS)
    return resized_img

def add_rounded_corners(img, radius):
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rounded_rectangle((0, 0, img.width, img.height), radius, fill=255)
    rounded_img = img.copy()
    rounded_img.putalpha(mask)
    return rounded_img

def create_collage_with_adjusted_height(images, output_filename, collage_width, padding, corner_radius):
    num_images = len(images)
    
    # Calculate an optimal number of columns and rows based on the total images and collage width
    columns = max(1, min(num_images, collage_width // 150))  # Roughly estimate columns based on 150 pixels width per image
    row_height = (collage_width - padding * (columns + 1)) // columns  # Fixed height per row

    # Arrange images into rows, and calculate the exact required height
    all_rows = []
    current_row = []
    current_row_width = 0

    for img in images:
        resized_img = resize_image_proportionally(img, row_height)
        rounded_img = add_rounded_corners(resized_img, corner_radius)

        if current_row_width + resized_img.width + padding > collage_width and current_row:
            all_rows.append((current_row, current_row_width))
            current_row = []
            current_row_width = 0

        current_row.append((rounded_img, resized_img.width))
        current_row_width += resized_img.width + padding

    if current_row:
        all_rows.append((current_row, current_row_width))

    # Calculate the exact collage height based on the number of rows
    required_collage_height = (row_height + padding) * len(all_rows) + padding
    collage_image = Image.new("RGB", (collage_width, required_collage_height), "black")

    # Place each row in the collage with center alignment
    y = padding
    images_used = 0

    for row_images, row_width in all_rows:
        x = (collage_width - row_width) // 2  # Center-align the row horizontally

        for r_img, _ in row_images:
            collage_image.paste(r_img, (x, y), r_img)
            x += r_img.width + padding
            images_used += 1

        y += row_height + padding

    # Save and show the final collage
    collage_image.save(output_filename)
    collage_image.show()

    # Print the number of images used
    print(f"Total images used in collage: {images_used}")

def select_folder():
    folder = filedialog.askdirectory()
    folder_entry.delete(0, tk.END)
    folder_entry.insert(0, folder)

def create_collage():
    try:
        width = int(width_entry.get())
        height = int(height_entry.get())
        folder_path = folder_entry.get()

        if not os.path.isdir(folder_path):
            messagebox.showerror("Error", "Please select a valid folder")
            return

        images = []
        for filename in os.listdir(folder_path):
            if filename.endswith((".jpg", ".jpeg", ".png", ".bmp")):
                img_path = os.path.join(folder_path, filename)
                img = Image.open(img_path)
                rotated_img = rotate_image_based_on_exif(img)
                images.append(rotated_img)

        if images:
            create_collage_with_adjusted_height(images, "collage.jpg", width, padding, corner_radius)
            messagebox.showinfo("Success", "Collage created successfully!")
        else:
            messagebox.showwarning("Warning", "No images found in the selected folder.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

app = tk.Tk()
app.title("Simple Collage Creator")

# Set the initial size of the window
app.geometry("600x300")  # Width x Height

# Add a descriptive text label at the top
title_label = tk.Label(app, text="Simple Image Collage Creator", font=("Arial", 12, "bold"))
title_label.grid(row=0, column=0, columnspan=3, pady=10)

# Add detailed instructions
info = (
    "Enter the width and height for the collage. Height is a bit of an indication, it will be adapted\n"
    "based on the number of images. Images will be proportionally resized but not stretched nor cropped.\n"
)
instructions_label = tk.Label(app, text=info, justify="left")
instructions_label.grid(row=1, column=0, columnspan=3, pady=5, padx=10)

# Create input fields for dimensions and folder selection
tk.Label(app, text="Collage Width:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
width_entry = tk.Entry(app)
width_entry.grid(row=2, column=1, padx=5, pady=5)
width_entry.insert(0, "1920")  # Default width

tk.Label(app, text="Collage Height:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
height_entry = tk.Entry(app)
height_entry.grid(row=3, column=1, padx=5, pady=5)
height_entry.insert(0, "1080")  # Default height

tk.Label(app, text="Select Folder:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
folder_entry = tk.Entry(app, width=30)
folder_entry.grid(row=4, column=1, padx=5, pady=5)
folder_button = tk.Button(app, text="Browse", command=select_folder)
folder_button.grid(row=4, column=2, padx=5, pady=5)

# Create Collage button
create_button = tk.Button(app, text="Create Collage", command=create_collage, font=("Arial", 10))
create_button.grid(row=5, column=1, pady=15)

# Function to open a URL
def open_link(event):
    webbrowser.open_new("https://github.com/mhurk/simple-collage")

# Add a small footer label at the bottom and make it a clickable link
footer_label = tk.Label(app, text="Version 0.1 - Source code on Github", font=("Arial", 8), fg="grey", cursor="hand2")
footer_label.grid(row=6, column=0, columnspan=3, pady=10)

# Bind the label to the open_link function
footer_label.bind("<Button-1>", open_link)

app.mainloop()
