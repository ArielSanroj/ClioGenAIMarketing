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

def render_consumer_archetypes():
    """Render the consumer archetypes display"""
    st.markdown("## Consumer Archetypes Analysis")
    
    # Load data
    archetypes_df, subscales_df = load_archetype_data()
    
    if archetypes_df is None or subscales_df is None:
        st.warning("Unable to load archetype data. Please check the Excel files.")
        return
    
    # Display archetypes overview
    st.subheader("Consumer Archetypes Overview")
    
    # Create tabs for different views
    tabs = st.tabs(["Archetypes", "Subscales", "Comparison"])
    
    with tabs[0]:
        # Archetypes visualization
        if 'Score' in archetypes_df.columns:
            fig = px.bar(archetypes_df, 
                        x='Archetype', 
                        y='Score',
                        title='Consumer Archetypes Distribution',
                        color='Score',
                        color_continuous_scale='Viridis')
            st.plotly_chart(fig, use_container_width=True)
        
        # Display archetype details in expandable sections
        for idx, row in archetypes_df.iterrows():
            with st.expander(f"📊 {row['Archetype']}"):
                st.markdown(f"**Description:** {row.get('Description', 'N/A')}")
                st.markdown(f"**Key Characteristics:**")
                characteristics = row.get('Characteristics', '').split(',')
                for char in characteristics:
                    if char.strip():
                        st.markdown(f"- {char.strip()}")
    
    with tabs[1]:
        # Subscales visualization
        if 'Value' in subscales_df.columns:
            fig = px.sunburst(subscales_df,
                            path=['Category', 'Subscale'],
                            values='Value',
                            title='Consumer Subscales Breakdown')
            st.plotly_chart(fig, use_container_width=True)
        
        # Display subscales details
        for category in subscales_df['Category'].unique():
            with st.expander(f"📈 {category}"):
                category_data = subscales_df[subscales_df['Category'] == category]
                for _, row in category_data.iterrows():
                    st.markdown(f"**{row['Subscale']}**")
                    st.markdown(f"Value: {row['Value']}")
                    if 'Description' in row:
                        st.markdown(f"_{row['Description']}_")
    
    with tabs[2]:
        # Create correlation matrix if applicable
        if 'Score' in archetypes_df.columns and 'Value' in subscales_df.columns:
            st.subheader("Archetype-Subscale Correlation")
            
            # Example correlation visualization
            fig = go.Figure(data=go.Heatmap(
                z=[[1, 0.8, 0.6], [0.8, 1, 0.7], [0.6, 0.7, 1]],  # Example correlation values
                x=['Archetype 1', 'Archetype 2', 'Archetype 3'],
                y=['Subscale 1', 'Subscale 2', 'Subscale 3'],
                colorscale='Viridis'
            ))
            fig.update_layout(title='Correlation Matrix')
            st.plotly_chart(fig, use_container_width=True)
    
    # Export functionality
    st.markdown("### Export Data")
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Export Archetypes"):
            # Convert DataFrame to CSV string
            csv = archetypes_df.to_csv(index=False)
            st.download_button(
                label="Download Archetypes CSV",
                data=csv,
                file_name="consumer_archetypes.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("Export Subscales"):
            # Convert DataFrame to CSV string
            csv = subscales_df.to_csv(index=False)
            st.download_button(
                label="Download Subscales CSV",
                data=subscales_df.to_csv(index=False),
                file_name="consumer_subscales.csv",
                mime="text/csv"
            )

if __name__ == "__main__":
    render_consumer_archetypes()
