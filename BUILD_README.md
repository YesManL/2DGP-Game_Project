# Sand Raiders - 빌드 가이드

## 빠른 빌드 방법

프로젝트 폴더에서 다음 중 하나를 실행하세요:

### 단일 EXE 파일 빌드 (권장 - 배포 편리)
```
build_onefile.bat
```
- **장점**: 하나의 EXE 파일만 배포하면 됨
- **단점**: 파일 크기가 크고 첫 실행 시 압축 해제 시간 필요
- **결과**: `dist/SandRaiders.exe` (단일 파일)

### 폴더 방식 빌드 (빠른 실행)
```
build_game.bat
```
또는
```
quick_build.bat
```
- **장점**: 실행 속도가 빠름
- **단점**: 폴더 전체를 배포해야 함
- **결과**: `dist/SandRaiders/` 폴더 (여러 파일)

### 명령줄 사용
```powershell
pyinstaller --clean --noconfirm SandRaiders.spec
```

빌드가 완료되면 `dist/SandRaiders` 폴더에 실행 파일이 생성됩니다.

## 빌드된 게임 실행 방법

1. `dist/SandRaiders` 폴더로 이동합니다.
2. `SandRaiders.exe` 파일을 더블 클릭하여 실행합니다.

## 배포 방법

게임을 다른 사람에게 배포하려면:
1. `dist/SandRaiders` 폴더 전체를 압축합니다.
2. 압축 파일을 공유합니다.
3. 받는 사람은 압축을 풀고 `SandRaiders.exe`를 실행하면 됩니다.

**중요**: 
- `SandRaiders.exe` 파일만 복사하면 안 됩니다.
- 반드시 `dist/SandRaiders` 폴더의 모든 파일과 하위 폴더를 함께 배포해야 합니다.

## 빌드 재생성 방법

소스 코드를 수정한 후 다시 빌드하려면:

```powershell
pyinstaller --clean SandRaiders.spec
```

## 빌드 시스템

- **빌드 도구**: PyInstaller 6.17.0
- **Python 버전**: 3.10.6
- **콘솔 창**: 숨김 (console=False)
- **포함된 리소스**:
  - 캐릭터 & 몬스터 애니메이션
  - 배경 & 프랍
  - 아이템 & 아이콘
  - GUI
  - VFX
  - SFX (사운드 효과)

## 문제 해결

### 게임이 실행되지 않을 때
1. Windows Defender나 백신 프로그램에서 차단하는지 확인
2. 모든 파일이 제대로 복사되었는지 확인
3. `dist/SandRaiders` 폴더에서 실행하는지 확인

### 리소스가 로드되지 않을 때
- 게임 실행 파일과 같은 폴더에 리소스 폴더들이 있는지 확인
- 폴더 구조를 변경하지 않았는지 확인

