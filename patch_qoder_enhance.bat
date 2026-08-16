@echo off
chcp 65001 >nul
rem Patch Qoder prompt enhance: remove length limits + force custom model meta (run as administrator)
python "%~dp0patch_qoder_enhance.py"
pause
