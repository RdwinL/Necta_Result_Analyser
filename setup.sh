#!/bin/bash

# NECTA Analysis Dashboard - Setup Script

echo "=================================================="
echo "NECTA Form 4 Results Analysis Dashboard - Setup"
echo "=================================================="
echo ""

# Check Python version
echo "Checking Python version..."
python_version=$(python3 --version 2>&1)
if [[ $python_version == *"Python 3."* ]]; then
    echo "✓ Python 3 detected: $python_version"
else
    echo "✗ Python 3 is required but not found"
    echo "Please install Python 3.8 or higher"
    exit 1
fi

echo ""
echo "Installing required packages..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "=================================================="
    echo "✓ Installation completed successfully!"
    echo "=================================================="
    echo ""
    echo "To start the application, run:"
    echo "  streamlit run necta_analysis_app.py"
    echo ""
    echo "The dashboard will open automatically in your browser at:"
    echo "  http://localhost:8501"
    echo ""
    echo "Features:"
    echo "  • Analyze NECTA Form 4 results"
    echo "  • View top performing schools"
    echo "  • Regional performance analysis"
    echo "  • Subject-wise comparisons"
    echo "  • Download data in CSV/Excel format"
    echo ""
    echo "=================================================="
else
    echo ""
    echo "✗ Installation failed"
    echo "Please check error messages above and try again"
    exit 1
fi
