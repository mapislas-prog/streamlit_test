import pandas as pd
import scipy.stats
import streamlit as st
import time

# Variables de estado que se conservan cuando Streamlit
# vuelve a ejecutar el script
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        columns=['no', 'iteraciones', 'media']
    )

st.header('Lanzar una moneda')

# Crea un espacio vacío para colocar y actualizar la gráfica
chart_placeholder = st.empty()


def toss_coin(n):

    # Genera n lanzamientos:
    # 0 representa cruz
    # 1 representa cara
    trial_outcomes = scipy.stats.bernoulli.rvs(
        p=0.5,
        size=n
    )

    outcome_1_count = 0

    # Aquí guardaremos todas las medias acumuladas
    means = []

    for outcome_no, result in enumerate(
        trial_outcomes,
        start=1
    ):

        if result == 1:
            outcome_1_count += 1

        # Proporción acumulada de caras
        mean = outcome_1_count / outcome_no

        # Guardamos la nueva media
        means.append(mean)

        # Creamos los datos para la gráfica
        chart_data = pd.DataFrame({
            'media': means
        })

        # Reemplaza la gráfica anterior por la actualizada
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

    st.session_state['experiment_no'] += 1

    mean = toss_coin(number_of_trials)

    new_experiment = pd.DataFrame({
        'no': [st.session_state['experiment_no']],
        'iteraciones': [number_of_trials],
        'media': [mean]
    })

    st.session_state['df_experiment_results'] = pd.concat(
        [
            st.session_state['df_experiment_results'],
            new_experiment
        ],
        ignore_index=True
    )

    st.success(
        f'Experimento terminado. Media final: {mean:.4f}'
    )

st.write(st.session_state['df_experiment_results'])