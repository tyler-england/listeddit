import app
from datetime import datetime

if __name__ == '__main__':
    x = 0
    y = 0
    while x == 0:
        x = 1
        try:
            # x = app.run()
            if y > 0:
                print("\nRestarting bot... " + datetime.now().strftime("%-d %b %Y, %H:%M:%S"))
            y = 1
            x = app.mainfunc()
        except:
            continue
