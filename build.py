import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'aeroinformes.py',
    '--onefile',
    '--noconsole',
    '--icon=.\\assets\\icons\\plane.ico',
])

folders = ["dist/assets/fonts", "dist/assets/icons", "dist/assets/img"]

for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)