from pyqt_browser import create_pyqt_browser

def main():
    app, browser_window, _ = create_pyqt_browser()
    browser_window.show()
    app.exec_()

if __name__ == '__main__':
    main()
