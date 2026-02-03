import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
import csv
import os
import tempfile


def scrape_data():
    url = url_entry.get().strip()

    if url == "":
        messagebox.showwarning("Input Error", "Please enter a URL")
        return

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.find_all("article", class_="product_pod")

        if not products:
            messagebox.showerror("Error", "No data found.")
            return

        temp_dir = tempfile.gettempdir()
        file_path = os.path.join(temp_dir, "products.csv")

        with open(file_path, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["Book Name", "Price", "Rating"])

            for product in products:
                name = product.h3.a["title"]
                price = product.find("p", class_="price_color").text
                rating = product.find("p", class_="star-rating")["class"][1]
                writer.writerow([name, price, rating])

        messagebox.showinfo(
            "Success",
            f"Data saved successfully!\n\nLocation:\n{file_path}"
        )

    except Exception as e:
        messagebox.showerror("Error", str(e))


root = tk.Tk()
root.title("Web Scraping Tool")
root.geometry("480x220")

tk.Label(root, text="Web Scraping Application",
         font=("Arial", 16, "bold")).pack(pady=10)

tk.Label(root, text="Enter Website URL:").pack()

url_entry = tk.Entry(root, width=55)
url_entry.pack(pady=5)

tk.Button(root, text="Scrape Data",
          command=scrape_data,
          bg="green",
          fg="white",
          width=15).pack(pady=15)

root.mainloop()
