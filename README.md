# NECTA Form 4 Results Analysis Dashboard 2025

A comprehensive Streamlit web application for analyzing NECTA (National Examinations Council of Tanzania) Certificate of Secondary Education Examination (CSEE) Form 4 results for the year 2025.

## 🎯 Features

### Core Functionality
- **Automated Web Scraping**: Extracts data from NECTA's official results website
- **Comprehensive School Analysis**: Analyzes performance metrics for all schools
- **Multiple Analysis Modes**: 
  - Quick Analysis (50 schools)
  - Full Analysis (all schools)
  - Custom Selection (select specific schools)

### Analysis & Visualizations

#### 1. Overall Performance Overview
- Total schools, students, and key metrics
- Distribution by school type (Boys/Girls/Mixed)
- Distribution by ownership (Government/Private)
- Division performance breakdown
- Interactive charts and graphs

#### 2. Top Performers
- Ranking by GPA, Division I rate, or Pass rate
- Filter by school type and ownership
- Top 10 detailed metrics
- Top 50 comprehensive ranking table
- Interactive scatter plots for comparison

#### 3. Regional Analysis
- Performance metrics by region
- Average GPA by region
- Pass rates comparison
- School distribution across regions
- Treemap visualization

#### 4. Subject-wise Analysis
- Science vs Arts performance comparison
- Top performing subjects
- Subject category breakdown
- Pass rates by subject
- GPA analysis per subject

#### 5. Comparative Analysis
- Boys vs Girls vs Mixed schools
- Government vs Private schools
- Multiple performance indicators
- Side-by-side comparisons

#### 6. Download Capabilities
- All schools data (CSV)
- Top 50 performers (CSV)
- Full Excel report with multiple sheets
- Custom filtered downloads
- Regional summaries

## 📊 Key Metrics Tracked

- **School Information**: Name, Code, Region, Type, Ownership
- **Performance Metrics**: GPA, Pass Rate, Division I Rate
- **Student Distribution**: Total students, Division breakdown (I, II, III, IV, 0)
- **Subject Performance**: Individual subject GPA, pass rates, student numbers
- **Regional Statistics**: Regional averages and comparisons

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- Internet connection (for scraping NECTA website)

### Setup Steps

1. **Clone or download this repository**
   ```bash
   # Create a new directory
   mkdir necta-analysis
   cd necta-analysis
   ```

2. **Install required packages**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   streamlit run necta_analysis_app.py
   ```

4. **Access the dashboard**
   - The app will automatically open in your default browser
   - Default URL: http://localhost:8501

## 💡 How to Use

### Step 1: Select Analysis Mode
Choose from the sidebar:
- **Quick Analysis**: Analyzes first 50 schools (fast, for demo)
- **Full Analysis**: Analyzes all schools (comprehensive, takes longer)
- **Custom Selection**: Select specific schools to analyze

### Step 2: Start Analysis
- Click "🚀 Start Analysis" button
- Wait for the scraping and analysis to complete
- Progress bar shows real-time status

### Step 3: Explore Results
Navigate through different tabs:
- **Overview**: General statistics and distributions
- **Top Performers**: Rankings and best schools
- **Regional Analysis**: Performance by region
- **Subject Analysis**: Subject-wise performance
- **Comparative Analysis**: Category comparisons
- **Download Data**: Export results in various formats

### Step 4: Download Results
- Choose from multiple download options
- Apply custom filters for specific data
- Export as CSV or Excel format

## 📈 Use Cases

### For Parents
- Identify best performing schools in your region
- Compare schools by type (boys/girls/mixed)
- Find schools with high Division I rates
- Download lists for decision making

### For Educators
- Analyze regional performance trends
- Compare subject performance
- Benchmark school performance
- Identify areas for improvement

### For Policy Makers
- Regional education analysis
- Government vs Private school comparison
- Resource allocation insights
- Performance monitoring

### For Students
- Find top performing schools for A-level selection
- Subject-wise school performance
- Regional school options
- Data-driven school selection

## 🔧 Technical Details

### Data Sources
- Primary: https://matokeo.necta.go.tz/results/2025/csee/
- Real-time web scraping from official NECTA website

### Technologies Used
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **BeautifulSoup**: Web scraping
- **Plotly**: Interactive visualizations
- **Requests**: HTTP library for web scraping

### Performance Optimization
- Caching mechanism for faster repeated access
- Progress tracking for long operations
- Rate limiting to avoid server overload
- Efficient data structures

## 📝 Data Fields Extracted

### School-Level Data
- School Name
- School Code
- Region
- Overall GPA
- School Type (Boys/Girls/Mixed)
- Ownership (Government/Private)
- Total Students
- Division Distribution (I, II, III, IV, 0)

### Subject-Level Data
- Subject Name
- Subject Code
- Students Registered
- Students Passed
- Subject GPA
- Pass Rate
- Subject Category (Science/Arts/Other)

## ⚠️ Important Notes

1. **Internet Connection**: Required for accessing NECTA website
2. **Processing Time**: Full analysis of all schools may take 10-30 minutes
3. **Rate Limiting**: Built-in delays to respect server resources
4. **Data Accuracy**: Data is scraped in real-time from official source
5. **Browser Compatibility**: Works best on modern browsers (Chrome, Firefox, Edge)

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Failed to load school links"
- **Solution**: Check internet connection, verify NECTA website is accessible

**Issue**: Slow performance
- **Solution**: Use Quick Analysis mode or select fewer schools

**Issue**: Some schools failed to extract
- **Solution**: Normal behavior, some school pages may have different formats

**Issue**: Charts not displaying
- **Solution**: Ensure JavaScript is enabled in your browser

## 🔄 Updates and Maintenance

The application scrapes data in real-time, so it will always reflect the current state of the NECTA website. No manual updates required.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### Important Notes:
- This software is provided for **educational and informational purposes only**
- All examination data is sourced from NECTA's official website
- The data remains the property of **NECTA (National Examinations Council of Tanzania)**
- This tool is **not affiliated with or endorsed by NECTA**
- Users should **verify critical information** with official NECTA sources
- Not for commercial use without proper authorization

### Third-Party Licenses:
This project uses the following open-source libraries:
- Streamlit (Apache 2.0 License)
- Pandas (BSD 3-Clause License)
- Plotly (MIT License)
- BeautifulSoup4 (MIT License)
- Requests (Apache 2.0 License)

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Ways to Contribute:
- 🐛 Report bugs
- 💡 Suggest new features
- 📝 Improve documentation
- 🔧 Submit code improvements
- 🧪 Help with testing

### Quick Contribution Guide:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and development process.

## 📧 Support

For issues or questions:
- Check the troubleshooting section
- Review NECTA's official website
- Verify internet connectivity

## 🎓 Acknowledgments

- Data source: NECTA (National Examinations Council of Tanzania)
- Built with Streamlit, Pandas, and Plotly
- Designed for education sector stakeholders in Tanzania

---

**Last Updated**: February 2025
**Version**: 1.0.0
**Status**: Active and Maintained
