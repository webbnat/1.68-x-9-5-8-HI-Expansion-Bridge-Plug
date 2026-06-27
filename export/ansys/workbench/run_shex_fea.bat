@echo off
REM SHEX Stage 3 Iris — launch ANSYS Workbench journal (batch)
REM Edit ANSYS_VERSION if needed (v231, v242, etc.)

set ANSYS_VERSION=v242
set RUNWB2=C:\Program Files\ANSYS Inc\%ANSYS_VERSION%\Framework\bin\Win64\runwb2.exe
set JOURNAL=%~dp0shex_stage3_iris.wbjn

if not exist "%RUNWB2%" (
    echo runwb2 not found at: %RUNWB2%
    echo Edit ANSYS_VERSION in this script.
    exit /b 1
)

echo Running Workbench journal: %JOURNAL%
"%RUNWB2%" -B -R "%JOURNAL%"
echo Exit code: %ERRORLEVEL%
