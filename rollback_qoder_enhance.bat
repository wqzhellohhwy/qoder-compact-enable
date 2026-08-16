@echo off
chcp 65001 >nul
rem Rollback Qoder prompt enhance patch (run as administrator)
python "%~dp0rollback_qoder_enhance.py"
pause
