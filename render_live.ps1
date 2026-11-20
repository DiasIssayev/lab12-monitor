$ErrorActionPreference = "Continue"
$url = "https://lab12-monitor.onrender.com"
Clear-Host
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "  LR12 — Render metrics via /stats (Free plan)"
Write-Host "  URL: $url"
Write-Host "  (Dashboard CPU/RAM locked on Free — we use API)"
Write-Host "=============================================="
Write-Host ""
Write-Host ">>> STEP 1/3: BEFORE LOAD — GET /stats" -ForegroundColor Yellow
Write-Host "Press Enter..."
Read-Host
Write-Host "`n--- /stats BEFORE ---" -ForegroundColor Green
curl.exe -sS "$url/stats"
Write-Host ""
Write-Host "`nPress Enter to START LOAD..." -ForegroundColor Yellow
Read-Host

Write-Host "`n>>> STEP 2/3: DURING LOAD — parallel /load + /stats" -ForegroundColor Yellow
$jobs = 1..30 | ForEach-Object {
  Start-Job -ScriptBlock {
    param($u)
    curl.exe -sS -o NUL "$u/load"
  } -ArgumentList $url
}
Start-Sleep -Seconds 2
Write-Host "`n--- /stats DURING ---" -ForegroundColor Green
curl.exe -sS "$url/stats"
Write-Host ""
$null = $jobs | Wait-Job
$jobs | Remove-Job | Out-Null
Write-Host "`nLoad finished. Press Enter for AFTER..." -ForegroundColor Yellow
Read-Host

Write-Host "`n>>> STEP 3/3: AFTER LOAD — wait 10s then /stats" -ForegroundColor Yellow
Start-Sleep -Seconds 10
Write-Host "`n--- /stats AFTER ---" -ForegroundColor Green
curl.exe -sS "$url/stats"
Write-Host ""
Write-Host "`n==============================================" -ForegroundColor Cyan
Write-Host "  DONE — copy CPU/RAM/Disk/Network/processes"
Write-Host "  into the lab table (before / during / after)"
Write-Host "=============================================="
Read-Host "Enter = close"
