# fix_and_push.ps1

Write-Host "⚙️ Cleaning up local repo and pushing safely..." -ForegroundColor Cyan

# 1. Load .env
$envVars = Get-Content .env | Where-Object { $_ -match "=" } | ForEach-Object {
    $parts = $_ -split "="
    [System.Environment]::SetEnvironmentVariable($parts[0], $parts[1])
}

# 2. Run Python setup
python -c "from fozzie.tools.git.setup import setup_github_env; setup_github_env(force=True)"

# 3. Untrack .env
git rm --cached .env -f
Add-Content .gitignore "`n.env"

# 4. Remove egg-info folder if present
if (Test-Path "fozzie.egg-info") {
    Remove-Item -Recurse -Force "fozzie.egg-info"
}

# 5. Re-add and recommit
git add .
git commit -m "Clean and safe commit after Git config & .env untracking"

# 6. Push
git push origin main

Write-Host "✅ Push complete." -ForegroundColor Green
