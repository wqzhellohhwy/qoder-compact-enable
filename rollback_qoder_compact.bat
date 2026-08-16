@echo off
chcp 65001 >nul
rem Rollback Qoder compact chat patch (run as administrator)
python "%~dp0rollback_qoder_compact.py"
pause
