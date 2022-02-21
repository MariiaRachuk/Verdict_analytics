import numpy as np
import pandas as pd
import streamlit as st
import input_sql
import plotly.express as px

# bin with np.histogram
counts, bins = np.histogram(input_sql.df['Сегмент боргу'], bins=100)
# turn into data frame
df = pd.DataFrame({"bins": bins[1:], "counts":counts})
# chart using Plotly.Express
fig = px.bar(df, x="bins", y="counts", text="counts")
st.plotly_chart(fig)