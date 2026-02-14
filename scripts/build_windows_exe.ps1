param(
    [string]$EntryScript = "flight_search/cli.py",
    [string]$ExeName = "flight-search"
)

$ErrorActionPreference = "Stop"

Write-Host "[1/4] Python 버전 확인"
py --version

Write-Host "[2/4] 가상환경 생성"
if (!(Test-Path ".venv")) {
    py -m venv .venv
}

Write-Host "[3/4] 의존성 설치"
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -e .
.\.venv\Scripts\python -m pip install pyinstaller

Write-Host "[4/4] EXE 빌드"
.\.venv\Scripts\pyinstaller --onefile --name $ExeName $EntryScript

Write-Host "완료: dist\$ExeName.exe 생성"
