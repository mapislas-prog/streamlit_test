import pandas as pd
import scipy.stats
import streamlit as st
import time

# Variables de estado
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'iteraciones', 'media']
    )

st.header('Lanzar una moneda')

# Espacio reservado para la gráfica
chart_placeholder = st.empty()


def toss_coin(n):
    # Genera n resultados:
    # 0 = cruz
    # 1 = cara
    trial_outcomes = scipy.stats.bernoulli.rvs(
        p=0.5,
        size=n
    )

    outcome_1_count = 0
    means = []

    for outcome_no, result in enumerate(trial_outcomes, start=1):

        if result == 1:
            outcome_1_count += 1

        mean = outcome_1_count / outcome_no
        means.append(mean)

        chart_data = pd.DataFrame({
            'Media acumulada': means
        })

        chart_placeholder.line_chart(chart_data)

        time.sleep(0.05)

    return mean


number_of_trials = st.slider(
    '¿Número de intentos?',
    min_value=1,
    max_value=1000,
    value=10
)

start_button = st.button('Ejecutar')

if start_button:
    st.write(
        f'Experimento con {number_of_trials} intentos en curso.'
    )

    mean = toss_coin(number_of_trials)

    st.session_state['experiment_no'] += 1

    new_result = pd.DataFrame({
        'no': [st.session_state['experiment_no']],
        'iteraciones': [number_of_trials],
        'media': [mean]
    })

    st.session_state['df_experiment_results'] = pd.concat(
        [
            st.session_state['df_experiment_results'],
            new_result
        ],
        ignore_index=True
    )

    st.success(f'Media final: {mean:.4f}')

st.subheader('Resultados de los experimentos')
st.dataframe(
    st.session_state['df_experiment_results'],
    use_container_width=True
)