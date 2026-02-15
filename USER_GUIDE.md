# NECTA Analysis Dashboard - User Guide

## Quick Start Guide

### Getting Started in 3 Steps

1. **Install & Run**
   ```bash
   pip install -r requirements.txt
   streamlit run necta_analysis_app.py
   ```

2. **Select Analysis Mode**
   - Quick Analysis: First 50 schools (recommended for testing)
   - Full Analysis: All schools (comprehensive results)
   - Custom Selection: Choose specific schools

3. **Start Analysis**
   - Click "🚀 Start Analysis"
   - Wait for completion (progress bar shows status)
   - Explore results in different tabs

## Detailed Feature Guide

### 1. Overview Tab 📈

**What You'll See:**
- Total number of schools analyzed
- Total students across all schools
- Average GPA
- Average pass rate
- Total Division I students

**Visualizations:**
- Pie charts showing distribution by school type and ownership
- Bar chart showing overall division performance

**Use This For:**
- Getting a quick snapshot of overall performance
- Understanding the composition of schools analyzed
- Seeing national-level statistics

### 2. Top Performers Tab 🏆

**Features:**
- Rank schools by GPA, Division I rate, or Pass rate
- Filter by school type (Boys/Girls/Mixed)
- Filter by ownership (Government/Private)
- View top 10 with detailed metrics
- Full top 50 ranking table
- Interactive scatter plot for comparison

**How to Use:**
1. Select ranking criteria from dropdown
2. Apply filters if needed
3. Click on expandable sections to see details
4. Use the table to compare multiple schools
5. Hover over scatter plot points for details

**Best For:**
- Parents looking for top schools for their children
- Students selecting A-level schools
- Comparing schools in specific categories

### 3. Regional Analysis Tab 📍

**What You'll Find:**
- Performance metrics by region
- Number of schools per region
- Total students per region
- Average GPA by region
- Average pass rates by region
- Total Division I students per region

**Visualizations:**
- Bar charts comparing regional GPA and pass rates
- Treemap showing school distribution

**Use Cases:**
- Identifying strongest regions for education
- Regional resource allocation planning
- Comparing regional performance
- Finding schools in specific regions

### 4. Subject Analysis Tab 📚

**Analysis Includes:**
- Science vs Arts performance comparison
- Top 20 subjects by GPA
- Subject category breakdown
- Pass rates by subject
- Student distribution across subjects

**Key Insights:**
- Which subjects perform best nationally
- Science vs Arts trends
- Subject-specific GPA analysis
- Pass rate patterns across subjects

**Useful For:**
- Understanding subject strengths
- Curriculum planning
- Subject selection guidance
- Resource allocation by subject

### 5. Comparative Analysis Tab 📊

**Comparisons Available:**
- Boys vs Girls vs Mixed schools
- Government vs Private schools
- Multiple performance indicators
- Side-by-side metrics

**Metrics Compared:**
- Average GPA
- Average pass rate
- Average Division I rate
- Number of schools
- Total students

**Applications:**
- Policy making
- Understanding school type impacts
- Ownership effect analysis
- Educational planning

### 6. Download Data Tab 💾

**Download Options:**

1. **All Schools Data (CSV)**
   - Complete dataset of all analyzed schools
   - Includes all metrics and performance data

2. **Top 50 Schools (CSV)**
   - Quick access to best performers
   - Useful for decision making

3. **Full Excel Report**
   - Multiple sheets with different views
   - All Schools sheet
   - Top 50 by GPA sheet
   - Regional summary sheet
   - Ready for further analysis

4. **Custom Filtered Download**
   - Filter by specific regions
   - Set minimum student count
   - Create custom datasets

## Tips and Best Practices

### For Parents

**Finding the Right School:**
1. Start with Regional Analysis to see schools in your area
2. Go to Top Performers and filter by your region
3. Compare GPA, Division I rate, and pass rate
4. Download filtered list for offline review
5. Consider school type (Boys/Girls/Mixed) for your child
6. Check subject performance if child has specific interests

**Key Metrics to Look For:**
- Division I Rate > 70% (excellent)
- Overall Pass Rate > 90% (good)
- GPA < 2.0 (excellent)

### For Educators

**Benchmarking Your School:**
1. Use Custom Selection to add your school and competitors
2. Compare performance metrics
3. Analyze subject-specific performance
4. Identify areas for improvement
5. Download comparative data

**Performance Tracking:**
- Monitor Division I rate trends
- Compare with regional averages
- Analyze subject-specific gaps
- Track pass rate improvements

### For Students

**Choosing A-Level School:**
1. Check Top Performers for schools with best A-level preparation
2. Look at subject performance in your areas of interest
3. Consider Division I rates as indicator of quality
4. Check school type preference
5. Balance location and performance

**Red Flags:**
- Division I rate < 30%
- Pass rate < 70%
- GPA > 3.5

## Understanding the Metrics

### GPA (Grade Point Average)
- Scale: 1.0 (best) to 5.0 (worst)
- < 2.0: Excellent
- 2.0 - 3.0: Good
- 3.0 - 4.0: Average
- > 4.0: Poor

### Division Breakdown
- **Division I**: Aggregate 4-13 (Excellent)
- **Division II**: Aggregate 14-23 (Good)
- **Division III**: Aggregate 24-29 (Average)
- **Division IV**: Aggregate 30-35 (Pass)
- **Division 0**: Failed

### Pass Rate
- Percentage of students passing (Div I-IV)
- 90%+: Excellent
- 80-90%: Very Good
- 70-80%: Good
- < 70%: Needs improvement

### Division I Rate
- Percentage of students achieving Division I
- 70%+: Outstanding
- 50-70%: Excellent
- 30-50%: Good
- < 30%: Average

## Frequently Asked Questions

**Q: How long does full analysis take?**
A: Full analysis of all schools can take 10-30 minutes depending on internet speed and total number of schools.

**Q: Can I analyze specific schools only?**
A: Yes! Use Custom Selection mode and search for specific schools.

**Q: Why do some schools fail to load?**
A: Some school pages may have different formats or be temporarily unavailable. This is normal.

**Q: Can I save my analysis for later?**
A: Yes, use the Download options to save data in CSV or Excel format.

**Q: Is the data updated automatically?**
A: The app scrapes data in real-time from NECTA website, so it always shows current data.

**Q: Can I compare schools across regions?**
A: Absolutely! Use Top Performers with no regional filter, or use Comparative Analysis.

**Q: What's the difference between GPA and Division I rate?**
A: GPA is the average grade across all divisions. Division I rate specifically shows percentage of top performers.

**Q: How accurate is the data?**
A: Data is scraped directly from official NECTA website in real-time, ensuring maximum accuracy.

## Advanced Features

### Custom Filters
- Combine multiple filters for precise analysis
- Filter by region, type, and ownership simultaneously
- Set minimum student thresholds
- Create focused datasets

### Export Options
- CSV for quick sharing
- Excel for detailed analysis with multiple sheets
- Filtered exports for targeted data

### Visualizations
- Interactive charts - click, zoom, hover for details
- Multiple chart types - bar, pie, scatter, treemap
- Color-coded performance indicators
- Responsive design for all screen sizes

## Technical Support

**Common Issues:**

1. **"Failed to load school links"**
   - Check internet connection
   - Verify NECTA website is accessible
   - Try again after a few minutes

2. **Slow Performance**
   - Use Quick Analysis mode
   - Select fewer schools in Custom mode
   - Close other browser tabs

3. **Charts Not Loading**
   - Enable JavaScript in browser
   - Clear browser cache
   - Try different browser

4. **Download Not Working**
   - Check browser download settings
   - Ensure sufficient disk space
   - Try different format (CSV vs Excel)

## Best Practices

1. **Start with Quick Analysis** to understand the interface
2. **Use filters** to narrow down to relevant schools
3. **Download data** for offline analysis and sharing
4. **Compare multiple metrics** for comprehensive view
5. **Regular updates** - run analysis periodically for latest data

## Conclusion

This dashboard provides comprehensive insights into NECTA Form 4 results, helping parents, students, educators, and policy makers make informed decisions about education in Tanzania.

For best results:
- Explore all tabs to get complete picture
- Use filters to focus on relevant data
- Download data for detailed offline analysis
- Compare multiple metrics, not just one
- Consider context (region, school type, etc.)

---

**Need Help?** Review the README.md file for installation and setup instructions.

**Found a Bug?** Report issues to help improve the tool.

**Have Suggestions?** Feedback welcome for new features and improvements.
