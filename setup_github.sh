#!/bin/bash

echo "🚀 Setting up GitHub Repository for Sai Venkat Raparthi"
echo "============================================================"

echo "📋 Steps to complete:"
echo ""
echo "1. Create GitHub Repository:"
echo "   - Go to: https://github.com/new"
echo "   - Repository name: real-time-taxi-demand"
echo "   - Description: Real-Time Taxi Demand Forecasting System"
echo "   - Make it Public"
echo "   - Don't initialize with README"
echo "   - Click 'Create repository'"
echo ""
echo "2. After creating the repository, run:"
echo "   git push -u origin master"
echo ""
echo "3. If you get authentication errors, try:"
echo "   - Use Personal Access Token"
echo "   - Or use GitHub CLI: gh auth login"
echo ""

# Check if GitHub CLI is available
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI is installed"
    echo "💡 You can also use: gh repo create saivenkat1437/real-time-taxi-demand --public --source=. --remote=origin --push"
else
    echo "⚠️  GitHub CLI not installed"
    echo "💡 Install with: brew install gh"
fi

echo ""
echo "📊 Current repository status:"
git status --short
echo ""
echo "📝 Commits ready to push:"
git log --oneline
echo ""
echo "🔗 Remote origin:"
git remote -v
echo ""
echo "🎯 Ready to push to: https://github.com/saivenkat1437/real-time-taxi-demand" 