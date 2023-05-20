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
st.set_page_config( page_title='Visão Entregadores', layout='wide')  



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


def Uniques_ID( df1 ):
    """
        Esta função tem por responsabilidade apresentar a média de avaliação por entregador através de um dataframe 
    """
    entregadores_unicos = (df1.loc[:, ['Delivery_person_ID', 'Delivery_person_Ratings']]
                              .groupby (['Delivery_person_ID'])
                              .mean()
                              .reset_index())
    entregadores_unicos.columns = ['ID ENTREGADOR', 'AVALIAÇÃO MÉDIA']
       
    return( entregadores_unicos )



def Mean_Std_Traffic( df1 ):       
    """
        Esta função tem por responsabilidade apresentar a média e o desvio padrão por condição de trânsito através de um dataframe
    """
    media_desvio = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                       .groupby (['Road_traffic_density'])
                       .agg({'Delivery_person_Ratings' : ['mean', 'std']}))
    media_desvio.columns = ['Média', 'Desvio Padrão']
    media_desvio.reset_index()
                
    return (media_desvio)


def Mean_Std_Weatherconditions( df1 ):
    """
        Esta função tem por responsabilidade apresentar a média e o desvio padrão por clima através de um dataframe
    """
    media_desvio = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                       .groupby (['Weatherconditions'])
                       .agg({'Delivery_person_Ratings' : ['mean', 'std']}))
                
    media_desvio.columns = ['Média', 'Desvio Padrão']                                      #Defnindo os nomes para as duas colunas retornadas pelo agg
    media_desvio.reset_index()                                                             #resetando o index para todos estarem em um mesmo padrão
                
    return (media_desvio)



def TopIn_Ten( df1 ):
    """
        Esta função tem por responsabilidade apresentar os dez entregadores mais repidos através de um dataframe
    """
    df2 = (df1.loc[:, ['City', 'Delivery_person_ID', 'Time_taken(min)']]
              .groupby (['City','Delivery_person_ID'])
              .min()
              .sort_values(['City', 'Time_taken(min)'],ascending=True).reset_index())

    aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10).reset_index(drop=True)
    aux01.columns = ['CIDADE', 'ENTREGADOR', 'TEMPO']                                               #Aqui estamos definindo novos nomes para nossas colunas
    aux02 = df2.loc[df2['City'] == 'Urban', :].head(10).reset_index(drop=True) 
    aux02.columns = ['CIDADE', 'ENTREGADOR', 'TEMPO']
    aux03 = df2.loc[df2["City"] == 'Semi-Urban', :].head(10).reset_index(drop=True)
    aux03.columns = ['CIDADE', 'ENTREGADOR', 'TEMPO']
           
    mais_rapidos = pd.concat( [aux01, aux02, aux03] ).reset_index(drop=True)                        #pd.concat é uma função do pandas p/concatenar dataframes
          
    return (mais_rapidos)


        
def TopDown_Ten( df1 ):
    """
        Esta função tem por responsabilidade apresentar os dez entregadores mais lentos através de um dataframe
    """
    df2 = ((df1.loc[:, ['City', 'Delivery_person_ID', 'Time_taken(min)']]
               .groupby (['City','Delivery_person_ID'])
               .max()
               .sort_values(['City', 'Time_taken(min)'],ascending=True).reset_index()))
    
    aux01 = df2.loc[df2['City'] == 'Metropolitian', :].tail(10).reset_index(drop=True)
    aux01.columns = ['CIDADE', 'ENTREGADOR', 'TEMPO']                                             #Aqui estamos definindo novos nomes para nossas colunas
    aux02 = df2.loc[df2['City'] == 'Urban', :].tail(10).reset_index(drop=True)                    # .tail(10) vai me mostrar as ultimas 10 linhas do meu dataframe
    aux02.columns = ['CIDADE', 'ENTREGADOR', 'TEMPO']
    aux03 = df2.loc[df2["City"] == 'Semi-Urban', :].tail(10).reset_index(drop=True)
    aux03.columns = ['CIDADE', 'ENTREGADOR', 'TEMPO']
            
    mais_lentos = pd.concat( [aux01, aux02, aux03] ).reset_index(drop=True)
           
    return (mais_lentos)        
        
        
        
        
#=========================================================================================================================================================================== 
#                                    INICIO DA ESTRUTURA LÓGICA DO CÓDIGO - CONSTRUINDO O STREAMLIT -  A VISÃO ENTREGADORES
#===========================================================================================================================================================================

# IMPORT DATASET 
df = pd.read_csv( 'dataset/train.csv' )

# LIMPANDO DATASET 
df1 = clean_code( df )



#=========================================================================================================================================================================== 
#                                                         CRIANDO A BARRA LATERAL (função sidebar) 
#===========================================================================================================================================================================

st.header('MARKET PLACE - VISÃO ENTREGADORES')

#Anexando uma imagem ao meu sidebar (barra lateral) do layout
#A variável image_path receberá o caminho de onde meu arquivo alvo.jpg está (deve ser dentro da mesma pasta onde estão os demais arquivos
#A variável image receberá a função Image.open abrindo o arquivo guardado na variável acima
#st.sidebar.image é a função que receberá o arquivo aberto e o tamanho dele (width) e executará o processo

image_path = 'entregadores.jpg'                                    
image = Image.open( image_path )
st.sidebar.image( image, width=230 )


#  CRIANDO BOTÕES NA LATERAL DO LAYOUT USANDO 'sidebar.markdown' -----------------------------------------------------------------------------------------------------------

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )                                                   #A função st.sidebar.markdown("""---""") vai determinar uma linha de separação
#st.dataframe( df1 )                                                               #Para vermos o df1 dentro do streamlit usamos st.dataframe e definimos df1 como variável


#  CRIANDO FILTROS DENTRO DA NOSSA BARRA LATERAL (sidebar) -----------------------------------------------------------------------------------------------------------------

# a função 'slider' cria um filtro p/escolha de uma data pelo usuário. Será pautada pela maior e menor data encontrados no df1

st.sidebar.markdown('## Selecione uma data limite' )
date_slider = st.sidebar.slider(                                         # Função slider retornará uma data que deve ser guardada em uma variável.
      'Até qual valor?',                                                 # Usamos pd.to_datetime p/definir a data -.to_pydatetime() p/chamar função no PY
      value=pd.to_datetime('2022, 4, 13').to_pydatetime(),               # value recebe a data padrão quando o usuário não definir nenhuma data
      min_value=pd.to_datetime('2022, 2, 11').to_pydatetime(),           # Após consultado no df1, definimos a data minima para a consulta
      max_value=pd.to_datetime('2022, 6, 4').to_pydatetime(),            # Após consultado no df1, definimos a data máxima para a consulta
      format='DD-MM-YYYY')                                               # O format altera a forma em que a data será recebida e apresentada    
#st.header( date_slider )                                                # A função st.header irá apresentar o valor da variável date_slider ao usuário
st.sidebar.markdown( """---""" )                                         # A função st.sidebar.markdown("""---""") vai determinar uma linha de separação
    
# a função 'multiselect' cria um filtro multiseleção p/o template (Trânsito)

traffic_options = st.sidebar.multiselect(                                          # Guardando meu filtro dentro da variável e toda sua função
   'Quais as condições de trânsito?',                                              # Frase que aparecerá ao usuário dentro do nosso filtro
   ['Low', 'Medium', 'High', 'Jam'],                                               # Passadas como lista, estas serão as opções apresentadas ao usuário
   default=['Low']  )                                                              # Definindo nosso valor padrão, caso não haja manifestação de escolha do usuário.
st.sidebar.markdown( """---""" )   

# a função 'multiselect' cria um filtro multiseleção p/o template (Clima)

weather_options = st.sidebar.multiselect(                                          # Guardando meu filtro dentro da variável e toda sua função
   'Quais as condições de clima?',                                                 # Frase que aparecerá ao usuário dentro do nosso filtro
   ['conditions Cloudy', 'conditions Fog', 'conditions Sandstorms', 
    'conditions Stormy', 'conditions Sunny', 'conditions Windy' ], 
   default=['conditions Cloudy']  )                                                # Definindo nosso valor padrão, caso não haja manifestação de escolha do usuário.
st.sidebar.markdown( """---""" )                                                   # A função st.sidebar.markdown("""---""") vai determinar uma linha de separação
st.sidebar.markdown( 'Powered by COMUNDADE DS')


# LINKANDO FILTROS DENTRO DA NOSSA BARRA LATERAL (sidebar) P/ALTERAREM AO RECEBEREM VALORES --------------------------------------------------------------------------------

#Filtro da Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de Trafego
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )      # '.isin' é a função que fará uma comparação da seleção da escolha do usuário com as opções
df1 = df1.loc[linhas_selecionadas, :]                                          # definidas dentro da variável traffic_options, da função acima.

#filtro de Clima
linhas_selecionadas = df1['Weatherconditions'].isin( weather_options )
df1 = df1.loc[linhas_selecionadas, :]




#=========================================================================================================================================================================== 
#                                                       CRIANDO O CORPO DO STREAMLIT (função sidebar)
#===========================================================================================================================================================================

# CRIANDO ABAS NO CORPO PRINCIPAL DA TELA DO MEU STREAMLIT -----------------------------------------------------------------------------------------------------------------

#a função st.tabs criará as abas passadas através de uma lista, os nomes das tags que queremos criar
tab1, tab2, tab3 = st.tabs( ['Visão Geral', '_', '_'] )                        #Criando tres botões de opção

with tab1:                                                                     #Definindo o primeiro botão
    with st.container():                                                       #Determinando que ele será um container e receberá um titulo
        st.header( 'METRICAS GERAIS' )
        
        col1, col2, col3, col4 = st.columns(4, gap='large')                    #Aqui defino que meu container terá 4 colunas. A distancia 'large'
      
        with col1:                                                             #Aqui definirei o que estará dentro da primeira coluna
            max_age = df1['Delivery_person_Age'].max()
            st.markdown('##### ENTREGADOR')
            col1.metric('Maior Idade', max_age)                                #col(x).metric irá apresentar o resultado recebido pela variávl max_age
        with col2:                                                             #Aqui definirei o que estará dentro da segundaa coluna
            min_age = df1['Delivery_person_Age'].min()                         #col(x).metric irá apresentar o resultado recebido pela variávl min_age
            st.markdown('##### ENTREGADOR')
            col2.metric('Menor Idade', min_age)
        with col3:                                                             #Aqui definirei o que estará dentro da terceira coluna
            max_condition = df1['Vehicle_condition'].max()
            st.markdown('##### VEÍCULO')
            col3.metric('Melhor condição', max_condition)
        with col4:                                                             #Aqui definirei o que estará dentro da quarta coluna
            min_condition = df1['Vehicle_condition'].min()
            st.markdown('##### VEÍCULO')
            col4.metric('Pior condição', min_condition)
            
    with st.container():                                                       #Determinando aqui meu segundo container dentro da tab1
        st.markdown( """---""" )
        st.header( 'AVALIAÇÕES' )
                     
        col1, col2 = st.columns(2, gap='large')
    
        with col1:
            st.markdown( '##### AVALIÇÃO MÉDIA POR ENTREGADOR' )
            entregadores_unicos = Uniques_ID( df1 )
            st.dataframe( entregadores_unicos )                                            #st.dataframe é utilizado para fazer a apresetação do dataframe/colunas
            
        with col2:
            with st.container():
                st.markdown( '##### AVALIÇÃO MÉDIA E DESVIO PADRÃO POR TRÂNSITO' )
                media_desvio = Mean_Std_Traffic( df1 )
                st.dataframe(media_desvio) 
                
            with st.container():  
                st.markdown( '##### AVALIÇÃO MÉDIA E DESVIO PADRÃO POR CLIMA' )
                media_desvio = Mean_Std_Weatherconditions( df1 )
                st.dataframe(media_desvio)
                                
    with st.container():
        st.markdown( """___""" )
        st.header( 'AVALIAÇÕES ENTREGADORES' )
       
        col1, col2 = st.columns(2, gap='large')
        
        with col1:
            st.markdown( '##### OS DEZ MAIS RÁPIDOS POR CIDADE' )
            mais_rapidos = TopIn_Ten( df1 )
            st.dataframe(mais_rapidos)
          
        with col2:    
            st.markdown( '##### OS DEZ MAIS LENTOS POR CIDADE' )
            mais_lentos = TopDown_Ten( df1 )
            st.dataframe(mais_lentos)
            
           
        
            