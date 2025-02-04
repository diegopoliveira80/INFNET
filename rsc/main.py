import pandas as pd
import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import time


def plano_fundo(colormap:dict):
    st.set_page_config(layout="wide") 
    
    col1, col2,col3 = st.columns([2,2,8])
    with col1:
        # Cores do plano de fundo
        background_color = st.selectbox("Escolha uma cor de fundo", colormap.keys())
    with col2:
        text_color = st.selectbox("Escolha a cor do texto", colormap.keys())
        st.markdown(f"""
        <style>
        .stApp {{
            background-color : {colormap[background_color]};
            color: {colormap[text_color]};
        }}
        </style>
        """, unsafe_allow_html=True)   
    

@st.cache_data
def load_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
        return df
    return None


def upload():
   
    # Upload de um arquivo
    st.title("1. Upload e Download de Arquivo CSV")
    col1,col2 = st.columns([3,6])
    with col1:
        uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="xlsx")
        return uploaded_file


def dashboard(df):
    if df is not None:
        col1,col2 = st.columns([3,6])
        with col1:
            # Utilizar Barra de Progresso e Spinners
            with st.spinner("Lendo o arquivo CSV..."):
                time.sleep(1)
                barra_progresso = st.progress(1)
                for counter in range(1,100):
                    time.sleep(0.01)
                    barra_progresso.progress(counter)  
             
                
        # Exibição dos dados checkbox
            if st.checkbox("Previa dos dados ?"):
                st.write(df.head(3))


        # Seleção dos dados dropdowns
        col1,col2 = st.columns([3,6])
        with col1:
            selecionar_colunas = st.multiselect("Selecionar colunas para exibir os dados", df.columns)
            dados_filtrados = df[selecionar_colunas]
            df['ano'] = df['ano'].astype(str)
            df['Valor'] = df['Valor'].replace(",",".").astype(float)
            
            #Filtrar dados conforme numero informado
            text_input = st.text_input("Informe um nomero para filtrar a coluna valor", "100")
            filtered_df = df[df['Valor'] < float(text_input)]
        
            with st.expander("Ver todos os dados"):
                st.write(filtered_df[selecionar_colunas])


       #Grafico comparado frequencia por cidades
        st.subheader('Comparativo entre as cidades')
        fig, ax = plt.subplots()
        df_grouped = df.groupby('cidades')['Valor'].sum().reset_index()
        ax.bar(df_grouped['cidades'].astype(str), df_grouped['Valor'], edgecolor='black')
        ax.set_title('Frequencia por cidades')
        ax.set_xlabel('Cidades')
        ax.set_ylabel('Frequencia')
        ax.set_xticks(df_grouped['cidades'].astype(str))
        ax.set_xticklabels(df_grouped['cidades'].astype(str), rotation=45, ha='right', fontsize=10)
        fig.tight_layout()
        st.pyplot(fig)
        st.write('')

        
        st.subheader('Metricas de todos os anos agrupados da cidade selecionada')
        col1, col2, col3 = st.columns([2, 2, 4])

        with col1: # Analisando os dados de uma cidade radio describe 
            selecione_linha = st.radio("Escolha uma cidade", df['cidades'].unique())
        with col2:
            calculos = df[["cidades","Valor"]]
            st.write(calculos[calculos['cidades'] == selecione_linha].describe())
        with col3: # Grafico ano
            grafico_filtrado = df[df['cidades'] == selecione_linha]
            grafico = grafico_filtrado[["ano","Valor"]]
            grafico.set_index('ano', inplace=True)
            st.bar_chart(grafico)
                

        st.subheader('Metricas de cada anos da cidade selecionada')
        calculo = df[df['cidades'] == selecione_linha]
        df_pivot = calculo.pivot_table(index="cidades",columns="ano",values="Valor",aggfunc='mean').describe()
        st.write(df_pivot)
        st.write('')

        
        
        # Gerar CSV filtrado para download
        csv = dados_filtrados.to_csv(index=False).encode('utf-8')
        
        st.download_button(
            label="Baixar Dados Filtrados",
            data=csv,
            file_name="filtered_data.csv",
            mime="text/csv"
        )
       

if __name__ == "__main__":
    plano_fundo(colormap = {
    "preto": "#000000",
    "branco" : "#FFFFFF",
    "vermelho": "#A52A2A",
    "roxo": "#800080",
    "cinza": "#808080",
    "azul": "#0000FF"
    })
    uploaded_file = upload()
    df = load_data(uploaded_file)
    dashboard(df)