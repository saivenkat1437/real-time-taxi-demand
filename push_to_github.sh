#!/bin/bash

echo "🚀 Pushing Real-Time Taxi Demand Forecasting System to GitHub"
echo "============================================================"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "❌ Git repository not initialized"
    echo "   Run: git init"
    exit 1
fi

# Check if we have commits
if ! git log --oneline -1 > /dev/null 2>&1; then
    echo "❌ No commits found"
    echo "   Run: git add . && git commit -m 'Initial commit'"
    exit 1
fi

echo "✅ Git repository is ready"
echo ""

# Get current status
echo "📊 Current Git Status:"
git status --short
echo ""

# Show last commit
echo "📝 Last Commit:"
git log --oneline -1
echo ""

# Instructions for GitHub
echo "🌐 To push to GitHub:"
echo ""
echo "1. Create a new repository on GitHub:"
echo "   - Go to https://github.com/new"
echo "   - Name: real-time-taxi-demand"
echo "   - Description: Real-Time Taxi Demand Forecasting System"
echo "   - Make it Public"
echo "   - Don't initialize with README (we already have one)"
echo ""
echo "2. Add the remote origin:"
echo "   git remote add origin https://github.com/YOUR_USERNAME/real-time-taxi-demand.git"
echo ""
echo "3. Push to GitHub:"
echo "   git push -u origin master"
echo ""
echo "4. Enable GitHub Pages (optional):"
echo "   - Go to repository Settings > Pages"
echo "   - Source: Deploy from a branch"
echo "   - Branch: master"
echo "   - Folder: / (root)"
echo ""

# Check if remote is already configured
if git remote -v | grep -q origin; then
    echo "✅ Remote origin is configured:"
    git remote -v
    echo ""
    echo "🚀 Ready to push! Run:"
    echo "   git push -u origin master"
else
    echo "⚠️  Remote origin not configured"
    echo "   Add it with: git remote add origin YOUR_GITHUB_URL"
fi

echo ""
echo "📋 Repository Summary:"
echo "   - Files: $(git ls-files | wc -l)"
echo "   - Lines of Code: $(find . -name '*.py' -exec wc -l {} + | tail -1 | awk '{print $1}')"
echo "   - Documentation: $(find . -name '*.md' | wc -l) markdown files"
echo "   - Scripts: $(find . -name '*.sh' | wc -l) shell scripts"
echo ""

echo "🎉 Your Real-Time Taxi Demand Forecasting System is ready for GitHub!"
echo ""
echo "💡 Pro Tips:"
echo "   - Add topics to your repository: real-time, dashboard, kafka, spark, python"
echo "   - Enable Issues and Discussions for community engagement"
echo "   - Set up GitHub Actions for CI/CD (optional)"
echo "   - Add a .github/workflows/ci.yml for automated testing" 