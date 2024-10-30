import tkinter as tk
from tkinter import filedialog, Label, messagebox
from PIL import Image, ImageTk
import requests
import os

# FastAPI server endpoint
API_URL = "http://localhost:8000/predict"

class WheatDiseaseDetectionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Wheat Disease Detection")
        self.root.geometry("600x400")

        # Label to display selected image
        self.image_label = Label(root)
        self.image_label.pack(pady=10)

        # Label to display prediction results
        self.result_label = Label(root, text="", font=("Arial", 14))
        self.result_label.pack(pady=20)

        # Button to select an image
        select_button = tk.Button(root, text="Select Image", command=self.select_image)
        select_button.pack(pady=10)

    def select_image(self):
        # Open a file dialog to select an image file
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg *.png *.jpeg")])
        if not file_path:
            return

        # Load and display the image
        image = Image.open(file_path)
        image = image.resize((250, 250))  # Resize for display
        img_tk = ImageTk.PhotoImage(image)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

        # Send image to FastAPI for prediction
        self.predict(file_path)

    def predict(self, file_path):
        try:
            # Send image to the FastAPI server for prediction
            with open(file_path, "rb") as image_file:
                response = requests.post(API_URL, files={"file": image_file})

            # Check if the response is successful
            if response.status_code == 200:
                result = response.json()
                predicted_class = result["class"]
                confidence = result["confidence"] * 100  # Convert to percentage
                self.result_label.config(text=f"Prediction: {predicted_class}\nConfidence: {confidence:.2f}%")
            else:
                self.show_error("Prediction failed. Server returned an error.")
        except requests.exceptions.RequestException as e:
            self.show_error(f"Request failed: {e}")
        except Exception as e:
            self.show_error(f"An unexpected error occurred: {e}")

    def show_error(self, message):
        # Display an error message in a dialog
        messagebox.showerror("Error", message)
        self.result_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = WheatDiseaseDetectionApp(root)
    root.mainloop()
