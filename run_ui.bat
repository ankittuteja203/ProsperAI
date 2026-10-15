@echo off
setlocal
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" run_ui.py
) else (
    py run_ui.py
)
endlocal
