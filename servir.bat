@echo off
chcp 65001 >nul
echo ==========================================
echo   CALANDRACOS - servidor local
echo ==========================================
echo En este PC:      http://localhost:8765
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /c:"IPv4"') do echo En el celular:    http://%%a:8765   (misma WiFi)
echo.
echo Deja esta ventana abierta mientras juegas. Ctrl+C para cerrar.
echo.
python -m http.server 8765
