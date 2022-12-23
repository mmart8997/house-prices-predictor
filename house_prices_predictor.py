
# arquivo de deploy do modelo de previsao dos precos dos imoveis


# bibliotecas utilizadas

import streamlit as st
import numpy as np
import pandas as pd
import pickle
import folium
from streamlit_folium import folium_static
import streamlit.components.v1 as components
from folium import plugins


# dicionario com os nomes dos bairros e as informações de latitude e longitude

dict_bairro ={
            'bairro': 
            [
             'Aclimação'
            ,'Barcelona'
            ,'Boa_Vista'
            ,'Ceramica'
            ,'Fundaçao'
            ,'Ipiranga'
            ,'Jardim_São_Caetano'
            ,'Maua'
            ,'Nova_Gerti'
            ,'Olímpico'
            ,'Osvaldo_Cruz'
            ,'Santa_Maria'
            ,'Santa_Paula'
            ,'Santo_Antônio'
            ,'Saúde'
            ,'Vila_Mariana'
            ,'Vila_Prudente'
            ],
            'latitude': 
            [
             -23.571487
            ,-23.6221281
            ,-23.6420773
            ,-23.626513
            ,-23.6042241
            ,-23.5880585
            ,-23.6377129
            ,-23.6431148
            ,-23.6422105
            ,-23.6286307
            ,-23.629477
            ,-23.6271534
            ,-23.6332595
            ,-23.6176297
            ,-23.6193695
            ,-23.6183379
            ,-23.589702
            ],
            'longitude':
            [
             -46.6309716
            ,-46.5523766
            ,-46.5583982
            ,-46.5752628
            ,-46.5715443
            ,-46.6041977
            ,-46.5800822
            ,-46.5716484
            ,-46.5656252
            ,-46.5608071
            ,-46.576397
            ,-46.5668298
            ,-46.5535808
            ,-46.5668298
            ,-46.5752628
            ,-46.6354972
            ,-46.6346381
            ]
            }

# transforma o dicionario em dataframe 

df = pd.DataFrame(dict_bairro)

# variaveis com as caracteristicas do imovel

quarto = [1,2,3,4]
banheiro = [1,2,3,4]
vaga = [1,2,3,4]
bairro = [
          'Aclimação'
         ,'Barcelona'
         ,'Boa_Vista'
         ,'Ceramica'
         ,'Fundaçao'
         ,'Ipiranga'
         ,'Jardim_São_Caetano'
         ,'Maua'
         ,'Nova_Gerti'
         ,'Olímpico'
         ,'Osvaldo_Cruz'
         ,'Santa_Maria'
         ,'Santa_Paula'
         ,'Santo_Antônio'
         ,'Saúde'
         ,'Vila_Mariana'
         ,'Vila_Prudente'
         ]



# titulo, subtitulo e instrução

st.header('Previsão do valor do imóvel')
st.subheader('Com base nas características do imóvel e bairro escolhido, veja qual é valor estimado da sua próxima residência.')
st.write('Informe as características do imóvel abaixo:')

# separacao dos selectbox em colunas

col0, col1, col2, col3 = st.columns(4)


with col0:
    q_bairro = st.selectbox(
        'Bairro:',
        bairro)

with col1:
    q_quarto = st.selectbox(
    'Quartos:',
     quarto)

with col2:
    q_banheiro = st.selectbox(
    'Banheiros:',
     banheiro)

with col3:
    q_vaga = st.selectbox(
    'Vagas:',
     vaga)

# seleciona as coordenadas do bairro para inclusao do marcador no mapa

filtro = df[(df['bairro']==q_bairro)].values.tolist()

# coloca o mapa dentro de uma caixa que pode ser expandida

with st.expander('Veja o mapa'):
    
    # configuracao inicial do mapa

    map = folium.Map(
                    location=[filtro[0][1], filtro[0][2]]
                    ,zoom_start=13
                    )

    # coloca o marcador no mapa

    tooltip = q_bairro
    folium.Marker(
            [filtro[0][1], filtro[0][2]], popup=q_bairro, tooltip=tooltip
        ).add_to(map)


    # insere o mapa ao contexto

    folium_static(map, width=700, height=280)


# cria um slider para a area do imovel
q_area = st.slider(
    'Área em metros quadrados:'
    ,min_value=100
    ,max_value=400
    )

# carregar modelo
arquivo = 'modelo_treinado_20221220.sav'
loaded_model = pickle.load(open(arquivo,'rb'))

# cria a funcao para estimar o valor do imovel

def prever_resultado(
                      area
                     ,quarto
                     ,banheiro
                     ,vagas_garagem
                     ,Aclimação
                     ,Barcelona
                     ,Boa_Vista
                     ,Ceramica
                     ,Fundaçao
                     ,Ipiranga
                     ,Jardim_São_Caetano
                     ,Maua
                     ,Nova_Gerti
                     ,Olímpico
                     ,Osvaldo_Cruz
                     ,Santa_Maria
                     ,Santa_Paula
                     ,Santo_Antônio
                     ,Saúde
                     ,Vila_Mariana
                     ,Vila_Prudente
       ):

# cria o input para receber as caracteristicas do imovel

    input = np.array([[np.log(float(area))
                     ,quarto
                     ,banheiro
                     ,vagas_garagem
                     ,Aclimação
                     ,Barcelona
                     ,Boa_Vista
                     ,Ceramica
                     ,Fundaçao
                     ,Ipiranga
                     ,Jardim_São_Caetano
                     ,Maua
                     ,Nova_Gerti
                     ,Olímpico
                     ,Osvaldo_Cruz
                     ,Santa_Maria
                     ,Santa_Paula
                     ,Santo_Antônio
                     ,Saúde
                     ,Vila_Mariana
                     ,Vila_Prudente
    ]]).astype(np.float64)

    previsao = loaded_model.predict(input)

    return previsao


# condicoes para a exibicao da previsao


if q_bairro == 'Aclimação':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)[0]))
if q_bairro == 'Barcelona':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)[0]))
if q_bairro == 'Boa_Vista':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0)[0]))
if q_bairro == 'Ceramica':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0)[0]))
if q_bairro == 'Fundaçao':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0)[0]))
if q_bairro == 'Ipiranga':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0)[0]))
if q_bairro == 'Jardim_São_Caetano':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0)[0]))
if q_bairro == 'Maua':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0)[0]))
if q_bairro == 'Nova_Gerti':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0)[0]))
if q_bairro == 'Olímpico':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0)[0]))
if q_bairro == 'Osvaldo_Cruz':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0)[0]))
if q_bairro == 'Santa_Maria':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0)[0]))
if q_bairro == 'Santa_Paula':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0)[0]))
if q_bairro == 'Santo_Antônio':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0)[0]))
if q_bairro == 'Saúde':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0)[0]))
if q_bairro == 'Vila_Mariana':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0)[0]))
if q_bairro == 'Vila_Prudente':
    st.subheader('O valor previsto é: R$ {:,.2f}'.format(prever_resultado(q_area,q_banheiro,q_vaga,q_quarto,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1)[0]))


st.write('*Nota: O modelo de previsão foi criado com base em 11.433 anúncios imóveis coletados em 16/08/2022*')