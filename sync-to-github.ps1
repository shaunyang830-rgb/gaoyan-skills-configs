# Claude Code Skills & Configs - 一键同步到 GitHub
# 使用方法：在 PowerShell 中运行 .\sync-to-github.ps1

Write-Host "🔄 开始同步 Claude Code Skills & Configs 到 GitHub..." -ForegroundColor Cyan
Write-Host ""

# 1. 复制最新 skills
Write-Host "📦 第一步：复制最新 skills..." -ForegroundColor Yellow
Copy-Item -Path "$env:USERPROFILE\.claude\skills\*" -Destination ".\skills\" -Recurse -Force
Write-Host "   ✅ Skills 已更新" -ForegroundColor Green

# 2. 复制最新 settings.json（但先清理 API 密钥）
Write-Host "⚙️  第二步：复制配置文件..." -ForegroundColor Yellow
$settingsContent = Get-Content "$env:USERPROFILE\.claude\settings.json" -Raw
# 清理常见 API 密钥
$settingsContent = $settingsContent -replace '"OPENROUTER_API_KEY":\s*"sk-or-[^"]*"', '"OPENROUTER_API_KEY": "YOUR_OPENROUTER_API_KEY_HERE"'
$settingsContent = $settingsContent -replace '"ANTHROPIC_API_KEY":\s*"sk-ant-[^"]*"', '"ANTHROPIC_API_KEY": "YOUR_ANTHROPIC_API_KEY_HERE"'
$settingsContent = $settingsContent -replace '"OPENAI_API_KEY":\s*"sk-[^"]*"', '"OPENAI_API_KEY": "YOUR_OPENAI_API_KEY_HERE"'
$settingsContent | Set-Content ".\configurations\settings\settings.json" -Encoding UTF8
Write-Host "   ✅ 配置文件已更新（API 密钥已自动移除）" -ForegroundColor Green

# 3. 检查变化
Write-Host ""
Write-Host "📊 第三步：检查变化..." -ForegroundColor Yellow
$status = git status --short
if (-not $status) {
    Write-Host "   ℹ️  没有任何变化，无需推送" -ForegroundColor Gray
    exit 0
}
Write-Host "   变更文件："
git status --short | ForEach-Object { Write-Host "   $_" -ForegroundColor Gray }

# 4. 提交
Write-Host ""
Write-Host "💾 第四步：提交变更..." -ForegroundColor Yellow
$date = Get-Date -Format "yyyy-MM-dd HH:mm"
git add .
git commit -m "chore: sync skills and configs - $date"
Write-Host "   ✅ 已提交" -ForegroundColor Green

# 5. 推送
Write-Host ""
Write-Host "🚀 第五步：推送到 GitHub..." -ForegroundColor Yellow
git push origin main
Write-Host "   ✅ 推送成功！" -ForegroundColor Green

Write-Host ""
Write-Host "🎉 同步完成！" -ForegroundColor Cyan
Write-Host "   仓库地址：https://github.com/shaunyang830-rgb/gaoyan-skills-configs" -ForegroundColor Blue
