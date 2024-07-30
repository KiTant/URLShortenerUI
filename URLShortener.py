import customtkinter as ctk
import pyshorteners
from CTkMessagebox import CTkMessagebox
from CTkListbox import CTkListbox

# Set the appearance and theme of the application
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Set up the main window properties
        self.title("URL Shortener")
        self.geometry("1100x250")
        self.resizable(True, False)
        self.minsize(1100, 250)

        # Initialize pyshorteners
        self.shortener = pyshorteners.Shortener()
        self.shortened_url = None
        self.expanded_url = None
        self.shorteners = ('clckru', 'tinyurl', 'osdb')

        # Initialize the UI components
        self._initialize_components()

    def _initialize_components(self):
        # URL entry
        self.url_entry = ctk.CTkEntry(self, placeholder_text="Your URL goes here", width=800)
        self.url_entry.pack(pady=20)

        # URL shorteners option menu
        self.url_shorteners = CTkListbox(self, command=self.selected_shortener_text)
        self.url_shorteners.pack(pady=5)
        for i in self.shorteners:
            self.url_shorteners.insert("END", i)

        # Selected URL shortener label
        self.selected_url_shortener = ctk.CTkLabel(self, text="Selected shortener: clckru",
                                                   fg_color="transparent", font=ctk.CTkFont(family="Arial", size=14))
        self.selected_url_shortener.pack()

        # Button to generate short URL
        self.generate_short_url_button = ctk.CTkButton(self, text="Generate Short URL", command=self.generate_short_url)
        self.generate_short_url_button.place(relx=0.045, rely=0.425)

        # Button to copy short URL
        self.copy_short_url_button = ctk.CTkButton(self, text="Copy Short URL",
                                                   command=lambda: self.copy_url(self.shortened_url))
        self.copy_short_url_button.place(relx=0.045, rely=0.7)

        # Button to expand short URL
        self.expand_short_url_button = ctk.CTkButton(self, text="Expand Short URL", command=self.expand_url)
        self.expand_short_url_button.place(relx=0.7, rely=0.425)

        # Button to copy expanded URL
        self.copy_expand_url_button = ctk.CTkButton(self, text="Copy Expanded URL",
                                                    command=lambda: self.copy_url(self.expanded_url))
        self.copy_expand_url_button.place(relx=0.7, rely=0.7)

        # Label to show the short URL
        self.short_url_label = ctk.CTkLabel(self, text="Shortened URL: Nothing to show here now",
                                            fg_color="transparent", font=ctk.CTkFont(family="Arial", size=14))
        self.short_url_label.place(relx=0.045, rely=0.57)

        # Label to show the expanded URL
        self.expand_url_label = ctk.CTkLabel(self, text="Expanded URL: Nothing to show here now",
                                             fg_color="transparent", font=ctk.CTkFont(family="Arial", size=14))
        self.expand_url_label.place(relx=0.7, rely=0.57)

        self.url_shorteners.activate(0)

    def generate_short_url(self):
        url = self.url_entry.get()
        shortener_service = self.url_shorteners.get()
        try:
            self.shortened_url = getattr(self.shortener, shortener_service).short(url)
            self.short_url_label.configure(text=f"Shortened URL: {self.shortened_url}")
        except pyshorteners.exceptions.BadURLException:
            CTkMessagebox(title="Shortened URL (Error 1)", message="Please enter a valid URL.",
                          icon="cancel", option_1="Ok", sound=True)
        except pyshorteners.exceptions.ShorteningErrorException:
            CTkMessagebox(title="Shortened URL (Error 2)", message="Could not shorten the URL.",
                          icon="cancel", option_1="Ok", sound=True)

    def expand_url(self):
        url = self.url_entry.get()
        expander_service = self.url_shorteners.get()
        try:
            self.expanded_url = getattr(self.shortener, expander_service).expand(url)
            self.expand_url_label.configure(text=f"Expanded URL: {self.expanded_url}")
        except pyshorteners.exceptions.BadURLException:
            CTkMessagebox(title="Expanded URL (Error 1)", message="Please enter a valid URL.",
                          icon="cancel", option_1="Ok", sound=True)
        except pyshorteners.exceptions.ExpansionErrorException:
            CTkMessagebox(title="Expanded URL (Error 2)", message="Could not expand the URL.",
                          icon="cancel", option_1="Ok", sound=True)

    def copy_url(self, url):
        if url:
            self.clipboard_clear()
            self.clipboard_append(url)
            CTkMessagebox(title="Copying URL", message="Successfully copied URL.",
                          icon="check", option_1="Ok", topmost=False)
        else:
            CTkMessagebox(title="Copying URL (Error)", message="Expanded or shortened URL is missing.",
                          icon="cancel", option_1="Ok", sound=True)

    def selected_shortener_text(self, shortener):
        self.selected_url_shortener.configure(text=f"Selected shortener: {shortener}")

if __name__ == '__main__':
    app = App()
    app.mainloop()
