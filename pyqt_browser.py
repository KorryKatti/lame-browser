import sys
import pickle
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtNetwork import QNetworkCookie, QNetworkCookieJar

home_url = 'https://bit.ly/dunk123'

def create_pyqt_browser():
    app = QApplication(sys.argv)

    # Initialize the main window and central widget
    browser_window = QMainWindow()
    central_widget = QWidget()
    browser_window.setCentralWidget(central_widget)

    # Layout for the main window
    layout = QVBoxLayout(central_widget)

    # Create the web engine view
    browser = QWebEngineView()
    browser.setUrl(QUrl(home_url))

    # Navigation buttons
    nav_layout = QHBoxLayout()
    home_button = QPushButton('Home')
    back_button = QPushButton('Back')
    forward_button = QPushButton('Forward')

    home_button.clicked.connect(lambda: browser.setUrl(QUrl(home_url)))
    back_button.clicked.connect(browser.back)
    forward_button.clicked.connect(browser.forward)

    nav_layout.addWidget(home_button)
    nav_layout.addWidget(back_button)
    nav_layout.addWidget(forward_button)

    layout.addLayout(nav_layout)
    layout.addWidget(browser)

    # Enable plugins, JavaScript, and local storage
    settings = browser.settings()
    settings.setAttribute(settings.JavascriptEnabled, True)
    settings.setAttribute(settings.LocalStorageEnabled, True)
    settings.setAttribute(settings.PluginsEnabled, True)

    # Load and save cookies
    load_cookies(browser)
    save_cookies(browser)

    browser_window.show()
    sys.exit(app.exec_())

def save_cookies(browser):
    cookie_store = browser.page().profile().cookieStore()
    cookie_store.cookieAdded.connect(lambda cookie: save_cookie_to_file(cookie.toRawForm()))

def save_cookie_to_file(cookie):
    try:
        cookies = pickle.load(open('cookies.pkl', 'rb'))
    except (FileNotFoundError, EOFError):
        cookies = []
    cookies.append(cookie)
    with open('cookies.pkl', 'wb') as f:
        pickle.dump(cookies, f)

def load_cookies(browser):
    try:
        cookies = pickle.load(open('cookies.pkl', 'rb'))
        cookie_store = browser.page().profile().cookieStore()
        for cookie in cookies:
            cookie_store.setCookie(QNetworkCookie.parseCookies(cookie)[0])
    except (FileNotFoundError, EOFError, pickle.PickleError):
        pass

if __name__ == "__main__":
    create_pyqt_browser()
