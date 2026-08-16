@echo off
chcp 65001 >nul
rem Patch Qoder compact chat always available (run as administrator)
python "%~dp0patch_qoder_compact.py"
pause
