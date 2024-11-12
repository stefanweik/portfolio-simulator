import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def simulate_portfolio(stocks_weight, bonds_weight, initial_amount, years):
    # Parameter für Renditen
    stocks_mean, stocks_std = 0.07, 0.15
    bonds_mean, bonds_std = 0.03, 0.05

    # Simulation für jedes Jahr
    portfolio_values = [initial_amount]

    for _ in range(years):
        stocks_return = np.random.normal(stocks_mean, stocks_std)
        bonds_return = np.random.normal(bonds_mean, bonds_std)
        portfolio_return = (stocks_weight * stocks_return) + (bonds_weight * bonds_return)
        new_value = portfolio_values[-1] * (1 + portfolio_return)
        portfolio_values.append(new_value)

    return portfolio_values

# Streamlit Interface and so on
st.title('Portfolio Simulator')

# Eingabefelder
col1, col2 = st.columns(2)
with col1:
    stocks = st.slider('Aktien (%)', 0, 100, 60)
    initial = st.number_input('Startkapital (€)', 1000, 1000000, 10000)

with col2:
    bonds = st.slider('Anleihen (%)', 0, 100, 40)
    years = st.slider('Jahre', 1, 30, 10)

# Prüfe, ob Gewichte 100% ergeben
if stocks + bonds != 100:
    st.error('Die Gewichte müssen sich zu 100% addieren!')
else:
    # Simulation durchführen
    results = simulate_portfolio(stocks/100, bonds/100, initial, years)

    # Ergebnisse plotten
    df = pd.DataFrame({
        'Jahr': range(years + 1),
        'Portfolio Wert': results
    })

    fig = px.line(df, x='Jahr', y='Portfolio Wert',
                  title='Portfolio Entwicklung über die Zeit')
    fig.update_layout(yaxis_tickformat = ',.0f')
    st.plotly_chart(fig)

    # Finale Statistiken
    st.write(f'Startkapital: {initial:,.2f} €')
    st.write(f'Endkapital: {results[-1]:,.2f} €')
    st.write(f'Gesamtrendite: {((results[-1]/initial - 1) * 100):,.2f}%')