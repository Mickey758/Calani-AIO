export PATH="$HOME/.local/bin:$PATH"
pyinstaller --clean --distpath EXE --icon icon.ico --onefile -p modules main.py