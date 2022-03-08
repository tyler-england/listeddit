import app

if __name__ == '__main__':
    x = 1
    while x != 0:
        try:
            x = app.run()
        except:
            print("x: " + x)
            continue
