#=======================================================================================================================================================================
                                                                             #LIBRARIES
#=======================================================================================================================================================================

from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go
import folium
import numpy as np

#=======================================================================================================================================================================
                                                                             #BIBLIOTECAS
#=======================================================================================================================================================================

import pandas as pd
import streamlit as st
from PIL import Image
from streamlit_folium import folium_static


#  AJUSTANDO NOSSOS GRÁFICOS A ÁREA TOTAL DE NOSSOS CONTAINERS-------------------------------------------------------------------------------------------
#Aqui estamos expandindo apresentação de nossos gráfico a toda área de nosso container. 
st.set_page_config( page_title='Visão Empresa', layout='wide')    

#=======================================================================================================================================================================
                                                                             #FUNÇÕES
#=======================================================================================================================================================================

def clean_code( df1 ):
    """
        Esta função tem por responsabilidade limpar o dataframe
        
        Tipos de limpeza:
        
        1. Remoção dos dados 'NaN';
        2. Inserção desta limpeza ao novo dataframe;
        3. Adequação de colunas ao tipo de dados correto para suas informações;
        4. Conversão do tipo de 'Texto' para 'Data';
        5. Conversão do tipo 'Texto' para 'Int';
        6. Transformando o tipo 'series' em 'string' para uso da função strip;
        7. Limpa a coluna Time_taken, retirando o (min) e deixando somente os minutos;
        8. Alterando a coluna 'Time_taken(min) para int.
        
        Imput: Dataframe
        Output: Dataframe
    """


    # Retirando as informações 'NaN ' das linhas da coluna Delivery_person_Age e selecionando os dados dentro de linhas_selecionadas
    age_clean = df1["Delivery_person_Age"]!= "NaN "
    density_clean = df1['Road_traffic_density'] != 'NaN '
    city_clean = df1['City'] != 'NaN '
    linhas_selecionadas = df1['multiple_deliveries'] != 'NaN '

    # fazendo o .loc para inserir novamente em df1 as informações com as linhas já tratadas e todas as colunas
    df1 = df1.loc[age_clean, : ].copy()
    df1 = df1.loc[density_clean, :].copy()
    df1 = df1.loc[city_clean, :].copy()
    df1 = df1.loc[linhas_selecionadas, : ].copy()


    # Alterando o tipo da coluna para int e guardando as informações novamente em df1 na coluna Delivery_person_Age
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    # Alterando o tipo da coluna Ratings de object para decimal (float)
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    # Convertendo o tipo "Texto" para "Data"
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format='%d-%m-%Y' )

    # Convertendo multiple_deliveries de texto para int
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    # Retirando os espeços de dentro das linhas de cada coluna
    # O comando ".reset_index" criará um novo index e o comando "(drop = True)" não permitirá que com a ação uma nova coluna seja criada
    # O comando "(len(df1))" do for retornará a quantidade de linhas a ser percorrida e a variável "i" irá percorrê-las
    # O comando ".strip()" irá retirar os espaços vazios da coluna. O valor desta operação deverá ser retornado ao mesmo ambiente de origem 
    #df1 = df1.reset_index(drop = True)
    #for i in range(len(df1)):
    #  df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()

    #Removendo os espacos dentro de strings/texto/object
    #a função strip não funciona para tipos 'series'. 
    #Usamos o comando str para transformar o tipo 'series' em 'string' e assim usar a função strip que em strings é aceita.

    df1.loc[:,'ID'] = df1.loc[:, 'ID'].str.strip()   
    df1.loc[:,'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:,'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:,'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:,'Festival'] = df1.loc[:, 'Festival'].str.strip()
    df1.loc[:,'City'] = df1.loc[:, 'City'].str.strip()

    #limpando a coluna Time_taken, retirando o (min) e deixando somente os minutos
    #lambda é a função que será aplicada a todo x, que são os indices de cada linda da tabela Time_taken
    #x.split é a operação que vai trocar todo valor (min) pela posição [1] da minha string (exemplo: trocará (mim) 33 por 33) que está na posição 1 da minha string. 
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: x.split( '(min)') [1])
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)

    return df1


def Order_Day( df1 ):
    """ 
        Esta função tem por responsabilidade retornar o total de pedidos por dia através a partir de um dataframe através de um gráfico de barras
    """
    coluns = ['ID', 'Order_Date']
    result = df1.loc[:, coluns].groupby (['Order_Date']).count().reset_index()
    #Aqui a variável fig recebe a função px.bar do nosso gráfico
    fig = px.bar(result, x='Order_Date', y="ID")                                   
    
    return (fig)


def Order_Traffic( df1 ):
    """ 
        Esta função tem por responsabilidade retornar a porcentagem da distribuição dos pedidos por tráfico a partir de um dataframe através de um gráfico de pizza
    """   
    df1_aux = df1.loc[:, ['ID', 'Road_traffic_density']].groupby (['Road_traffic_density']).count().reset_index()
    df1_aux['perc_ID'] = 100 * ( df1_aux['ID'] / df1_aux['ID'].sum() )
    fig = px.pie(df1_aux, values = 'perc_ID', names = 'Road_traffic_density')
    
    return (fig)


def Order_CityTraffic ( df1 ):
    """ 
        Esta função tem por responsabilidade retornar o volume de pedidos por cidade e tráfego através de um grafico de bolhas
    """  
    df1_aux = df1.loc[:, ['ID', 'City', 'Road_traffic_density']].groupby (['City', 'Road_traffic_density']).count().reset_index()    
    fig = px.scatter(df1_aux, x = 'City', y ='Road_traffic_density', size = 'ID', color = 'City')
    return (fig)


def Order_Week( df1 ):
    """ 
        Esta função tem por responsabilidade retornar o total de pedidos por semana em um gráfico de linhas
    """  
    df1['Week_of_year'] = df1['Order_Date'].dt.strftime ( '%U')
    coluns = ['ID', 'Week_of_year']
    result = df1.loc[:, coluns].groupby (['Week_of_year']).count().reset_index()
    fig = px.line(result, x='Week_of_year', y='ID')
       
    return (fig) 


def Order_IDWeek( df1 ): 
    """ 
        Esta função tem por responsabilidade retornar o total de pedidos por entregador por semana em um gráfico de linhas
    """ 
    df_aux01 = df1.loc[:, ['ID', 'Week_of_year']].groupby (['Week_of_year']).count().reset_index()
    df_aux02 = df1.loc[:, ['Delivery_person_ID', 'Week_of_year']].groupby (['Week_of_year']).nunique().reset_index()
    df_aux = pd.merge(df_aux01, df_aux02, how = 'inner')
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    fig = px.line(df_aux, x= 'Week_of_year', y = 'order_by_delivery')
        
    return( fig )
    

def Localization( df1 ):
    """ 
        Esta função tem por responsabilidade retornar a localização dos restaurantes a partir de um gráfico de mapa
    """ 
    df1_aux = (df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']]
                  .groupby (['City', 'Road_traffic_density'])
                  .median().reset_index())
   
    map = folium.Map( zoom_start=11)
    for index, location_info in df1_aux.iterrows():
        folium.Marker( [location_info['Delivery_location_longitude'],
                        location_info['Delivery_location_longitude']],
                        popup=location_info[['City', 'Road_traffic_density']]).add_to (map)
        
    folium_static( map, width=1024, height=500 )
          
    return( map )    
    
    


#=========================================================================================================================================================================== 
#                                    INICIO DA ESTRUTURA LÓGICA DO CÓDIGO - CONSTRUINDO O STREAMLIT -  A VISÃO DA EMPRESA 
#===========================================================================================================================================================================

# IMPORT DATASET 
df = pd.read_csv( 'dataset/train.csv' )

# LIMPANDO DATASET 
df1 = clean_code( df )


#=========================================================================================================================================================================== 
#                                                         CRIANDO A BARRA LATERAL (função sidebar) 
#===========================================================================================================================================================================

st.header('MARKET PLACE - VISÃO EMPRESA')

# Anexando uma imagem ao meu sidebar (barra lateral) do layout
# A variável image_path receberá o caminho de onde meu arquivo alvo.jpg está (deve ser dentro da mesma pasta onde estão os demais arquivos
# A variável image receberá a função Image.open abrindo o arquivo guardado na variável acima
# st.sidebar.image é a função que receberá o arquivo aberto e o tamanho dele (width) e executará o processo

image_path = 'empresas.jpg'                                    
image = Image.open( image_path )
st.sidebar.image( image, width=230 )


#  CRIANDO BOTÕES NA LATERAL DO LAYOUT USANDO 'sidebar.markdown' -----------------------------------------------------------------------------------------------------------

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )                              # A função st.sidebar.markdown("""---""") vai determinar uma linha de separação
#st.dataframe( df1 )                                          # Para vermos o df1 dentro do streamlit usamos st.dataframe e definimos df1 como variável



#  CRIANDO FILTROS DENTRO DA NOSSA BARRA LATERAL (sidebar) -----------------------------------------------------------------------------------------------------------------

# a função 'slider' cria um filtro p/escolha de uma data pelo usuário. Será pautada pela maior e menor data encontrados no df1

st.sidebar.markdown( '## Selecione uma data limite' )
date_slider = st.sidebar.slider(                              # Função slider retornará uma data que deve ser guardada em uma variável.
      'Até qual valor?',
      value=pd.datetime( 13, 4, 2022 ),                       # value recebe a data padrão quando o usuário não definir nenhuma data
      min_value=pd.datetime( 11, 2, 2022 ),                   # Após consultado no df1, definimos a data minima para a consulta
      max_value=pd.datetime( 6, 4, 2022 ),                    # Após consultado no df1, definimos a data máxima para a consulta
      format='DD-MM-YYYY' )                                   # O format altera a forma em que a data será recebida e apresentada    
#st.header( date_slider )                                     # A função st.header irá apresentar o valor da variável date_slider ao usuário
st.sidebar.markdown( """---""" )                              # A função st.sidebar.markdown("""---""") vai determinar uma linha de separação


# a função 'multiselect' cria um filtro multiseleção p/o template 

traffic_options = st.sidebar.multiselect(                     # Guardando meu filtro dentro da variável e toda sua função
   'Quais as condições de trânsito?',                         # Frase que aparecerá ao usuário dentro do nosso filtro
   ['Low', 'Medium', 'High', 'Jam'],                          # Passadas como lista, estas serão as opções apresentadas ao usuário
   default=['Low']  )                                         # Definindo nosso valor padrão, caso não haja manifestação de escolha do usuário.
st.sidebar.markdown( """---""" )                              # A função st.sidebar.markdown("""---""") vai determinar uma linha de separação
st.sidebar.markdown( 'Powered by COMUNDADE DS')


 
# LINKANDO FILTROS DENTRO DA NOSSA BARRA LATERAL (sidebar) P/ALTERAREM AO RECEBEREM VALORES --------------------------------------------------------------------------------

# filtro da data 
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

# filtro de trafego 
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )      # '.isin' é a função que fará uma comparação da seleção da escolha do usuário com as opções
df1 = df1.loc[linhas_selecionadas, :]                                          # definidas dentro da variável traffic_options, da função acima.




#=========================================================================================================================================================================== 
#                                                       CRIANDO O CORPO DO STREAMLIT (função sidebar)
#===========================================================================================================================================================================

# CRIANDO ABAS NO CORPO PRINCIPAL DA TELA DO MEU STREAMLIT ----------------------------------------------------------------------------------------------------------------- 

#a função st.tabs criará as abas passadas através de uma lista, os nomes das tags que queremos criar
tab1, tab2, tab3 = st.tabs( ['Visão Geral', 'Visão Tática', 'Visão Geográfica'] )

#Os 'with', assim como o 'for' relacionará tudo o que dentro dele estiver identado.  
with tab1:  
    with st.container():                                                        #Aqui criamos o 1º container do nosso layout para o nosso primeiro gráfico
        st.markdown( '### TOTAL DE PEDIDOS POR DIA' )  
        fig = Order_Day( df1 )
        # Usamos st.plotly_chart p/plotar o gráfico passando a variável 'fig' e condição 'use_container_width=True' p/que o gráfico fique do tamanho do container
        st.plotly_chart( fig, use_container_width=True )                               
                                                                                       
    with st.container():                                                               #Aqui criamos o 2º container com 1 linha e 2 colunas
        col1, col2 = st.columns(2)                                                     #Aqui col1 e col2 recebem as 2 colunas criadas por st.columns()
        with col1:                                                                     #usamos o with p/separar as colunas definindo o que vão receber
            st.markdown( '### DISTRIBUIÇÃO DOS PEDIDOS POR TRÁFEGO (%)' )
            fig = Order_Traffic( df1 )
            st.plotly_chart( fig, use_container_width=True ) 
      
        with col2:
            st.markdown( '### VOLUME DE PEDIDOS POR CIDADE E TRÁFEGO' )
            fig = Order_CityTraffic( df1 )
            st.plotly_chart( fig, use_container_width=True )
        
with tab2:
    with st.container():
        st.markdown('### QUANTIDADE DE PEDIDOS POR SEMANA') 
        fig = Order_Week( df1 )
        st.plotly_chart( fig, use_container_width=True)
 
    with st.container():
        st.markdown('### QUANTIDADE DE PEDIDOS POR ENTREGADOR POR SEMANA') 
        fig = Order_IDWeek( df1 )
        st.plotly_chart( fig, use_container_width=True)
        
with tab3:    
    st.markdown( '### LOCALIZAÇÃO CENTRAL - Cidades por tipo de Tráfego' )
    map = Localization( df1 )
   

