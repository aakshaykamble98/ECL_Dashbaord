import streamlit as st
from PIL import Image
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.graph_objects as go
from babel.numbers import format_decimal
import os

import Scenario_builder



# Construct the path to the image
image_path = os.path.join(os.path.dirname(__file__), 'Images', 'NIMBUS_logo.png')
image = Image.open(image_path)

#Setting wide layout for streamlit app
st.set_page_config(
    page_title="ECL Dashboard", layout="wide", page_icon=image
)

# #CSS to hide the Streamlit stop button
# hide_st_button = """
#     <style>
#     #MainMenu {visibility: hidden;}
#     footer {visibility: hidden;}
#     header {visibility: hidden;}
#     .stApp > header {visibility: hidden;}
#     </style>
# """
# st.markdown(hide_st_button, unsafe_allow_html=True)

# # Inject custom styles at the beginning of the Streamlit app
# def inject_custom_styles():
#     style = """
#     <style>
#     .stButton button,
#     .stDownloadButton button {
#         border: 1px solid #ccc !important;
#         color: #333 !important;
#         background-color: #f0f0f0 !important;
#         box-shadow: 3px 3px 5px #aaa !important;
#         padding: 0.5em 1em;
#         font-size: 1em;
#         border-radius: 5px;
#         transition: transform 0.1s ease-in-out;
#     }
#     .stButton button:hover,
#     .stDownloadButton button:hover {
#         transform: translateY(-2px);
#         box-shadow: 5px 5px 7px #999 !important;
#     }
#     .stButton button:active,
#     .stDownloadButton button:active {
#         transform: translateY(2px);
#         box-shadow: 1px 1px 2px #bbb !important;
#     }
#     .ppt-download-button,
#     .excel-download-button {
#         display: inline-flex;
#         align-items: center;
#         border: 1px solid #ccc !important;
#         color: #333 !important;
#         background-color: #f0f0f0 !important;
#         box-shadow: 3px 3px 5px #aaa !important;
#         padding: 0.5em 1em;
#         font-size: 1em;
#         border-radius: 5px;
#         transition: transform 0.1s ease-in-out;
#     }
#     .ppt-download-button:hover,
#     .excel-download-button:hover {
#         transform: translateY(-2px);
#         box-shadow: 5px 5px 7px #999 !important;
#     }
#     .ppt-download-button:active,
#     .excel-download-button:active {
#         transform: translateY(2px);
#         box-shadow: 1px 1px 2px #bbb !important;
#     }
#     .ppt-download-button img,
#     .excel-download-button img {
#         margin-left: -0.1em;
#         margin-right: -0.1em;
#         width: 32px;
#         height: 27px;
#     }
#     </style>
#     """
#     st.markdown(style, unsafe_allow_html=True)

# # Inject styles
# inject_custom_styles()


class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        self.apps.append({
            "title": title,
            "function": func
        })

    def run(self):
        with st.sidebar:
            app = option_menu(
                menu_title='ECL - Dashboard',
                options=['ECL Reports',  'Scenario Builder'],
                icons=['clipboard-data', 'graph-down'],
                menu_icon='bank',
                default_index=0,
                styles={
                    "container": {"padding": "20px", "background-color": 'white', "border-radius": "5px", "text-align": "center"},
                    "icon": {"color": "#008080", "font-size": "17px"},
                    "nav-link": {"color": "black", "font-size": "13.5px", "text-align": "left", "margin": "2px", "--hover-color": "#B9DFFE", "font-family": "sans-serif"},
                    "nav-link-selected": {"background-color": "#AFDBF5", "border-radius": "5px"},
                }
            )
            

        if app == "ECL Reports":
            # Centered text in the floating container
            st.markdown(
                """
                <div style='background-color: #008080; border-radius: 5px; padding: 0px;'>
                    <h1 style='text-align: center; font-size: 28px; color: white;'>ECL Reports</h1>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            report_option = st.sidebar.selectbox(
                "Select Report Type",
                ["ECL Dashbaord and Summary", "Staging", "ECL Report: Account wise", "ECL Report: Product wise", "ECL Report: Stage wise", "ECL Report: Stage Migration Report", "ECL Report: Stage wise trend", "ECL Report: Business Segment wise", "ECL Report: Product wise ECL Forecasting", "ECL Report: Bussiness Segment wise ECL Forecasting"]
            )

            # Determine the number of tabs based on the selected report
            if report_option in ["ECL Dashbaord and Summary"]:
                tab1, tab2 = st.tabs(["ECL Dashboard","ECL Summary"])
                with tab2:
                    st.markdown(
                        """
                        <div style='text-align: center;
                        font-size: 20px;'>
                            <strong>ECL Summary Data</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Construct the path to the Excel file
                    excel_path = os.path.join(os.path.dirname(__file__), 'Datasets', 'ECL_Summary.xlsx')
                    ecl_summary = pd.read_excel(excel_path)
                    
                    ecl_summary['LoanAmtLcy'] = ecl_summary['LoanAmtLcy'].astype(float)
                    # Apply formatting to the entire DataFrame using Babel
                    ecl_summary = ecl_summary.applymap(
                        lambda x: format_decimal(x, format='#,##0.00', locale='en_IN').rstrip('0').rstrip('.') 
                        if pd.notnull(x) and isinstance(x, (int, float)) else str(x)
                    )
                    st.dataframe(ecl_summary, width =1200)
                    
                with tab1:
                    st.markdown(
                        """
                        <div style='text-align: center;
                        font-size: 20px;'>
                            <strong>ECL Dashboard</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Function to create 1 Year ECL pie chart
                    def pie_chart_1_year_ecl(df):
                        fig = go.Figure()
                        fig.add_trace(go.Pie(
                            labels=df['Product_Code'],
                            values=df['1 Year ECL'],
                            textinfo='label+percent',
                            marker=dict(
                                colors=['#003366', '#3399FF', '#CCCCCC', '#FF6600']  # Dark Blue, Blue, Gray, Orange
                        
                            ),
                        ))
                        fig.update_layout(
                            title='1 Year ECL Composition',
                            title_x=0.1,
                            title_font=dict(
                                size=15,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.13,  # Move the legend below the chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1,
                                font=dict(
                                size=9,  # Font size for the legend
                                color='black'
                            )
                            ),
                            margin=dict(l=10, r=10, t=80, b=100),
                            showlegend=True,
                            width=600,
                            height=400,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Function to create Lifetime ECL pie chart
                    def pie_chart_lifetime_ecl(df):
                        fig = go.Figure()
                        fig.add_trace(go.Pie(
                            labels=df['Product_Code'],
                            values=df['Lifetime ECL'],
                            textinfo='label+percent',
                            marker=dict(
                                colors=['#003366', '#3399FF', '#CCCCCC', '#FF6600']  # Dark Blue, Blue, Gray, Orange
                            ),
                        ))
                        fig.update_layout(
                            title='Lifetime ECL Composition',
                            title_x=0.3,
                            title_font=dict(
                                size=15,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.13,  # Position the legend closer to the pie chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1,
                                font=dict(
                                size=9,  # Font size for the legend
                                color='black')
                            ),
                            margin=dict(l=60, r=10, t=80, b=100),  # Adjust margins for better spacing
                            showlegend=True,
                            width=600,  # Adjusted width for side-by-side display
                            height=400,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Function to create Stage-wise ECL pie chart with updated styling
                    def pie_chart_stage_wise_ecl(df):
                        fig = go.Figure()
                        fig.add_trace(go.Pie(
                            labels=df['Stage'],
                            values=df['ECL Amount'],
                            textinfo='label+percent',
                            marker=dict(
                                colors=['#003366', '#3399FF', '#CCCCCC'],  # Dark Blue, Blue, Gray
                            ),
                        ))
                        fig.update_layout(
                            title='Stage-wise ECL Composition',
                            title_x=0.3,  # Center the title
                            title_font=dict(
                                size=15,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0.2,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.13,  # Position the legend closer to the chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1,
                                font=dict(
                                size=10,  # Font size for the legend
                                color='black')
                            ),
                            margin=dict(l=60, r=10, t=90, b=100),  # Increase top margin to add space between the title and chart
                            width=600,
                            height=400,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Function to create Stage-wise O/s Balance vs ECL Amount bar chart with updated styling
                    def bar_chart_stage_wise(df):
                        fig = go.Figure()
                    
                        # Adding bars for O/s Balance and ECL Amount
                        fig.add_trace(go.Bar(
                            x=df['Stage'], y=df['O/s Balance'], name='O/s Balance',
                            marker_color='#003366'
                        ))
                        fig.add_trace(go.Bar(
                            x=df['Stage'], y=df['ECL Amount'], name='ECL Amount',
                            marker_color='#3399FF'
                        ))
                    
                        fig.update_layout(
                            title='Stage-wise O/s Balance vs ECL Amount',
                            title_x=0,  # Center the title
                            title_font=dict(
                                size=14,
                                color='black',
                                family='Calibri'
                            ),
                            xaxis_title='Stage',
                            yaxis_title='Amount',
                            legend=dict(
                                orientation='h',
                                x=0.15,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.3,  # Position the legend closer to the chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1,
                                font=dict(
                                size=10,  # Font size for the legend
                                color='black')
                            ),
                            margin=dict(l=10, r=10, t=100, b=80),  # Increase top margin to add space between the title and chart
                            barmode='group',  # Group bars together
                            width=600,
                            height=400,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Function to create pie chart for Business Segment-wise 1 Year ECL
                    def pie_chart_buis_seg_1_year_ecl(df):
                        fig = go.Figure()
                        fig.add_trace(go.Pie(
                            labels=df['Business Segment'],
                            values=df['1 Year ECL'],
                            textinfo='label+percent',
                            marker=dict(
                                colors=['#003366', '#CCCCCC'],  # Blue and Grey
                            ),
                        ))
                        fig.update_layout(
                            title='Business Segment-wise 1 Year ECL Composition',
                            title_x=0.1,  # Center the title
                            title_font=dict(
                                size=13.5,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0.1,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.13,  # Position the legend closer to the pie chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1,
                                font=dict(
                                size=10,  # Font size for the legend
                                color='black')
                            ),
                            margin=dict(l=10, r=10, t=100, b=80),  # Adjust margins for better spacing
                            showlegend=True,
                            width=600,  # Adjusted width for side-by-side display
                            height=400,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Function to create pie chart for Business Segment-wise Lifetime ECL
                    def pie_chart_buis_seg_lifetime_ecl(df):
                        fig = go.Figure()
                        fig.add_trace(go.Pie(
                            labels=df['Business Segment'],
                            values=df['Lifetime ECL'],
                            textinfo='label+percent',
                            marker=dict(
                                colors=['#003366', '#CCCCCC'],  # Blue and Grey
                            ),
                        ))
                        fig.update_layout(
                            title='Business Segment-wise Lifetime ECL Composition',
                            title_x=0.1,  # Center the title
                            title_font=dict(
                                size=13.5,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0.10,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.13,  # Position the legend closer to the pie chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1,
                                font=dict(
                                size=10,  # Font size for the legend
                                color='black')
                            ),
                            margin=dict(l=10, r=10, t=100, b=80),  # Adjust margins for better spacing
                            showlegend=True,
                            width=600,  # Adjusted width for side-by-side display
                            height=400,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Function to create Business Segment-wise ECL Comparison bar chart
                    def bar_chart_buis_comp_ecl(df):
                        # Melt the dataframe to have a long format suitable for plotting
                        df_melted = df.melt(id_vars='Business Segment', value_vars=['O/s Balance', '1 Year ECL', 'Lifetime ECL'], 
                                            var_name='ECL Category', value_name='Amount')
                        
                        fig = go.Figure()
                        
                        # Custom colors for each Business Segment
                        colors = {
                            'Retail Banking': '#003366',  # Dark Blue
                            'Corporate Banking': '#ED7013',  # orange
                        }
                    
                        # Adding bars for each Business Segment
                        for segment in df['Business Segment'].unique():
                            df_segment = df_melted[df_melted['Business Segment'] == segment]
                            fig.add_trace(go.Bar(
                                x=df_segment['ECL Category'],
                                y=df_segment['Amount'],
                                name=segment,
                                marker_color=colors.get(segment, '#000000')  # Use custom color or default to black if not specified
                            ))
                    
                        fig.update_layout(
                            title='Business Segment-wise ECL Comparison',
                            title_x=0.12,  # Center the title
                            title_font=dict(
                                size=14,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0.15,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.25,  # Position the legend closer to the chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1,
                                font=dict(
                                size=10,  # Font size for the legend
                                color='black')
                            ),
                            margin=dict(l=10, r=10, t=90, b=80),  # Increase top margin to add space between the title and chart
                            xaxis_title='ECL Category',
                            yaxis_title='Amount',
                            barmode='group',  # Group bars for each category
                            width=600,
                            height=450,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Function to create Product-wise ECL Forecast bar chart
                    def bar_chart_product_forecast(df):
                        fig = go.Figure()
                    
                        # Adding bars for each ECL category
                        fig.add_trace(go.Bar(
                            x=df['Product_Code'], y=df['1 Year ECL'], name='1 Year ECL',
                            marker_color='#210BC7'
                        ))
                        fig.add_trace(go.Bar(
                            x=df['Product_Code'], y=df['2 Year ECL'], name='2 Year ECL',
                            marker_color='#ED7013' 
                        ))
                        fig.add_trace(go.Bar(
                            x=df['Product_Code'], y=df['3 Year ECL'], name='3 Year ECL',
                            marker_color='#CCCCCC'
                        ))
                        fig.add_trace(go.Bar(
                            x=df['Product_Code'], y=df['Lifetime ECL'], name='Lifetime ECL',
                            marker_color='#F4B720'
                        ))
                    
                        fig.update_layout(
                            title='Product-wise ECL Forecast',
                            title_x=0.25,  # Center the title
                            title_font=dict(
                                size=14,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0.2,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.37,  # Position the legend closer to the chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1,
                                font=dict(
                                size=10,  # Font size for the legend
                                color='black')
                            ),
                            margin=dict(l=10, r=10, t=90, b=80),  # Increased top margin to add space between the title and chart
                            xaxis_title='Product Code',
                            yaxis_title='ECL Amount',
                            barmode='group',
                            width=600,
                            height=500,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Function to create Business Segment-wise ECL Forecast bar chart
                    def bar_chart_buiswise_forecast(df):
                        fig = go.Figure()
                    
                        # Adding bars for each Business Segment
                        fig.add_trace(go.Bar(
                            x=['1 Year ECL', '2 Year ECL', '3 Year ECL', 'Lifetime ECL'], 
                            y=df.loc[df['Business Segment'] == 'Retail Banking'].iloc[0, 2:], 
                            name='Retail Banking',
                            marker_color='#003366'
                        ))
                        fig.add_trace(go.Bar(
                            x=['1 Year ECL', '2 Year ECL', '3 Year ECL', 'Lifetime ECL'], 
                            y=df.loc[df['Business Segment'] == 'Corporate Banking'].iloc[0, 2:], 
                            name='Corporate Banking',
                            marker_color='#ED7013'
                        ))
                    
                        fig.update_layout(
                            title='Business Segment-wise ECL Forecast',
                            title_x=0.25,  # Center the title
                            title_font=dict(
                                size=14,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0.2,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.3,  # Position the legend closer to the chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1,
                                font=dict(
                                size=10,  # Font size for the legend
                                color='black')
                            ),
                            margin=dict(l=10, r=10, t=90, b=80),  # Increased top margin to add space between the title and chart
                            xaxis_title='ECL Type',
                            yaxis_title='ECL Amount',
                            barmode='group',
                            width=600,
                            height=485,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Base directory of the current script
                    base_dir = os.path.dirname(__file__)
                    
                    # Construct paths for each dataset and load them into DataFrames
                    df_buiswise_forecast = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Bussiness_Segment_wise_ECL_Forecasting.xlsx"))
                    
                    df_forecast = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Product_wise_ECL_Forecasting.xlsx"))
                    
                    df_seg = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Business_Segment_wise.xlsx"))
                    
                    df_stage_ecl = pd.read_excel(os.path.join(base_dir, "Datasets", "Stage_wise_ecl_com.xlsx"))
                    
                    df = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Product_wise.xlsx"))
                        
                    # Create two columns for side-by-side charts
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        fig1 = pie_chart_1_year_ecl(df)
                        st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        fig2 = pie_chart_lifetime_ecl(df)
                        st.plotly_chart(fig2, use_container_width=True)
                        
                    with col3:
                        fig3 = pie_chart_stage_wise_ecl(df_stage_ecl)
                        st.plotly_chart(fig3, use_container_width=True)
                        
                    with col1:
                        fig4 = bar_chart_stage_wise(df_stage_ecl)
                        st.plotly_chart(fig4, use_container_width=True)
                        
                    with col2:
                        fig5 = pie_chart_buis_seg_1_year_ecl(df_seg)
                        st.plotly_chart(fig5, use_container_width=True)
                    
                    with col3:
                        fig6 = pie_chart_buis_seg_lifetime_ecl(df_seg)
                        st.plotly_chart(fig6, use_container_width=True)
                    
                    with col1:
                        fig7 = bar_chart_buis_comp_ecl(df_seg)
                        st.plotly_chart(fig7, use_container_width=True)
                        
                    with col2:
                        fig8 = bar_chart_product_forecast(df_forecast)
                        st.plotly_chart(fig8, use_container_width=True)
                        
                    with col3:
                        fig9 = bar_chart_buiswise_forecast(df_buiswise_forecast)
                        st.plotly_chart(fig9, use_container_width=True)
                    
            elif report_option in ["Staging"]:
                tab1 = st.tabs(["Data"])[0]
                with tab1:
                    st.markdown(
                        """
                        <div style='text-align: center;
                        font-size: 20px;'>
                            <strong>Staging Data</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    base_dir = os.path.dirname(__file__)
                    staging_table = pd.read_excel(os.path.join(base_dir, "Datasets", "Staging_table.xlsx"))
                    # Ensure that the columns is in datetime format
                    staging_table['Origination_Date'] = pd.to_datetime(staging_table['Origination_Date'])
                    staging_table['Last_Run_Date'] = pd.to_datetime(staging_table['Last_Run_Date'])
                    staging_table['Current_Run_Date'] = pd.to_datetime(staging_table['Current_Run_Date'])
                    
                    # Format the 'Percentage' column to show as percentage with a '%' sign
                    staging_table['PD_at_Origination'] = staging_table['PD_at_Origination'].apply(lambda x: "{:.2%}".format(x))
                    staging_table['PD_at_Last_Run'] = staging_table['PD_at_Last_Run'].apply(lambda x: "{:.2%}".format(x))
                    staging_table['PD_at_Current_Run'] = staging_table['PD_at_Current_Run'].apply(lambda x: "{:.2%}".format(x))
                   
                   
                    # Convert the  columns to string format to remove the time component
                    staging_table['Origination_Date'] = staging_table['Origination_Date'].dt.strftime('%d-%m-%Y')
                    staging_table['Last_Run_Date'] = staging_table['Last_Run_Date'].dt.strftime('%d-%m-%Y')
                    staging_table['Current_Run_Date'] = staging_table['Current_Run_Date'].dt.strftime('%d-%m-%Y')
                    
                    staging_table['Loan_Amt'] = staging_table['Loan_Amt'].astype(float)
                    
                    # Apply formatting to the entire DataFrame
                    # Apply formatting to the entire DataFrame using Babel
                    staging_table = staging_table.applymap(
                        lambda x: format_decimal(x, format='#,##0.00', locale='en_IN').rstrip('0').rstrip('.') 
                        if pd.notnull(x) and isinstance(x, (int, float)) else str(x)
                    )
                                
                    st.dataframe(staging_table, width = 1200)
            
            elif report_option in ["ECL Report: Account wise"]:
                tab1 = st.tabs(["Report"])[0]
                with tab1:
                    st.markdown(
                        """
                        <div style='text-align: center;
                        font-size: 20px;'>
                            <strong>ECL Report: Account wise</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    base_dir = os.path.dirname(__file__)
                    account_wise_ecl = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Account_wise.xlsx"))
                    # Apply formatting to the entire DataFrame using Babel
                    account_wise_ecl = account_wise_ecl.applymap(
                        lambda x: format_decimal(x, format='#,##0.00', locale='en_IN').rstrip('0').rstrip('.') 
                        if pd.notnull(x) and isinstance(x, (int, float)) else str(x)
                    )
                    st.dataframe(account_wise_ecl, width = 1200)
                    
            elif report_option in ["ECL Report: Product wise"]:
                tab1, tab2 = st.tabs(["Report", "Graphs"])
                with tab1:
                    st.markdown(
                        """
                        <div style='text-align: center;
                        font-size: 20px;'>
                            <strong>ECL Report: Product wise</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    base_dir = os.path.dirname(__file__)
                    product_wise_ecl = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Product_wise.xlsx"))
                    product_wise_ecl = product_wise_ecl.fillna("")
                    
                    product_wise_ecl['1 Year ECL (% of Business Segment)'] = pd.to_numeric(product_wise_ecl['1 Year ECL (% of Business Segment)'], errors='coerce')
                    product_wise_ecl['Lifetime ECL (% of Business Segment)'] = pd.to_numeric(product_wise_ecl['Lifetime ECL (% of Business Segment)'], errors='coerce')
                    
                    # Format the 'Percentage' column to show as percentage with a '%' sign
                    product_wise_ecl['1 Year ECL (% of Business Segment)'] = product_wise_ecl['1 Year ECL (% of Business Segment)'].apply(lambda x: "{:.2%}".format(x) if pd.notnull(x) else "")
                    product_wise_ecl['Lifetime ECL (% of Business Segment)'] = product_wise_ecl['Lifetime ECL (% of Business Segment)'].apply(lambda x: "{:.2%}".format(x) if pd.notnull(x) else "")
                    
                    # Apply formatting to the entire DataFrame
                    product_wise_ecl = product_wise_ecl.applymap(
                        lambda x: format_decimal(x, format='#,##0.00', locale='en_IN').rstrip('0').rstrip('.') 
                        if pd.notnull(x) and isinstance(x, (int, float)) else str(x)
                    )
                    st.dataframe(product_wise_ecl, width = 1200)
                    
                with tab2:
                    # Function to create 1 Year ECL pie chart
                    def pie_chart_1_year_ecl(df):
                        fig = go.Figure()
                        fig.add_trace(go.Pie(
                            labels=df['Product_Code'],
                            values=df['1 Year ECL'],
                            textinfo='label+percent',
                            marker=dict(
                                colors=['#003366', '#3399FF', '#CCCCCC', '#FF6600']  # Dark Blue, Blue, Gray, Orange
                        
                            ),
                        ))
                        fig.update_layout(
                            title='1 Year ECL Composition',
                            title_x=0.35,
                            title_font=dict(
                                size=17,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.13,  # Move the legend below the chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1
                            ),
                            margin=dict(l=60, r=10, t=40, b=100),
                            showlegend=True,
                            width=600,
                            height=500,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Function to create Lifetime ECL pie chart
                    def pie_chart_lifetime_ecl(df):
                        fig = go.Figure()
                        fig.add_trace(go.Pie(
                            labels=df['Product_Code'],
                            values=df['Lifetime ECL'],
                            textinfo='label+percent',
                            marker=dict(
                                colors=['#003366', '#3399FF', '#CCCCCC', '#FF6600']  # Dark Blue, Blue, Gray, Orange
                            ),
                        ))
                        fig.update_layout(
                            title='Lifetime ECL Composition',
                            title_x=0.35,
                            title_font=dict(
                                size=17,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.13,  # Position the legend closer to the pie chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1
                            ),
                            margin=dict(l=60, r=10, t=40, b=100),  # Adjust margins for better spacing
                            showlegend=True,
                            width=600,  # Adjusted width for side-by-side display
                            height=500,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Assuming 'Datasets/ECL_Report_Product_wise.xlsx' is your file
                    base_dir = os.path.dirname(__file__)
                    df = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Product_wise.xlsx"))
                        
                        
                    # Create two columns for side-by-side charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig1 = pie_chart_1_year_ecl(df)
                        st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        fig2 = pie_chart_lifetime_ecl(df)
                        st.plotly_chart(fig2, use_container_width=True)
 
                
            elif report_option in ["ECL Report: Stage wise"]:
                tab1, tab2 = st.tabs(["Report", "Graphs"])
                with tab1:
                    st.markdown(
                        """
                        <div style='text-align: center;
                        font-size: 20px;'>
                            <strong>ECL Report: Stage wise</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    base_dir = os.path.dirname(__file__)
                    stage_wise_ecl = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Stage_wise.xlsx"))
                    
                    # Format the 'Percentage' column to show as percentage with a '%' sign
                    stage_wise_ecl = stage_wise_ecl.fillna("")
                    
                    # Convert percentage columns to numeric (float)
                    stage_wise_ecl['1 Year ECL (% of Total Assets)'] = pd.to_numeric(stage_wise_ecl['1 Year ECL (% of Total Assets)'], errors='coerce')
                    stage_wise_ecl['Lifetime ECL (% of Stage)'] = pd.to_numeric(stage_wise_ecl['Lifetime ECL (% of Stage)'], errors='coerce')


                    stage_wise_ecl['1 Year ECL (% of Total Assets)']  = stage_wise_ecl['1 Year ECL (% of Total Assets)'].apply(lambda x: "{:.2%}".format(x) if pd.notnull(x) else "")
                    stage_wise_ecl['Lifetime ECL (% of Stage)'] = stage_wise_ecl['Lifetime ECL (% of Stage)'].apply(lambda x: "{:.2%}".format(x) if pd.notnull(x) else "")
                    
                    
                    # Formatting the column
                    # Apply formatting to the entire DataFrame
                    stage_wise_ecl = stage_wise_ecl.applymap(
                        lambda x: format_decimal(x, format='#,##0.00', locale='en_IN').rstrip('0').rstrip('.') 
                        if pd.notnull(x) and isinstance(x, (int, float)) else str(x)
                    )
                   
                    st.dataframe(stage_wise_ecl, width = 1200)
                
                with tab2: 
                    st.write("Graphs")
                    # Function to create Stage-wise ECL pie chart with updated styling
                    def pie_chart_stage_wise_ecl(df):
                        fig = go.Figure()
                        fig.add_trace(go.Pie(
                            labels=df['Stage'],
                            values=df['ECL Amount'],
                            textinfo='label+percent',
                            marker=dict(
                                colors=['#003366', '#3399FF', '#CCCCCC'],  # Dark Blue, Blue, Gray
                            ),
                        ))
                        fig.update_layout(
                            title='Stage-wise ECL Composition',
                            title_x=0.3,  # Center the title
                            title_font=dict(
                                size=17,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0.17,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.2,  # Position the legend closer to the chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1
                            ),
                            margin=dict(l=80, r=10, t=80, b=80),  # Increase top margin to add space between the title and chart
                            width=800,
                            height=500,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Function to create Stage-wise O/s Balance vs ECL Amount bar chart with updated styling
                    def bar_chart_stage_wise(df):
                        fig = go.Figure()
                    
                        # Adding bars for O/s Balance and ECL Amount
                        fig.add_trace(go.Bar(
                            x=df['Stage'], y=df['O/s Balance'], name='O/s Balance',
                            marker_color='#003366'
                        ))
                        fig.add_trace(go.Bar(
                            x=df['Stage'], y=df['ECL Amount'], name='ECL Amount',
                            marker_color='#3399FF'
                        ))
                    
                        fig.update_layout(
                            title='Stage-wise O/s Balance vs ECL Amount',
                            title_x=0.2,  # Center the title
                            title_font=dict(
                                size=17,
                                color='black',
                                family='Calibri'
                            ),
                            xaxis_title='Stage',
                            yaxis_title='Amount',
                            legend=dict(
                                orientation='h',
                                x=0.1,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.2,  # Position the legend closer to the chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1
                            ),
                            margin=dict(l=10, r=10, t=100, b=80),  # Increase top margin to add space between the title and chart
                            barmode='group',  # Group bars together
                            width=800,
                            height=500,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    base_dir = os.path.dirname(__file__)
                    df_stage_ecl = pd.read_excel(os.path.join(base_dir, "Datasets", "Stage_wise_ecl_com.xlsx"))
                    
                    # Create two columns for side-by-side charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig1 = bar_chart_stage_wise(df_stage_ecl)
                        st.plotly_chart(fig1, use_container_width=True)
                    
                    with col2:
                        fig2 = pie_chart_stage_wise_ecl(df_stage_ecl)
                        st.plotly_chart(fig2, use_container_width=True)
                    
                    
            elif report_option in ["ECL Report: Stage Migration Report"]:
                tab1 = st.tabs(["Report"])[0]
                with tab1:
                    st.markdown(
                        """
                        <div style='text-align: center;
                        font-size: 20px;'>
                            <strong>ECL Report: Stage Migration Report</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    base_dir = os.path.dirname(__file__)
                    stage_migration = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Stage_Migration_Report.xlsx"))
                            
                    # Function to format the columns
                    def format_column(column):
                        # Save the first element and keep it as is
                        first_element = column.iloc[0]
                        # Convert the rest of the column to numeric
                        column.iloc[1:] = pd.to_numeric(column.iloc[1:], errors='coerce')
                        # Reinsert the first element back into the column
                        column.iloc[0] = first_element
            
                        # Format only the numeric values and keep the first element unchanged
                        return column.apply(lambda x: "{:.2%}".format(x) if pd.notnull(x) and isinstance(x, (int, float)) else x)
            
                    # Format the specific columns
                    stage_migration['O/s  Balance.'] = format_column(stage_migration['O/s  Balance.'])
                    stage_migration['1 Year ECL.'] = format_column(stage_migration['1 Year ECL.'])
                    stage_migration['Lifetime ECL.'] = format_column(stage_migration['Lifetime ECL.'])
                    
                    stage_migration['O/s Balance'].iloc[0] = stage_migration['O/s Balance'].iloc[0].strftime('%d-%m-%Y')
                    stage_migration['O/s  Balance'].iloc[0] = stage_migration['O/s  Balance'].iloc[0].strftime('%d-%m-%Y')
                    stage_migration['1 Year ECL'].iloc[0] = stage_migration['1 Year ECL'].iloc[0].strftime('%d-%m-%Y')
                    stage_migration['1  Year ECL'].iloc[0] = stage_migration['1  Year ECL'].iloc[0].strftime('%d-%m-%Y')
                    stage_migration['Lifetime ECL'].iloc[0] = stage_migration['Lifetime ECL'].iloc[0].strftime('%d-%m-%Y')
                    stage_migration[' Lifetime ECL'].iloc[0] = stage_migration[' Lifetime ECL'].iloc[0].strftime('%d-%m-%Y')
                    
                    stage_migration = stage_migration.fillna("")

                    
                    # Apply formatting to the entire DataFrame
                    stage_migration = stage_migration.applymap(
                        lambda x: format_decimal(x, format='#,##0.00', locale='en_IN').rstrip('0').rstrip('.') 
                        if pd.notnull(x) and isinstance(x, (int, float)) else str(x)
                    )
            
                    # Display the dataframe
                    st.dataframe(stage_migration, width=1200)
                    
                    
            elif report_option in ["ECL Report: Stage wise trend"]:
                tab1 = st.tabs(["Report"])[0]
                with tab1:
                    st.markdown(
                        """
                        <div style='text-align: center;
                        font-size: 20px;'>
                            <strong>ECL Report: Stage wise trend</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    base_dir = os.path.dirname(__file__)
                    stage_wise_trend = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Stage_wise_trend.xlsx"))
                    
                    stage_wise_trend['Run_Date'] = stage_wise_trend['Run_Date'].dt.strftime('%d-%m-%Y')
                    
                    # Apply formatting to the fourth element (index 3) of the 'Lifetime ECL (% of Business Segment)' column
                    stage_wise_trend['Stage 1.'].iloc[3] = "{:.2%}".format(stage_wise_trend['Stage 1.'].iloc[3])
                    stage_wise_trend['Stage 3.'].iloc[3] = "{:.2%}".format(stage_wise_trend['Stage 3.'].iloc[3])
                    
                    stage_wise_trend = stage_wise_trend.fillna('')
                    
                    # Apply formatting to the entire DataFrame
                    stage_wise_trend = stage_wise_trend.applymap(
                        lambda x: format_decimal(x, format='#,##0.00', locale='en_IN').rstrip('0').rstrip('.') 
                        if pd.notnull(x) and isinstance(x, (int, float)) else str(x)
                    )

                    st.dataframe(stage_wise_trend, width = 1200)
            
            elif report_option in ["ECL Report: Business Segment wise"]:
                tab1, tab2 = st.tabs(["Report", "Graphs"])
                with tab1:
                    st.markdown(
                        """
                        <div style='text-align: center;
                        font-size: 20px;'>
                            <strong>ECL Report: Business Segment wise</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    base_dir = os.path.dirname(__file__)
                    bussines_seg = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Business_Segment_wise.xlsx"))
                    
                    bussines_seg['1 Year ECL (% of BS)'] = bussines_seg['1 Year ECL (% of BS)'].apply(lambda x: "{:.2%}".format(x))
                    bussines_seg['Lifetime ECL (% of BS)'] = bussines_seg['Lifetime ECL (% of BS)'].apply(lambda x: "{:.2%}".format(x))
                    
                    # Formatting the column
                    # Apply formatting to the entire DataFrame
                    bussines_seg = bussines_seg.applymap(
                        lambda x: format_decimal(x, format='#,##0.00', locale='en_IN').rstrip('0').rstrip('.') 
                        if pd.notnull(x) and isinstance(x, (int, float)) else str(x)
                    )

                    st.dataframe(bussines_seg, width = 1200)
                
                with tab2:
                    # Function to create pie chart for Business Segment-wise 1 Year ECL
                    def pie_chart_buis_seg_1_year_ecl(df):
                        fig = go.Figure()
                        fig.add_trace(go.Pie(
                            labels=df['Business Segment'],
                            values=df['1 Year ECL'],
                            textinfo='label+percent',
                            marker=dict(
                                colors=['#003366', '#CCCCCC'],  # Blue and Grey
                            ),
                        ))
                        fig.update_layout(
                            title='Business Segment-wise 1 Year ECL Composition',
                            title_x=0.20,  # Center the title
                            title_font=dict(
                                size=17,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0.18,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.05,  # Position the legend closer to the pie chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1
                            ),
                            margin=dict(l=60, r=10, t=80, b=80),  # Adjust margins for better spacing
                            showlegend=True,
                            width=600,  # Adjusted width for side-by-side display
                            height=500,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Function to create pie chart for Business Segment-wise Lifetime ECL
                    def pie_chart_buis_seg_lifetime_ecl(df):
                        fig = go.Figure()
                        fig.add_trace(go.Pie(
                            labels=df['Business Segment'],
                            values=df['Lifetime ECL'],
                            textinfo='label+percent',
                            marker=dict(
                                colors=['#003366', '#CCCCCC'],  # Blue and Grey
                            ),
                        ))
                        fig.update_layout(
                            title='Business Segment-wise Lifetime ECL Composition',
                            title_x=0.17,  # Center the title
                            title_font=dict(
                                size=17,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0.19,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.05,  # Position the legend closer to the pie chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1
                            ),
                            margin=dict(l=60, r=10, t=80, b=80),  # Adjust margins for better spacing
                            showlegend=True,
                            width=600,  # Adjusted width for side-by-side display
                            height=500,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Assuming 'Datasets/ECL_Report_Product_wise.xlsx' is your file
                    base_dir = os.path.dirname(__file__)
                    df_seg = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Business_Segment_wise.xlsx"))
                                            
                        
                    # Create two columns for side-by-side charts
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig3 = pie_chart_buis_seg_1_year_ecl(df_seg)
                        st.plotly_chart(fig3, use_container_width=True)
                    
                    with col2:
                        fig4 = pie_chart_buis_seg_lifetime_ecl(df_seg)
                        st.plotly_chart(fig4, use_container_width=True)
                        
                    # Function to create Business Segment-wise ECL Comparison bar chart
                    def bar_chart_buis_comp_ecl(df):
                        # Melt the dataframe to have a long format suitable for plotting
                        df_melted = df.melt(id_vars='Business Segment', value_vars=['O/s Balance', '1 Year ECL', 'Lifetime ECL'], 
                                            var_name='ECL Category', value_name='Amount')
                        
                        fig = go.Figure()
                        
                        # Custom colors for each Business Segment
                        colors = {
                            'Retail Banking': '#003366',  # Dark Blue
                            'Corporate Banking': '#ED7013',  # orange
                        }
                    
                        # Adding bars for each Business Segment
                        for segment in df['Business Segment'].unique():
                            df_segment = df_melted[df_melted['Business Segment'] == segment]
                            fig.add_trace(go.Bar(
                                x=df_segment['ECL Category'],
                                y=df_segment['Amount'],
                                name=segment,
                                marker_color=colors.get(segment, '#000000')  # Use custom color or default to black if not specified
                            ))
                    
                        fig.update_layout(
                            title='Business Segment-wise ECL Comparison',
                            title_x=0.3,  # Center the title
                            title_font=dict(
                                size=17,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0.3,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.2,  # Position the legend closer to the chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1
                            ),
                            margin=dict(l=10, r=10, t=80, b=80),  # Increase top margin to add space between the title and chart
                            xaxis_title='ECL Category',
                            yaxis_title='Amount',
                            barmode='group',  # Group bars for each category
                            width=800,
                            height=500,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    # Assuming 'Datasets/ECL_Report_Product_wise.xlsx' is your file
                    base_dir = os.path.dirname(__file__)
                    df_seg = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Business_Segment_wise.xlsx"))
                                         
                    fig6 = bar_chart_buis_comp_ecl(df_seg)
                    st.plotly_chart(fig6)
                    
                            
                
            elif report_option in ["ECL Report: Product wise ECL Forecasting"]:
                tab1, tab2 = st.tabs(["Report", "Graphs"])
                with tab1:
                    st.markdown(
                        """
                        <div style='text-align: center;
                        font-size: 20px;'>
                            <strong>ECL Report: Product wise ECL Forecasting</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    base_dir = os.path.dirname(__file__)
                    product_forecast = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Product_wise_ECL_Forecasting.xlsx"))
                                         
                    # Apply formatting to the entire DataFrame
                    product_forecast = product_forecast.applymap(
                        lambda x: format_decimal(x, format='#,##0.00', locale='en_IN').rstrip('0').rstrip('.') 
                        if pd.notnull(x) and isinstance(x, (int, float)) else str(x)
                    )

                    st.dataframe(product_forecast, width = 1200)
                
                with tab2:
                    # Function to create Product-wise ECL Forecast bar chart
                    def bar_chart_product_forecast(df):
                        fig = go.Figure()
                    
                        # Adding bars for each ECL category
                        fig.add_trace(go.Bar(
                            x=df['Product_Code'], y=df['1 Year ECL'], name='1 Year ECL',
                            marker_color='#210BC7'
                        ))
                        fig.add_trace(go.Bar(
                            x=df['Product_Code'], y=df['2 Year ECL'], name='2 Year ECL',
                            marker_color='#ED7013' 
                        ))
                        fig.add_trace(go.Bar(
                            x=df['Product_Code'], y=df['3 Year ECL'], name='3 Year ECL',
                            marker_color='#CCCCCC'
                        ))
                        fig.add_trace(go.Bar(
                            x=df['Product_Code'], y=df['Lifetime ECL'], name='Lifetime ECL',
                            marker_color='#F4B720'
                        ))
                    
                        fig.update_layout(
                            title='Product-wise ECL Forecast',
                            title_x=0.4,  # Center the title
                            title_font=dict(
                                size=17,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0.3,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.2,  # Position the legend closer to the chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1
                            ),
                            margin=dict(l=10, r=10, t=60, b=80),  # Increased top margin to add space between the title and chart
                            xaxis_title='Product Code',
                            yaxis_title='ECL Amount',
                            barmode='group',
                            width=800,
                            height=500,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    base_dir = os.path.dirname(__file__)
                    df_forecast = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Product_wise_ECL_Forecasting.xlsx"))
                                         
                    fig5 = bar_chart_product_forecast(df_forecast)
                    st.plotly_chart(fig5)
            
            
            elif report_option in ["ECL Report: Bussiness Segment wise ECL Forecasting"]:
                tab1, tab2 = st.tabs(["Report", "Graphs"])
                with tab1:
                    st.markdown(
                        """
                        <div style='text-align: center;
                        font-size: 20px;'>
                            <strong>ECL Report: Bussiness Segment wise ECL Forecasting</strong>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    base_dir = os.path.dirname(__file__)
                    bussiness_forecast = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Bussiness_Segment_wise_ECL_Forecasting.xlsx"))
                                         
                    # Apply formatting to the entire DataFrame
                    bussiness_forecast = bussiness_forecast.applymap(
                        lambda x: format_decimal(x, format='#,##0.00', locale='en_IN').rstrip('0').rstrip('.') 
                        if pd.notnull(x) and isinstance(x, (int, float)) else str(x)
                    )

                    st.dataframe(bussiness_forecast, width = 1200)
                
                with tab2:
                    # Function to create Business Segment-wise ECL Forecast bar chart
                    def bar_chart_buiswise_forecast(df):
                        fig = go.Figure()
                    
                        # Adding bars for each Business Segment
                        fig.add_trace(go.Bar(
                            x=['1 Year ECL', '2 Year ECL', '3 Year ECL', 'Lifetime ECL'], 
                            y=df.loc[df['Business Segment'] == 'Retail Banking'].iloc[0, 2:], 
                            name='Retail Banking',
                            marker_color='#003366'
                        ))
                        fig.add_trace(go.Bar(
                            x=['1 Year ECL', '2 Year ECL', '3 Year ECL', 'Lifetime ECL'], 
                            y=df.loc[df['Business Segment'] == 'Corporate Banking'].iloc[0, 2:], 
                            name='Corporate Banking',
                            marker_color='#ED7013'
                        ))
                    
                        fig.update_layout(
                            title='Business Segment-wise ECL Forecast',
                            title_x=0.35,  # Center the title
                            title_font=dict(
                                size=17,
                                color='black',
                                family='Calibri'
                            ),
                            legend=dict(
                                orientation='h',
                                x=0.3,  # Align the legend to the left edge
                                xanchor='left',  # Align the legend to the left edge of the chart
                                y=-0.2,  # Position the legend closer to the chart
                                traceorder='normal',  # Ensure the items are in the same order as the traces
                                bordercolor='black', borderwidth=1
                            ),
                            margin=dict(l=10, r=10, t=80, b=80),  # Increased top margin to add space between the title and chart
                            xaxis_title='ECL Type',
                            yaxis_title='ECL Amount',
                            barmode='group',
                            width=800,
                            height=500,
                            paper_bgcolor='white',  # Background color of the chart
                            plot_bgcolor='white',  # Background color of the plot area
                        )
                        return fig
                    
                    base_dir = os.path.dirname(__file__)
                    df_buiswise_forecast = pd.read_excel(os.path.join(base_dir, "Datasets", "ECL_Report_Bussiness_Segment_wise_ECL_Forecasting.xlsx"))
                                         
                    fig6 = bar_chart_buiswise_forecast(df_buiswise_forecast)
                    st.plotly_chart(fig6)
        
        else:
            selected_app = next((a for a in self.apps if a["title"] == app), None)
            if selected_app:
                selected_app["function"].app()


if __name__ == "__main__":
    multi_app = MultiApp()
    
    multi_app.add_app("Scenario Builder", Scenario_builder)
    # multi_app.add_app("Scenarion wise ECL Reports", Scenario_ECL_Reports)

    multi_app.run()
