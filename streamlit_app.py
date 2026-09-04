import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

st.set_page_config(page_title='AI Data Analytics - Streamlit Demo')
st.title('AI Data Analytics — Streamlit Demo (statsmodels)')

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

        if st.button('Run Forecast (statsmodels - Holt-Winters)'):
            try:
                from statsmodels.tsa.holtwinters import ExponentialSmoothing

                # Prepare time series: set index and ensure regular daily frequency (fill gaps)
                ts = df_ts.set_index('ds')['y']

                # If index does not have a regular freq, resample to daily and interpolate
                try:
                    inferred = pd.infer_freq(ts.index)
                except Exception:
                    inferred = None

                if inferred is None:
                    ts = ts.resample('D').mean().interpolate()
                else:
                    ts = ts.asfreq(inferred).interpolate()

                # Choose seasonal period if enough data (weekly seasonality default)
                seasonal_periods = 7 if len(ts) >= 14 else None

                if seasonal_periods:
                    model = ExponentialSmoothing(ts, trend='add', seasonal='add', seasonal_periods=seasonal_periods)
                else:
                    model = ExponentialSmoothing(ts, trend='add', seasonal=None)

                fit = model.fit(optimized=True)
                periods = 30
                forecast = fit.forecast(periods)

                # Estimate simple prediction intervals using residual std
                resid = fit.resid.dropna()
                se = resid.std() if len(resid) > 0 else 0.0
                z = 1.96
                forecast_df = pd.DataFrame({
                    'ds': forecast.index,
                    'yhat': forecast.values,
                    'yhat_lower': forecast.values - z * se,
                    'yhat_upper': forecast.values + z * se,
                })

                st.write(forecast_df.tail(periods))

                # Plot history + forecast
                fig, ax = plt.subplots(figsize=(10, 4))
                ts.plot(label='history', ax=ax)
                forecast.plot(label='forecast', ax=ax)
                ax.fill_between(forecast.index, forecast_df['yhat_lower'], forecast_df['yhat_upper'], color='gray', alpha=0.2)
                ax.legend()
                ax.set_title('History and forecast')
                st.pyplot(fig)

            except Exception as e:
                st.error('Forecast failed: ' + str(e))

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
