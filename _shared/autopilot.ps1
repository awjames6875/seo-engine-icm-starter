# SEO engine autopilot (Windows Task Scheduler runs this).
#   -Mode sunday : room 07 report, then pick + draft + email Adam   (Sundays 8:00 AM)
#   -Mode check  : read email replies and move the article along   (daily 7 AM, noon, 6 PM)
param([ValidateSet('sunday', 'check')][string]$Mode = 'check')

$repo = 'C:\Users\1alph\seo-engine-icm-starter'
$today = Get-Date -Format 'yyyy-MM-dd'
$logFolder = Join-Path $repo "_shared\autopilot-logs"
New-Item -ItemType Directory -Force $logFolder | Out-Null
$log = Join-Path $logFolder "$today-$Mode-$(Get-Date -Format HHmm).txt"
Set-Location $repo

$config = Get-Content (Join-Path $repo '_shared\autopilot.json') -Raw | ConvertFrom-Json
if ($Mode -eq 'check' -and $null -eq $config.state) { exit 0 }   # nothing waiting: don't start Claude

if ($Mode -eq 'sunday') {
    & powershell -NoProfile -ExecutionPolicy Bypass -File (Join-Path $repo '07_see-what-worked\references\auto-run.ps1') $today
}

$prompt = (Get-Content (Join-Path $repo "_shared\autopilot-$Mode.md") -Raw).Replace('RUN_DATE', $today)
$tools = 'mcp__claude_ai_composio__COMPOSIO_MULTI_EXECUTE_TOOL mcp__claude_ai_composio__COMPOSIO_SEARCH_TOOLS ' +
         'mcp__claude_ai_composio__COMPOSIO_GET_TOOL_SCHEMAS Read Write Edit Glob Grep ' +
         'Bash(py:*) Bash(git:*) Bash(gh:*) Bash(curl:*) Bash(npm:*)'
& claude -p $prompt --allowedTools $tools *> $log
