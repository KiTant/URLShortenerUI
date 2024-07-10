import customtkinter as ctk
import pyshorteners

# Set the appearance and theme of the application
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set up the main window properties
        self.title("URL Shortener")
        self.geometry("1100x250")
        self.resizable(False, False)

        # Initialize pyshorteners
        self.shortener = pyshorteners.Shortener()
        self.shortened_url = None
        self.expanded_url = None

        # Initialize the UI components
        self._initialize_components()

    def _initialize_components(self):
        # URL entry
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Your URL goes here", width=400)
        self.url_entry.pack(pady=25)

        # URL shorteners option menu
        self.url_shorteners = ctk.CTkOptionMenu(self, values=['clckru', 'tinyurl', 'osdb'])
        self.url_shorteners.pack()

        # Button to generate short URL
        self.generate_short_url_button = ctk.CTkButton(self, text="Generate Short URL", command=self.generate_short_url)
        self.generate_short_url_button.place(x=50, y=111)

        # Button to copy short URL
        self.copy_short_url_button = ctk.CTkButton(self, text="Copy Short URL", command=lambda: self.copy_url(self.shortened_url))
        self.copy_short_url_button.place(x=50, y=173)

        # Button to expand short URL
        self.expand_short_url_button = ctk.CTkButton(self, text="Expand Short URL", command=self.expand_url)
        self.expand_short_url_button.place(x=800, y=111)

        # Label to show the short URL
        self.short_url_label = ctk.CTkLabel(self, text="Shortened URL: Nothing to show here now", fg_color="transparent", font=ctk.CTkFont(family="Arial", size=14))
        self.short_url_label.place(x=50, y=141)

        # Label to show the expanded URL
        self.expand_url_label = ctk.CTkLabel(self, text="Expanded URL: Nothing to show here now", fg_color="transparent", font=ctk.CTkFont(family="Arial", size=14))
        self.expand_url_label.place(x=700, y=141)

        # Button to copy expanded URL
        self.copy_expand_url_button = ctk.CTkButton(self, text="Copy Expanded URL", command=lambda: self.copy_url(self.expanded_url))
        self.copy_expand_url_button.place(x=800, y=173)

    def generate_short_url(self):
        url = self.url_entry.get()
        shortener_service = self.url_shorteners.get()
        try:
            self.shortened_url = getattr(self.shortener, shortener_service).short(url)
            self.short_url_label.configure(text=f"Shortened URL: {self.shortened_url}")
        except pyshorteners.exceptions.BadURLException:
            self.short_url_label.configure(text="Shortened URL: Error, please enter a valid URL")
        except pyshorteners.exceptions.ShorteningErrorException:
            self.short_url_label.configure(text="Shortened URL: Error, could not shorten the URL")

    def expand_url(self):
        url = self.url_entry.get()
        expander_service = self.url_shorteners.get()
        try:
            self.expanded_url = getattr(self.shortener, expander_service).expand(url)
            self.expand_url_label.configure(text=f"Expanded URL: {self.expanded_url}")
        except pyshorteners.exceptions.BadURLException:
            self.expand_url_label.configure(text="Expanded URL: Error, please enter a valid URL")
        except pyshorteners.exceptions.ExpansionErrorException:
            self.expand_url_label.configure(text="Expanded URL: Error, could not expand the URL")

    def copy_url(self, url):
        if url:
            self.clipboard_clear()
            self.clipboard_append(url)

if __name__ == '__main__':
    app = App()
    app.mainloop()
