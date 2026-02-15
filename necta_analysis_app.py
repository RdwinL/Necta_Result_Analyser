import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import re
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
import time

# Page configuration
st.set_page_config(
    page_title="NECTA Form 4 Results Analysis 2025",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 20px;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stDownloadButton button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Caching functions for better performance
@st.cache_data(ttl=3600)
def get_school_links():
    """Extract all school links from the index page"""
    base_url = "https://matokeo.necta.go.tz/results/2025/csee/"
    index_url = f"{base_url}index.htm"
    
    try:
        response = requests.get(index_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        school_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('results/') and href.endswith('.htm'):
                school_code = href.split('/')[-1].replace('.htm', '')
                school_name = link.get_text(strip=True)
                school_links.append({
                    'code': school_code.upper(),
                    'name': school_name,
                    'url': f"{base_url}{href}"
                })
        
        return school_links
    except Exception as e:
        st.error(f"Error fetching school links: {e}")
        return []

@st.cache_data(ttl=3600)
def extract_school_data(url):
    """Extract detailed data from a school's result page"""
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Extract school name
        school_name_tag = soup.find('h3')
        school_name = school_name_tag.get_text(strip=True) if school_name_tag else "Unknown"
        
        # Extract region and GPA
        info_tables = soup.find_all('table')
        region = "Unknown"
        gpa = None
        school_type = "Unknown"
        
        for table in info_tables:
            text = table.get_text()
            if "REGION" in text:
                region_match = re.search(r'REGION\s*\|\s*([A-Z\s]+)', text)
                if region_match:
                    region = region_match.group(1).strip()
            if "GPA" in text:
                gpa_match = re.search(r'GPA\s*\|\s*([\d.]+)', text)
                if gpa_match:
                    gpa = float(gpa_match.group(1))
        
        # Determine school type from name
        name_lower = school_name.lower()
        if "girls" in name_lower or "girl's" in name_lower:
            school_type = "Girls"
        elif "boys" in name_lower or "boy's" in name_lower:
            school_type = "Boys"
        else:
            school_type = "Mixed"
        
        # Determine ownership (Government/Private)
        ownership = "Private" if any(word in name_lower for word in ['seminary', 'islamic', 'christian', 'catholic']) else "Government"
        
        # Extract division summary
        div_summary = {}
        div_table = None
        for table in soup.find_all('table'):
            if 'DIVISION PERFORMANCE SUMMARY' in table.get_text():
                div_table = table
                break
        
        if div_table:
            rows = div_table.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')
                if len(cols) >= 6:
                    sex = cols[0].get_text(strip=True)
                    if sex in ['F', 'M', 'T']:
                        div_summary[sex] = {
                            'I': int(cols[1].get_text(strip=True) or 0),
                            'II': int(cols[2].get_text(strip=True) or 0),
                            'III': int(cols[3].get_text(strip=True) or 0),
                            'IV': int(cols[4].get_text(strip=True) or 0),
                            '0': int(cols[5].get_text(strip=True) or 0)
                        }
        
        # Extract subject performance
        subjects_performance = []
        subjects_table = None
        for table in soup.find_all('table'):
            if 'SUBJECTS PERFORMANCE' in table.get_text():
                subjects_table = table
                break
        
        if subjects_table:
            rows = subjects_table.find_all('tr')
            for row in rows[1:]:
                cols = row.find_all('td')
                if len(cols) >= 8:
                    try:
                        code = cols[0].get_text(strip=True)
                        subject = cols[1].get_text(strip=True)
                        sat = int(cols[3].get_text(strip=True) or 0)
                        passed = int(cols[6].get_text(strip=True) or 0)
                        subject_gpa = float(cols[7].get_text(strip=True) or 0)
                        
                        subjects_performance.append({
                            'code': code,
                            'subject': subject,
                            'students': sat,
                            'passed': passed,
                            'gpa': subject_gpa,
                            'pass_rate': (passed / sat * 100) if sat > 0 else 0
                        })
                    except:
                        continue
        
        # Calculate total students
        total_students = div_summary.get('T', {}).get('I', 0) + \
                        div_summary.get('T', {}).get('II', 0) + \
                        div_summary.get('T', {}).get('III', 0) + \
                        div_summary.get('T', {}).get('IV', 0) + \
                        div_summary.get('T', {}).get('0', 0)
        
        return {
            'name': school_name,
            'region': region,
            'gpa': gpa,
            'type': school_type,
            'ownership': ownership,
            'divisions': div_summary,
            'subjects': subjects_performance,
            'total_students': total_students
        }
    except Exception as e:
        st.error(f"Error extracting data from {url}: {e}")
        return None

def categorize_subject(subject_name):
    """Categorize subjects into Science and Arts"""
    science_keywords = ['PHYSICS', 'CHEMISTRY', 'BIOLOGY', 'MATHEMATICS', 'MATH']
    arts_keywords = ['HISTORY', 'GEOGRAPHY', 'CIVICS', 'KISWAHILI', 'ENGLISH']
    
    subject_upper = subject_name.upper()
    if any(keyword in subject_upper for keyword in science_keywords):
        return 'Science'
    elif any(keyword in subject_upper for keyword in arts_keywords):
        return 'Arts'
    return 'Other'

def main():
    st.markdown('<h1 class="main-header">📊 NECTA CSEE 2025 Results Analysis Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.title("🔍 Navigation & Filters")
    
    # Get school links
    with st.spinner("Loading school data..."):
        school_links = get_school_links()
    
    if not school_links:
        st.error("Failed to load school links. Please check your internet connection.")
        return
    
    st.sidebar.success(f"Found {len(school_links)} schools")
    
    # Analysis options
    analysis_mode = st.sidebar.radio(
        "Select Analysis Mode",
        ["Quick Analysis (Sample)", "Full Analysis (All Schools)", "Custom Selection"]
    )
    
    schools_to_analyze = []
    
    if analysis_mode == "Quick Analysis (Sample)":
        # Analyze first 50 schools for quick demo
        schools_to_analyze = school_links[:50]
        st.sidebar.info("Analyzing first 50 schools for quick results")
        
    elif analysis_mode == "Full Analysis (All Schools)":
        schools_to_analyze = school_links
        st.sidebar.warning(f"This will analyze all {len(school_links)} schools. This may take several minutes.")
        
    else:  # Custom Selection
        # Filter options
        search_term = st.sidebar.text_input("Search School Name", "")
        
        filtered_schools = [s for s in school_links if search_term.lower() in s['name'].lower()]
        
        selected_schools = st.sidebar.multiselect(
            "Select Schools",
            options=filtered_schools,
            format_func=lambda x: x['name'],
            max_selections=100
        )
        schools_to_analyze = selected_schools
    
    # Start Analysis Button
    if st.sidebar.button("🚀 Start Analysis", type="primary"):
        if not schools_to_analyze:
            st.warning("Please select at least one school to analyze")
            return
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        all_data = []
        failed_schools = []
        
        for idx, school in enumerate(schools_to_analyze):
            status_text.text(f"Analyzing: {school['name']} ({idx+1}/{len(schools_to_analyze)})")
            progress_bar.progress((idx + 1) / len(schools_to_analyze))
            
            data = extract_school_data(school['url'])
            if data:
                data['code'] = school['code']
                data['url'] = school['url']
                all_data.append(data)
            else:
                failed_schools.append(school['name'])
            
            # Rate limiting
            time.sleep(0.5)
        
        progress_bar.empty()
        status_text.empty()
        
        if failed_schools:
            st.warning(f"Failed to extract data from {len(failed_schools)} schools")
        
        if not all_data:
            st.error("No data extracted. Please try again.")
            return
        
        # Store in session state
        st.session_state['analysis_data'] = all_data
        st.success(f"✅ Successfully analyzed {len(all_data)} schools!")
    
    # Display analysis if data exists
    if 'analysis_data' in st.session_state:
        display_analysis(st.session_state['analysis_data'])

def display_analysis(data):
    """Display comprehensive analysis with visualizations"""
    
    # Convert to DataFrame for easier analysis
    df_schools = pd.DataFrame([{
        'School Name': d['name'],
        'Code': d['code'],
        'Region': d['region'],
        'GPA': d['gpa'],
        'Type': d['type'],
        'Ownership': d['ownership'],
        'Total Students': d['total_students'],
        'Div I': d['divisions'].get('T', {}).get('I', 0),
        'Div II': d['divisions'].get('T', {}).get('II', 0),
        'Div III': d['divisions'].get('T', {}).get('III', 0),
        'Div IV': d['divisions'].get('T', {}).get('IV', 0),
        'Div 0': d['divisions'].get('T', {}).get('0', 0),
    } for d in data])
    
    # Calculate pass rate (Div I-IV)
    df_schools['Pass Rate (%)'] = ((df_schools['Div I'] + df_schools['Div II'] + 
                                     df_schools['Div III'] + df_schools['Div IV']) / 
                                    df_schools['Total Students'] * 100).fillna(0)
    
    df_schools['Div I Rate (%)'] = (df_schools['Div I'] / df_schools['Total Students'] * 100).fillna(0)
    
    # Tabs for different views
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "📈 Overview", "🏆 Top Performers", "📍 Regional Analysis", 
        "📚 Subject Analysis", "📊 Comparative Analysis", "💾 Download Data"
    ])
    
    with tab1:
        display_overview(df_schools, data)
    
    with tab2:
        display_top_performers(df_schools)
    
    with tab3:
        display_regional_analysis(df_schools)
    
    with tab4:
        display_subject_analysis(data)
    
    with tab5:
        display_comparative_analysis(df_schools)
    
    with tab6:
        display_download_options(df_schools, data)

def display_overview(df_schools, raw_data):
    """Display overview statistics and metrics"""
    st.header("📈 Overall Performance Overview")
    
    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("Total Schools", len(df_schools))
    
    with col2:
        st.metric("Total Students", f"{df_schools['Total Students'].sum():,}")
    
    with col3:
        avg_gpa = df_schools['GPA'].mean()
        st.metric("Average GPA", f"{avg_gpa:.2f}")
    
    with col4:
        avg_pass_rate = df_schools['Pass Rate (%)'].mean()
        st.metric("Avg Pass Rate", f"{avg_pass_rate:.1f}%")
    
    with col5:
        div_i_students = df_schools['Div I'].sum()
        st.metric("Division I Students", f"{div_i_students:,}")
    
    st.markdown("---")
    
    # Distribution charts
    col1, col2 = st.columns(2)
    
    with col1:
        # School type distribution
        fig = px.pie(df_schools, names='Type', title='Distribution by School Type',
                     color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Ownership distribution
        fig = px.pie(df_schools, names='Ownership', title='Distribution by Ownership',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    
    # Division distribution
    st.subheader("Division Distribution Across All Schools")
    div_totals = {
        'Division I': df_schools['Div I'].sum(),
        'Division II': df_schools['Div II'].sum(),
        'Division III': df_schools['Div III'].sum(),
        'Division IV': df_schools['Div IV'].sum(),
        'Division 0': df_schools['Div 0'].sum()
    }
    
    fig = px.bar(x=list(div_totals.keys()), y=list(div_totals.values()),
                 labels={'x': 'Division', 'y': 'Number of Students'},
                 title='Overall Division Performance',
                 color=list(div_totals.values()),
                 color_continuous_scale='RdYlGn')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def display_top_performers(df_schools):
    """Display top performing schools with various filters"""
    st.header("🏆 Top Performing Schools")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ranking_criteria = st.selectbox(
            "Rank By",
            ["GPA", "Division I Rate (%)", "Pass Rate (%)"]
        )
    
    with col2:
        filter_type = st.selectbox(
            "Filter by Type",
            ["All", "Boys", "Girls", "Mixed"]
        )
    
    with col3:
        filter_ownership = st.selectbox(
            "Filter by Ownership",
            ["All", "Government", "Private"]
        )
    
    # Apply filters
    filtered_df = df_schools.copy()
    if filter_type != "All":
        filtered_df = filtered_df[filtered_df['Type'] == filter_type]
    if filter_ownership != "All":
        filtered_df = filtered_df[filtered_df['Ownership'] == filter_ownership]
    
    # Sort by selected criteria
    top_schools = filtered_df.nlargest(50, ranking_criteria)
    
    # Display top 10 in metrics
    st.subheader(f"Top 10 Schools by {ranking_criteria}")
    
    for idx, row in top_schools.head(10).iterrows():
        with st.expander(f"#{top_schools.index.get_loc(idx) + 1} - {row['School Name']} ({row['Region']})"):
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("GPA", f"{row['GPA']:.2f}")
            col2.metric("Div I Rate", f"{row['Div I Rate (%)']:.1f}%")
            col3.metric("Pass Rate", f"{row['Pass Rate (%)']:.1f}%")
            col4.metric("Students", int(row['Total Students']))
    
    # Full ranking table
    st.subheader(f"Top 50 Schools Ranking")
    display_df = top_schools[['School Name', 'Region', 'Type', 'Ownership', 'GPA', 
                               'Div I Rate (%)', 'Pass Rate (%)', 'Total Students']].reset_index(drop=True)
    display_df.index += 1
    st.dataframe(display_df, use_container_width=True, height=600)
    
    # Visualization
    st.subheader("Performance Comparison")
    fig = px.scatter(top_schools, x='GPA', y='Div I Rate (%)', 
                     size='Total Students', color='Type',
                     hover_data=['School Name', 'Region'],
                     title='GPA vs Division I Rate',
                     labels={'GPA': 'School GPA', 'Div I Rate (%)': 'Division I Rate (%)'},
                     color_discrete_sequence=px.colors.qualitative.Bold)
    st.plotly_chart(fig, use_container_width=True)

def display_regional_analysis(df_schools):
    """Display regional performance analysis"""
    st.header("📍 Regional Performance Analysis")
    
    # Regional summary
    regional_stats = df_schools.groupby('Region').agg({
        'School Name': 'count',
        'Total Students': 'sum',
        'GPA': 'mean',
        'Pass Rate (%)': 'mean',
        'Div I Rate (%)': 'mean',
        'Div I': 'sum'
    }).round(2)
    
    regional_stats.columns = ['Number of Schools', 'Total Students', 'Avg GPA', 
                              'Avg Pass Rate (%)', 'Avg Div I Rate (%)', 'Total Div I']
    regional_stats = regional_stats.sort_values('Avg GPA', ascending=False)
    
    # Display table
    st.subheader("Regional Performance Summary")
    st.dataframe(regional_stats, use_container_width=True)
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Regional GPA comparison
        fig = px.bar(regional_stats.reset_index(), x='Region', y='Avg GPA',
                     title='Average GPA by Region',
                     color='Avg GPA',
                     color_continuous_scale='Viridis')
        fig.update_xaxis(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Regional pass rate comparison
        fig = px.bar(regional_stats.reset_index(), x='Region', y='Avg Pass Rate (%)',
                     title='Average Pass Rate by Region',
                     color='Avg Pass Rate (%)',
                     color_continuous_scale='Blues')
        fig.update_xaxis(tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    
    # School distribution by region
    st.subheader("School Distribution by Region")
    region_counts = df_schools['Region'].value_counts().reset_index()
    region_counts.columns = ['Region', 'Number of Schools']
    
    fig = px.treemap(region_counts, path=['Region'], values='Number of Schools',
                     title='School Distribution Across Regions',
                     color='Number of Schools',
                     color_continuous_scale='Reds')
    st.plotly_chart(fig, use_container_width=True)

def display_subject_analysis(data):
    """Display subject-wise performance analysis"""
    st.header("📚 Subject-wise Performance Analysis")
    
    # Compile all subject data
    all_subjects = []
    for school in data:
        for subj in school.get('subjects', []):
            all_subjects.append({
                'School': school['name'],
                'Region': school['region'],
                'Subject': subj['subject'],
                'Category': categorize_subject(subj['subject']),
                'Students': subj['students'],
                'Passed': subj['passed'],
                'GPA': subj['gpa'],
                'Pass Rate': subj['pass_rate']
            })
    
    if not all_subjects:
        st.warning("No subject data available")
        return
    
    df_subjects = pd.DataFrame(all_subjects)
    
    # Subject category analysis
    col1, col2 = st.columns(2)
    
    with col1:
        category_stats = df_subjects.groupby('Category').agg({
            'Students': 'sum',
            'Pass Rate': 'mean',
            'GPA': 'mean'
        }).round(2)
        
        st.subheader("Performance by Subject Category")
        st.dataframe(category_stats, use_container_width=True)
    
    with col2:
        fig = px.pie(df_subjects, names='Category', values='Students',
                     title='Student Distribution by Subject Category',
                     color_discrete_sequence=px.colors.qualitative.Set2)
        st.plotly_chart(fig, use_container_width=True)
    
    # Best performing subjects
    st.subheader("Top Performing Subjects")
    
    subject_summary = df_subjects.groupby('Subject').agg({
        'Students': 'sum',
        'Passed': 'sum',
        'GPA': 'mean',
        'Pass Rate': 'mean'
    }).round(2)
    
    subject_summary = subject_summary.sort_values('GPA', ascending=False).head(20)
    
    fig = px.bar(subject_summary.reset_index(), x='Subject', y='GPA',
                 title='Top 20 Subjects by Average GPA',
                 color='GPA',
                 color_continuous_scale='RdYlGn',
                 hover_data=['Students', 'Pass Rate'])
    fig.update_xaxis(tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)
    
    # Science vs Arts comparison
    st.subheader("Science vs Arts Performance Comparison")
    
    science_arts = df_subjects[df_subjects['Category'].isin(['Science', 'Arts'])].groupby('Category').agg({
        'Students': 'sum',
        'GPA': 'mean',
        'Pass Rate': 'mean'
    }).round(2)
    
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Average GPA', x=science_arts.index, y=science_arts['GPA']))
    fig.add_trace(go.Bar(name='Average Pass Rate (%)', x=science_arts.index, y=science_arts['Pass Rate']))
    fig.update_layout(title='Science vs Arts: GPA and Pass Rate Comparison',
                      barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    # Full subject table
    st.subheader("Detailed Subject Performance")
    subject_display = subject_summary.reset_index()
    st.dataframe(subject_display, use_container_width=True, height=400)

def display_comparative_analysis(df_schools):
    """Display comparative analysis between different school categories"""
    st.header("📊 Comparative Analysis")
    
    # Boys vs Girls vs Mixed
    st.subheader("Performance by School Type (Boys/Girls/Mixed)")
    
    type_comparison = df_schools.groupby('Type').agg({
        'School Name': 'count',
        'Total Students': 'sum',
        'GPA': 'mean',
        'Pass Rate (%)': 'mean',
        'Div I Rate (%)': 'mean'
    }).round(2)
    
    type_comparison.columns = ['Number of Schools', 'Total Students', 'Avg GPA', 
                               'Avg Pass Rate (%)', 'Avg Div I Rate (%)']
    
    st.dataframe(type_comparison, use_container_width=True)
    
    # Visualization
    fig = go.Figure()
    fig.add_trace(go.Bar(name='Avg GPA', x=type_comparison.index, y=type_comparison['Avg GPA']))
    fig.add_trace(go.Bar(name='Avg Pass Rate (%)', x=type_comparison.index, 
                         y=type_comparison['Avg Pass Rate (%)']))
    fig.add_trace(go.Bar(name='Avg Div I Rate (%)', x=type_comparison.index, 
                         y=type_comparison['Avg Div I Rate (%)']))
    fig.update_layout(title='Performance Comparison by School Type', barmode='group')
    st.plotly_chart(fig, use_container_width=True)
    
    # Government vs Private
    st.subheader("Performance by Ownership (Government/Private)")
    
    ownership_comparison = df_schools.groupby('Ownership').agg({
        'School Name': 'count',
        'Total Students': 'sum',
        'GPA': 'mean',
        'Pass Rate (%)': 'mean',
        'Div I Rate (%)': 'mean'
    }).round(2)
    
    ownership_comparison.columns = ['Number of Schools', 'Total Students', 'Avg GPA', 
                                    'Avg Pass Rate (%)', 'Avg Div I Rate (%)']
    
    st.dataframe(ownership_comparison, use_container_width=True)
    
    # Visualization
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(ownership_comparison.reset_index(), x='Ownership', y='Avg GPA',
                     title='Average GPA: Government vs Private',
                     color='Avg GPA',
                     color_continuous_scale='Viridis')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig = px.bar(ownership_comparison.reset_index(), x='Ownership', y='Avg Pass Rate (%)',
                     title='Average Pass Rate: Government vs Private',
                     color='Avg Pass Rate (%)',
                     color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)

def display_download_options(df_schools, raw_data):
    """Provide download options for different datasets"""
    st.header("💾 Download Analysis Data")
    
    st.write("Download the analyzed data in various formats for further analysis or sharing.")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Download all schools data
        csv_all = df_schools.to_csv(index=False)
        st.download_button(
            label="📥 Download All Schools Data (CSV)",
            data=csv_all,
            file_name="necta_2025_all_schools.csv",
            mime="text/csv"
        )
    
    with col2:
        # Download top performers
        top_50 = df_schools.nlargest(50, 'GPA')
        csv_top = top_50.to_csv(index=False)
        st.download_button(
            label="🏆 Download Top 50 Schools (CSV)",
            data=csv_top,
            file_name="necta_2025_top_50_schools.csv",
            mime="text/csv"
        )
    
    with col3:
        # Download Excel with multiple sheets
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_schools.to_excel(writer, sheet_name='All Schools', index=False)
            df_schools.nlargest(50, 'GPA').to_excel(writer, sheet_name='Top 50 by GPA', index=False)
            
            regional_stats = df_schools.groupby('Region').agg({
                'School Name': 'count',
                'Total Students': 'sum',
                'GPA': 'mean',
                'Pass Rate (%)': 'mean'
            }).round(2)
            regional_stats.to_excel(writer, sheet_name='Regional Summary')
        
        excel_data = output.getvalue()
        st.download_button(
            label="📊 Download Full Report (Excel)",
            data=excel_data,
            file_name="necta_2025_full_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    # Custom filters for download
    st.subheader("Custom Filtered Download")
    
    col1, col2 = st.columns(2)
    
    with col1:
        selected_regions = st.multiselect(
            "Select Regions",
            options=df_schools['Region'].unique().tolist(),
            default=[]
        )
    
    with col2:
        min_students = st.number_input("Minimum Students", min_value=0, value=0)
    
    if selected_regions:
        filtered_df = df_schools[df_schools['Region'].isin(selected_regions)]
        if min_students > 0:
            filtered_df = filtered_df[filtered_df['Total Students'] >= min_students]
        
        st.write(f"Filtered Results: {len(filtered_df)} schools")
        
        csv_filtered = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv_filtered,
            file_name="necta_2025_filtered_schools.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
