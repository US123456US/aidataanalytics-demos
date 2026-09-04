import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title='AI Data Analytics - Streamlit Demo')
st.title('AI Data Analytics — Streamlit Demo')

os.makedirs('data', exist_ok=True)
HISTORY_PATH = 'data/history.csv'

uploaded = st.file_uploader('Upload a CSV file (must contain a date/time column and a numeric value column)', type=['csv'])

if uploaded is not None:
    df = pd.read_csv(uploaded)
    st.write('Preview of uploaded data', df.head())

    if st.button('Append to history and save'):
        if os.path.exists(HISTORY_PATH):
            history = pd.read_csv(HISTORY_PATH)
            history = pd.concat([history, df], ignore_index=True)
        else:
            history = df.copy()
        history.to_csv(HISTORY_PATH, index=False)
        st.success('Saved to data/history.csv')

if os.path.exists(HISTORY_PATH):
    st.subheader('Full history (saved)')
    history = pd.read_csv(HISTORY_PATH)
    st.write(history.tail(20))

    # Try to detect a date and numeric column
    date_cols = [c for c in history.columns if 'date' in c.lower() or 'time' in c.lower()]
    numeric_cols = history.select_dtypes(include=['number']).columns.tolist()

    st.markdown('Detected date columns: ' + (', '.join(date_cols) if date_cols else 'None'))
    st.markdown('Detected numeric columns: ' + (', '.join(numeric_cols) if numeric_cols else 'None'))

    if date_cols and numeric_cols:
        date_col = st.selectbox('Choose date column', date_cols)
        value_col = st.selectbox('Choose numeric value column', numeric_cols)

        df_ts = history[[date_col, value_col]].dropna()
        df_ts[date_col] = pd.to_datetime(df_ts[date_col])
        df_ts = df_ts.sort_values(date_col)
        df_ts = df_ts.rename(columns={date_col: 'ds', value_col: 'y'})

        st.line_chart(df_ts.set_index('ds')['y'])

        if st.button('Run Prophet forecast (uses open-source Prophet)'):
            try:
                from prophet import Prophet
                m = Prophet()
                m.fit(df_ts)
                future = m.make_future_dataframe(periods=30)
                forecast = m.predict(future)
                st.write(forecast[['ds','yhat','yhat_lower','yhat_upper']].tail(30))

                fig = m.plot(forecast)
                st.pyplot(fig)
            except Exception as e:
                st.error('Prophet forecast failed: ' + str(e) + '\nMake sure the `prophet` package is installed.')

    # Simple automated summary (rule-based) as a lightweight "AI" fallback
    st.subheader('Automated summary (rule-based)')
    try:
        mean_val = history[numeric_cols].mean().iloc[0]
        st.write(f'Latest value: {history[numeric_cols].iloc[-1,0]}')
        st.write(f'Average: {mean_val}')
    except Exception:
        st.write('No numeric summary available')

else:
    st.info('No history yet. Upload a CSV to get started. Example CSVs are in data/*.csv')
