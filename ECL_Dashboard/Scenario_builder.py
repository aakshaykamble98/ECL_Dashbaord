import streamlit as st
import pandas as pd
from babel.numbers import format_decimal
import os

# Streamlit app
def app():
    st.markdown(
        """
        <div style='background-color: #008080; border-radius: 5px; padding: 0px;'>
            <h1 style='text-align: center; font-size: 28px; color: white;'>Scenario Builder</h1>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Tabs for options
    tab1, tab2, tab3 = st.tabs(["Scenario Builder", "ECL Weighted", "Account Wise Scenario Report"])
    
    with tab1:
        st.markdown(
            """
            <div style='text-align: center;
            font-size: 20px;'>
                <strong>Scenario Probability Table</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        base_dir = os.path.dirname(__file__)
        Scenario_Probability = pd.read_excel(os.path.join(base_dir, "Datasets", "Scenario_Probability.xlsx"))
                           
        Scenario_Probability['BaseCase'] = Scenario_Probability['BaseCase'].apply(lambda x: "{:.2%}".format(x))
        Scenario_Probability['Optimistic'] = Scenario_Probability['Optimistic'].apply(lambda x: "{:.2%}".format(x))
        Scenario_Probability['Pessimistic'] = Scenario_Probability['Pessimistic'].apply(lambda x: "{:.2%}".format(x))
        st.dataframe(Scenario_Probability, width=1200)
        
        st.markdown(
            """
            <div style='text-align: center;
            font-size: 20px;'>
                <strong>Other Parameters</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        base_dir = os.path.dirname(__file__)
        other_parameters = pd.read_excel(os.path.join(base_dir, "Datasets", "Other_parameters.xlsx"))
                           
        other_parameters['Values'] = other_parameters['Values'].apply(lambda x: "{:.2%}".format(x))
        st.dataframe(other_parameters, width=1200)
        
        st.markdown(
            """
            <div style='text-align: center;
            font-size: 20px;'>
                <strong>Staging Rules</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        base_dir = os.path.dirname(__file__)
        Staging_rules = pd.read_excel(os.path.join(base_dir, "Datasets", "Staging_rules.xlsx"))
                            
        Staging_rules['Values'].iloc[0] = "{:.2%}".format(Staging_rules['Values'].iloc[0])
        st.dataframe(Staging_rules, width=1200)
        
    with tab2:
        st.markdown(
            """
            <div style='text-align: center;
            font-size: 20px;'>
                <strong>ECL Weighted Data</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        ECL_weighted = pd.read_excel("Datasets/ECL_weighted.xlsx")

        # Apply formatting to the entire DataFrame
        ECL_weighted = ECL_weighted.applymap(
            lambda x: format_decimal(x, format='#,##0.00', locale='en_IN').rstrip('0').rstrip('.') 
            if pd.notnull(x) and isinstance(x, (int, float)) else str(x)
        )
        st.dataframe(ECL_weighted, width=1200)
        # Add your ECL Weighted code here

    with tab3:
        st.markdown(
            """
            <div style='text-align: center;
            font-size: 20px;'>
                <strong>Account Wise Scenario Report</strong>
            </div>
            """,
            unsafe_allow_html=True
        )
        Account_wise_scenario_report = pd.read_excel("Datasets/Account_wise_scenario_report.xlsx")
        
        Account_wise_scenario_report = Account_wise_scenario_report.fillna('')
        
        # Apply formatting to the entire DataFrame
        Account_wise_scenario_report = Account_wise_scenario_report.applymap(
            lambda x: format_decimal(x, format='#,##0.00', locale='en_IN').rstrip('0').rstrip('.') 
            if pd.notnull(x) and isinstance(x, (int, float)) else str(x)
        )

        st.dataframe(Account_wise_scenario_report, width=1200)
        

if __name__ == "__main__":
    app()
