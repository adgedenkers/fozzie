# Define your repository path
$repoPath = "C:\src\fozzie\"

# Change to the repository directory
Set-Location -Path $repoPath

# Git commands to commit and push changes
git add .
git commit -m "Auto-commit latest ChatGPT updates"
git push origin main
