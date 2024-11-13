import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px

def simulate_portfolio(stocks_weight, savings_weight, startup_weight, startups_weight, initial_amount, years):
    # Parameter für Renditen
    stocks_mean, stocks_std = 0.10, 0.22
    savings_mean, savings_std = 0.005, 0
    startups_mean, startups_std = 0.20, 0.40
    
    # Einmalige Entscheidung über Startup Erfolg
    startup_success = np.random.random() < 0.1  # 10% Chance auf Erfolg
    if startup_success:
        startup_yearly_return = np.random.uniform(0.3, 0.4)  # Fixe jährliche Rendite zwischen 30-50%
    
    # Simulation für jedes Jahr
    portfolio_values = [initial_amount]
    
    for year in range(years):
        stocks_return = np.random.normal(stocks_mean, stocks_std)
        savings_return = np.random.normal(savings_mean, savings_std)
        startups_return = np.random.normal(startups_mean, startups_std)
        
        # Startup Return basierend auf initialem Erfolg/Misserfolg
        if not startup_success and year == 0:
            startup_return = -1.0  # Totalverlust im ersten Jahr
        elif startup_success:
            startup_return = startup_yearly_return  # Konstante jährliche Rendite bei Erfolg
        else:
            startup_return = 0  # Nach Totalverlust keine weitere Änderung
            
        portfolio_return = (stocks_weight * stocks_return) + \
                         (savings_weight * savings_return) + \
                         (startup_weight * startup_return) + \
                         (startups_weight * startups_return)
        
        new_value = portfolio_values[-1] * (1 + portfolio_return)
        portfolio_values.append(new_value)
    
    return portfolio_values

# Streamlit Interface
st.title('Zukunftstag Investment Challenge')
st.text('Du hast 100 CHF Taschengeld angespart und kannst in Aktien, ein Sparbuch, ein Startup oder ein Portfolio von 100 Startups investieren.')
st.markdown('**Ziel**: Finde die besten Portfolio-Strategie (linke spalte) für die nächsten 10 Jahre!')

# Eingabefelder
col1, col2 = st.columns(2)
with col1:
    stocks = st.slider('Aktien (%)', 0, 100, 25)
    savings = st.slider('Sparbuch (%)', 0, 100, 25)
    startup = st.slider('1 Startup (%)', 0, 100, 25)
    startups = st.slider('Portfolio von 100 Startups (%)', 0, 100, 25)

with col2:
    initial = st.number_input('Startkapital (CHF)', 100, 10000, 100)
    years = st.slider('Jahre', 1, 60, 10)

# Add refresh button
refresh = st.button('Neu simulieren')
if refresh:
    st.rerun()

# Prüfe, ob Gewichte 100% ergeben
total_weight = stocks + savings + startup + startups
if total_weight != 100:
    st.error('Die Gewichte müssen sich zu 100% addieren!')
else:
    # Simulation durchführen
    results = simulate_portfolio(stocks/100, savings/100, startup/100, startups/100, initial, years)
    
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
    st.write(f'Startkapital: {initial:,.2f} CHF')
    st.write(f'Endkapital: {results[-1]:,.2f} CHF')
    st.write(f'Gesamtrendite: {((results[-1]/initial - 1) * 100):,.2f}%')

# Zusätzliche Informationen
st.markdown("""
### Informationen über die Investment-Optionen:
- **Aktien**: Durchschnittliche Rendite 10% pro Jahr, Risiko hoch
- **Sparbuch**: Durchschnittliche Rendite 0.5% pro Jahr, kein Risiko
- **Startup**: 
  - 10% Chance auf dauerhaften Erfolg mit 30-50% Rendite pro Jahr
  - 90% Chance auf Totalverlust im ersten Jahr
- **Portfolio von 100 Startups**: Durchschnittliche Rendite 20% pro Jahr, Risiko sehr hoch
""")