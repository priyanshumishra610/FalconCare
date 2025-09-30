# FalconCare - Government Health Dashboard
# Real-time monitoring for District Health Officers and ASHA workers

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime, timedelta
import json
import random

# Set page config
st.set_page_config(
    page_title="FalconCare - Government Dashboard",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

class HealthDashboard:
    """Government Health Dashboard for monitoring and analytics"""
    
    def __init__(self):
        self.initialize_data()
    
    def initialize_data(self):
        """Initialize mock data for demonstration"""
        # Districts in Chhattisgarh (example state)
        self.districts = ["Raipur", "Bilaspur", "Durg", "Korba", "Rajnandgaon", "Bastar", "Surguja"]
        
        # Generate mock health data
        self.health_data = self.generate_mock_health_data()
        self.user_interactions = self.generate_mock_user_data()
        self.outbreak_data = self.generate_outbreak_data()
        self.asha_performance = self.generate_asha_data()
    
    def generate_mock_health_data(self):
        """Generate realistic health statistics"""
        data = []
        for district in self.districts:
            for disease in ["Dengue", "Malaria", "Typhoid", "Diarrhea", "COVID-19"]:
                cases = random.randint(10, 200)
                trend = random.choice(["Increasing", "Stable", "Decreasing"])
                alert = cases > 100 and trend == "Increasing"
                
                data.append({
                    "District": district,
                    "Disease": disease,
                    "Cases": cases,
                    "Trend": trend,
                    "Alert": alert,
                    "Week": f"Week {random.randint(1, 52)}"
                })
        
        return pd.DataFrame(data)
    
    def generate_mock_user_data(self):
        """Generate user interaction data"""
        data = []
        for i in range(1000):
            data.append({
                "Timestamp": datetime.now() - timedelta(hours=random.randint(0, 168)),
                "District": random.choice(self.districts),
                "Intent": random.choice(["symptom_fever", "vaccination_covid", "find_doctor", "emergency_severe", "myth_detection"]),
                "Triage_Level": random.choice(["GREEN", "YELLOW", "RED"]),
                "Language": random.choice(["Hindi", "English", "Mixed"]),
                "Channel": random.choice(["WhatsApp", "SMS", "USSD", "Web"]),
                "Age_Group": random.choice(["0-18", "18-35", "35-60", "60+"]),
                "Response_Time": random.uniform(1.0, 5.0)
            })
        
        return pd.DataFrame(data)
    
    def generate_outbreak_data(self):
        """Generate outbreak detection data"""
        data = []
        for district in self.districts:
            for disease in ["Dengue", "Malaria", "Diarrhea"]:
                risk_score = random.uniform(0.1, 0.9)
                status = "High Risk" if risk_score > 0.7 else "Medium Risk" if risk_score > 0.4 else "Low Risk"
                
                data.append({
                    "District": district,
                    "Disease": disease,
                    "Risk_Score": risk_score,
                    "Status": status,
                    "Predicted_Cases": int(risk_score * 100),
                    "Confidence": random.uniform(0.7, 0.95)
                })
        
        return pd.DataFrame(data)
    
    def generate_asha_data(self):
        """Generate ASHA worker performance data"""
        data = []
        for i in range(50):
            data.append({
                "ASHA_ID": f"ASHA_{i+1:03d}",
                "Name": f"ASHA Worker {i+1}",
                "District": random.choice(self.districts),
                "Villages_Covered": random.randint(3, 8),
                "Households_Visited": random.randint(50, 200),
                "Emergency_Responses": random.randint(0, 15),
                "Health_Education_Sessions": random.randint(5, 30),
                "Vaccination_Referrals": random.randint(10, 50),
                "Performance_Score": random.uniform(0.6, 1.0),
                "Last_Active": datetime.now() - timedelta(hours=random.randint(0, 72))
            })
        
        return pd.DataFrame(data)
    
    def render_dashboard(self):
        """Render the complete dashboard"""
        # Header
        st.markdown("""
        <div style="background: linear-gradient(90deg, #2E8B57, #3CB371); padding: 20px; border-radius: 10px; margin-bottom: 20px;">
            <h1 style="color: white; text-align: center; margin: 0;">
                🏥 FalconCare - Government Dashboard
            </h1>
            <p style="color: white; text-align: center; margin: 0; font-size: 18px;">
                Real-time Health Monitoring & Analytics for Government Officials
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Sidebar
        self.render_sidebar()
        
        # Main content
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📊 Overview", 
            "🚨 Disease Surveillance", 
            "🤖 AI Analytics", 
            "👩‍⚕️ ASHA Performance", 
            "📱 User Engagement"
        ])
        
        with tab1:
            self.render_overview()
        
        with tab2:
            self.render_disease_surveillance()
        
        with tab3:
            self.render_ai_analytics()
        
        with tab4:
            self.render_asha_performance()
        
        with tab5:
            self.render_user_engagement()
    
    def render_sidebar(self):
        """Render sidebar with filters and controls"""
        st.sidebar.markdown("### 🎛️ Dashboard Controls")
        
        # Time range selector
        time_range = st.sidebar.selectbox(
            "📅 Time Range",
            ["Last 24 Hours", "Last 7 Days", "Last 30 Days", "Last 3 Months"]
        )
        
        # District filter
        selected_districts = st.sidebar.multiselect(
            "🏘️ Select Districts",
            self.districts,
            default=self.districts
        )
        
        # Alert threshold
        alert_threshold = st.sidebar.slider(
            "🚨 Alert Threshold",
            min_value=50,
            max_value=200,
            value=100,
            help="Number of cases to trigger alert"
        )
        
        # Language filter
        languages = st.sidebar.multiselect(
            "🗣️ Languages",
            ["Hindi", "English", "Mixed"],
            default=["Hindi", "English", "Mixed"]
        )
        
        # Real-time toggle
        real_time = st.sidebar.checkbox("⚡ Real-time Updates", value=True)
        
        # Emergency notification
        if st.sidebar.button("🚨 Test Emergency Alert"):
            st.sidebar.error("🚨 Emergency Alert Sent to District Health Officer!")
            st.sidebar.info("SMS sent to: +91-98765-43210")
        
        # Export data
        if st.sidebar.button("📥 Export Dashboard Data"):
            st.sidebar.success("✅ Data exported to health_data.xlsx")
        
        st.sidebar.markdown("---")
        st.sidebar.markdown("### 📞 Emergency Contacts")
        st.sidebar.markdown("**District Health Officer:** 0771-2221111")
        st.sidebar.markdown("**ASHA Coordinator:** 0771-2222222")
        st.sidebar.markdown("**Emergency:** 108")
    
    def render_overview(self):
        """Render overview dashboard"""
        st.markdown("### 📊 FalconCare - System Overview")
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_users = len(self.user_interactions)
            st.metric(
                label="👥 Total Users Served",
                value=f"{total_users:,}",
                delta=f"+{random.randint(50, 200)} today"
            )
        
        with col2:
            emergency_cases = len(self.user_interactions[self.user_interactions['Triage_Level'] == 'RED'])
            st.metric(
                label="🚨 Emergency Cases",
                value=emergency_cases,
                delta=f"+{random.randint(5, 15)} today"
            )
        
        with col3:
            avg_response = self.user_interactions['Response_Time'].mean()
            st.metric(
                label="⚡ Avg Response Time",
                value=f"{avg_response:.1f}s",
                delta="-0.3s"
            )
        
        with col4:
            accuracy = 87.5  # AI accuracy
            st.metric(
                label="🎯 AI Accuracy",
                value=f"{accuracy}%",
                delta="+2.1%"
            )
        
        # Disease trends
        st.markdown("### 📈 Disease Trends Across Districts")
        
        disease_summary = self.health_data.groupby(['Disease', 'District'])['Cases'].sum().reset_index()
        
        fig = px.bar(
            disease_summary,
            x='Disease',
            y='Cases',
            color='District',
            title="Disease Cases by District",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
        
        # Real-time activity
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔴 Live Activity Feed")
            
            # Simulate real-time activity
            activities = [
                "🚨 Emergency alert: Chest pain case in Raipur",
                "💉 Vaccination query: COVID vaccine in Bilaspur",
                "🤒 Fever symptoms reported in Durg",
                "❌ Myth detected: Turmeric cancer cure",
                "🏥 Hospital finder query in Bastar",
                "📱 ASHA worker login: Surguja district"
            ]
            
            for activity in activities[:6]:
                st.text(f"{datetime.now().strftime('%H:%M:%S')} - {activity}")
        
        with col2:
            st.markdown("### 🗺️ Geographic Distribution")
            
            # District-wise case distribution
            district_cases = self.health_data.groupby('District')['Cases'].sum().reset_index()
            
            fig = px.pie(
                district_cases,
                values='Cases',
                names='District',
                title="Cases by District"
            )
            fig.update_layout(height=300)
            st.plotly_chart(fig, use_container_width=True)
    
    def render_disease_surveillance(self):
        """Render disease surveillance dashboard"""
        st.markdown("### 🚨 Disease Surveillance & Outbreak Detection")
        
        # Outbreak alerts
        high_risk = self.outbreak_data[self.outbreak_data['Status'] == 'High Risk']
        
        if not high_risk.empty:
            st.error("🚨 **HIGH RISK OUTBREAK DETECTED**")
            
            for _, row in high_risk.iterrows():
                st.warning(f"**{row['Disease']}** in **{row['District']}** - Risk Score: {row['Risk_Score']:.2f}")
        
        # Disease surveillance table
        st.markdown("### 📊 Current Disease Status")
        
        # Enhanced disease data with color coding
        display_data = self.health_data.copy()
        
        # Color code based on alert status
        def get_status_color(row):
            if row['Alert']:
                return "🔴"
            elif row['Trend'] == 'Increasing':
                return "🟡"
            else:
                return "🟢"
        
        display_data['Status'] = display_data.apply(get_status_color, axis=1)
        
        # Display table
        st.dataframe(
            display_data[['Status', 'District', 'Disease', 'Cases', 'Trend']],
            use_container_width=True
        )
        
        # Trend analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Weekly Trends")
            
            # Generate weekly trend data
            weeks = range(1, 13)
            diseases = ["Dengue", "Malaria", "Typhoid"]
            
            fig = go.Figure()
            
            for disease in diseases:
                cases = [random.randint(20, 100) for _ in weeks]
                fig.add_trace(go.Scatter(
                    x=list(weeks),
                    y=cases,
                    mode='lines+markers',
                    name=disease,
                    line=dict(width=3)
                ))
            
            fig.update_layout(
                title="Disease Trends (Last 12 Weeks)",
                xaxis_title="Week",
                yaxis_title="Cases",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 🎯 Outbreak Prediction")
            
            # Risk matrix
            risk_matrix = self.outbreak_data.pivot(
                index='District',
                columns='Disease',
                values='Risk_Score'
            )
            
            fig = px.imshow(
                risk_matrix,
                title="Outbreak Risk Matrix",
                color_continuous_scale="Reds",
                aspect="auto"
            )
            fig.update_layout(height=400)
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Recommendations
        st.markdown("### 💡 AI Recommendations")
        
        recommendations = [
            "🔍 **Increased surveillance** recommended for Dengue in Raipur district",
            "💉 **Vaccination drive** needed in Bilaspur for seasonal flu",
            "🧼 **Hygiene awareness** campaign required in Bastar region",
            "🚰 **Water quality testing** suggested for Diarrhea hotspots",
            "📱 **ASHA worker training** on new symptoms reporting"
        ]
        
        for rec in recommendations:
            st.info(rec)
    
    def render_ai_analytics(self):
        """Render AI analytics dashboard"""
        st.markdown("### 🤖 AI Performance & Analytics")
        
        # AI metrics
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("🎯 Intent Accuracy", "92.3%", "+1.5%")
        
        with col2:
            st.metric("🔍 Entity Extraction", "87.8%", "+2.1%")
        
        with col3:
            st.metric("❌ Myth Detection", "94.1%", "+0.8%")
        
        # Language performance
        st.markdown("### 🗣️ Multilingual Performance")
        
        lang_performance = pd.DataFrame({
            'Language': ['Hindi', 'English', 'Hindi (Roman)', 'Mixed'],
            'Accuracy': [89.2, 93.5, 85.7, 88.1],
            'Volume': [45, 30, 15, 10]
        })
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(x=lang_performance['Language'], y=lang_performance['Accuracy'], name="Accuracy %"),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=lang_performance['Language'], y=lang_performance['Volume'], 
                      mode='lines+markers', name="Usage %"),
            secondary_y=True,
        )
        
        fig.update_layout(title="Language Performance vs Usage")
        fig.update_yaxes(title_text="Accuracy %", secondary_y=False)
        fig.update_yaxes(title_text="Usage %", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Triage accuracy
        st.markdown("### 🚦 Triage System Performance")
        
        triage_data = self.user_interactions['Triage_Level'].value_counts()
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.pie(
                values=triage_data.values,
                names=triage_data.index,
                title="Triage Distribution",
                color_discrete_map={
                    'GREEN': '#28a745',
                    'YELLOW': '#ffc107', 
                    'RED': '#dc3545'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Triage accuracy by level
            accuracy_data = pd.DataFrame({
                'Triage_Level': ['GREEN', 'YELLOW', 'RED'],
                'Accuracy': [89.5, 92.1, 96.8],
                'Cases': [650, 280, 70]
            })
            
            fig = px.bar(
                accuracy_data,
                x='Triage_Level',
                y='Accuracy',
                title="Triage Accuracy by Level",
                color='Triage_Level',
                color_discrete_map={
                    'GREEN': '#28a745',
                    'YELLOW': '#ffc107',
                    'RED': '#dc3545'
                }
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Myth detection statistics
        st.markdown("### ❌ Myth Detection Analytics")
        
        myth_stats = pd.DataFrame({
            'Myth_Category': ['Home Remedies', 'False Cures', 'Vaccine Myths', 'COVID Myths'],
            'Detected': [156, 89, 67, 134],
            'Corrected': [152, 85, 65, 128]
        })
        
        fig = px.bar(
            myth_stats,
            x='Myth_Category',
            y=['Detected', 'Corrected'],
            title="Myth Detection & Correction Statistics",
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # AI learning progress
        st.markdown("### 📚 AI Learning Progress")
        
        learning_data = pd.DataFrame({
            'Week': range(1, 13),
            'Accuracy': np.cumsum(np.random.normal(0.5, 0.2, 12)) + 85,
            'Training_Data': np.cumsum(np.random.randint(100, 500, 12))
        })
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Scatter(x=learning_data['Week'], y=learning_data['Accuracy'], 
                      mode='lines+markers', name="Accuracy %"),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Bar(x=learning_data['Week'], y=learning_data['Training_Data'], 
                   name="Training Samples", opacity=0.6),
            secondary_y=True,
        )
        
        fig.update_layout(title="AI Learning Progress Over Time")
        fig.update_yaxes(title_text="Accuracy %", secondary_y=False)
        fig.update_yaxes(title_text="Training Samples", secondary_y=True)
        
        st.plotly_chart(fig, use_container_width=True)
    
    def render_asha_performance(self):
        """Render ASHA worker performance dashboard"""
        st.markdown("### 👩‍⚕️ ASHA Worker Performance & Management")
        
        # ASHA summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            active_asha = len(self.asha_performance)
            st.metric("👩‍⚕️ Active ASHA Workers", active_asha, "+3 this month")
        
        with col2:
            avg_performance = self.asha_performance['Performance_Score'].mean()
            st.metric("⭐ Avg Performance", f"{avg_performance:.1%}", "+2.3%")
        
        with col3:
            total_households = self.asha_performance['Households_Visited'].sum()
            st.metric("🏠 Households Reached", f"{total_households:,}", "+150 today")
        
        with col4:
            emergency_responses = self.asha_performance['Emergency_Responses'].sum()
            st.metric("🚨 Emergency Responses", emergency_responses, "+5 today")
        
        # Performance distribution
        st.markdown("### 📊 Performance Distribution")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.histogram(
                self.asha_performance,
                x='Performance_Score',
                nbins=20,
                title="ASHA Performance Score Distribution",
                color_discrete_sequence=['#2E8B57']
            )
            fig.update_layout(xaxis_title="Performance Score", yaxis_title="Number of ASHA Workers")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Top performers
            top_performers = self.asha_performance.nlargest(10, 'Performance_Score')[
                ['Name', 'District', 'Performance_Score', 'Households_Visited']
            ]
            
            fig = px.bar(
                top_performers,
                x='Performance_Score',
                y='Name',
                title="Top 10 ASHA Performers",
                orientation='h',
                color='Performance_Score',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # District-wise performance
        st.markdown("### 🏘️ District-wise ASHA Performance")
        
        district_performance = self.asha_performance.groupby('District').agg({
            'Performance_Score': 'mean',
            'Households_Visited': 'sum',
            'Emergency_Responses': 'sum',
            'Health_Education_Sessions': 'sum'
        }).reset_index()
        
        fig = px.scatter(
            district_performance,
            x='Households_Visited',
            y='Performance_Score',
            size='Emergency_Responses',
            color='Health_Education_Sessions',
            hover_data=['District'],
            title="District Performance vs Reach",
            color_continuous_scale='Viridis'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # ASHA activity timeline
        st.markdown("### ⏰ Recent ASHA Activities")
        
        recent_activities = [
            "👩‍⚕️ ASHA_001 (Raipur) - Emergency response: Chest pain case",
            "💉 ASHA_045 (Bilaspur) - Vaccination drive: 25 children covered",
            "🏠 ASHA_023 (Durg) - House visit: Elderly health checkup",
            "📚 ASHA_067 (Bastar) - Health education: Hygiene awareness session",
            "🤒 ASHA_012 (Surguja) - Symptom reported: Fever in child",
            "📱 ASHA_089 (Korba) - Used Health Guardian AI: Myth correction"
        ]
        
        for activity in recent_activities:
            st.text(f"{datetime.now().strftime('%H:%M')} - {activity}")
        
        # ASHA leaderboard
        st.markdown("### 🏆 ASHA Leaderboard (This Month)")
        
        leaderboard = self.asha_performance.nlargest(5, 'Performance_Score')[
            ['Name', 'District', 'Performance_Score', 'Households_Visited', 'Emergency_Responses']
        ].copy()
        
        leaderboard['Rank'] = range(1, len(leaderboard) + 1)
        leaderboard['Badge'] = ['🥇', '🥈', '🥉', '🏅', '🏅']
        
        st.dataframe(
            leaderboard[['Badge', 'Rank', 'Name', 'District', 'Performance_Score', 'Households_Visited']],
            use_container_width=True
        )
    
    def render_user_engagement(self):
        """Render user engagement analytics"""
        st.markdown("### 📱 User Engagement & Platform Analytics")
        
        # Channel distribution
        col1, col2 = st.columns(2)
        
        with col1:
            channel_data = self.user_interactions['Channel'].value_counts()
            
            fig = px.pie(
                values=channel_data.values,
                names=channel_data.index,
                title="Usage by Channel",
                color_discrete_sequence=px.colors.qualitative.Set2
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            language_data = self.user_interactions['Language'].value_counts()
            
            fig = px.bar(
                x=language_data.index,
                y=language_data.values,
                title="Language Preference",
                color=language_data.index,
                color_discrete_sequence=px.colors.qualitative.Pastel
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Usage patterns
        st.markdown("### ⏰ Usage Patterns")
        
        # Generate hourly usage data
        hours = range(24)
        usage_pattern = [random.randint(10, 100) for _ in hours]
        
        fig = px.line(
            x=hours,
            y=usage_pattern,
            title="24-Hour Usage Pattern",
            labels={'x': 'Hour of Day', 'y': 'Number of Queries'}
        )
        fig.update_traces(line=dict(width=3, color='#2E8B57'))
        
        st.plotly_chart(fig, use_container_width=True)
        
        # User demographics
        st.markdown("### 👥 User Demographics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            age_data = self.user_interactions['Age_Group'].value_counts()
            
            fig = px.bar(
                x=age_data.index,
                y=age_data.values,
                title="Users by Age Group",
                color=age_data.values,
                color_continuous_scale='Blues'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Query types
            intent_data = self.user_interactions['Intent'].value_counts()
            
            fig = px.bar(
                x=intent_data.values,
                y=intent_data.index,
                title="Most Common Queries",
                orientation='h',
                color=intent_data.values,
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Geographic reach
        st.markdown("### 🗺️ Geographic Reach")
        
        district_users = self.user_interactions['District'].value_counts().reset_index()
        district_users.columns = ['District', 'Users']
        
        fig = px.bar(
            district_users,
            x='District',
            y='Users',
            title="Users by District",
            color='Users',
            color_continuous_scale='viridis'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # User satisfaction metrics
        st.markdown("### 😊 User Satisfaction")
        
        satisfaction_metrics = pd.DataFrame({
            'Metric': ['Response Accuracy', 'Response Time', 'Language Support', 'Overall Experience'],
            'Score': [4.2, 4.5, 4.1, 4.3],
            'Target': [4.0, 4.0, 4.0, 4.0]
        })
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=satisfaction_metrics['Metric'],
            y=satisfaction_metrics['Score'],
            name='Current Score',
            marker_color='lightblue'
        ))
        
        fig.add_trace(go.Scatter(
            x=satisfaction_metrics['Metric'],
            y=satisfaction_metrics['Target'],
            mode='markers',
            name='Target',
            marker=dict(color='red', size=10, symbol='diamond')
        ))
        
        fig.update_layout(
            title="User Satisfaction Scores (out of 5)",
            yaxis_title="Score",
            barmode='group'
        )
        
        st.plotly_chart(fig, use_container_width=True)


def main():
    """Main dashboard application"""
    dashboard = HealthDashboard()
    dashboard.render_dashboard()
    
    # Auto-refresh option
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Refresh Data"):
        st.experimental_rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; font-size: 14px;">
        🏥 FalconCare Dashboard | Government of India | 
        Last Updated: {} | 
        🔒 Secure & Compliant
    </div>
    """.format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)


if __name__ == "__main__":
    main()