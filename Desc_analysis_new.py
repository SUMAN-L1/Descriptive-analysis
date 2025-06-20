import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import skew, kurtosis
import io

st.set_page_config(page_title="Descriptive Statistics: Developed by Suman_econ (UAS-B)", layout="wide")

st.title("Descriptive Statistics: Developed by Suman_econ (UAS-B)")

# File Upload
uploaded_file = st.file_uploader("Upload File (CSV, XLS, XLSX)", type=["csv", "xls", "xlsx"])

sheet_name = None
df = None

if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1]

    if file_type in ["xls", "xlsx"]:
        excel_file = pd.ExcelFile(uploaded_file)
        sheet_name = st.selectbox("Select Sheet", options=excel_file.sheet_names)
        df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
    else:
        df = pd.read_csv(uploaded_file)

    st.subheader("Data Preview")
    st.dataframe(df.head())

    process = st.button("Process Data")

    if process:
        # Numeric Statistics
        num_df = df.select_dtypes(include=np.number).dropna(how="all", axis=1)
        num_stats = []

        for col in num_df.columns:
            col_data = num_df[col].dropna()
            if len(col_data) == 0:
                continue
            stats = {
                "Column": col,
                "Min": np.min(col_data),
                "Max": np.max(col_data),
                "Range": np.max(col_data) - np.min(col_data),
                "Mean": np.mean(col_data),
                "Median": np.median(col_data),
                "Mode": col_data.mode().iloc[0] if not col_data.mode().empty else np.nan,
                "Std_Dev": np.std(col_data, ddof=1),
                "CV (%)": (np.std(col_data, ddof=1) / np.mean(col_data)) * 100 if np.mean(col_data) != 0 else np.nan,
                "Skewness": skew(col_data),
                "Kurtosis": kurtosis(col_data),
                "Mean_Deviation": np.mean(np.abs(col_data - np.mean(col_data))),
                "Count": len(col_data),
                "Sum": np.sum(col_data),
                "Std_Error": np.std(col_data, ddof=1) / np.sqrt(len(col_data)),
                "Q1": np.percentile(col_data, 25),
                "Q3": np.percentile(col_data, 75),
                "P10": np.percentile(col_data, 10),
                "P90": np.percentile(col_data, 90)
            }
            num_stats.append(stats)

        num_stats_df = pd.DataFrame(num_stats)

        # Categorical Statistics
        cat_df = df.select_dtypes(include='object').dropna(how="all", axis=1)
        cat_stats = []

        for col in cat_df.columns:
            freq = cat_df[col].value_counts(dropna=False)
            for val, count in freq.items():
                cat_stats.append({
                    "Column": col,
                    "Value": val,
                    "Frequency": count,
                    "Proportion": count / freq.sum()
                })

        cat_stats_df = pd.DataFrame(cat_stats)

        st.subheader("Summary of Numeric Statistics")
        st.dataframe(num_stats_df)

        st.subheader("Summary of Categorical Statistics")
        st.dataframe(cat_stats_df)

        # Download options
        st.subheader("Download Results")
        download_format = st.radio("Select Download Format", ["CSV", "Excel (.xlsx)"])

        if download_format == "CSV":
            csv_num = num_stats_df.to_csv(index=False)
            csv_cat = cat_stats_df.to_csv(index=False)

            st.download_button("Download Numeric Statistics (CSV)", csv_num, "numeric_stats.csv", "text/csv")
            st.download_button("Download Categorical Statistics (CSV)", csv_cat, "categorical_stats.csv", "text/csv")
        else:
            import openpyxl
            import xlsxwriter
            import io

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                num_stats_df.to_excel(writer, sheet_name='Numeric_Statistics', index=False)
                cat_stats_df.to_excel(writer, sheet_name='Categorical_Statistics', index=False)
                writer.save()
            st.download_button("Download All Results (Excel)", output.getvalue(), "desc_stats.xlsx", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

# Contact Info
st.markdown("---")
st.markdown("For more collaboration: [Sumanecon.uas@outlook.in](mailto:Sumanecon.uas@outlook.in)")
