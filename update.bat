@echo off
pyinstaller --noconsole --onefile --add-data "C:\Users\guime\AppData\Local\Programs\Python\Python311\Lib\site-packages\tkinterdnd2;tkinterdnd2" --icon=icone.ico intercalador_interface.py
pause
