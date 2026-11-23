# Room 07 on autopilot: pulls Search Console via Claude Code + Composio, then runs run.py.
# Usage: powershell -File auto-run.ps1 [YYYY-MM-DD]   (default: today)
param([string]$RunDate = (Get-Date -Format 'yyyy-MM-dd'))

$repo = 'C:\Users\1alph\seo-engine-icm-starter'
$runFolder = Join-Path $repo "07_see-what-worked\output\$RunDate"
New-Item -ItemType Directory -Force $runFolder | Out-Null

$prompt = (Get-Content (Join-Path $PSScriptRoot 'auto-run-prompt.md') -Raw).Replace('RUN_DATE', $RunDate)
$tools = 'mcp__claude_ai_composio__COMPOSIO_MULTI_EXECUTE_TOOL mcp__claude_ai_composio__COMPOSIO_SEARCH_TOOLS mcp__claude_ai_composio__COMPOSIO_GET_TOOL_SCHEMAS Read Write Bash(py:*)'

Set-Location $repo
& claude -p $prompt --allowedTools $tools *> (Join-Path $runFolder 'run-log.txt')
