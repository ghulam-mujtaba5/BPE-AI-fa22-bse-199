# Quick Deploy Script
# Run this to deploy your application

Write-Host "🚀 Starting Deployment Process..." -ForegroundColor Green

# Step 1: Push to GitHub
Write-Host "
📤 Step 1: Pushing to GitHub..." -ForegroundColor Cyan
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Successfully pushed to GitHub!" -ForegroundColor Green
    
    Write-Host "
📋 Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Go to https://vercel.com" -ForegroundColor White
    Write-Host "2. Click 'New Project'" -ForegroundColor White
    Write-Host "3. Import 'BPE-AI-Next' repository" -ForegroundColor White
    Write-Host "4. Click 'Deploy'" -ForegroundColor White
    Write-Host "
⏱️  Deployment takes 2-3 minutes" -ForegroundColor Cyan
    Write-Host "
✨ Your app will be live at: https://bpe-ai-next.vercel.app" -ForegroundColor Green
} else {
    Write-Host "❌ Push failed. Please check your GitHub credentials." -ForegroundColor Red
}

Write-Host "
📊 Project Location: C:\Users\ghula\OneDrive\Desktop\bpe-ai-nextjs" -ForegroundColor Gray
Write-Host "📝 Documentation: README.md & DEPLOYMENT.md" -ForegroundColor Gray
