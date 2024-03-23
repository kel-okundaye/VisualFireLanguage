import tkinter as tk
from PIL import Image, ImageTk

from Visual_Language import place_images_for_word


def setup_gui(root):
    """
    Sets up the GUI components including the input field, process button, and image display label.
    :param root: The Tkinter root window.
    """
    global entry, img_label  # Declare global variables for entry and image label to access them across functions

    # Entry widget for user input
    entry = tk.Entry(root)
    entry.pack()

    # Button that triggers the image processing function
    process_button = tk.Button(root, text="Process Word", command=process_word)
    process_button.pack()

    # Label to display the resulting image
    img_label = tk.Label(root)
    img_label.pack()


def process_word():
    """
    Processes the input word and updates the GUI with the resulting image.
    """
    # Load the base image whenever process_word is called to ensure it's fresh
    base_image = Image.open('Main_Base_Test.png')

    # Get the word from the entry widget
    retrieve_word = entry.get()

    # Turn word to lowercase
    word = retrieve_word.lower()

    # Generate the image based on the input word
    result_image = place_images_for_word(base_image, word, (1000, 1000))

    # Resize the resulting image to fit in the GUI window
    display_size = (500, 500)  # Set the display size to fit within the window
    resized_image = result_image.resize(display_size, Image.Resampling.LANCZOS)

    # Convert the resized image for Tkinter compatibility and display it
    img = ImageTk.PhotoImage(resized_image)
    img_label.config(image=img)
    img_label.image = img  # Keep a reference to avoid garbage collection


def main():
    """
    Initializes and runs the Tkinter GUI application.
    """
    # Initialize the root Tkinter window
    root = tk.Tk()
    root.title("Word to Image Converter")  # Set the window title
    root.geometry("550x550")  # Set the window size to 550x550 pixels

    # Set up the GUI layout
    setup_gui(root)

    # Run the Tkinter event loop
    root.mainloop()


if __name__ == "__main__":
    main()
