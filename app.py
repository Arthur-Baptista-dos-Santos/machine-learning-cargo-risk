# =============================================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# =============================================================================
import streamlit as st
import pandas as pd
import pickle
from geopy.geocoders import Nominatim  # Para o bônus de geocodificação

# =============================================================================
# 2. CARREGAMENTO DO MODELO (Cumpre Critério 1: Carregar .pkl)
# =============================================================================

# Define o nome do arquivo do modelo
MODELO_PKL = 'melhor_modelo_risco_carga.pkl'

# Carrega o pipeline de pré-processamento e o modelo
try:
    with open(MODELO_PKL, 'rb') as file:
        model = pickle.load(file)
except FileNotFoundError:
    st.error(f"Arquivo do modelo '{MODELO_PKL}' não encontrado.")
    st.info("Por favor, copie o arquivo .pkl gerado na Sprint 3 para a pasta deste app.")
    st.stop()
except Exception as e:
    st.error(f"Erro ao carregar o modelo: {e}")
    st.stop()

# =============================================================================
# 3. DEFINIÇÕES E CONFIGURAÇÕES DA PÁGINA
# =============================================================================

# Configuração da página do Streamlit
st.set_page_config(
    page_title="Previsão de Risco de Carga",
    page_icon="🚚",
    layout="wide"
)

# --- (CRÍTICO!) Mapeamento da Previsão ---
#  ['Risco Alto', 'Risco Baixo', 'Risco Médio']
risk_mapping = {
    0: 'Risco Alto',
    1: 'Risco Baixo',
    2: 'Risco Médio'
}
# ----------------------------------------

# --- Opções para os Selectbox ---
dias_semana_options = ['domingo', 'segunda-feira', 'terça-feira', 'quarta-feira', 'quinta-feira', 'sexta-feira', 'sábado']
fase_dia_options = ['Pleno dia', 'Plena Noite', 'Amanhecer', 'Anoitecer'] # Adicionando opções comuns
sentido_via_options = ['Crescente', 'Decrescente']
condicao_met_options = ['Céu Claro', 'Chuva', 'Nublado', 'Nevoeiro', 'Sol', 'Vento'] # Adicionando opções comuns
tipo_pista_options = ['Simples', 'Dupla', 'Múltipla']
tracado_via_options = ['Reta', 'Curva', 'Interseção', 'Rotatória', 'Viaduto'] # Adicionando opções comuns
postos_prf_options = ['Média', 'Alta', 'Baixa']


# =============================================================================
# 4. FUNÇÃO DE GERAÇÃO DA INTERFACE (Cumpre Critério 2: Interface Web)
# =============================================================================

def get_user_inputs(scenario_name):
    """
    Cria um conjunto de widgets de input para um cenário (Origem/Destino)
    e retorna um dicionário com os dados.
    """
    st.subheader(f"Cenário: {scenario_name}")
    
    
    col1, col2 = st.columns(2)
    
    with col1:
        dia_semana = st.selectbox(f'Dia da Semana ({scenario_name})', options=dias_semana_options, key=f'dia_{scenario_name}')
        fase_dia = st.selectbox(f'Fase do Dia ({scenario_name})', options=fase_dia_options, key=f'fase_{scenario_name}')
        condicao_metereologica = st.selectbox(f'Condição Meteorológica ({scenario_name})', options=condicao_met_options, key=f'cond_{scenario_name}')
        postos_policiais_PRF = st.selectbox(f'Nível de Policiamento PRF ({scenario_name})', options=postos_prf_options, key=f'prf_{scenario_name}')

    with col2:
        sentido_via = st.selectbox(f'Sentido da Via ({scenario_name})', options=sentido_via_options, key=f'sent_{scenario_name}')
        tipo_pista = st.selectbox(f'Tipo de Pista ({scenario_name})', options=tipo_pista_options, key=f'pista_{scenario_name}')
        tracado_via = st.selectbox(f'Traçado da Via ({scenario_name})', options=tracado_via_options, key=f'trac_{scenario_name}')
        # Para BR e Delegacia, usamos st.text_input pois são muitas opções
        br = st.text_input(f'Rodovia (ex: BR-365) ({scenario_name})', value='BR-365', key=f'br_{scenario_name}')
        delegacia = st.text_input(f'Delegacia (ex: DEL10-MG) ({scenario_name})', value='DEL10-MG', key=f'del_{scenario_name}')

    st.markdown("---")
    col_num1, col_num2, col_num3 = st.columns(3)
    
    with col_num1:
        # Usando valores de exemplo do df.head()
        km = st.number_input(f'KM da Rodovia ({scenario_name})', format="%.1f", value=361.7, key=f'km_{scenario_name}')
    with col_num2:
        latitude = st.number_input(f'Latitude ({scenario_name})', format="%.5f", value=-18.50801, key=f'lat_{scenario_name}')
    with col_num3:
        longitude = st.number_input(f'Longitude ({scenario_name})', format="%.5f", value=-46.12129, key=f'lon_{scenario_name}')


    # Coleta todos os dados em um dicionário
    data = {
        'dia_semana': dia_semana,
        'br': br,
        'km': km,
        'fase_dia': fase_dia,
        'sentido_via': sentido_via,
        'condicao_metereologica': condicao_metereologica,
        'tipo_pista': tipo_pista,
        'tracado_via': tracado_via,
        'latitude': latitude,
        'longitude': longitude,
        'delegacia': delegacia,
        'postos_policiais_PRF': postos_policiais_PRF
    }
    return data

# =============================================================================
# 5. LAYOUT DA PÁGINA PRINCIPAL
# =============================================================================

# --- Título e Descrição ---
st.title("🚚 Previsão de Risco de Acidentes para Cargas")
st.markdown("""
Esta aplicação utiliza o modelo de Machine Learning (Random Forest) treinado na Sprint 3 para
prever a classificação de risco de um acidente. 

Preencha os dados para dois cenários (ex: Origem e Destino) para comparar os riscos.
""")

# --- (OPCIONAL) Geocodificação ---
with st.sidebar:
    st.header("📍 Geocodificador Opcional")
    st.markdown("Não sabe a Lat/Long? Digite um endereço para descobrir.")
    
    endereco = st.text_input("Digite um endereço (ex: 'Av. Paulista, 1000, São Paulo')")
    
    if st.button("Buscar Coordenadas"):
        if not endereco:
            st.warning("Por favor, insira um endereço.")
        else:
            try:
                geolocator = Nominatim(user_agent="sprint4_app_gemini")
                location = geolocator.geocode(endereco)
                
                if location:
                    st.success(f"Latitude: `{location.latitude}`")
                    st.success(f"Longitude: `{location.longitude}`")
                    st.info("Copie e cole os valores nos campos ao lado.")
                else:
                    st.error("Endereço não encontrado.")
            except Exception as e:
                st.error(f"Erro de geocodificação: {e}")

# --- Coleta de Inputs (Cumpre Desejável: 2 locais) ---
with st.container(border=True):
    col_origem, col_destino = st.columns(2)
    
    with col_origem:
        data_origem = get_user_inputs("Origem")
    
    with col_destino:
        data_destino = get_user_inputs("Destino")

# =============================================================================
# 6. LÓGICA DE PREVISÃO (Cumpre Critério 3: Previsão)
# =============================================================================

# Botão para executar a previsão
if st.button('Calcular Risco', type="primary", use_container_width=True):
    
    # Define os nomes das colunas na ordem exata que o modelo espera
    colunas_features = [
        'dia_semana', 'br', 'km', 'fase_dia', 'sentido_via',
        'condicao_metereologica', 'tipo_pista', 'tracado_via',
        'latitude', 'longitude', 'delegacia', 'postos_policiais_PRF'
    ]
    
    # Cria DataFrames para os cenários
    df_origem = pd.DataFrame([data_origem], columns=colunas_features)
    df_destino = pd.DataFrame([data_destino], columns=colunas_features)
    
    # Combina os DataFrames para fazer uma única chamada de previsão
    df_combinado = pd.concat([df_origem, df_destino], ignore_index=True)
    
    try:
        # --- PREVISÃO ---
        # br/delegacia nao estao no pipeline treinado (alta cardinalidade removida)
        df_pred = df_combinado.drop(['br', 'delegacia'], axis=1)
        predicoes_numericas = model.predict(df_pred)
        probabilidades = model.predict_proba(df_pred)
        
        # Pega os resultados individuais
        risco_origem = risk_mapping.get(predicoes_numericas[0], "Erro")
        risco_destino = risk_mapping.get(predicoes_numericas[1], "Erro")
        
        prob_origem = probabilidades[0]
        prob_destino = probabilidades[1]
        
        # --- Exibição dos Resultados ---
        st.header("Resultados da Previsão")
        res_col1, res_col2 = st.columns(2)
        
        with res_col1:
            st.subheader(f"Cenário Origem: {risco_origem}")
            # Cria um DataFrame para mostrar as probabilidades
            prob_df_1 = pd.DataFrame(
                prob_origem,
                index=[risk_mapping[i] for i in range(len(prob_origem))],
                columns=['Probabilidade']
            )
            prob_df_1['Probabilidade'] = prob_df_1['Probabilidade'].apply(lambda x: f"{x*100:.2f}%")
            st.dataframe(prob_df_1.sort_values(by='Probabilidade', ascending=False), use_container_width=True)

        with res_col2:
            st.subheader(f"Cenário Destino: {risco_destino}")
            # Cria um DataFrame para mostrar as probabilidades
            prob_df_2 = pd.DataFrame(
                prob_destino,
                index=[risk_mapping[i] for i in range(len(prob_destino))],
                columns=['Probabilidade']
            )
            prob_df_2['Probabilidade'] = prob_df_2['Probabilidade'].apply(lambda x: f"{x*100:.2f}%")
            st.dataframe(prob_df_2.sort_values(by='Probabilidade', ascending=False), use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao realizar a previsão: {e}")
        st.error("Verifique se os valores de texto (como 'br' ou 'delegacia') "
                 "são valores que o modelo já viu durante o treinamento.")
