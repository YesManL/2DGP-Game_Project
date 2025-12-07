@echo off
echo 빌드를 시작합니다...
C:\Users\ht515\AppData\Local\Programs\Python\Python310\Scripts\pyinstaller.exe --clean --noconfirm SandRaiders.spec
if %ERRORLEVEL% EQU 0 (
    echo 빌드 완료!
    echo 실행 파일: dist\SandRaiders\SandRaiders.exe
) else (
    echo 빌드 실패!
)

