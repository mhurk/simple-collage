# Simple Collage

This tool creates a simple collage from a folder with images.
 - Set width and height of your collage. Height is more of an indication as this is adapted to get a nice filling
 - Rounds the corners a bit for a better look (I think)
 - Images are sorted by filename which is often also chronological.
 - Executable for easier use


__UI:__

![image](https://github.com/user-attachments/assets/5b27a97e-b296-4d4e-8ebf-81f684e1a406)


__Example output:__
These are some images I took with my phone, displayed in a gallery.

![image](https://github.com/mhurk/simple-collage/blob/main/collage.jpg)


Install the required packages with `pip install -r requirements.txt`

Run `pyinstaller --onefile --windowed collage_app.py --name SimpleCollage` to create the executable.
