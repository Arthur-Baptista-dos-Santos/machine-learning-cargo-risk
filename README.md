[![Live Demo](https://img.shields.io/badge/Live%20Demo-abs--cargo--risk.streamlit.app-FF4B4B?logo=streamlit&logoColor=white)](https://abs-cargo-risk.streamlit.app)

# `machine-learning-cargo-risk: Previsao de Risco de Roubo de Cargas`

> Random Forest treinado em dados reais de roubos de carga no Brasil para classificacao de risco (Alto/Medio/Baixo) + app Streamlit de inferencia em producao com geocodificacao. Sprint 3 e 4, FIAP 2025.

---

## `Tecnologias`

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-RandomForest-orange)
![Streamlit](https://img.shields.io/badge/Streamlit-app-ff4b4b)
![Pandas](https://img.shields.io/badge/pandas-ETL-green)
![Geopy](https://img.shields.io/badge/geopy-geocodificacao-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## `O que faz`

**Sprint 3** (`cargo_risk_model_training.ipynb`): treina o classificador
- EDA do dataset de roubos de carga
- Feature engineering: hora do dia, tipo de carga, valor, regiao
- Pipeline sklearn: StandardScaler + RandomForestClassifier
- Validacao cruzada 5-fold, matriz de confusao, curva ROC
- Exporta modelo como `melhor_modelo_risco_carga.pkl`

**Sprint 4** (`app.py`): app Streamlit de inferencia
- Carrega o `.pkl` do Sprint 3
- Input: dados da carga via formulario
- Bonus: geocodificacao do endereco via Geopy/Nominatim
- Output: predicao de risco (Alto/Medio/Baixo) com probabilidades

---

## `Pipeline`

```
Dataset CSV (roubos de carga 2024)
    |
    EDA: distribuicoes, correlacoes, outliers
    |
    Feature Engineering
        hora_dia (manha/tarde/noite)
        valor_categoria (faixas)
        estado_risco (historico de incidencias)
    |
    Pipeline sklearn
        StandardScaler + RandomForestClassifier
        GridSearchCV: n_estimators, max_depth
    |
    Avaliacao: F1-macro, AUC-ROC, Confusion Matrix
    |
    Export: melhor_modelo_risco_carga.pkl
    |
    App Streamlit (app.py)
        Formulario de entrada → predicao em tempo real
```

---

## `Como usar`

```bash
git clone https://github.com/Arthur-Baptista-dos-Santos/machine-learning-cargo-risk.git
cd machine-learning-cargo-risk

# Treinamento (gera o pkl)
# Abra cargo_risk_model_training.ipynb no Colab

# App de inferencia (requer o .pkl gerado)
pip install streamlit scikit-learn pandas geopy
streamlit run app.py
```

---

## `Nota sobre o modelo`

O arquivo `melhor_modelo_risco_carga.pkl` (5MB) nao esta versionado. Execute o notebook de treinamento para gera-lo antes de rodar o app.

---

## `Conceitos aplicados`

- **`Random Forest`**: ensemble de arvores de decisao com bootstrap aggregating
- **`GridSearchCV`**: busca exaustiva de hiperparametros com validacao cruzada
- **`Pipeline sklearn`**: encapsula pre-processamento + modelo em um objeto serializado
- **`Geocodificacao`**: conversao de endereco textual em coordenadas via API Nominatim

---

## `Licenca`

Distribuido sob a licenca MIT.

---

## `Autor`

**Arthur Baptista dos Santos**
RM 565346 · Inteligencia Artificial · FIAP 2025-2026

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Arthur%20Baptista-0077B5?logo=linkedin)](https://linkedin.com/in/arthur-baptista-dos-santos)
[![GitHub](https://img.shields.io/badge/GitHub-Arthur--Baptista--dos--Santos-181717?logo=github)](https://github.com/Arthur-Baptista-dos-Santos)
