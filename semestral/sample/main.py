from loop import Loop
import os

settings_path = os.path.relpath('src/settings.conf')

l = Loop(settings_path)
l.loop()
