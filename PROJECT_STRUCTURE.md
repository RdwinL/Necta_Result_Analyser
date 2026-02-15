# Project Structure

This document provides an overview of the NECTA Analysis Dashboard project structure and organization.

## 📁 Directory Structure

```
necta-analysis-dashboard/
│
├── necta_analysis_app.py      # Main Streamlit application
├── requirements.txt            # Python dependencies
│
├── setup.sh                    # Linux/Mac setup script
├── setup.bat                   # Windows setup script
│
├── README.md                   # Project overview and setup guide
├── QUICK_START.md             # Quick start guide for new users
├── USER_GUIDE.md              # Detailed user guide
├── CONTRIBUTING.md            # Contribution guidelines
├── CHANGELOG.md               # Version history and changes
├── LICENSE                    # MIT License
├── PROJECT_STRUCTURE.md       # This file
│
├── .gitignore                 # Git ignore rules
│
└── (future directories)
    ├── data/                  # Cached data (not tracked)
    ├── tests/                 # Unit tests (future)
    ├── docs/                  # Additional documentation (future)
    └── assets/                # Images and resources (future)
```

## 📄 File Descriptions

### Core Application Files

#### `necta_analysis_app.py`
**Purpose:** Main Streamlit application file
**Size:** ~28KB
**Key Components:**
- Web scraping functions
- Data processing and analysis
- Visualization components
- User interface layout
- Download functionality

**Main Functions:**
```python
get_school_links()              # Fetches all school URLs
extract_school_data()           # Scrapes individual school data
categorize_subject()            # Categorizes subjects
main()                          # Main application entry point
display_analysis()              # Renders analysis tabs
display_overview()              # Overview tab content
display_top_performers()        # Top performers tab
display_regional_analysis()     # Regional analysis tab
display_subject_analysis()      # Subject analysis tab
display_comparative_analysis()  # Comparative analysis tab
display_download_options()      # Download functionality
```

#### `requirements.txt`
**Purpose:** Python package dependencies
**Contents:**
- streamlit==1.31.0
- pandas==2.1.4
- requests==2.31.0
- beautifulsoup4==4.12.3
- plotly==5.18.0
- openpyxl==3.1.2
- lxml==5.1.0

### Setup and Installation

#### `setup.sh`
**Purpose:** Automated setup for Linux/Mac
**Features:**
- Python version check
- Dependency installation
- Success/failure reporting
- Usage instructions

#### `setup.bat`
**Purpose:** Automated setup for Windows
**Features:**
- Same as setup.sh but for Windows
- Batch script format
- Pause for user to read output

### Documentation

#### `README.md`
**Purpose:** Main project documentation
**Sections:**
- Project overview
- Features list
- Installation instructions
- Usage guide
- Technical details
- Troubleshooting
- License information

**Size:** ~7KB
**Target Audience:** All users

#### `QUICK_START.md`
**Purpose:** Quick setup and first-use guide
**Sections:**
- Installation steps
- First-time usage
- Key features overview
- Common tasks
- Tips and troubleshooting

**Size:** ~3KB
**Target Audience:** New users

#### `USER_GUIDE.md`
**Purpose:** Comprehensive user manual
**Sections:**
- Detailed feature explanations
- Step-by-step guides
- Use cases by user type
- Metrics definitions
- FAQs
- Advanced features

**Size:** ~9KB
**Target Audience:** All users seeking detailed information

#### `CONTRIBUTING.md`
**Purpose:** Developer contribution guidelines
**Sections:**
- Code of conduct
- Development setup
- Coding standards
- Submission process
- Bug reporting
- Feature requests

**Size:** ~8KB
**Target Audience:** Contributors and developers

#### `CHANGELOG.md`
**Purpose:** Version history and updates
**Sections:**
- Current version details
- Future roadmap
- Breaking changes
- Bug fixes
- Security updates

**Size:** ~6KB
**Target Audience:** All users and developers

#### `PROJECT_STRUCTURE.md`
**Purpose:** Project organization overview
**This File**
**Target Audience:** Developers and contributors

### Legal and Configuration

#### `LICENSE`
**Purpose:** MIT License with disclaimers
**Key Points:**
- MIT License terms
- Educational use disclaimer
- NECTA data ownership
- Liability limitations

**Size:** ~2KB
**Target Audience:** Legal review and users

#### `.gitignore`
**Purpose:** Git exclusion rules
**Excludes:**
- Python cache files
- Virtual environments
- IDE configurations
- Log files
- Temporary files
- Data cache files

**Size:** ~2KB
**Target Audience:** Developers using Git

## 🏗️ Architecture Overview

### Application Architecture

```
┌─────────────────────────────────────────┐
│         User Interface (Streamlit)       │
│  ┌────────────────────────────────────┐ │
│  │  Sidebar: Navigation & Filters     │ │
│  └────────────────────────────────────┘ │
│  ┌────────────────────────────────────┐ │
│  │  Main Area: Tabs & Content         │ │
│  │  - Overview                         │ │
│  │  - Top Performers                   │ │
│  │  - Regional Analysis                │ │
│  │  - Subject Analysis                 │ │
│  │  - Comparative Analysis             │ │
│  │  - Download Data                    │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│         Data Layer (Pandas)              │
│  ┌────────────────────────────────────┐ │
│  │  DataFrames & Processing           │ │
│  │  - School data                      │ │
│  │  - Subject data                     │ │
│  │  - Aggregations                     │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│    Web Scraping Layer (BeautifulSoup)   │
│  ┌────────────────────────────────────┐ │
│  │  HTTP Requests & HTML Parsing      │ │
│  │  - School list extraction          │ │
│  │  - Individual school scraping      │ │
│  │  - Rate limiting                    │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
                    │
                    ▼
┌─────────────────────────────────────────┐
│      Data Source (NECTA Website)        │
│         matokeo.necta.go.tz             │
└─────────────────────────────────────────┘
```

### Data Flow

```
1. User Selection
   ↓
2. Fetch School Links (cached)
   ↓
3. Scrape School Data
   ├── Progress Tracking
   ├── Rate Limiting
   └── Error Handling
   ↓
4. Data Processing
   ├── Clean & Transform
   ├── Calculate Metrics
   └── Aggregate Statistics
   ↓
5. Visualization & Display
   ├── Interactive Charts
   ├── Tables
   └── Metrics
   ↓
6. Export Options
   ├── CSV
   └── Excel
```

## 🔧 Key Components

### Web Scraping Module

**Functions:**
- `get_school_links()` - Scrapes index page for school URLs
- `extract_school_data()` - Extracts detailed data from school pages

**Features:**
- Caching with `@st.cache_data`
- Rate limiting (0.5s delay)
- Error handling
- Progress tracking

### Data Processing Module

**Features:**
- DataFrame creation and manipulation
- Metric calculations
- Aggregations by region, type, ownership
- Subject categorization

### Visualization Module

**Chart Types:**
- Pie charts (distributions)
- Bar charts (comparisons)
- Scatter plots (correlations)
- Treemaps (hierarchical data)

**Library:** Plotly Express and Plotly Graph Objects

### Export Module

**Formats:**
- CSV (comma-separated values)
- Excel (multiple sheets)

**Options:**
- All schools
- Top performers
- Filtered datasets
- Custom selections

## 📊 Data Models

### School Data Structure
```python
{
    'name': str,              # School name
    'code': str,              # School code (e.g., 'S0239')
    'region': str,            # Region name
    'gpa': float,             # Overall GPA
    'type': str,              # Boys/Girls/Mixed
    'ownership': str,         # Government/Private
    'total_students': int,    # Total student count
    'divisions': {            # Division breakdown
        'T': {
            'I': int,
            'II': int,
            'III': int,
            'IV': int,
            '0': int
        }
    },
    'subjects': [             # Subject performance list
        {
            'subject': str,
            'students': int,
            'passed': int,
            'gpa': float,
            'pass_rate': float
        }
    ]
}
```

### DataFrame Schema

**Schools DataFrame:**
```
School Name      | str
Code            | str
Region          | str
GPA             | float
Type            | str (Boys/Girls/Mixed)
Ownership       | str (Government/Private)
Total Students  | int
Div I           | int
Div II          | int
Div III         | int
Div IV          | int
Div 0           | int
Pass Rate (%)   | float
Div I Rate (%)  | float
```

**Subjects DataFrame:**
```
School          | str
Region          | str
Subject         | str
Category        | str (Science/Arts/Other)
Students        | int
Passed          | int
GPA             | float
Pass Rate       | float
```

## 🎨 UI Components

### Sidebar
- Navigation controls
- Analysis mode selection
- School search/filter
- Custom selection

### Main Area
- Tab navigation
- Content display
- Interactive charts
- Download buttons

### Styling
- Custom CSS for headers
- Color-coded metrics
- Responsive design
- Clean, professional layout

## 🔐 Security Considerations

### Current Implementations
- Rate limiting to prevent abuse
- Input validation
- Error handling
- No sensitive data storage

### Future Enhancements
- API rate limiting
- User authentication (if needed)
- Data encryption (if storing sensitive info)
- HTTPS enforcement

## 🚀 Performance Optimizations

### Current
- Caching with Streamlit decorators
- Efficient pandas operations
- Progressive loading indicators
- Minimal unnecessary re-renders

### Future
- Concurrent web scraping
- Database caching
- Lazy loading for large datasets
- Code profiling and optimization

## 📈 Scalability

### Current Capacity
- Handles 1000+ schools
- Processing time: 10-30 minutes for full analysis
- Memory efficient with pandas

### Future Scaling
- Database integration
- Distributed scraping
- API endpoints
- Horizontal scaling

## 🧪 Testing Strategy

### Current
- Manual testing across features
- Cross-browser testing
- Multi-platform testing

### Future
- Unit tests with pytest
- Integration tests
- Automated UI tests
- Performance benchmarks
- CI/CD pipeline

## 📚 Dependencies

### Core Dependencies
```
streamlit       # Web framework
pandas          # Data processing
requests        # HTTP library
beautifulsoup4  # Web scraping
plotly          # Visualizations
openpyxl        # Excel export
lxml            # XML/HTML parsing
```

### Dependency Graph
```
necta_analysis_app.py
├── streamlit
│   ├── plotly
│   └── pandas
├── pandas
├── requests
├── beautifulsoup4
│   └── lxml
└── openpyxl
```

## 🔄 Version Control Strategy

### Branch Structure
```
main            # Stable release branch
develop         # Development branch
feature/*       # Feature branches
fix/*           # Bug fix branches
hotfix/*        # Critical fixes
```

### Commit Convention
```
feat: Add new feature
fix: Bug fix
docs: Documentation update
style: Code style changes
refactor: Code refactoring
test: Test additions
chore: Build/config changes
```

## 📦 Distribution

### Package Structure
```
necta-analysis-dashboard-v1.0.0/
├── necta_analysis_app.py
├── requirements.txt
├── setup.sh
├── setup.bat
├── README.md
├── QUICK_START.md
├── USER_GUIDE.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── LICENSE
└── .gitignore
```

### Installation Methods
1. Direct download (ZIP)
2. Git clone
3. PyPI package (future)
4. Docker container (future)

## 🎯 Future Enhancements

### Planned Structure Changes
```
necta-analysis-dashboard/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── scraper.py
│   ├── analyzer.py
│   └── visualizer.py
├── tests/
│   ├── test_scraper.py
│   ├── test_analyzer.py
│   └── test_visualizer.py
├── data/
│   └── cache/
├── config/
│   └── settings.py
└── docs/
    └── api/
```

## 📝 Maintenance

### Regular Tasks
- Update dependencies
- Fix reported bugs
- Improve documentation
- Add requested features
- Performance monitoring

### Release Cycle
- Major: New features (x.0.0)
- Minor: Enhancements (0.x.0)
- Patch: Bug fixes (0.0.x)

---

**Last Updated:** February 15, 2025
**Document Version:** 1.0.0
**Project Version:** 1.0.0
