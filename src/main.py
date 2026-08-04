from textual.app import App
from pages.home import HomeScreen


class NoodleApp(App):
    CSS_PATH = "styles/app.tcss"
    SCREENS = {"home": HomeScreen}

    def on_mount(self):
        self.push_screen("home")

def main():
    app = NoodleApp()
    app.run()
if __name__ == "__main__":
    main()
