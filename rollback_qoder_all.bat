@echo off
chcp 65001 >nul
rem Rollback all compact+enhance patches (keep experts patches untouched). Run as administrator.
python "%~dp0rollback_qoder_all.py"
pause
