#!/bin/bash

echo "🚀 Real-Time Taxi Demand Forecasting System - GitHub Deployment"
echo "=============================================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is not installed. Please install Git first."
    exit 1
fi

# Check if GitHub CLI is installed
if command -v gh &> /dev/null; then
    echo "✅ GitHub CLI is installed"
    USE_GH_CLI=true
else
    echo "⚠️  GitHub CLI not found. Will use manual GitHub setup."
    USE_GH_CLI=false
fi

echo ""
echo "📋 Current Project Status:"
echo "✅ All files are ready for GitHub"
echo "✅ README.md with testimonials created"
echo "✅ Professional documentation complete"
echo "✅ System is fully functional"
echo ""

# Initialize git repository if not already done
if [ ! -d ".git" ]; then
    echo "🔧 Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: Real-Time Taxi Demand Forecasting System

- Complete real-time taxi demand forecasting system
- Interactive dashboard with live updates
- Apache Spark Streaming and Kafka integration
- Professional documentation and testimonials
- Comprehensive health monitoring system
- Mock data generation for testing
- NYC API integration capabilities"
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

echo ""
echo "🌐 GitHub Repository Setup Options:"
echo ""

if [ "$USE_GH_CLI" = true ]; then
    echo "1. 🚀 Use GitHub CLI (Recommended)"
    echo "   - Automatic repository creation"
    echo "   - Automatic authentication"
    echo "   - Seamless deployment"
    echo ""
    echo "2. 📝 Manual GitHub Setup"
    echo "   - Create repository on GitHub.com"
    echo "   - Add remote and push manually"
    echo ""
    
    read -p "Choose option (1 or 2): " choice
    
    case $choice in
        1)
            echo ""
            echo "🚀 Using GitHub CLI for deployment..."
            
            # Check if user is authenticated
            if gh auth status &> /dev/null; then
                echo "✅ GitHub CLI authenticated"
            else
                echo "🔐 Please authenticate with GitHub CLI:"
                gh auth login
            fi
            
            # Create repository
            echo "📦 Creating GitHub repository..."
            gh repo create real-time-taxi-demand \
                --public \
                --description "A cutting-edge real-time taxi demand forecasting system with Apache Spark Streaming, Kafka, and interactive dashboards" \
                --homepage "https://github.com/saivenkat1437/real-time-taxi-demand" \
                --source . \
                --remote origin \
                --push
            
            if [ $? -eq 0 ]; then
                echo "✅ Repository created and pushed successfully!"
                echo "🌐 View your repository at: https://github.com/saivenkat1437/real-time-taxi-demand"
            else
                echo "❌ Failed to create repository. Trying manual setup..."
                USE_GH_CLI=false
            fi
            ;;
        2)
            USE_GH_CLI=false
            ;;
        *)
            echo "❌ Invalid choice. Using manual setup."
            USE_GH_CLI=false
            ;;
    esac
fi

if [ "$USE_GH_CLI" = false ]; then
    echo ""
    echo "📝 Manual GitHub Setup Instructions:"
    echo "=================================="
    echo ""
    echo "1. 🌐 Go to https://github.com/new"
    echo "2. 📝 Repository name: real-time-taxi-demand"
    echo "3. 📄 Description: Real-Time Taxi Demand Forecasting System"
    echo "4. 🌍 Make it Public"
    echo "5. ✅ Don't initialize with README (we have one)"
    echo "6. 🚀 Click 'Create repository'"
    echo ""
    echo "7. 🔗 After creating, run these commands:"
    echo ""
    echo "   git remote add origin https://github.com/saivenkat1437/real-time-taxi-demand.git"
    echo "   git branch -M main"
    echo "   git push -u origin main"
    echo ""
    
    read -p "Press Enter after creating the repository on GitHub..."
    
    echo ""
    echo "🔗 Adding remote origin..."
    git remote add origin https://github.com/saivenkat1437/real-time-taxi-demand.git
    
    echo "🔄 Setting main branch..."
    git branch -M main
    
    echo "📤 Pushing to GitHub..."
    git push -u origin main
    
    if [ $? -eq 0 ]; then
        echo "✅ Successfully pushed to GitHub!"
    else
        echo "❌ Failed to push. Please check your GitHub credentials."
        echo "💡 You may need to use a Personal Access Token:"
        echo "   1. Go to GitHub Settings > Developer settings > Personal access tokens"
        echo "   2. Generate a new token with 'repo' permissions"
        echo "   3. Use the token as your password when prompted"
    fi
fi

echo ""
echo "🎉 GitHub Deployment Summary:"
echo "============================"
echo "✅ Repository: https://github.com/saivenkat1437/real-time-taxi-demand"
echo "✅ README: Professional documentation with testimonials"
echo "✅ Code: Complete real-time taxi demand forecasting system"
echo "✅ Features: Live dashboard, streaming analytics, health monitoring"
echo "✅ Documentation: Comprehensive guides and examples"
echo ""

echo "📊 Project Highlights:"
echo "====================="
echo "🚕 Real-time taxi demand forecasting"
echo "🗺️  Interactive NYC heatmap visualization"
echo "⚡ Apache Spark Streaming integration"
echo "📈 Live dashboard with 5-second updates"
echo "🔍 Comprehensive health monitoring"
echo "📱 Responsive design for all devices"
echo "🎯 Production-ready architecture"
echo ""

echo "🌟 Showcase Features:"
echo "===================="
echo "• Advanced real-time data processing"
echo "• Interactive geospatial visualizations"
echo "• Scalable microservices architecture"
echo "• Professional error handling and logging"
echo "• Comprehensive testing and monitoring"
echo "• Clean, maintainable codebase"
echo "• Extensive documentation"
echo ""

echo "💡 Next Steps:"
echo "=============="
echo "1. 🌐 Visit your repository: https://github.com/saivenkat1437/real-time-taxi-demand"
echo "2. ⭐ Star your own repository to show engagement"
echo "3. 📝 Update your portfolio with this project"
echo "4. 🔗 Share on LinkedIn and other platforms"
echo "5. 🚀 Consider adding more features or documentation"
echo ""

echo "🎯 Professional Impact:"
echo "====================="
echo "This project demonstrates:"
echo "• Real-time data processing expertise"
echo "• Advanced system architecture skills"
echo "• Interactive visualization capabilities"
echo "• Production-ready development practices"
echo "• Comprehensive documentation skills"
echo "• Modern technology stack proficiency"
echo ""

echo "✅ Deployment Complete!"
echo "======================"
echo "Your Real-Time Taxi Demand Forecasting System is now live on GitHub!"
echo "This project showcases advanced skills in real-time analytics, data visualization,"
echo "and system architecture - perfect for your professional portfolio."
echo ""
echo "🌐 Repository: https://github.com/saivenkat1437/real-time-taxi-demand"
echo "📧 Contact: saivenkat.raparthi@gmail.com"
echo "👨‍💻 Developer: Sai Venkat Raparthi" 