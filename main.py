import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px


from utils.utils import loadData
# Configurar el título de la aplicación
st.title("Purchases Data Analysis Dashboard")

# Cargar el dataset
@st.cache_data
def load_data():
    df = pd.read_csv('data/Groceries_dataset.csv')
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')
    df['Year'] = df['Date'].dt.year
    return df

data = load_data()

# Agregar un filtro para la fecha
st.sidebar.subheader("Date Filter")
start_date = st.sidebar.date_input('Start Date', data['Date'].min())
end_date = st.sidebar.date_input('End Date', data['Date'].max())
filtered_data = data[(data['Date'] >= pd.Timestamp(start_date)) & (data['Date'] <= pd.Timestamp(end_date))]

### KPIs 
num_transactions = filtered_data.shape[0]
num_custumers = filtered_data['Member_number'].nunique()
num_unique_items = filtered_data['itemDescription'].nunique()

# Mostrar métricas en la misma fila
st.subheader("Key Performance Indicators")
col1, col2, col3 = st.columns(3)  # Crear dos columnas

with col1:
    st.metric(label="Number of transactions", value=num_transactions)
with col2:
    st.metric(label="Number of unique products", value=num_unique_items)
with col3:
    st.metric(label="Number of customers", value=num_custumers)


# Mostrar estadísticas de 'itemDescription'
st.subheader("Top 15 Best-Selling Products")
item_counts = pd.DataFrame(data['itemDescription'].value_counts().sort_values(ascending=False).head(15)).reset_index()
st.bar_chart(item_counts, x="itemDescription", y="count")


st.subheader("Top 10 Best Clients")
clients = data.groupby(['Member_number', 'Year']).size().unstack(fill_value=0)
clients['Total Transactions'] = clients.sum(axis=1)
clients.sort_values(by='Total Transactions', ascending=False).head(10)
st.dataframe(clients)

transactions_per_year = data.groupby('Year').size()

# Convertir a DataFrame para usar en Streamlit
transactions_per_year_df = transactions_per_year.reset_index(name='Number of Transactions')

# Mostrar la tabla y el gráfico en Streamlit
st.title('Number of Transactions per Year')
st.dataframe(transactions_per_year_df)

# Mostrar gráfico de barras
st.bar_chart(transactions_per_year_df.set_index('Year'))


# Extraer el año y el mes de la fecha


data['YearMonth'] = data['Date'].dt.to_period('M')

# Contar el número de transacciones por año y mes
transactions_per_month = data.groupby('YearMonth').size()

# Convertir a DataFrame para usar en Streamlit
transactions_per_month_df = transactions_per_month.reset_index(name='Number of Transactions')
transactions_per_month_df['YearMonth'] = transactions_per_month_df['YearMonth'].dt.to_timestamp()
# Mostrar la tabla y el gráfico en Streamlit
st.title('Number of Transactions per Month')
st.dataframe(transactions_per_month_df)

# Mostrar gráfico de líneas
fig = px.line(transactions_per_month_df, x='YearMonth', y='Number of Transactions',
              title='Number of Transactions per Month',
              labels={'YearMonth': 'Month', 'Number of Transactions': 'Number of Transactions'})

st.plotly_chart(fig)

