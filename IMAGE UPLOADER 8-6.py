# the application gives the user an additional option to search for images online and upload them as profile pictures
# here the users are not limited to a few options but a wider variety from the internet at the same time


import urllib.request
import urllib.parse
import webbrowser
from tkinter import *
from tkinter import filedialog
from bs4 import BeautifulSoup
from PIL import Image, ImageTk

# Function to get user input for text description


def user_search():
    search_query = input("Enter text description: ")
    return urllib.parse.quote(search_query)

# Function to search for images on Google


def search_images():
    url_to_search = f'https://www.google.com/search?q={user_search()}&tbm=isch'
    headers = {'User-Agent': 'Mozilla/5.0'}
    request = urllib.request.Request(url_to_search, headers=headers)
    response = urllib.request.urlopen(request)
    soup = BeautifulSoup(response, 'html.parser')
    images = soup.find_all('img')
    image_urls = []
    for img in images:
        try:
            image_urls.append(img['src'])
        except KeyError:
            pass
    return image_urls[:5]

# Function to display images in a new browser tab


def display_images(image_urls):
    for i in range(len(image_urls)):
        webbrowser.open_new_tab(image_urls[i])

# Function to select image file for upload


def select_file():
    file_path = filedialog.askopenfilename()
    return file_path

# Function to upload selected image to profile picture slot


def upload_image():
    file_path = select_file()
    # code to upload file to profile picture slot
    image = Image.open(file_path)
    image = image.resize((100, 100), Image.ANTIALIAS)
    photo = ImageTk.PhotoImage(image)
    canvas.delete('all')
    canvas.create_image(0, 0, image=photo, anchor='nw')
    canvas.image = photo  # to prevent garbage collection

# Tkinter GUI setup


root = Tk()
root.geometry('400x400')
root.title('Profile Picture Uploader')

# Frame for profile picture slot
frame = Frame(root)
frame.pack(pady=50)

# Canvas for profile picture slot
canvas = Canvas(frame, width=100, height=100)
canvas.pack(fill=BOTH, expand=True)

# Button to search for images
search_button = Button(root, text='Search Images', command=lambda: display_images(search_images()))
search_button.pack(side=BOTTOM, pady=10)

# Button to upload image
upload_button = Button(root, text='Upload Image', command=upload_image)
upload_button.pack(side=BOTTOM, pady=10)

root.mainloop()
