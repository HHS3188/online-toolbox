# 一键启动销售 - 自动打开所有平台
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🚀 一键启动销售 - 赚取10元" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 1. 打开闲鱼
Write-Host "[1/4] 打开闲鱼..." -ForegroundColor Yellow
Start-Process "https://www.goofish.com/"
Write-Host "  ✅ 已打开闲鱼网站" -ForegroundColor Green
Write-Host "  📋 标题: Python办公自动化脚本 Excel批量处理 文件重命名工具" -ForegroundColor White
Write-Host "  💰 价格: 10元" -ForegroundColor White
Write-Host ""

# 2. 打开Fiverr
Write-Host "[2/4] 打开Fiverr..." -ForegroundColor Yellow
Start-Process "https://www.fiverr.com/"
Write-Host "  ✅ 已打开Fiverr网站" -ForegroundColor Green
Write-Host "  📋 标题: I will write python automation scripts for Excel and file management" -ForegroundColor White
Write-Host "  💰 价格: $5-20" -ForegroundColor White
Write-Host ""

# 3. 打开微信
Write-Host "[3/4] 打开微信..." -ForegroundColor Yellow
Start-Process "weixin://"
Write-Host "  ✅ 已打开微信" -ForegroundColor Green
Write-Host "  📋 朋友圈文案已复制到剪贴板" -ForegroundColor White
Write-Host ""

# 4. 复制朋友圈文案
$friendCircleText = @"
推荐一个超实用的办公工具包！
包含 Excel 批量处理、文件重命名、微信聊天分析三个工具
效率提升10倍，告别重复劳动
仅需10元，一次购买永久使用
详情：https://hhs3188.github.io/online-toolbox/
"@

Set-Clipboard -Value $friendCircleText
Write-Host "[4/4] 朋友圈文案已复制" -ForegroundColor Yellow
Write-Host "  ✅ 文案已复制到剪贴板" -ForegroundColor Green
Write-Host ""

# 5. 打开产品页面
Write-Host "[5/5] 打开产品页面..." -ForegroundColor Yellow
Start-Process "https://hhs3188.github.io/online-toolbox/"
Write-Host "  ✅ 已打开产品页面" -ForegroundColor Green
Write-Host ""

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  ✅ 所有平台已打开！" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📋 接下来你需要做的:" -ForegroundColor White
Write-Host "  1. 在闲鱼发布产品（标题和价格已准备好）" -ForegroundColor White
Write-Host "  2. 在Fiverr创建Gig（标题和价格已准备好）" -ForegroundColor White
Write-Host "  3. 在微信朋友圈发布（文案已复制）" -ForegroundColor White
Write-Host "  4. 等待买家付款" -ForegroundColor White
Write-Host ""
Write-Host "💡 提示: 买家付款后，发送以下文件:" -ForegroundColor White
Write-Host "  - office-tools.zip (产品包)" -ForegroundColor White
Write-Host "  - products/使用说明.txt (使用说明)" -ForegroundColor White
Write-Host ""
Write-Host "🎯 目标: 1-3天内赚到10元！" -ForegroundColor Green
Write-Host ""
Read-Host "按Enter键退出"
