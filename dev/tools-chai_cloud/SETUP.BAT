@echo off

echo ::::: Python, easy_install, Django Installer :::::

rem Python setup
echo Installing Python 2.7.8...
msiexec /i bin\python-2.7.8.msi /passive
setx PATH C:\Python27;C:\Python27\Scripts;%PATH% /M
set PATH=C:\Python27;C:\Python27\Scripts;%PATH%
echo [DONE]
rem easy_install setup
echo Installing easy_install...
python bin\ez_setup.py
echo [DONE]
rem django setup
echo Installing Django...
easy_install django
echo [DONE]
rem install notepad++
bin\npp.6.7.4.Installer.exe /S
rem instlal github (requires user actions)
bin\GitHubSetup.exe

set /p DUMMY=All installed successfully. Hit ENTER to quit...