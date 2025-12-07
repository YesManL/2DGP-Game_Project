@echo off
chcp 65001 > nul
echo ====================================
echo    Sand Raiders 빌드 스크립트
echo ====================================
echo.
echo 게임을 빌드하고 있습니다...
echo.

pyinstaller --clean SandRaiders.spec

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================
    echo    빌드 완료!
    echo ====================================
    echo.
    echo 빌드된 게임 위치: dist\SandRaiders\
    echo 실행 파일: dist\SandRaiders\SandRaiders.exe
    echo.
    echo 배포하려면 dist\SandRaiders 폴더 전체를 압축하세요.
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

