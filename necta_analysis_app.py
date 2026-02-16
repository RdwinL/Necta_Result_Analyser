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
    page_title="NECTA Form 4 Results Analysis 2025 - Enhanced",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)
def get_school_links():
    """Extract all school links from the index page - both P and S codes"""
    base_url = "https://matokeo.necta.go.tz/results/2025/csee/"
    index_url = f"{base_url}index.htm"
    
    try:
        response = requests.get(index_url, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        school_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith('results/') and href.endswith('.htm'):
                school_code = href.split('/')[-1].replace('.htm', '').upper()
                school_name = link.get_text(strip=True)
                
                # Identify school type from code
                if school_code.startswith('P'):
                    centre_type = "Private Candidates"
                elif school_code.startswith('S'):
                    centre_type = "School Candidates"
                else:
                    centre_type = "Other"
                
                school_links.append({
                    'code': school_code,
                    'name': school_name,
                    'url': f"{base_url}{href}",
                    'centre_type': centre_type
                })
        
        return school_links
    except Exception as e:
        st.error(f"Error fetching school links: {e}")
        return []

def determine_school_level(school_name):
    """Determine if school is Secondary School or High School"""
    name_lower = school_name.lower()
    
    # Check for high school indicators
    if any(indicator in name_lower for indicator in ['high school', 'high']):
        return "High School"
    # Check for secondary school indicators
    elif any(indicator in name_lower for indicator in ['secondary school', 'secondary', 'sec']):
        return "Secondary School"
    # Seminary, seminary schools are typically secondary
    elif 'seminary' in name_lower:
        return "Secondary School (Seminary)"
    else:
        return "Secondary School"  # Default

def parse_detailed_subjects(subject_string):
    """Parse detailed subject results string into structured data"""
    subjects = {}
    
    # Pattern: SUBJECT_CODE - 'GRADE'
    pattern = r"([A-Z/]+)\s*-\s*'([A-F])'"
    matches = re.findall(pattern, subject_string)
    
    for subject_code, grade in matches:
        subjects[subject_code.strip()] = grade.strip()
    
    return subjects

def extract_candidate_results(soup):
    """Extract individual candidate results from the results table"""
    candidates = []
    
    # Find the table with candidate results (CNO, SEX, AGGT, DIV, DETAILED SUBJECTS)
    tables = soup.find_all('table')
    
    for table in tables:
        rows = table.find_all('tr')
        
        for row in rows:
            cols = row.find_all(['td', 'th'])
            
            # Look for rows with candidate data (should have CNO pattern)
            if len(cols) >= 5:
                first_col = cols[0].get_text(strip=True)
                
                # Check if this is a candidate row (format: S0239/0001 or P0239/0001)
                if re.match(r'[PS]\d{4}/\d{4}', first_col):
                    try:
                        cno = first_col
                        sex = cols[1].get_text(strip=True)
                        aggt = cols[2].get_text(strip=True)
                        div = cols[3].get_text(strip=True)
                        detailed_subjects = cols[4].get_text(strip=True) if len(cols) > 4 else ""
                        
                        # Parse subjects
                        subjects_dict = parse_detailed_subjects(detailed_subjects)
                        
                        candidates.append({
                            'CNO': cno,
                            'SEX': sex,
                            'AGGT': int(aggt) if aggt.isdigit() else None,
                            'DIV': div,
                            'subjects': subjects_dict,
                            'subject_string': detailed_subjects
                        })
                    except (ValueError, IndexError) as e:
                        continue
    
    return candidates

@st.cache_data(ttl=3600, show_spinner=False)
def extract_school_data_enhanced(url, max_retries=2):
    """Enhanced extraction with candidate-level data and all table structures"""
    
    for attempt in range(max_retries):
        try:
            # Set a reasonable timeout
            response = requests.get(url, timeout=15)
            
            if response.status_code != 200:
                if attempt < max_retries - 1:
                    time.sleep(1)
                    continue
                return None
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract school code from URL
            school_code = url.split('/')[-1].replace('.htm', '').upper()
            
            # Extract school name
            school_name_tag = soup.find('h3')
            school_name = school_name_tag.get_text(strip=True) if school_name_tag else "Unknown"
            
            # Determine school level
            school_level = determine_school_level(school_name)
            
            # Determine centre type from code
            if school_code.startswith('P'):
                centre_type = "Private Candidates"
            elif school_code.startswith('S'):
                centre_type = "School Candidates"
            else:
                centre_type = "Other"
            
            # Extract all text content for searching
            page_text = soup.get_text()
            
            # Extract Region
            region = "Unknown"
            region_patterns = [
                r'EXAMINATION CENTRE REGION\s*[|\s]*([A-Z\s]+)',
                r'REGION\s*[|\s]*([A-Z\s]+)',
                r'CENTRE REGION\s*[|\s]*([A-Z\s]+)'
            ]
            for pattern in region_patterns:
                region_match = re.search(pattern, page_text, re.IGNORECASE)
                if region_match:
                    region = region_match.group(1).strip()
                    break
            
            # Extract GPA
            gpa = None
            gpa_patterns = [
                r'EXAMINATION CENTRE GPA\s*[|\s]*([\d.]+)',
                r'GPA\s*[|\s]*([\d.]+)',
                r'CENTRE GPA\s*[|\s]*([\d.]+)'
            ]
            for pattern in gpa_patterns:
                gpa_match = re.search(pattern, page_text)
                if gpa_match:
                    try:
                        gpa = float(gpa_match.group(1))
                        break
                    except ValueError:
                        continue
            
            # Extract Total Passed Candidates
            total_passed = None
            passed_patterns = [
                r'TOTAL PASSED CANDIDATES\s*[|\s]*(\d+)',
                r'PASSED CANDIDATES\s*[|\s]*(\d+)'
            ]
            for pattern in passed_patterns:
                passed_match = re.search(pattern, page_text)
                if passed_match:
                    try:
                        total_passed = int(passed_match.group(1))
                        break
                    except ValueError:
                        continue
            
            # Determine school type from name
            name_lower = school_name.lower()
            if "girls" in name_lower or "girl's" in name_lower:
                school_type = "Girls"
            elif "boys" in name_lower or "boy's" in name_lower:
                school_type = "Boys"
            else:
                school_type = "Mixed"
            
            # Determine ownership
            ownership = "Private" if any(word in name_lower for word in ['seminary', 'islamic', 'christian', 'catholic', 'private']) else "Government"
            
            # Extract Division Performance Summary (the first table)
            div_summary = {}
            tables = soup.find_all('table')
            
            for table in tables:
                table_text = table.get_text().upper()
                if any(indicator in table_text for indicator in ['DIVISION PERFORMANCE SUMMARY', 'SEX', 'DIV']):
                    rows = table.find_all('tr')
                    for row in rows:
                        cols = row.find_all(['td', 'th'])
                        if len(cols) >= 6:
                            sex = cols[0].get_text(strip=True)
                            if sex in ['F', 'M', 'T']:
                                try:
                                    div_summary[sex] = {
                                        'I': int(cols[1].get_text(strip=True) or 0),
                                        'II': int(cols[2].get_text(strip=True) or 0),
                                        'III': int(cols[3].get_text(strip=True) or 0),
                                        'IV': int(cols[4].get_text(strip=True) or 0),
                                        '0': int(cols[5].get_text(strip=True) or 0)
                                    }
                                except (ValueError, IndexError):
                                    continue
                    break
            
            # Extract Centre Division Performance (different structure)
            centre_division_perf = {}
            for table in tables:
                table_text = table.get_text().upper()
                if 'EXAMINATION CENTRE DIVISION PERFORMANCE' in table_text or 'CENTRE DIVISION' in table_text:
                    rows = table.find_all('tr')
                    for row in rows:
                        cols = row.find_all(['td', 'th'])
                        if len(cols) >= 11:
                            first_val = cols[0].get_text(strip=True)
                            if first_val.isdigit():
                                try:
                                    centre_division_perf = {
                                        'REGIST': int(cols[0].get_text(strip=True) or 0),
                                        'ABSENT': int(cols[1].get_text(strip=True) or 0),
                                        'SAT': int(cols[2].get_text(strip=True) or 0),
                                        'WITHHELD': int(cols[3].get_text(strip=True) or 0),
                                        'NO-CA': int(cols[4].get_text(strip=True) or 0),
                                        'CLEAN': int(cols[5].get_text(strip=True) or 0),
                                        'DIV_I': int(cols[6].get_text(strip=True) or 0),
                                        'DIV_II': int(cols[7].get_text(strip=True) or 0),
                                        'DIV_III': int(cols[8].get_text(strip=True) or 0),
                                        'DIV_IV': int(cols[9].get_text(strip=True) or 0),
                                        'DIV_0': int(cols[10].get_text(strip=True) or 0)
                                    }
                                except (ValueError, IndexError):
                                    continue
                    break
            
            # Extract Subject Performance
            subjects_performance = []
            for table in tables:
                if 'SUBJECTS PERFORMANCE' in table.get_text().upper():
                    rows = table.find_all('tr')
                    for row in rows[1:]:
                        cols = row.find_all(['td', 'th'])
                        if len(cols) >= 9:
                            try:
                                code = cols[0].get_text(strip=True)
                                if code.isdigit():
                                    subject_name = cols[1].get_text(strip=True)
                                    reg = int(cols[2].get_text(strip=True) or 0)
                                    sat = int(cols[3].get_text(strip=True) or 0)
                                    no_ca = int(cols[4].get_text(strip=True) or 0)
                                    whd = int(cols[5].get_text(strip=True) or 0)
                                    clean = int(cols[6].get_text(strip=True) or 0)
                                    passed = int(cols[7].get_text(strip=True) or 0)
                                    subject_gpa_text = cols[8].get_text(strip=True)
                                    subject_gpa = float(subject_gpa_text.split()[0]) if subject_gpa_text else 0
                                    competency = cols[9].get_text(strip=True) if len(cols) > 9 else ""
                                    
                                    subjects_performance.append({
                                        'code': code,
                                        'subject': subject_name,
                                        'registered': reg,
                                        'sat': sat,
                                        'no_ca': no_ca,
                                        'withheld': whd,
                                        'clean': clean,
                                        'passed': passed,
                                        'gpa': subject_gpa,
                                        'competency_level': competency,
                                        'pass_rate': (passed / sat * 100) if sat > 0 else 0
                                    })
                            except (ValueError, IndexError, ZeroDivisionError):
                                continue
                    break
            
            # Extract candidate-level results (limit to avoid memory issues)
            candidates = extract_candidate_results(soup)
            # Limit candidates to first 500 to save memory
            if len(candidates) > 500:
                candidates = candidates[:500]
            
            # Calculate total students
            total_students = 0
            if 'T' in div_summary:
                total_students = sum(div_summary['T'].values())
            elif centre_division_perf:
                total_students = centre_division_perf.get('SAT', 0)
            elif candidates:
                total_students = len(candidates)
            
            return {
                'code': school_code,
                'name': school_name,
                'centre_type': centre_type,
                'school_level': school_level,
                'region': region,
                'gpa': gpa,
                'type': school_type,
                'ownership': ownership,
                'total_passed': total_passed,
                'divisions': div_summary,
                'centre_division_perf': centre_division_perf,
                'subjects': subjects_performance,
                'candidates': candidates,
                'total_students': total_students
            }
            
        except requests.Timeout:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return None
        except requests.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(2)
                continue
            return None
        except Exception as e:
            # Log the error but don't crash
            return None
    
    return None

def categorize_subject(subject_name):
    """Categorize subjects into Science and Arts"""
    science_keywords = ['PHYSICS', 'CHEMISTRY', 'BIOLOGY', 'MATHEMATICS', 'MATH']
    arts_keywords = ['HISTORY', 'GEOGRAPHY', 'CIVICS', 'KISWAHILI', 'ENGLISH', 'BIBLE', 'QURAN', 'ISLAMIC']
    
    subject_upper = subject_name.upper()
    if any(keyword in subject_upper for keyword in science_keywords):
        return 'Science'
    elif any(keyword in subject_upper for keyword in arts_keywords):
        return 'Arts'
    return 'Other'

def main():
    st.markdown('<h1 class="main-header">📊 NECTA CSEE 2025 Enhanced Results Analysis</h1>', unsafe_allow_html=True)
    
    st.info("🎓 **Enhanced Version**: Now includes Private Candidates (P), School Candidates (S), candidate-level data, and detailed performance metrics!")
    
    # Show current progress if analysis is running
    if 'analysis_data' in st.session_state and 'processed_codes' in st.session_state:
        current_data = st.session_state.get('analysis_data', [])
        if len(current_data) > 0:
            st.success(f"""
            📊 **Current Analysis Status**
            - Centres analyzed: {len(current_data)}
            - Data in memory: {len(st.session_state.get('processed_codes', set()))} unique centres
            - Click "View Results" below to see current data
            """)
            
            if st.button("📈 View Current Results"):
                # Force display of current results
                pass  # Will fall through to display_analysis_enhanced below
    
    # Sidebar
    st.sidebar.title("🔍 Navigation & Filters")
    
    # Get school links
    with st.spinner("Loading school data..."):
        school_links = get_school_links()
    
    if not school_links:
        st.error("Failed to load school links. Please check your internet connection.")
        return
    
    # Count by centre type
    centre_counts = {}
    for school in school_links:
        ctype = school['centre_type']
        centre_counts[ctype] = centre_counts.get(ctype, 0) + 1
    
    # Sort school links - prioritize School Candidates (S) over Private Candidates (P)
    school_links_sorted = sorted(school_links, key=lambda x: (0 if x['centre_type'] == 'School Candidates' else 1, x['code']))
    
    st.sidebar.success(f"Found {len(school_links_sorted)} examination centres")
    st.sidebar.write(f"- School Candidates (S): {centre_counts.get('School Candidates', 0)}")
    st.sidebar.write(f"- Private Candidates (P): {centre_counts.get('Private Candidates', 0)}")
    st.sidebar.info("📌 School candidates (S) are prioritized in the list")
    
    # Centre type filter
    centre_type_filter = st.sidebar.selectbox(
        "Filter by Centre Type",
        ["All", "School Candidates (S)", "Private Candidates (P)"]
    )
    
    # Filter schools based on centre type (use sorted list)
    if centre_type_filter != "All":
        filtered_schools = [s for s in school_links_sorted if s['centre_type'] == centre_type_filter]
    else:
        filtered_schools = school_links_sorted
    
    # Analysis options
    analysis_mode = st.sidebar.radio(
        "Select Analysis Mode",
        ["Quick Analysis (Sample)", "Full Analysis (All Centres)", "Custom Selection"]
    )
    
    schools_to_analyze = []
    
    if analysis_mode == "Quick Analysis (Sample)":
        schools_to_analyze = filtered_schools[:50]
        st.sidebar.info(f"Analyzing first 50 centres from selected type")
        
    elif analysis_mode == "Full Analysis (All Centres)":
        schools_to_analyze = filtered_schools
        st.sidebar.warning(f"""
        ⚠️ **Full Analysis Mode**
        - Total centres: {len(filtered_schools)}
        - Estimated time: {len(filtered_schools) * 0.5 / 60:.0f}-{len(filtered_schools) / 60:.0f} minutes
        - Memory intensive operation
        
        💡 **Tips:**
        - Keep browser tab open
        - Don't refresh the page
        - Progress is saved every 10 centres
        - Can resume if interrupted
        """)
        
        # Add batch processing option
        use_batch = st.sidebar.checkbox("Use Batch Processing (Recommended)", value=True)
        if use_batch:
            batch_size = st.sidebar.slider("Batch Size", 100, 500, 200, 50)
            
            # Get already processed codes
            processed_codes = st.session_state.get('processed_codes', set())
            
            # Filter to get only unprocessed schools
            unprocessed_schools = [s for s in filtered_schools if s['code'] not in processed_codes]
            
            # Take next batch from unprocessed schools
            schools_to_analyze = unprocessed_schools[:batch_size]
            
            # Display progress info
            total_schools = len(filtered_schools)
            already_processed = len(processed_codes)
            remaining = len(unprocessed_schools)
            
            st.sidebar.info(f"""
            📊 **Batch Progress:**
            - Total centres: {total_schools:,}
            - Already processed: {already_processed:,}
            - Remaining: {remaining:,}
            - This batch: {len(schools_to_analyze)}
            """)
            
            if len(schools_to_analyze) == 0:
                st.sidebar.success("🎉 All centres processed!")

        
    else:  # Custom Selection
        search_term = st.sidebar.text_input("Search Centre Name", "")
        
        if search_term:
            search_filtered = [s for s in filtered_schools if search_term.lower() in s['name'].lower()]
        else:
            search_filtered = filtered_schools
        
        selected_schools = st.sidebar.multiselect(
            "Select Centres",
            options=search_filtered[:100],  # Limit for performance
            format_func=lambda x: f"{x['code']} - {x['name']}",
            max_selections=100
        )
        schools_to_analyze = selected_schools
    
    # Start Analysis Button
    if st.sidebar.button("🚀 Start Analysis", type="primary"):
        if not schools_to_analyze:
            st.warning("Please select at least one centre to analyze")
            return
        
        # Initialize or retrieve existing data
        if 'analysis_data' not in st.session_state:
            st.session_state['analysis_data'] = []
        if 'processed_codes' not in st.session_state:
            st.session_state['processed_codes'] = set()
        
        # Check if this is a continuation
        existing_data = st.session_state.get('analysis_data', [])
        processed_codes = st.session_state.get('processed_codes', set())
        
        # Filter out already processed schools
        schools_to_process = [s for s in schools_to_analyze if s['code'] not in processed_codes]
        
        if len(schools_to_process) == 0:
            if len(existing_data) > 0:
                st.success(f"""
                ✅ **Batch Complete!** 
                - Centres analyzed in this session: {len(schools_to_analyze)}
                - Total centres in memory: {len(existing_data)}
                
                Click 'Start Analysis' again to process the next batch!
                """)
            else:
                st.info("No centres selected for analysis.")
            return
        
        # Progress tracking
        progress_bar = st.progress(0)
        status_text = st.empty()
        stats_text = st.empty()
        
        all_data = list(existing_data)  # Start with existing data
        failed_schools = []
        successful_count = len(existing_data)
        total_to_process = len(schools_to_process)
        
        # Process in chunks to avoid memory issues
        CHUNK_SIZE = 50
        SAVE_INTERVAL = 10  # Save every 10 schools
        
        try:
            for idx, school in enumerate(schools_to_process):
                try:
                    current_progress = (idx + 1) / total_to_process
                    status_text.text(f"Analyzing: {school['name']} ({idx+1}/{total_to_process})")
                    progress_bar.progress(current_progress)
                    
                    # Extract data with timeout protection
                    data = extract_school_data_enhanced(school['url'])
                    
                    if data:
                        data['url'] = school['url']
                        all_data.append(data)
                        processed_codes.add(school['code'])
                        successful_count += 1
                        
                        # Save progress periodically
                        if idx > 0 and idx % SAVE_INTERVAL == 0:
                            st.session_state['analysis_data'] = all_data
                            st.session_state['processed_codes'] = processed_codes
                        
                        stats_text.success(f"✓ Extracted: {successful_count} | Failed: {len(failed_schools)} | Progress: {idx+1}/{total_to_process}")
                    else:
                        failed_schools.append(school['name'])
                        stats_text.warning(f"✓ Extracted: {successful_count} | Failed: {len(failed_schools)} | Progress: {idx+1}/{total_to_process}")
                    
                    # Rate limiting
                    time.sleep(0.3)
                    
                    # Memory management - clear cache every 100 schools
                    if idx > 0 and idx % 100 == 0:
                        st.cache_data.clear()
                        
                except Exception as e:
                    failed_schools.append(f"{school['name']} (Error: {str(e)[:50]})")
                    stats_text.error(f"Error processing {school['name']}: {str(e)[:100]}")
                    continue
                
        except Exception as e:
            st.error(f"Critical error during analysis: {str(e)}")
            st.info(f"Partial results available: {successful_count} centres analyzed")
        
        finally:
            # Always save progress
            st.session_state['analysis_data'] = all_data
            st.session_state['processed_codes'] = processed_codes
            
            progress_bar.empty()
            status_text.empty()
            stats_text.empty()
        
        # Display results
        if failed_schools:
            with st.expander(f"⚠️ Failed to extract {len(failed_schools)} centres - Click to see"):
                for school in failed_schools[:100]:  # Limit display
                    st.text(f"• {school}")
                if len(failed_schools) > 100:
                    st.text(f"... and {len(failed_schools) - 100} more")
        
        if not all_data:
            st.error("No data extracted. Please try again.")
            return
        
        # Display summary
        total_students = sum(d['total_students'] for d in all_data)
        total_candidates = sum(len(d.get('candidates', [])) for d in all_data)
        
        st.success(f"""
        ✅ **Analysis Complete!**
        - Successfully analyzed: {len(all_data)} centres
        - Total students: {total_students:,}
        - Individual candidate records: {total_candidates:,}
        - Failed: {len(failed_schools)}
        """)
        
        # Add option to clear and restart
        if st.sidebar.button("🔄 Clear Data & Restart"):
            st.session_state.clear()
            st.rerun()
    
    # Display analysis if data exists
    if 'analysis_data' in st.session_state:
        display_analysis_enhanced(st.session_state['analysis_data'])

def display_analysis_enhanced(data):
    """Display comprehensive analysis with enhanced features"""
    
    # Create tabs
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "📈 Overview", "🏆 Top Performers", "📍 Regional Analysis",
        "📚 Subject Analysis", "👥 Candidate Analysis", "📊 Comparative Analysis", "💾 Download"
    ])
    
    with tab1:
        display_overview_enhanced(data)
    
    with tab2:
        display_top_performers_enhanced(data)
    
    with tab3:
        display_regional_analysis_enhanced(data)
    
    with tab4:
        display_subject_analysis_enhanced(data)
    
    with tab5:
        display_candidate_analysis(data)
    
    with tab6:
        display_comparative_analysis_enhanced(data)
    
    with tab7:
        display_download_options_enhanced(data)

def display_overview_enhanced(data):
    """Enhanced overview with centre type breakdown"""
    st.header("📈 Enhanced Performance Overview")
    
    # Key Metrics
    col1, col2, col3, col4, col5 = st.columns(5)
    
    total_centres = len(data)
    total_students = sum(d['total_students'] for d in data)
    total_candidates = sum(len(d.get('candidates', [])) for d in data)
    school_centres = sum(1 for d in data if d['centre_type'] == 'School Candidates')
    private_centres = sum(1 for d in data if d['centre_type'] == 'Private Candidates')
    
    col1.metric("Total Centres", total_centres)
    col2.metric("School Centres (S)", school_centres)
    col3.metric("Private Centres (P)", private_centres)
    col4.metric("Total Students", f"{total_students:,}")
    col5.metric("Candidate Records", f"{total_candidates:,}")
    
    st.markdown("---")
    
    # Additional metrics
    col1, col2, col3 = st.columns(3)
    
    # Average GPA
    valid_gpas = [d['gpa'] for d in data if d['gpa'] is not None]
    avg_gpa = sum(valid_gpas) / len(valid_gpas) if valid_gpas else 0
    col1.metric("Average GPA", f"{avg_gpa:.2f}")
    
    # Total Division I
    total_div_i = sum(d['divisions'].get('T', {}).get('I', 0) for d in data)
    col2.metric("Total Division I", f"{total_div_i:,}")
    
    # Average pass rate
    total_passed = sum(d.get('total_passed', 0) for d in data if d.get('total_passed'))
    pass_rate = (total_passed / total_students * 100) if total_students > 0 else 0
    col3.metric("Overall Pass Rate", f"{pass_rate:.1f}%")
    
    st.markdown("---")
    
    # Visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        # Centre type distribution
        centre_types = [d['centre_type'] for d in data]
        fig = px.pie(names=centre_types, title='Distribution by Centre Type',
                     color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # School level distribution
        school_levels = [d['school_level'] for d in data]
        fig = px.pie(names=school_levels, title='Distribution by School Level',
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)

def display_top_performers_enhanced(data):
    """Enhanced top performers with centre type filter"""
    st.header("🏆 Top Performing Centres")
    
    # Create DataFrame
    df = pd.DataFrame([{
        'Centre Code': d['code'],
        'Centre Name': d['name'],
        'Centre Type': d['centre_type'],
        'School Level': d['school_level'],
        'Region': d['region'],
        'GPA': d['gpa'],
        'Type': d['type'],
        'Ownership': d['ownership'],
        'Total Students': d['total_students'],
        'Div I': d['divisions'].get('T', {}).get('I', 0),
        'Total Passed': d.get('total_passed', 0)
    } for d in data])
    
    # Ensure numeric columns
    df['GPA'] = pd.to_numeric(df['GPA'], errors='coerce')
    df['Total Students'] = pd.to_numeric(df['Total Students'], errors='coerce').fillna(0)
    df['Div I'] = pd.to_numeric(df['Div I'], errors='coerce').fillna(0)
    df['Total Passed'] = pd.to_numeric(df['Total Passed'], errors='coerce').fillna(0)
    
    # Calculate rates
    df['Div I Rate (%)'] = ((df['Div I'] / df['Total Students']) * 100).fillna(0)
    df['Pass Rate (%)'] = ((df['Total Passed'] / df['Total Students']) * 100).fillna(0)
    
    # Check if dataframe is empty
    if len(df) == 0:
        st.warning("No centre data available for analysis.")
        return
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        ranking_by = st.selectbox("Rank By", ["GPA", "Div I Rate (%)", "Pass Rate (%)"])
    
    with col2:
        centre_filter = st.selectbox("Centre Type", ["All", "School Candidates", "Private Candidates"])
    
    with col3:
        type_filter = st.selectbox("Filter by Gender", ["All", "Boys", "Girls", "Mixed"])
    
    # Apply filters
    filtered = df.copy()
    if centre_filter != "All":
        filtered = filtered[filtered['Centre Type'] == centre_filter]
    if type_filter != "All":
        filtered = filtered[filtered['Type'] == type_filter]
    
    # Check if filtered dataframe is empty
    if len(filtered) == 0:
        st.warning("No centres found with the selected filters. Please adjust your filters.")
        return
    
    # Sort and handle NaN values
    if ranking_by == "GPA":
        # For GPA, lower is better - remove NaN values
        filtered_valid = filtered.dropna(subset=['GPA'])
        if len(filtered_valid) == 0:
            st.warning("No centres have valid GPA data with the selected filters.")
            return
        top = filtered_valid.nsmallest(min(50, len(filtered_valid)), 'GPA')
    else:
        # For percentages, higher is better
        filtered['temp_col'] = filtered[ranking_by]
        top = filtered.nlargest(min(50, len(filtered)), 'temp_col')
        top = top.drop('temp_col', axis=1)
    
    # Display
    st.subheader(f"Top {len(top)} Centres by {ranking_by}")
    
    # Format display
    display_df = top[['Centre Code', 'Centre Name', 'Centre Type', 'School Level', 'Region', 
                      'GPA', 'Div I Rate (%)', 'Pass Rate (%)', 'Total Students']].copy()
    
    # Format columns for display
    display_df['GPA'] = display_df['GPA'].apply(lambda x: f"{x:.2f}" if pd.notna(x) else 'N/A')
    display_df['Div I Rate (%)'] = display_df['Div I Rate (%)'].apply(lambda x: f"{x:.1f}%")
    display_df['Pass Rate (%)'] = display_df['Pass Rate (%)'].apply(lambda x: f"{x:.1f}%")
    display_df['Total Students'] = display_df['Total Students'].astype(int)
    
    display_df = display_df.reset_index(drop=True)
    display_df.index += 1
    
    st.dataframe(display_df, use_container_width=True, height=600)

def display_regional_analysis_enhanced(data):
    """Enhanced regional analysis"""
    st.header("📍 Regional Performance Analysis")
    
    df = pd.DataFrame([{
        'Region': d['region'],
        'Centre Type': d['centre_type'],
        'GPA': d['gpa'],
        'Students': d['total_students'],
        'Div I': d['divisions'].get('T', {}).get('I', 0)
    } for d in data])
    
    # Ensure numeric types
    df['GPA'] = pd.to_numeric(df['GPA'], errors='coerce')
    df['Students'] = pd.to_numeric(df['Students'], errors='coerce').fillna(0)
    df['Div I'] = pd.to_numeric(df['Div I'], errors='coerce').fillna(0)
    
    regional_stats = df.groupby('Region').agg({
        'Region': 'count',
        'Students': 'sum',
        'GPA': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else 0,
        'Div I': 'sum'
    }).rename(columns={'Region': 'Centres'})
    
    regional_stats = regional_stats.sort_values('GPA', ascending=True, na_position='last')
    
    st.dataframe(regional_stats, use_container_width=True)
    
    # Visualization - only plot regions with valid GPA
    plot_data = regional_stats[regional_stats['GPA'] > 0].reset_index()
    
    if len(plot_data) > 0:
        fig = px.bar(plot_data, x='Region', y='GPA',
                     title='Average GPA by Region',
                     color='GPA', color_continuous_scale='Viridis')
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No valid GPA data available for visualization")

def display_subject_analysis_enhanced(data):
    """Enhanced subject analysis"""
    st.header("📚 Subject Performance Analysis")
    
    all_subjects = []
    for d in data:
        for subj in d.get('subjects', []):
            all_subjects.append({
                'Centre': d['name'],
                'Centre Type': d['centre_type'],
                'Subject': subj['subject'],
                'Category': categorize_subject(subj['subject']),
                'GPA': subj['gpa'],
                'Pass Rate': subj['pass_rate'],
                'Students': subj['sat']
            })
    
    if not all_subjects:
        st.warning("No subject data available")
        return
    
    df = pd.DataFrame(all_subjects)
    
    # Summary by category
    category_stats = df.groupby('Category').agg({
        'Students': 'sum',
        'GPA': 'mean',
        'Pass Rate': 'mean'
    }).round(2)
    
    st.subheader("Performance by Subject Category")
    st.dataframe(category_stats, use_container_width=True)
    
    # Top subjects
    subject_summary = df.groupby('Subject').agg({
        'Students': 'sum',
        'GPA': 'mean',
        'Pass Rate': 'mean'
    }).sort_values('GPA').head(20)
    
    fig = px.bar(subject_summary.reset_index(), x='Subject', y='GPA',
                 title='Top 20 Subjects by GPA',
                 color='GPA', color_continuous_scale='RdYlGn_r')
    fig.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig, use_container_width=True)

def display_candidate_analysis(data):
    """NEW: Candidate-level analysis"""
    st.header("👥 Candidate-Level Analysis")
    
    st.info("📊 Individual candidate results extracted from examination centres")
    
    # Collect all candidates
    all_candidates = []
    for d in data:
        for candidate in d.get('candidates', []):
            all_candidates.append({
                'Centre': d['name'],
                'Centre Code': d['code'],
                'Centre Type': d['centre_type'],
                'Region': d['region'],
                'CNO': candidate['CNO'],
                'SEX': candidate['SEX'],
                'AGGT': candidate['AGGT'],
                'DIV': candidate['DIV'],
                'Num Subjects': len(candidate['subjects'])
            })
    
    if not all_candidates:
        st.warning("No candidate-level data available in current selection")
        return
    
    df = pd.DataFrame(all_candidates)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Candidates", len(df))
    col2.metric("Female", len(df[df['SEX'] == 'F']))
    col3.metric("Male", len(df[df['SEX'] == 'M']))
    col4.metric("Division I", len(df[df['DIV'] == 'I']))
    
    # Division distribution
    st.subheader("Division Distribution")
    div_counts = df['DIV'].value_counts().sort_index()
    fig = px.bar(x=div_counts.index, y=div_counts.values,
                 labels={'x': 'Division', 'y': 'Number of Candidates'},
                 title='Candidate Distribution by Division')
    st.plotly_chart(fig, use_container_width=True)
    
    # Sample data
    st.subheader("Sample Candidate Records")
    st.dataframe(df.head(100), use_container_width=True, height=400)

def display_comparative_analysis_enhanced(data):
    """Enhanced comparative analysis"""
    st.header("📊 Comparative Analysis")
    
    df = pd.DataFrame([{
        'Centre Type': d['centre_type'],
        'School Level': d['school_level'],
        'Type': d['type'],
        'Ownership': d['ownership'],
        'GPA': d['gpa'],
        'Students': d['total_students']
    } for d in data])
    
    # Ensure numeric types
    df['GPA'] = pd.to_numeric(df['GPA'], errors='coerce')
    df['Students'] = pd.to_numeric(df['Students'], errors='coerce').fillna(0)
    
    # Centre Type Comparison
    st.subheader("School vs Private Candidates Performance")
    centre_comp = df.groupby('Centre Type').agg({
        'Centre Type': 'count',
        'GPA': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else 0,
        'Students': 'sum'
    }).rename(columns={'Centre Type': 'Count'})
    
    centre_comp['GPA'] = centre_comp['GPA'].round(2)
    st.dataframe(centre_comp, use_container_width=True)
    
    # Visualization
    if centre_comp['GPA'].sum() > 0:
        fig = px.bar(centre_comp.reset_index(), x='Centre Type', y='GPA',
                     title='Average GPA by Centre Type',
                     color='GPA', color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig, use_container_width=True)
    
    # School Level Comparison
    st.subheader("Secondary School vs High School")
    level_comp = df.groupby('School Level').agg({
        'School Level': 'count',
        'GPA': lambda x: x.dropna().mean() if len(x.dropna()) > 0 else 0,
        'Students': 'sum'
    }).rename(columns={'School Level': 'Count'})
    
    level_comp['GPA'] = level_comp['GPA'].round(2)
    st.dataframe(level_comp, use_container_width=True)
    
    # Visualization
    if level_comp['GPA'].sum() > 0:
        fig = px.bar(level_comp.reset_index(), x='School Level', y='GPA',
                     title='Average GPA by School Level',
                     color='GPA', color_continuous_scale='RdYlGn_r')
        st.plotly_chart(fig, use_container_width=True)

def display_download_options_enhanced(data):
    """Enhanced download options"""
    st.header("💾 Download Enhanced Data")
    
    col1, col2, col3 = st.columns(3)
    
    # All centres
    with col1:
        df_centres = pd.DataFrame([{
            'Code': d['code'],
            'Name': d['name'],
            'Centre Type': d['centre_type'],
            'School Level': d['school_level'],
            'Region': d['region'],
            'GPA': d['gpa'],
            'Total Students': d['total_students'],
            'Div I': d['divisions'].get('T', {}).get('I', 0),
            'Total Passed': d.get('total_passed', 0)
        } for d in data])
        
        csv = df_centres.to_csv(index=False)
        st.download_button(
            "📥 Download All Centres",
            csv,
            "necta_2025_all_centres.csv",
            "text/csv"
        )
    
    # Candidate data
    with col2:
        all_candidates = []
        for d in data:
            for c in d.get('candidates', []):
                all_candidates.append({
                    'Centre Code': d['code'],
                    'Centre Name': d['name'],
                    'CNO': c['CNO'],
                    'SEX': c['SEX'],
                    'AGGT': c['AGGT'],
                    'DIV': c['DIV']
                })
        
        if all_candidates:
            df_cand = pd.DataFrame(all_candidates)
            csv = df_cand.to_csv(index=False)
            st.download_button(
                "📥 Download Candidate Data",
                csv,
                "necta_2025_candidates.csv",
                "text/csv"
            )
    
    # Subject data
    with col3:
        all_subjects = []
        for d in data:
            for s in d.get('subjects', []):
                all_subjects.append({
                    'Centre': d['name'],
                    'Subject': s['subject'],
                    'GPA': s['gpa'],
                    'Pass Rate': s['pass_rate']
                })
        
        if all_subjects:
            df_subj = pd.DataFrame(all_subjects)
            csv = df_subj.to_csv(index=False)
            st.download_button(
                "📥 Download Subject Data",
                csv,
                "necta_2025_subjects.csv",
                "text/csv"
            )

if __name__ == "__main__":
    main()
