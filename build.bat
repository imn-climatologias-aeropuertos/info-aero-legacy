del .\build\
del .\dist\
del *.spec
python .\build.py
copy .\assets\fonts\*.ttf .\dist\assets\fonts
copy .\assets\icons\plane.* .\dist\assets\icons
copy .\assets\img\*.png .\dist\assets\img
copy .\README.md .\dist