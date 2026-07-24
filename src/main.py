from textual.app import App
from pages.home import HomeScreen


class BellyApp(App):
    CSS_PATH = "styles/app.tcss"
    SCREENS = {"home": HomeScreen}

    def on_mount(self):
        self.push_screen("home")


if __name__ == "__main__":
    app = BellyApp()
    app.run()
