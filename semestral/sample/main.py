from loop import Loop
import os

def main():
    settings_path = os.path.relpath('src/settings.conf')

    l = Loop(settings_path)
    l.loop()

if __name__ == "__main__":
    main()