"""
Simple script to create a table in Postgres (TimescaleDB), insert synthetic time series data, run a Holt-Winters forecast using statsmodels, and write back forecasted values.
Requires environment:
- POSTGRES_HOST=timescaledb
- POSTGRES_USER=tsuser
- POSTGRES_PASSWORD=secret
- POSTGRES_DB=timeseriesdb

When run from the docker-compose backend service this will connect to the timescaledb container.
"""

import os
import time
import pandas as pd
from statsmodels.tsa.holtwinters import ExponentialSmoothing
import psycopg2
from psycopg2.extras import execute_values

PG_HOST = os.getenv('POSTGRES_HOST', 'timescaledb')
PG_USER = os.getenv('POSTGRES_USER', 'tsuser')
PG_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'secret')
PG_DB = os.getenv('POSTGRES_DB', 'timeseriesdb')
PG_PORT = os.getenv('POSTGRES_PORT', '5432')

# Wait a bit for DB to be ready
print('Waiting for Postgres...')
time.sleep(5)

conn = psycopg2.connect(host=PG_HOST,user=PG_USER,password=PG_PASSWORD,dbname=PG_DB,port=PG_PORT)
cur = conn.cursor()

# Create table
cur.execute("""
CREATE TABLE IF NOT EXISTS sensor_data (
    time timestamptz PRIMARY KEY,
    value DOUBLE PRECISION
);
""")
conn.commit()

# Insert synthetic data: last 100 days daily
import datetime
base = datetime.datetime.now()
rows = []
for i in range(100):
    t = base - datetime.timedelta(days=100-i)
    val = 20 + 5 * (i/100.0) + (i%7)  # simple trend + weekday pattern
    rows.append((t, float(val)))

execute_values(cur, "INSERT INTO sensor_data (time, value) VALUES %s ON CONFLICT (time) DO NOTHING", rows)
conn.commit()

# Read into DataFrame
cur.execute("SELECT time, value FROM sensor_data ORDER BY time")
rows = cur.fetchall()
df = pd.DataFrame(rows, columns=['ds','y'])

# Forecast using Holt-Winters
# set index
df['ds'] = pd.to_datetime(df['ds'])
df = df.set_index('ds')
# resample to daily and interpolate
try:
    inferred = pd.infer_freq(df.index)
except Exception:
    inferred = None
if inferred is None:
    ts = df['y'].resample('D').mean().interpolate()
else:
    ts = df['y'].asfreq(inferred).interpolate()

seasonal_periods = 7 if len(ts) >= 14 else None
if seasonal_periods:
    model = ExponentialSmoothing(ts, trend='add', seasonal='add', seasonal_periods=seasonal_periods)
else:
    model = ExponentialSmoothing(ts, trend='add', seasonal=None)

fit = model.fit(optimized=True)
future = fit.forecast(30)

# Write forecast back to DB into a table
cur.execute("""
CREATE TABLE IF NOT EXISTS sensor_forecast (
    time timestamptz PRIMARY KEY,
    yhat DOUBLE PRECISION,
    yhat_lower DOUBLE PRECISION,
    yhat_upper DOUBLE PRECISION
);
""")
conn.commit()

# estimate residual std for simple intervals
resid = fit.resid.dropna()
se = resid.std() if len(resid) > 0 else 0.0
z = 1.96

frows = [(pd.Timestamp(idx).to_pydatetime(), float(val), float(val - z*se), float(val + z*se)) for idx,val in future.items()]
execute_values(cur, "INSERT INTO sensor_forecast (time,yhat,yhat_lower,yhat_upper) VALUES %s ON CONFLICT (time) DO UPDATE SET yhat = EXCLUDED.yhat, yhat_lower = EXCLUDED.yhat_lower, yhat_upper = EXCLUDED.yhat_upper", frows)
conn.commit()

print('Ingest and forecast complete. Forecast rows written:', len(frows))

cur.close()
conn.close()
