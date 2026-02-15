# 🚀 Quick Start Guide - NECTA Analysis Dashboard

## Installation (5 minutes)

### Option 1: Automatic Setup (Recommended)

**Windows:**
```cmd
setup.bat
```

**Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

### Option 2: Manual Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run necta_analysis_app.py
```

## First Time Usage

1. **Open the app** - It will automatically open in your browser at http://localhost:8501

2. **Choose Analysis Mode:**
   - Click "Quick Analysis" for first try (analyzes 50 schools, ~2-3 minutes)
   - Or select "Custom Selection" to pick specific schools

3. **Start Analysis:**
   - Click the "🚀 Start Analysis" button
   - Wait for the progress bar to complete

4. **Explore Results:**
   - Navigate through the 6 tabs at the top
   - Each tab shows different analysis views

## Key Features at a Glance

### 📈 Overview Tab
See total schools, students, and performance distributions

### 🏆 Top Performers Tab
Find the best schools ranked by GPA or Division I rate

### 📍 Regional Analysis Tab
Compare performance across different regions

### 📚 Subject Analysis Tab
Analyze Science vs Arts performance

### 📊 Comparative Analysis Tab
Compare Boys/Girls/Mixed and Government/Private schools

### 💾 Download Data Tab
Export results as CSV or Excel files

## Common Tasks

### Find Top Schools in Your Region
1. Go to "Top Performers" tab
2. Select your ranking criteria
3. Scroll through the rankings
4. Download the list

### Compare School Types
1. Go to "Comparative Analysis" tab
2. View Boys vs Girls vs Mixed comparison
3. Check Government vs Private performance

### Download Results
1. Go to "Download Data" tab
2. Choose from:
   - All Schools (CSV)
   - Top 50 Schools (CSV)
   - Full Excel Report
3. Click download button

## Tips for Best Experience

✅ **DO:**
- Start with Quick Analysis for testing
- Use filters to narrow down results
- Download data for offline analysis
- Explore all tabs for complete insights

❌ **DON'T:**
- Run Full Analysis on slow internet
- Refresh page during analysis (you'll lose progress)
- Expect instant results with Full Analysis

## Need Help?

📖 **Read the full documentation:**
- README.md - Complete setup guide
- USER_GUIDE.md - Detailed feature explanations

## System Requirements

- Python 3.8 or higher
- Internet connection
- Modern web browser (Chrome, Firefox, Edge)
- 4GB RAM minimum (8GB recommended for Full Analysis)

## Troubleshooting

**App won't start?**
- Check Python version: `python --version`
- Reinstall dependencies: `pip install -r requirements.txt`

**Analysis taking too long?**
- Use Quick Analysis mode
- Check internet connection
- Try at off-peak hours

**Can't see charts?**
- Enable JavaScript in browser
- Clear browser cache
- Try different browser

## What's Next?

After your first successful analysis:
1. Try Full Analysis for complete data
2. Experiment with Custom Selection
3. Download reports for sharing
4. Compare multiple metrics

---

**Ready to start?** Run the setup script and begin your analysis! 🎯
