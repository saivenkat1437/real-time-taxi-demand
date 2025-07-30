#!/bin/bash

echo "🚀 Deploying Real-Time Taxi Demand Forecasting System to GitHub"
echo "============================================================"

# Check if git is ready
if [ ! -d ".git" ]; then
    echo "❌ Git repository not found!"
    exit 1
fi

echo "✅ Local repository is ready"
echo "📝 Commits ready to push:"
git log --oneline
echo ""

# Check if remote is configured
if git remote -v | grep -q origin; then
    echo "✅ Remote origin is configured:"
    git remote -v
    echo ""
    echo "🚀 Ready to push! Run:"
    echo "   git push -u origin master"
else
    echo "⚠️  Remote origin not configured"
    echo ""
    echo "📋 To deploy to GitHub:"
    echo ""
    echo "1. Create a new repository on GitHub:"
    echo "   - Go to https://github.com/new"
    echo "   - Name: real-time-taxi-demand"
    echo "   - Description: Real-Time Taxi Demand Forecasting System"
    echo "   - Make it Public"
    echo "   - Don't initialize with README"
    echo ""
    echo "2. Add the remote (replace YOUR_USERNAME with your GitHub username):"
    echo "   git remote add origin https://github.com/YOUR_USERNAME/real-time-taxi-demand.git"
    echo ""
    echo "3. Push to GitHub:"
    echo "   git push -u origin master"
    echo ""
    
    # Ask for GitHub username
    read -p "Enter your GitHub username: " github_username
    
    if [ ! -z "$github_username" ]; then
        echo ""
        echo "🔗 Adding remote origin..."
        git remote add origin "https://github.com/$github_username/real-time-taxi-demand.git"
        
        echo "🚀 Pushing to GitHub..."
        git push -u origin master
        
        if [ $? -eq 0 ]; then
            echo ""
            echo "🎉 SUCCESS! Your repository is now live on GitHub!"
            echo "🌐 View it at: https://github.com/$github_username/real-time-taxi-demand"
            echo ""
            echo "💡 Next steps:"
            echo "   - Add repository topics: real-time, dashboard, kafka, spark, python"
            echo "   - Enable Issues and Discussions"
            echo "   - Share with the community!"
        else
            echo "❌ Push failed. Please check your GitHub repository URL."
        fi
    else
        echo "❌ No username provided. Please run the commands manually."
    fi
fi

echo ""
echo "📊 Repository Summary:"
echo "   - Files: $(git ls-files | wc -l)"
echo "   - Commits: $(git log --oneline | wc -l)"
echo "   - Documentation: $(find . -name '*.md' | wc -l) markdown files"
echo "   - Scripts: $(find . -name '*.sh' | wc -l) shell scripts" 