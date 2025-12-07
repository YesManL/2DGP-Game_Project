@echo off
chcp 65001 > nul
echo ====================================
echo    Sand Raiders - 단일 EXE 빌드
echo ====================================
echo.
echo 모든 리소스를 하나의 EXE 파일로 통합합니다...
echo 빌드 시간이 조금 걸릴 수 있습니다.
echo.

C:\Users\ht515\AppData\Local\Programs\Python\Python310\Scripts\pyinstaller.exe --clean --noconfirm SandRaiders.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================
    echo    빌드 완료!
    echo ====================================
    echo.
    echo 빌드된 게임 위치: dist\SandRaiders.exe
    echo.
    echo 이제 하나의 EXE 파일만 배포하면 됩니다!
    echo 리소스가 모두 포함되어 있어 폴더 없이도 실행됩니다.
    echo.
    echo 주의: 파일 크기가 크고 실행 시 압축 해제 시간이 필요합니다.
    echo.
) else (
    echo.
    echo ====================================
    echo    빌드 실패
    echo ====================================
    echo.
    echo 오류가 발생했습니다. 위의 메시지를 확인하세요.
    echo.
)

pause

