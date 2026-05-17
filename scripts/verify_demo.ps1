# Verify demo public data and API responses (run API separately or start below)
param(
    [string]$BaseUrl = "http://127.0.0.1:8000"
)

Write-Host "=== Checking data/public ===" -ForegroundColor Cyan
$root = Join-Path (Join-Path $PSScriptRoot "..") "data\public"
$mdCount = (Get-ChildItem -Path $root -Recurse -Filter "*.md" | Where-Object { $_.FullName -notmatch "\\graph\\" }).Count
Write-Host "Markdown documents: $mdCount"
if ($mdCount -lt 6) { Write-Warning "Expected at least 6 demo markdown files" }

Write-Host "`n=== API checks at $BaseUrl ===" -ForegroundColor Cyan
try {
    $health = Invoke-RestMethod "$BaseUrl/health"
    Write-Host "Health: $($health.status)"

    $docs = Invoke-RestMethod "$BaseUrl/api/v1/documents"
    Write-Host "Documents indexed: $($docs.count)"

    $askBody = '{"question":"Which unresolved certification risks could delay flight testing?","program_id":"dap-100"}'
    $ask = Invoke-RestMethod "$BaseUrl/api/v1/ask" -Method Post -Body $askBody -ContentType "application/json"
    Write-Host "Ask confidence: $($ask.confidence)"
    Write-Host "Evidence chunks: $($ask.evidence.Count)"
    Write-Host "Answer preview: $($ask.answer.Substring(0, [Math]::Min(200, $ask.answer.Length)))..."

    $impactBody = '{"entity_id":"sw-req-1042","program_id":"dap-100","change_description":"Avionics firmware v2.4.1"}'
    $impact = Invoke-RestMethod "$BaseUrl/api/v1/impact/analyze" -Method Post -Body $impactBody -ContentType "application/json"
    Write-Host "Impact items: $($impact.evidence.Count)"

    Write-Host "`nDemo verification PASSED" -ForegroundColor Green
} catch {
    Write-Host "API not reachable. Start with:" -ForegroundColor Yellow
    Write-Host '  $env:PYTHONPATH = "packages/domain/src;services/intelligence/src;services/graph/src;services/gateway/src"'
    Write-Host "  python -m uvicorn gateway.main:app --port 8000"
    exit 1
}
