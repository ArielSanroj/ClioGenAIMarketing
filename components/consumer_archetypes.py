import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def load_archetype_data():
    """Load data from Excel files"""
    try:
        archetypes_df = pd.read_excel("Consumer Archetype.xlsx")
        subscales_df = pd.read_excel("Consumer Subscales.xlsx")
        return archetypes_df, subscales_df
    except Exception as e:
        st.error(f"Error loading archetype data: {str(e)}")
        return None, None

def create_archetype_visualization(df):
    """Create visualization for archetypes"""
    try:
        # Archetype score visualization
        fig = px.bar(df, 
                    x='Name',
                    y='Score',
                    title='Consumer Archetypes Distribution',
                    color='Score',
                    color_continuous_scale='viridis')
        fig.update_layout(
            xaxis_title="Archetype",
            yaxis_title="Score",
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display archetype details
        for _, row in df.iterrows():
            with st.expander(f"📊 {row['Name']} - Score: {row['Score']}"):
                st.markdown(f"**Description:** {row['Description']}")
                st.markdown("**Key Characteristics:**")
                characteristics = row['Characteristics'].split(',')
                for char in characteristics:
                    st.markdown(f"- {char.strip()}")
                
    except Exception as e:
        st.error(f"Error creating archetype visualization: {str(e)}")

def create_subscale_visualization(df):
    """Create visualization for subscales"""
    try:
        # Create sunburst chart for subscales
        fig = px.sunburst(df,
                         path=['Category', 'Subscale'],
                         values='Value',
                         color='Value',
                         color_continuous_scale='viridis',
                         title='Consumer Subscales Distribution')
        st.plotly_chart(fig, use_container_width=True)
        
        # Display subscale details by category
        for category in df['Category'].unique():
            with st.expander(f"📈 {category} Subscales"):
                category_data = df[df['Category'] == category]
                for _, row in category_data.iterrows():
                    st.markdown(f"**{row['Subscale']}** (Score: {row['Value']})")
                    st.markdown(f"_{row['Description']}_")
                    st.markdown("---")
                
    except Exception as e:
        st.error(f"Error creating subscale visualization: {str(e)}")

def create_comparison_view(archetypes_df, subscales_df):
    """Create comparison visualization between archetypes and subscales"""
    try:
        st.markdown("### Archetype-Subscale Relationship Analysis")
        
        # Create a correlation matrix visualization (mock data for demonstration)
        categories = subscales_df['Category'].unique()
        archetypes = archetypes_df['Name'].unique()
        
        # Create a sample correlation matrix
        correlation_data = []
        for archetype in archetypes:
            row = []
            for category in categories:
                # Generate a mock correlation value between 0 and 1
                correlation = abs(hash(f"{archetype}-{category}") % 100) / 100
                row.append(correlation)
            correlation_data.append(row)
        
        fig = go.Figure(data=go.Heatmap(
            z=correlation_data,
            x=categories,
            y=archetypes,
            colorscale='Viridis',
            hoverongaps=False))
        
        fig.update_layout(
            title="Archetype-Category Correlation Matrix",
            xaxis_title="Categories",
            yaxis_title="Archetypes"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error creating comparison view: {str(e)}")

def render_consumer_archetypes():
    """Render the consumer archetypes display"""
    st.markdown("## Consumer Archetypes Analysis")
    
    # Load data
    archetypes_df, subscales_df = load_archetype_data()
    
    if archetypes_df is None or subscales_df is None:
        st.warning("Unable to load archetype data. Please check the Excel files.")
        return
    
    # Create tabs for different views
    tabs = st.tabs(["Archetypes", "Subscales", "Comparison"])
    
    with tabs[0]:
        st.subheader("Consumer Archetypes")
        create_archetype_visualization(archetypes_df)
        
        # Raw data view
        with st.expander("View Raw Archetype Data"):
            st.dataframe(archetypes_df)
    
    with tabs[1]:
        st.subheader("Consumer Subscales")
        create_subscale_visualization(subscales_df)
        
        # Raw data view
        with st.expander("View Raw Subscale Data"):
            st.dataframe(subscales_df)
    
    with tabs[2]:
        create_comparison_view(archetypes_df, subscales_df)
    
    # Export functionality
    st.markdown("### Export Data")
    col1, col2 = st.columns(2)
    
    with col1:
        csv = archetypes_df.to_csv(index=False)
        st.download_button(
            label="Download Archetypes CSV",
            data=csv,
            file_name="consumer_archetypes.csv",
            mime="text/csv"
        )
    
    with col2:
        csv = subscales_df.to_csv(index=False)
        st.download_button(
            label="Download Subscales CSV",
            data=subscales_df.to_csv(index=False),
            file_name="consumer_subscales.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    render_consumer_archetypes()
