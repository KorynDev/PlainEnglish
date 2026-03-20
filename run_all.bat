@echo off
echo =========================================
echo PlainEnglish Test Suite v1.0
echo =========================================

echo Running Math Demo...
python plainenglish.py examples\math_demo.ple
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

echo.
echo Running Advanced Utilities Demo...
python plainenglish.py examples\advanced_utilities_demo.ple
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

echo.
echo Running Demo...
python plainenglish.py examples\demo.ple
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

echo.
echo Running Factorial...
python plainenglish.py examples\factorial.ple
if %ERRORLEVEL% neq 0 exit /b %ERRORLEVEL%

echo.
echo =========================================
echo ALL TESTS PASSED SUCCESSFULLY!
echo =========================================
exit /b 0
