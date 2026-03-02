"""
Office Management System - Enhanced Version
Professional Streamlit Dashboard with Advanced Features
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
import database
import hashlib
import time

# Page Configuration
st.set_page_config(
    page_title="Office Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state - MUST BE FIRST
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user' not in st.session_state:
    st.session_state.user = None
if 'page' not in st.session_state:
    st.session_state.page = 'login'
if 'show_landing' not in st.session_state:
    st.session_state.show_landing = True
if 'form_key' not in st.session_state:
    st.session_state.form_key = 0
if 'success_message' not in st.session_state:
    st.session_state.success_message = None
if 'error_message' not in st.session_state:
    st.session_state.error_message = None

# Custom CSS - Professional Dark Theme
st.markdown("""
<style>
    /* Main App Background - Dark Elegant */
    .stApp { 
        background: linear-gradient(145deg, #0d1117 0%, #161b22 50%, #0d1117 100%); 
        min-height: 100vh; 
    }
    
    /* Sidebar - Dark with subtle border */
    [data-testid="stSidebar"] { 
        background: linear-gradient(180deg, #161b22 0%, #0d1117 100%); 
        border-right: 1px solid #30363d;
    }
    
    /* Typography - Clean white */
    h1, h2, h3 {
        color: #e6edf3;
        font-weight: 600;
    }
    
    h1 { font-size: 28px; margin-bottom: 20px; }
    h2 { font-size: 22px; margin-bottom: 15px; }
    h3 { font-size: 18px; margin-bottom: 10px; }
    
    /* Cards - Dark with glow */
    .card { 
        background: linear-gradient(145deg, rgba(22, 27, 34, 0.95), rgba(13, 17, 23, 0.95)); 
        border-radius: 16px; 
        padding: 24px; 
        margin: 12px 0; 
        border: 1px solid #30363d;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        transition: all 0.3s ease;
    }
    .card:hover {
        border-color: #58a6ff;
        box-shadow: 0 8px 30px rgba(88, 166, 255, 0.1);
    }
    
    /* Metric Values */
    [data-testid="stMetricValue"] { 
        font-size: 28px; 
        color: #58a6ff; 
        font-weight: 700; 
    }
    [data-testid="stMetricLabel"] {
        color: #8b949e;
        font-size: 14px;
    }
    
    /* Buttons - Vibrant Blue */
    .stButton>button { 
        background: linear-gradient(135deg, #238636, #2ea043); 
        border: none; 
        border-radius: 8px; 
        padding: 10px 24px; 
        font-weight: 500; 
        color: white;
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2ea043, #3fb950);
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(46, 160, 67, 0.4);
    }
    
    /* Info Box */
    .info-box { 
        background: rgba(22, 27, 34, 0.9); 
        border-left: 3px solid #58a6ff; 
        padding: 16px 20px; 
        border-radius: 0 12px 12px 0; 
        margin: 10px 0; 
        border: 1px solid #30363d;
    }
    
    /* Profile Card */
    .profile-card { 
        background: linear-gradient(145deg, rgba(22, 27, 34, 0.95), rgba(13, 17, 23, 0.95)); 
        border-radius: 16px; 
        padding: 20px; 
        text-align: center; 
        border: 1px solid #30363d;
    }
    .profile-avatar { 
        width: 72px; 
        height: 72px; 
        border-radius: 50%; 
        background: linear-gradient(135deg, #58a6ff, #a371f7); 
        display: flex; 
        align-items: center; 
        justify-content: center; 
        margin: 0 auto 12px; 
        font-size: 24px; 
        color: white; 
        font-weight: 600;
        box-shadow: 0 4px 20px rgba(88, 166, 255, 0.3);
    }
    
    /* Progress Bar */
    .progress-bar { 
        background: #21262d; 
        border-radius: 8px; 
        height: 10px; 
        overflow: hidden; 
    }
    .progress-fill { 
        background: linear-gradient(90deg, #58a6ff, #a371f7); 
        height: 100%; 
        border-radius: 8px; 
        transition: width 0.5s ease;
    }
    
    /* Login Container */
    .login-container { 
        background: linear-gradient(145deg, rgba(22, 27, 34, 0.98), rgba(13, 17, 23, 0.98)); 
        border-radius: 20px; 
        padding: 40px; 
        border: 1px solid #30363d; 
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.5); 
    }
    
    /* Feature Card */
    .feature-card { 
        background: linear-gradient(145deg, rgba(22, 27, 34, 0.9), rgba(13, 17, 23, 0.9)); 
        border-radius: 16px; 
        padding: 24px; 
        margin: 10px 0; 
        border: 1px solid #30363d;
        transition: all 0.3s ease;
    }
    .feature-card:hover {
        border-color: #58a6ff;
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(88, 166, 255, 0.15);
    }
    
    /* Hero */
    .hero-title { 
        font-size: 48px; 
        font-weight: 700; 
        text-align: center; 
        background: linear-gradient(135deg, #58a6ff, #a371f7); 
        -webkit-background-clip: text; 
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    .hero-subtitle { 
        text-align: center; 
        color: #8b949e; 
        font-size: 18px;
        margin-bottom: 30px;
    }
    
    /* Status Badges */
    .status-badge {
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 500;
    }
    .status-complete { background: rgba(46, 160, 67, 0.2); color: #3fb950; }
    .status-progress { background: rgba(210, 153, 34, 0.2); color: #d29922; }
    .status-pending { background: rgba(88, 166, 255, 0.2); color: #58a6ff; }
    .status-absent { background: rgba(248, 81, 73, 0.2); color: #f85149; }
    .status-present { background: rgba(46, 160, 67, 0.2); color: #3fb950; }
    
    /* Form Elements */
    .stTextInput>div>div>input, .stTextArea>div>div>textarea, .stSelectbox>div>div>div {
        background: #0d1117;
        border: 1px solid #30363d;
        border-radius: 8px;
        color: #e6edf3;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #58a6ff;
        box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.2);
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background: #21262d;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
        color: #8b949e;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #238636, #2ea043);
        color: white;
    }
    
    /* DataFrame */
    [data-testid="stDataFrame"] {
        background: rgba(22, 27, 34, 0.9);
        border-radius: 12px;
        border: 1px solid #30363d;
    }
    
    /* Sidebar Navigation Buttons */
    [data-testid="stSidebar"] .stButton>button {
        background: transparent;
        color: #c9d1d9;
        border: none;
        text-align: left;
        padding: 12px 16px;
        border-radius: 8px;
        font-weight: 500;
    }
    [data-testid="stSidebar"] .stButton>button:hover {
        background: rgba(88, 166, 255, 0.1);
        color: #58a6ff;
        transform: none;
        box-shadow: none;
    }
    
    /* Notifications */
    .notification {
        background: rgba(22, 27, 34, 0.9);
        border-left: 3px solid #58a6ff;
        padding: 12px 16px;
        border-radius: 0 8px 8px 0;
        margin: 8px 0;
        border: 1px solid #30363d;
    }
    
    /* Success/Error Messages */
    [data-testid="stSuccess"] {
        background: rgba(46, 160, 67, 0.15);
        color: #3fb950;
        border-radius: 8px;
        border: 1px solid rgba(46, 160, 67, 0.3);
    }
    [data-testid="stError"] {
        background: rgba(248, 81, 73, 0.15);
        color: #f85149;
        border-radius: 8px;
        border: 1px solid rgba(248, 81, 73, 0.3);
    }
    [data-testid="stInfo"] {
        background: rgba(88, 166, 255, 0.15);
        color: #58a6ff;
        border-radius: 8px;
        border: 1px solid rgba(88, 166, 255, 0.3);
    }
    
    /* Divider */
    hr {
        border: none;
        border-top: 1px solid #30363d;
        margin: 20px 0;
    }
    
    /* Welcome text */
    .welcome-text {
        color: #e6edf3;
        font-size: 24px;
        font-weight: 600;
        margin-bottom: 8px;
    }
    .welcome-subtext {
        color: #8b949e;
        font-size: 14px;
    }
    
    /* Text colors for better visibility on dark */
    p, div, span {
        color: #c9d1d9;
    }
    
    /* Input placeholders */
    ::placeholder {
        color: #6e7681;
    }
</style>
""", unsafe_allow_html=True)

def show_message(message, msg_type="success"):
    if msg_type == "success":
        st.session_state.success_message = message
    else:
        st.session_state.error_message = message

def clear_form():
    st.session_state.form_key += 1

def landing_page():
    st.markdown('<h1 class="hero-title">🏢 Office Management System</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-subtitle">Streamline your workplace operations with elegance</p>', unsafe_allow_html=True)
    if st.button("🚀 Get Started / Login", use_container_width=False):
        st.session_state.show_landing = False
        st.rerun()
    st.markdown("---")
    st.markdown("### ✨ Key Features", unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1: st.markdown("""<div class="feature-card"><div style="font-size:32px;">👥</div><div style="color:#00d4ff;font-weight:600;">Employee Management</div><div style="color:#a0a0c0;font-size:14px;">Complete employee database</div></div>""", unsafe_allow_html=True)
    with col2: st.markdown("""<div class="feature-card"><div style="font-size:32px;">📅</div><div style="color:#00d4ff;font-weight:600;">Attendance Tracking</div><div style="color:#a0a0c0;font-size:14px;">Real-time attendance</div></div>""", unsafe_allow_html=True)
    with col3: st.markdown("""<div class="feature-card"><div style="font-size:32px;">🍃</div><div style="color:#00d4ff;font-weight:600;">Leave Management</div><div style="color:#a0a0c0;font-size:14px;">Leave requests workflow</div></div>""", unsafe_allow_html=True)

def login_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""<div style="text-align: center; margin-bottom: 40px;"><h1 style="font-size: 48px;">🏢 Office Management System</h1><p style="color: #a0a0c0; font-size: 20px;">Manage your workforce with elegance</p></div>""", unsafe_allow_html=True)
        with st.container():
            st.markdown('<div class="login-container">', unsafe_allow_html=True)
            st.markdown('<h2 style="text-align: center;">🔐 Welcome Back</h2>', unsafe_allow_html=True)
            with st.form("login_form"):
                emp_id = st.text_input("Employee ID", placeholder="Enter your Employee ID")
                password = st.text_input("Password", type="password", placeholder="Enter your password")
                submit = st.form_submit_button("🚀 Login", use_container_width=True)
                if submit:
                    if emp_id and password:
                        with st.spinner('Authenticating...'): time.sleep(0.5)
                        user = database.authenticate_user(emp_id, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user = user
                            st.session_state.page = 'dashboard'
                            st.session_state.show_landing = False
                            st.balloons()
                            st.rerun()
                        else: 
                            show_message("❌ Invalid Employee ID or Password!", "error")
                    else: 
                        show_message("⚠️ Please enter both fields!", "error")
            st.markdown('</div>', unsafe_allow_html=True)
            st.markdown("""<div class="card" style="margin-top: 30px; text-align: center;"><h3 style="color: #00d4ff;">📋 Demo Credentials</h3><div style="display: flex; justify-content: space-around; gap: 10px;"><div style="background: rgba(0,212,255,0.1); padding: 15px; border-radius: 10px;"><p style="color: #00d4ff; font-weight: bold;">HR</p><p>EMP0001</p><p>RAJU0001</p></div><div style="background: rgba(138,43,226,0.1); padding: 15px; border-radius: 10px;"><p style="color: #8a2be2; font-weight: bold;">Manager</p><p>EMP0003</p><p>ARPI0003</p></div><div style="background: rgba(0,255,136,0.1); padding: 15px; border-radius: 10px;"><p style="color: #00ff88; font-weight: bold;">Employee</p><p>EMP0002</p><p>SAIK0002</p></div></div></div>""", unsafe_allow_html=True)
            if st.button("🏠 Back to Home", use_container_width=True):
                st.session_state.show_landing = True
                st.rerun()

def logout():
    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.page = 'login'
    st.rerun()

def get_user_role():
    return st.session_state.user.get('post', '') if st.session_state.user else None

def is_hr(): return get_user_role() == 'HR'
def is_manager(): return get_user_role() == 'Manager'

def sidebar_navigation():
    with st.sidebar:
        st.markdown("""<div style="text-align: center; padding: 25px 0;"><div style="width: 70px; height: 70px; background: linear-gradient(135deg, #00d4ff, #00ff88); border-radius: 50%; margin: 0 auto; display: flex; align-items: center; justify-content: center; font-size: 32px;">🏢</div><h2 style="color: #00d4ff; margin-top: 15px;">OMS</h2></div>""", unsafe_allow_html=True)
        if st.session_state.user:
            user = st.session_state.user
            initials = ''.join([n[0] for n in user['emp_name'].split()]).upper()
            role_color = {'HR': '#00d4ff', 'Manager': '#8a2be2', 'Employee': '#00ff88'}.get(user['post'], '#00d4ff')
            st.markdown(f"""<div class="profile-card"><div class="profile-avatar">{initials}</div><h3 style="color: #00d4ff;">{user['emp_name']}</h3><p style="color: {role_color}; font-weight: bold;">{user['post']}</p><p style="color: #808090;">ID: {user['emp_id']}</p></div>""", unsafe_allow_html=True)
        st.markdown("<hr>", unsafe_allow_html=True)
        
        menu = [("Dashboard", "📊", "dashboard"), ("Employees", "👥", "employees"), ("Attendance", "📅", "attendance"), ("Leave", "🍃", "leave"), ("Projects", "📁", "projects"), ("Tasks", "✅", "tasks"), ("Notices", "📢", "notices"), ("Holiday Calendar", "📅", "holiday"), ("Payslips", "💰", "payslips")] if is_hr() or is_manager() else [("Dashboard", "📊", "dashboard"), ("Attendance", "📅", "attendance"), ("Leave", "🍃", "leave"), ("Projects", "📁", "projects"), ("Tasks", "✅", "tasks"), ("Notices", "📢", "notices"), ("Holiday Calendar", "📅", "holiday"), ("Payslips", "💰", "payslips"), ("Profile", "👤", "profile")]
        
        for item in menu:
            if st.button(f"{item[1]} {item[0]}", use_container_width=True, key=f"nav_{item[2]}"):
                st.session_state.page = item[2]
                st.rerun()
        
        try:
            notifs = database.get_user_notifications(user['emp_id'])
            if not notifs.empty:
                st.markdown("---")
                st.markdown("### 🔔 Notifications")
                for _, row in notifs.iterrows():
                    st.markdown(f"""<div style="background: linear-gradient(135deg, rgba(0,212,255,0.1), rgba(138,43,226,0.1)); border-left: 4px solid #00d4ff; padding: 15px; border-radius: 0 10px 10px 0; margin: 10px 0;"><p style="margin: 0; color: #ffffff; font-size: 14px;">{row['message']}</p></div>""", unsafe_allow_html=True)
                    col1, col2 = st.columns([1, 1])
                    with col1:
                        if st.button("✅", key=f"read_{row['id']}"):
                            database.mark_notification_read(row['id'])
                            st.rerun()
                    with col2:
                        if st.button("🗑️", key=f"del_{row['id']}"):
                            database.delete_notification(row['id'])
                            st.rerun()
        except: pass
        
        st.markdown("<hr>", unsafe_allow_html=True)
        if st.button("🚪 Logout", use_container_width=True): logout()

def dashboard_page():
    user = st.session_state.user
    st.markdown(f"""<div style="margin-bottom: 40px;"><h1>Welcome back, {user['emp_name']}! 👋</h1><p style="color: #a0a0c0; font-size: 18px;">Here's what's happening today.</p></div>""", unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    emp_df = database.get_all_employees()
    proj_df = database.get_all_projects()
    notice_df = database.get_all_notices()
    today = date.today()
    att_today = database.get_attendance_records(start_date=today, end_date=today)
    present = len(att_today[att_today['status'] == 'P']) if not att_today.empty else 0
    active_proj = len(proj_df[proj_df['status'] == 'In Progress']) if not proj_df.empty else 0
    
    with col1: st.markdown(f"""<div class="card" style="text-align: center; padding: 30px;"><div style="font-size: 40px;">👥</div><p style="color: #00d4ff; font-size: 36px; font-weight: bold; margin: 0;">{len(emp_df)}</p><p style="color: #a0a0c0; margin: 0;">Employees</p></div>""", unsafe_allow_html=True)
    with col2: st.markdown(f"""<div class="card" style="text-align: center; padding: 30px;"><div style="font-size: 40px;">📁</div><p style="color: #00ff88; font-size: 36px; font-weight: bold; margin: 0;">{active_proj}</p><p style="color: #a0a0c0; margin: 0;">Active Projects</p></div>""", unsafe_allow_html=True)
    with col3: st.markdown(f"""<div class="card" style="text-align: center; padding: 30px;"><div style="font-size: 40px;">✅</div><p style="color: #8a2be2; font-size: 36px; font-weight: bold; margin: 0;">{present}</p><p style="color: #a0a0c0; margin: 0;">Present Today</p></div>""", unsafe_allow_html=True)
    with col4: st.markdown(f"""<div class="card" style="text-align: center; padding: 30px;"><div style="font-size: 40px;">📢</div><p style="color: #ffc107; font-size: 36px; font-weight: bold; margin: 0;">{len(notice_df)}</p><p style="color: #a0a0c0; margin: 0;">Notices</p></div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    trend_df = database.get_attendance_trend()
    if not trend_df.empty:
        st.markdown("### 📈 Attendance Trend (Last 7 Days)")
        st.line_chart(trend_df.set_index('curr_date')[['present', 'absent']])
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 📊 Recent Projects")
        if not proj_df.empty:
            for _, row in proj_df.head(4).iterrows():
                prog = row['progression'] if row['progression'] else 0
                st.markdown(f"""<div class="info-box"><div style="display: flex; justify-content: space-between;"><strong>{row['project_name']}</strong><span style="background: {'#00c853' if row['status']=='Complete' else '#ffc107' if row['status']=='In Progress' else '#9e9e9e'}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 11px;">{row['status'] if row['status'] else 'Not Started'}</span></div><div class="progress-bar" style="margin-top: 10px;"><div class="progress-fill" style="width: {prog}%;"></div></div></div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("### 📢 Recent Notices")
        if not notice_df.empty:
            for _, row in notice_df.head(4).iterrows():
                t = row['time'].strftime('%b %d, %Y') if isinstance(row['time'], datetime) else str(row['time'])
                st.markdown(f"""<div class="info-box"><p style="margin: 0;">{row['notice']}</p><p style="color: #808090; font-size: 11px; margin: 10px 0 0 0;">{t}</p></div>""", unsafe_allow_html=True)

def employees_page():
    st.markdown("""<div style="margin-bottom: 30px;"><h1>👥 Employee Management</h1></div>""", unsafe_allow_html=True)
    
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        st.session_state.error_message = None
    
    tab1, tab2, tab3, tab4 = st.tabs(["📋 View", "➕ Add", "✏️ Update", "📊 Stats"])
    emp_df = database.get_all_employees()
    
    with tab1:
        if not emp_df.empty:
            search = st.text_input("🔍 Search", placeholder="Search by name or ID")
            if search: emp_df = emp_df[emp_df['emp_name'].str.contains(search, case=False) | emp_df['emp_id'].str.contains(search, case=False)]
            st.dataframe(emp_df[['emp_id', 'emp_name', 'email_id', 'phone_no', 'post', 'basic']], use_container_width=True, hide_index=True)
            
            sel = st.selectbox("Select Employee", ["Select..."] + emp_df['emp_name'].tolist())
            if sel and sel != "Select...":
                e = emp_df[emp_df['emp_name'] == sel].iloc[0]
                col1, col2, col3 = st.columns(3)
                with col1: st.info(f"**ID:** {e['emp_id']}\n\n**Name:** {e['emp_name']}")
                with col2: st.info(f"**Email:** {e['email_id']}\n\n**Phone:** {e['phone_no']}")
                with col3: st.info(f"**Post:** {e['post']}\n\n**Salary:** ₹{e['basic']:,}")
                if st.button("🗑️ Delete Employee", use_container_width=True):
                    if database.delete_employee(e['emp_id']): 
                        show_message("🗑️ Employee deleted successfully!")
                        st.rerun()
    
    with tab2:
        form_key = st.session_state.form_key
        with st.form(f"add_emp_{form_key}"):
            c1, c2 = st.columns(2)
            with c1: emp_id = st.text_input("ID", placeholder="EMP0007"); emp_name = st.text_input("Name")
            with c2: phone = st.text_input("Phone"); post = st.selectbox("Post", ["Employee", "Manager", "HR"])
            basic = st.number_input("Salary", 0, 200000)
            pw = st.text_input("Password", type="password")
            
            if st.form_submit_button("➕ Add Employee", use_container_width=True):
                if emp_id and emp_name and phone and pw:
                    if database.add_employee(emp_id, emp_name, f"{emp_id}@company.com", "", phone, post, pw, date.today(), basic): 
                        show_message(f"✅ Employee '{emp_name}' added successfully!")
                        database.add_notification(emp_id, f"Welcome! Your account has been created with ID: {emp_id}")
                        clear_form()
                        st.rerun()
                    else:
                        show_message("❌ Failed to add employee! Database error.", "error")
                else:
                    show_message("⚠️ Please fill all required fields!", "error")
    
    with tab3:
        if not emp_df.empty:
            update_sel = st.selectbox("Select Employee to Update", ["Select..."] + emp_df['emp_name'].tolist(), key="update_emp_select")
            
            if update_sel and update_sel != "Select...":
                e = emp_df[emp_df['emp_name'] == update_sel].iloc[0]
                
                st.markdown("---")
                st.markdown(f"### ✏️ Update: {e['emp_name']}")
                
                form_key = st.session_state.form_key
                with st.form(f"update_emp_{form_key}"):
                    c1, c2 = st.columns(2)
                    with c1: 
                        upd_emp_id = e['emp_id']
                        st.markdown(f"<p style='color: #808090;'>ID: {upd_emp_id}</p>", unsafe_allow_html=True)
                        upd_name = st.text_input("Name", value=e['emp_name'])
                        upd_email = st.text_input("Email", value=e['email_id'] if e['email_id'] else "")
                    with c2: 
                        upd_phone = st.text_input("Phone", value=e['phone_no'] if e['phone_no'] else "")
                        upd_post = st.selectbox("Post", ["Employee", "Manager", "HR"], index=["Employee", "Manager", "HR"].index(e['post']) if e['post'] in ["Employee", "Manager", "HR"] else 0)
                        upd_basic = st.number_input("Salary", 0, 200000, value=int(e['basic']) if e['basic'] else 0)
                    
                    upd_address = st.text_input("Address", value=e['address'] if e['address'] else "")
                    
                    if st.form_submit_button("💾 Update Employee", use_container_width=True):
                        if upd_name and upd_phone:
                            if database.update_employee(upd_emp_id, upd_name, upd_email, upd_address, upd_phone, upd_post, upd_basic):
                                show_message(f"✅ Employee '{upd_name}' updated successfully!")
                                database.add_notification(upd_emp_id, f"Your profile has been updated.")
                                clear_form()
                                st.rerun()
                            else:
                                show_message("❌ Failed to update employee!", "error")
                        else:
                            show_message("⚠️ Please fill required fields!", "error")
            else:
                st.info("Please select an employee to update their details.")
    
    with tab4:
        if not emp_df.empty:
            c1, c2 = st.columns(2)
            with c1: st.bar_chart(emp_df['post'].value_counts())
            with c2: st.bar_chart(emp_df.set_index('emp_name')['basic'])

def attendance_page():
    user = st.session_state.user
    
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        st.session_state.error_message = None
    
    st.markdown("""<div style="margin-bottom: 30px;"><h1>📅 Attendance</h1></div>""", unsafe_allow_html=True)
    
    if is_hr() or is_manager():
        tab1, tab2, tab3 = st.tabs(["📋 Records", "✅ Mark", "📊 Summary"])
        emp_df = database.get_all_employees()
        
        with tab1:
            c1, c2, c3 = st.columns(3)
            with c1: emp_f = st.selectbox("Employee", ["All"] + emp_df['emp_id'].tolist())
            with c2: sd = st.date_input("Start", date.today().replace(day=1))
            with c3: ed = st.date_input("End", date.today())
            
            att = database.get_attendance_records(emp_id=emp_f if emp_f != "All" else None, start_date=sd, end_date=ed)
            if not att.empty:
                att = att.merge(emp_df[['emp_id', 'emp_name', 'post']], on='emp_id')
                att['Status'] = att['status'].map({'P': '✅ Present', 'A': '❌ Absent', 'H': '🎉 Holiday', 'L': '📝 Leave'})
                st.dataframe(att[['curr_date', 'emp_id', 'emp_name', 'post', 'Status']], use_container_width=True, hide_index=True)
        
        with tab2:
            c1, c2, c3 = st.columns(3)
            with c1: es = st.selectbox("Employee", emp_df['emp_id'].tolist())
            with c2: dt = st.date_input("Date", date.today())
            with c3: st_sel = st.selectbox("Status", ["P - Present", "A - Absent", "H - Holiday", "L - Leave"])
            status_text = {"P": "Present", "A": "Absent", "H": "Holiday", "L": "Leave"}
            if st.button("✅ Mark Attendance", use_container_width=True):
                if database.mark_attendance(es, dt, st_sel[0]): 
                    show_message(f"✅ Attendance marked: {status_text.get(st_sel[0])} on {dt}!")
                    st.rerun()
                else:
                    show_message("❌ Failed to mark attendance!", "error")
        
        with tab3:
            m, y = st.columns(2)
            with m: month = st.selectbox("Month", list(range(1,13)), index=date.today().month-1, format_func=lambda x: date(2000,x,1).strftime('%B'))
            with y: year = st.selectbox("Year", list(range(2020,2031)), index=date.today().year-2020)
            sm = database.get_attendance_summary(month=month, year=year)
            if not sm.empty:
                sm = sm.merge(emp_df[['emp_id', 'emp_name']], on='emp_id')
                st.dataframe(sm[['emp_name', 'present', 'absent', 'holiday', 'leave']], use_container_width=True, hide_index=True)
    else:
        tab1, tab2 = st.tabs(["📋 My Records", "📊 Summary"])
        with tab1:
            att = database.get_attendance_records(emp_id=user['emp_id'])
            if not att.empty:
                att['Status'] = att['status'].map({'P': '✅', 'A': '❌', 'H': '🎉', 'L': '📝'})
                st.dataframe(att[['curr_date', 'Status']], use_container_width=True, hide_index=True)
        with tab2:
            m, y = st.columns(2)
            with m: month = st.selectbox("Month", list(range(1,13)), index=date.today().month-1, format_func=lambda x: date(2000,x,1).strftime('%B'))
            with y: year = st.selectbox("Year", list(range(2020,2031)), index=date.today().year-2020)
            sm = database.get_attendance_summary(emp_id=user['emp_id'], month=month, year=year)
            if not sm.empty:
                 st.metric("Present", sm['present'].sum())
                 st.metric("Absent", sm['absent'].sum())

def projects_page():
    user = st.session_state.user
    
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        st.session_state.error_message = None
    
    st.markdown("""<div style="margin-bottom: 30px;"><h1>📁 Projects</h1></div>""", unsafe_allow_html=True)
    
    proj_df = database.get_all_projects()
    
    if is_hr() or is_manager():
        tab1, tab2 = st.tabs(["📋 View All", "➕ Add New"])
        
        with tab1:
            if not proj_df.empty:
                for _, r in proj_df.iterrows():
                    prog = r['progression'] if r['progression'] else 0
                    st.markdown(f"""<div class="card"><div style="display: flex; justify-content: space-between;"><h3 style="color: #00d4ff; margin: 0;">{r['project_name']}</h3><span style="background: {'#00c853' if r['status']=='Complete' else '#ffc107' if r['status']=='In Progress' else '#9e9e9e'}; color: white; padding: 5px 15px; border-radius: 20px;">{r['status'] if r['status'] else 'Not Started'}</span></div><p style="color: #a0a0c0;">{r['description']}</p><div class="progress-bar"><div class="progress-fill" style="width: {prog}%;"></div></div></div>""", unsafe_allow_html=True)
        
        with tab2:
            form_key = st.session_state.form_key
            with st.form(f"add_proj_{form_key}"):
                c1, c2 = st.columns(2)
                with c1: pid = st.text_input("Project ID", placeholder="PROJ005"); pname = st.text_input("Name")
                with c2: sd = st.date_input("Start", date.today()); ed = st.date_input("End", date.today()+timedelta(days=90))
                desc = st.text_area("Description")
                if st.form_submit_button("➕ Add Project", use_container_width=True):
                    if pid and pname and desc:
                        if database.add_project(pid, pname, desc, sd, ed): 
                            show_message(f"✅ Project '{pname}' added successfully!")
                            clear_form()
                            st.rerun()
                        else:
                            show_message("❌ Failed to add project!", "error")
    else:
        emp_proj_df = database.get_projects_by_employee(user['emp_id'])
        
        if not emp_proj_df.empty:
            st.markdown("### 📋 My Assigned Projects")
            for _, r in emp_proj_df.iterrows():
                prog = r['progression'] if r['progression'] else 0
                st.markdown(f"""<div class="card"><div style="display: flex; justify-content: space-between;"><h3 style="color: #00d4ff; margin: 0;">{r['project_name']}</h3><span style="background: {'#00c853' if r['status']=='Complete' else '#ffc107' if r['status']=='In Progress' else '#9e9e9e'}; color: white; padding: 5px 15px; border-radius: 20px;">{r['status'] if r['status'] else 'Not Started'}</span></div><p style="color: #a0a0c0;">{r['description']}</p><div class="progress-bar"><div class="progress-fill" style="width: {prog}%;"></div></div></div>""", unsafe_allow_html=True)
            
            st.markdown("### ✏️ Update My Project Status")
            form_key = st.session_state.form_key
            with st.form(f"update_proj_{form_key}"):
                sel_proj = st.selectbox("Select Project", emp_proj_df['project_id'].tolist(), format_func=lambda x: emp_proj_df[emp_proj_df['project_id']==x]['project_name'].values[0])
                new_status = st.selectbox("Status", ["Not Started", "In Progress", "Complete"])
                curr_val = emp_proj_df[emp_proj_df['project_id']==sel_proj]['progression'].values[0]
                default_prog = int(curr_val) if pd.notna(curr_val) else 0
                new_prog = st.slider("Progress (%)", 0, 100, default_prog)
                if st.form_submit_button("✅ Update Status", use_container_width=True):
                    if database.update_project_status_by_employee(sel_proj, new_status, new_prog):
                        show_message(f"✅ Project status updated to {new_status} ({new_prog}%)!")
                        st.rerun()
                    else:
                        show_message("❌ Failed to update project!", "error")
        else:
            st.info("No projects assigned to you yet!")

def tasks_page():
    user = st.session_state.user
    
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None
    
    st.markdown("""<div style="margin-bottom: 30px;"><h1>✅ Tasks</h1></div>""", unsafe_allow_html=True)
    
    if is_hr() or is_manager():
        tab1, tab2 = st.tabs(["📋 All Tasks", "➕ Assign"])
        with tab1:
            tdf = database.get_all_tasks()
            if not tdf.empty: st.dataframe(tdf[['project_name', 'emp_name', 'role']], use_container_width=True, hide_index=True)
        with tab2:
            form_key = st.session_state.form_key
            with st.form(f"assign_task_{form_key}"):
                pdf = database.get_all_projects()
                edf = database.get_employees_list()
                pid = st.selectbox("Project", pdf['project_id'].tolist())
                eid = st.selectbox("Employee", edf['emp_id'].tolist())
                role = st.text_input("Role")
                if st.form_submit_button("➕ Assign Task", use_container_width=True):
                    if pid and eid and role:
                        if database.add_task(pid, eid, role): 
                            show_message(f"✅ Task assigned to {eid} for project {pid}!")
                            database.add_notification(eid, f"You have been assigned a new task: {role} in project {pid}")
                            clear_form()
                            st.rerun()
    else:
        tdf = database.get_tasks_by_employee(user['emp_id'])
        if not tdf.empty:
            for _, r in tdf.iterrows():
                st.markdown(f"""<div class="info-box"><strong>{r['project_name']}</strong><p style="color: #a0a0c0;">Role: {r['role']}</p></div>""", unsafe_allow_html=True)
        else: st.info("No tasks!")

def notices_page():
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None
    
    st.markdown("""<div style="margin-bottom: 30px;"><h1>📢 Notices</h1></div>""", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        ndf = database.get_all_notices()
        if not ndf.empty:
            for _, r in ndf.iterrows():
                t = r['time'].strftime('%b %d, %Y') if isinstance(r['time'], datetime) else str(r['time'])
                st.markdown(f"""<div class="info-box"><p style="margin: 0; font-size: 15px;">{r['notice']}</p><p style="color: #808090; font-size: 11px; margin: 10px 0 0 0;">{t}</p></div>""", unsafe_allow_html=True)
        else: st.info("No notices!")
    
    with col2:
        if is_hr() or is_manager():
            form_key = st.session_state.form_key
            with st.form(f"add_notice_{form_key}"):
                nt = st.text_area("Notice", height=100)
                if st.form_submit_button("📢 Post Notice", use_container_width=True):
                    if nt and database.add_notice(nt): 
                        show_message("✅ Notice posted successfully!")
                        clear_form()
                        st.rerun()

def holiday_page():
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None
    
    st.markdown("""<div style="margin-bottom: 30px;"><h1>🎉 Holiday Calendar</h1></div>""", unsafe_allow_html=True)
    
    current_year = date.today().year
    selected_year = st.selectbox("Select Year", list(range(current_year-2, current_year+3)), index=2)
    holidays_df = database.get_all_holidays(selected_year)
    
    if is_hr() or is_manager():
        tab1, tab2 = st.tabs(["📅 View Holidays", "➕ Add Holiday"])
        
        with tab1:
            if not holidays_df.empty:
                for _, row in holidays_df.iterrows():
                    holiday_date = row['holiday_date']
                    if hasattr(holiday_date, 'strftime'):
                        date_str = holiday_date.strftime('%B %d, %Y')
                    else:
                        date_str = str(holiday_date)
                    st.markdown(f"""<div class="info-box"><div style="display: flex; justify-content: space-between;"><strong>{row['holiday_name']}</strong><span style="background: #00c853; color: white; padding: 4px 12px; border-radius: 20px; font-size: 11px;">{date_str}</span></div></div>""", unsafe_allow_html=True)
            else:
                st.info(f"No holidays for {selected_year}")
        
        with tab2:
            form_key = st.session_state.form_key
            with st.form(f"add_holiday_{form_key}"):
                holiday_name = st.text_input("Holiday Name")
                holiday_date = st.date_input("Date")
                description = st.text_area("Description (Optional)")
                if st.form_submit_button("➕ Add Holiday", use_container_width=True):
                    if holiday_name:
                        if database.add_holiday(holiday_name, holiday_date, description):
                            show_message(f"✅ Holiday '{holiday_name}' added successfully!")
                            clear_form()
                            st.rerun()
    else:
        if not holidays_df.empty:
            for _, row in holidays_df.iterrows():
                holiday_date = row['holiday_date']
                if hasattr(holiday_date, 'strftime'):
                    date_str = holiday_date.strftime('%B %d, %Y')
                else:
                    date_str = str(holiday_date)
                st.markdown(f"""<div class="info-box"><div style="display: flex; justify-content: space-between;"><strong>{row['holiday_name']}</strong><span style="background: #00c853; color: white; padding: 4px 12px; border-radius: 20px; font-size: 11px;">{date_str}</span></div></div>""", unsafe_allow_html=True)

def leave_page():
    user = st.session_state.user
    
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        st.session_state.error_message = None
    
    st.markdown("""<div style="margin-bottom: 30px;"><h1>🍃 Leave Management</h1></div>""", unsafe_allow_html=True)
    
    if is_hr() or is_manager():
        tab1, tab2 = st.tabs(["⏳ Pending Requests", "📜 All History"])
        with tab1:
            all_req = database.get_all_leave_requests()
            if not all_req.empty:
                pending = all_req[all_req['status'] == 'Pending']
                if not pending.empty:
                    for _, row in pending.iterrows():
                        with st.container():
                            c1, c2, c3, c4 = st.columns([3, 2, 1, 1])
                            with c1:
                                st.markdown(f"**{row['emp_name']}** ({row['emp_id']})")
                                st.caption(f"Reason: {row['reason']}")
                            with c2: st.markdown(f"📅 {row['start_date']} to {row['end_date']}")
                            with c3:
                                if st.button("✅ Approve", key=f"app_{row['request_id']}"):
                                    if database.update_leave_status(row['request_id'], 'Approved'): 
                                        show_message(f"✅ Leave request approved for {row['emp_name']}!")
                                        st.rerun()
                            with c4:
                                if st.button("❌ Reject", key=f"rej_{row['request_id']}"):
                                    if database.update_leave_status(row['request_id'], 'Rejected'): 
                                        show_message(f"❌ Leave request rejected for {row['emp_name']}!")
                                        st.rerun()
                            st.divider()
                else: st.info("No pending leave requests.")
        with tab2:
            if not all_req.empty:
                st.dataframe(all_req[['emp_name', 'start_date', 'end_date', 'reason', 'status', 'request_date']], use_container_width=True, hide_index=True)
    else:
        tab1, tab2 = st.tabs(["➕ Request Leave", "📜 My History"])
        with tab1:
            form_key = st.session_state.form_key
            with st.form(f"leave_req_{form_key}"):
                c1, c2 = st.columns(2)
                with c1: sd = st.date_input("From Date", min_value=date.today())
                with c2: ed = st.date_input("To Date", min_value=sd)
                reason = st.text_area("Reason")
                if st.form_submit_button("🚀 Submit Request", use_container_width=True):
                    if reason:
                        if database.add_leave_request(user['emp_id'], sd, ed, reason): 
                            show_message(f"✅ Leave request submitted from {sd} to {ed}!")
                            clear_form()
                            st.rerun()
                        else:
                            show_message("❌ Failed to submit request!", "error")
                    else:
                        show_message("⚠️ Please provide a reason!", "error")
        with tab2:
            my_req = database.get_employee_leave_requests(user['emp_id'])
            if not my_req.empty:
                st.dataframe(my_req[['start_date', 'end_date', 'reason', 'status', 'request_date']], use_container_width=True, hide_index=True)

def payslips_page():
    user = st.session_state.user
    
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None
    
    st.markdown("""<div style="margin-bottom: 30px;"><h1>💰 Payslips & Salary</h1></div>""", unsafe_allow_html=True)
    
    if is_hr() or is_manager():
        tab1, tab2 = st.tabs(["📋 All Payslips", "🆕 Generate"])
        
        with tab1:
            all_payslips = database.get_all_payslips()
            if not all_payslips.empty:
                st.dataframe(all_payslips[['emp_name', 'month', 'year', 'basic_salary', 'deduction_amount', 'net_salary']], use_container_width=True, hide_index=True)
        
        with tab2:
            form_key = st.session_state.form_key
            with st.form(f"payslip_{form_key}"):
                emp_df = database.get_all_employees()
                sel_emp = st.selectbox("Select Employee", emp_df['emp_id'].tolist(), format_func=lambda x: f"{emp_df[emp_df['emp_id']==x]['emp_name'].values[0]} ({x})")
                c1, c2 = st.columns(2)
                with c1: month = st.selectbox("Month", list(range(1,13)), index=date.today().month-1, format_func=lambda x: date(2000,x,1).strftime('%B'))
                with c2: year = st.selectbox("Year", list(range(2020,2031)), index=date.today().year-2020)
                
                if st.form_submit_button("🆕 Generate Payslip", use_container_width=True):
                    payslip = database.generate_payslip(sel_emp, month, year)
                    if payslip:
                        month_name = date(2000, month, 1).strftime('%B')
                        show_message(f"✅ Payslip generated for {payslip['emp_name']} ({month_name} {year})!")
                        database.add_notification(sel_emp, f"Your payslip for {month_name} {year} has been generated. Net Salary: ₹{payslip['net_salary']:,.2f}")
                        clear_form()
                        st.rerun()
    else:
        tab1, tab2 = st.tabs(["📋 My Payslips", "🆕 Current Month"])
        
        with tab1:
            my_payslips = database.get_all_payslips(user['emp_id'])
            if not my_payslips.empty:
                st.dataframe(my_payslips[['month', 'year', 'basic_salary', 'deduction_amount', 'net_salary']], use_container_width=True, hide_index=True)
        
        with tab2:
            current_month = date.today().month
            current_year = date.today().year
            existing = database.get_payslip(user['emp_id'], current_month, current_year)
            
            if existing:
                st.markdown(f"**Basic Salary: ₹{existing['basic_salary']:,.2f}**")
                st.markdown(f"**Deductions: ₹{existing['deduction_amount']:,.2f}**")
                st.markdown(f"**Net Salary: ₹{existing['net_salary']:,.2f}**")
            else:
                st.info(f"No payslip for {date(2000, current_month, 1).strftime('%B')} {current_year}")
                
            if st.button("🆕 Generate", use_container_width=True):
                payslip = database.generate_payslip(user['emp_id'], current_month, current_year)
                if payslip:
                    month_name = date(2000, current_month, 1).strftime('%B')
                    show_message(f"✅ Payslip generated for {month_name} {current_year}!")
                    st.rerun()

def profile_page():
    user = st.session_state.user
    st.markdown("""<div style="margin-bottom: 30px;"><h1>👤 My Profile</h1></div>""", unsafe_allow_html=True)
    init = ''.join([n[0] for n in user['emp_name'].split()]).upper()
    st.markdown(f"""<div class="card" style="text-align: center;"><div class="profile-avatar" style="width: 120px; height: 120px; font-size: 48px;">{init}</div><h2 style="color: #00d4ff;">{user['emp_name']}</h2><p style="color: #00ff88; font-weight: bold;">{user['post']}</p><p>ID: {user['emp_id']}</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="card"><h3>📋 Details</h3><p><strong>Email:</strong> {user['email_id']}</p><p><strong>Phone:</strong> {user['phone_no']}</p><p><strong>Joined:</strong> {user['date_of_join']}</p><p><strong>Salary:</strong> ₹{user['basic']:,}</p></div>""", unsafe_allow_html=True)

def main():
    # Display persistent messages at the top
    if st.session_state.success_message:
        st.success(st.session_state.success_message)
        st.session_state.success_message = None
    if st.session_state.error_message:
        st.error(st.session_state.error_message)
        st.session_state.error_message = None
    
    if st.session_state.show_landing:
        landing_page()
    elif not st.session_state.logged_in: 
        login_page()
    else:
        sidebar_navigation()
        page = st.session_state.page
        if page == 'dashboard': dashboard_page()
        elif page == 'employees' and (is_hr() or is_manager()): employees_page()
        elif page == 'attendance': attendance_page()
        elif page == 'leave': leave_page()
        elif page == 'projects': projects_page()
        elif page == 'tasks': tasks_page()
        elif page == 'notices': notices_page()
        elif page == 'profile': profile_page()
        elif page == 'payslips': payslips_page()
        elif page == 'holiday': holiday_page()
        else: dashboard_page()

if __name__ == '__main__': main()
