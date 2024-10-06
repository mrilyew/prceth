@echo off
if exist "%CD%\venv" (
echo Venv exists
%CD%\venv\Scripts\activate.bat
cd "%CD%\src"
) else (
python -m venv %CD%\venv 
%CD%\venv\Scripts\activate.bat
pip install -r %CD%\requirements.txt
cd "%CD%\src"
)
