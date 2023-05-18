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
st.set_page_config( page_title='Visão Restaurantes', layout='wide')  


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



def Calc_STD( df1, Condition ):
    """
        Esta função tem por responsabilidade apresentar o desvio padrão do tempo de entrega no festival ou fora dele, através de um dataframe
    """
    cols = ['Time_taken(min)', 'Festival']                                                             #Selecionando as colunas do problema
    df1_aux = df1.loc[:, cols].groupby (['Festival']).agg({'Time_taken(min)' : ['mean', 'std']})       #Realizando os calculos com a função agg
    df1_aux.columns = ['Time_mean', 'Time_std']                                                        #Renomeando as duas novas colunas
    df1_aux = df1_aux.reset_index()                                                                    #Reindexando o indice para igualar todas as colunas
    linhas_selecionadas = df1_aux['Festival'] == Condition                                             #np.round (xxxx, 2) mostrará 2 digitos apos a virgula
    time_std = np.round(df1_aux.loc[linhas_selecionadas, 'Time_std'], 2)                               #time_std receberá apenas a média do calculo
                
    return (time_std)


def Calc_MEAN( df1, Condition ):
    """
        Esta função tem por responsabilidade apresentar a media do tempo de entrega no festival ou fora dele, através de um dataframe
    """
    cols = ['Time_taken(min)', 'Festival']                                                             #Selecionando as colunas do problema
    df1_aux = df1.loc[:, cols].groupby (['Festival']).agg({'Time_taken(min)' : ['mean', 'std']})       #Realizando os calculos com a função agg
    df1_aux.columns = ['Time_mean', 'Time_std']                                                        #Renomeando as duas novas colunas
    df1_aux = df1_aux.reset_index()                                                                    #Reindexando o indice para igualar todas as colunas
    linhas_selecionadas = df1_aux['Festival'] == Condition                                             #np.round (xxxx, 2) mostrará 2 digitos apos a virgula
    time_mean = np.round(df1_aux.loc[linhas_selecionadas, 'Time_mean'], 2)                             #time_std receberá apenas o desvio padrão do calculo
                   
    return (time_mean)


def Distance_Mediun( df1 ):
    """
        Esta função tem por responsabilidade apresentar distancia média entre os restaurantes e os pontos de entrega, através de um dataframe
    """
    #st.markdown('###### Distância Média')
    coluns = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
    #Aplicando a função apply lambda para percorrer todas as linhas das colunas selecionadas 
    #Aplicamos a função haversine (calcula a distancia entre restaurantes e destino da entrega)
    #Por ultimo criamos a coluna distance junto ao nosso Dataframe
    df1['Distance'] = ((df1.loc[:, coluns]
                           .apply (lambda x: haversine(( x['Restaurant_latitude'], 
                                                         x['Restaurant_longitude'] ), 
                                                       ( x['Delivery_location_latitude'],        
                                                         x['Delivery_location_longitude']) ), axis=1)) )
    #Calculando agora a distância média dos restaurantes aos pontos de entrega   
    #np.round é uma função do numpy que reduz a quantidade de digitos apos a virgula
    distance_mean = np.round(df1['Distance'].mean(), 2)                      
                 
    return (distance_mean)



def Pie_Distance_Mediun( df1 ):
    """
        Esta função tem por responsabilidade apresentar um grafico em pizza com a distância média de entregas por cidade
    """
    #Selecionando as colunas que desejo
    coluns = ['Restaurant_latitude', 'Restaurant_longitude', 'Delivery_location_latitude', 'Delivery_location_longitude']
    #Aplicando a função apply lambda para percorrer todas as linhas das colunas selecionadas 
    #Aplicamos a função haversine (calcula a distancia entre restaurantes e destino da entrega)
    #Por ultimo criamos a coluna distance junto ao nosso Dataframe
    df1['Distance'] = ( df1.loc[:, coluns]
                           .apply (lambda x: haversine(( x['Restaurant_latitude'],
                                                         x['Restaurant_longitude']), 
                                                       ( x['Delivery_location_latitude'],
                                                         x['Delivery_location_longitude'])), axis=1) )
    #Calculando agora a distância média dos restaurantes aos pontos de entrega
    #agruparemos por cidade com função mean e usaremos a função np.round( variável, 2) para concatenar 2 digitos apos a virgula
    avg_distance = np.round(df1.loc[:, ['City', 'Distance']].groupby(['City']).mean().reset_index(), 2)
    #montando o grafico de pizza com puxadinho
    #usaremos a função da biblioteca plotly go.Figure que recebe o parâmetro 'City' como labels e 'Distance' como value e pull com os três espaçamentos
    fig = go.Figure( data=[ go.Pie( labels=avg_distance['City'], values=avg_distance['Distance'], pull=[0, 0.1, 0])])
           
    return (fig)



def Mean_Std_City_Calc( df1 ):
    """
        Esta função tem por responsabilidade apresentar um grafico 'barmode' (de barras) com ambas as informações de media e std de tempo de entrega por cidade
    """
    cols = ['City', 'Time_taken(min)']                                              #Definindo as colunas para a operação
    df1_aux = (df1.loc[:, cols].groupby('City')
                  .agg({'Time_taken(min)': ['mean', 'std']} ) )                     #Realizando a operação com função agg
    df1_aux.columns = ['Time_mean', 'Time_std']                                     #Aqui renomeamos as duas colunas que vieram após a operação ser realizada
    df1_aux = df1_aux.reset_index()                                                 #df1_aux recebe um reset_index() deixando todas as colunas c/mesmo indice
    fig = go.Figure()                                                               #criando o gráfico
    fig.add_trace( go.Bar( name='Control',
                   x=df1_aux['City'],
                   y=df1_aux['Time_mean'],
                   error_y=dict( type='data', array=df1_aux['Time_std'] )))
    fig.update_layout(barmode='group')
                
    return (fig)


def Mean_Std_City_Traffic_Calc( df1 ):
    """
        Esta função tem por responsabilidade apresentar um grafico 'sunburst' (pizza) com tempo médio e Desvio Padrão - Entrega por cidade e tipo de tráfego
    """
    coluns = ['City', 'Road_traffic_density', 'Time_taken(min)']                    #Definindo as colunas para a operação
    df1_aux =( df1.loc[:, coluns]
                  .groupby (['City', 'Road_traffic_density'])
                  .agg({'Time_taken(min)':['mean','std']}) )                         #Realizando a operação com função agg
    df1_aux.columns = ['Time_mean', 'Time_std']                                      #Aqui renomeamos as duas colunas que vieram após a operação ser realizada
    df1_aux = df1_aux.reset_index()                                                  #df1_aux recebe um reset_index() deixando todas as colunas c/mesmo indice
    fig = (px.sunburst(df1_aux, path=['City', 'Road_traffic_density'],               #criando o gráfico
                       values='Time_mean', color='Time_std', 
                       color_continuous_scale='RdBu',
                       color_continuous_midpoint=np.average(df1_aux['Time_std'])) )

    return (fig)


def Mean_Std_Order_City_Calc( df1 ): 
    """
        Esta função tem por responsabilidade apresentar um dataframe com a media e desvio padrão do tempo dos pedidos por cidade
    """
    coluns = ['City', 'Type_of_order', 'Time_taken(min)']
    df1_aux = (df1.loc[:, ['City', 'Type_of_order', 'Time_taken(min)']]
                  .groupby (['City', 'Type_of_order'])
                  .agg({'Time_taken(min)' :['mean', 'std']}))

    df1_aux.columns = ['Time_mean', 'Time_std']
    df1_aux = df1_aux.reset_index()
            
    return (df1_aux)



        
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

st.header('MARKET PLACE - VISÃO RESTAURANTES')

#Anexando uma imagem ao meu sidebar (barra lateral) do layout
#A variável image_path receberá o caminho de onde meu arquivo alvo.jpg está (deve ser dentro da mesma pasta onde estão os demais arquivos
#A variável image receberá a função Image.open abrindo o arquivo guardado na variável acima
#st.sidebar.image é a função que receberá o arquivo aberto e o tamanho dele (width) e executará o processo

image_path = 'restaurantes.jpg'                                    
image = Image.open( image_path )
st.sidebar.image( image, width=230 )


#  CRIANDO BOTÕES NA LATERAL DO LAYOUT USANDO 'sidebar.markdown' -----------------------------------------------------------------------------------------------------------

st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )                                                   #A função st.sidebar.markdown("""---""") vai determinar uma linha de separação
#st.dataframe( df1 )                                                               #Para vermos o df1 dentro do streamlit usamos st.dataframe e definimos df1 como variável


#  CRIANDO FILTROS DENTRO DA NOSSA BARRA LATERAL (sidebar) ----------------------------------------------------------------------------------------------------------------

# a função 'slider' cria um filtro p/escolha de uma data pelo usuário. Será pautada pela maior e menor data encontrados no df1

st.sidebar.markdown( '## Selecione uma data limite' )
date_slider = st.sidebar.slider(                                                   # Função slider retornará uma data que deve ser guardada em uma variável.
      'Até qual valor?',
      value=pd.datetime( 2022, 4, 13 ),                                            # value recebe a data padrão quando o usuário não definir nenhuma data
      min_value=pd.datetime( 2022, 2, 11 ),                                          # Após consultado no df1, definimos a data minima para a consulta
      max_value=pd.datetime( 2022, 6, 4 ),                                           # Após consultado no df1, definimos a data máxima para a consulta
      format='DD/MM/YYYY' )                                                        # O format altera a forma em que a data será recebida e apresentada    
#st.header( date_slider )                                                          # A função st.header irá apresentar o valor da variável date_slider ao usuário
st.sidebar.markdown( """---""" )                                                   # A função st.sidebar.markdown("""---""") vai determinar uma linha de separação
    
# a função 'multiselect' cria um filtro multiseleção p/o template (Trânsito)

traffic_options = st.sidebar.multiselect(                                          # Guardando meu filtro dentro da variável e toda sua função
   'Quais as condições de trânsito?',                                              # Frase que aparecerá ao usuário dentro do nosso filtro
   ['Low', 'Medium', 'High', 'Jam'],                                               # Passadas como lista, estas serão as opções apresentadas ao usuário
   default=['Low']  )                                                              # Definindo nosso valor padrão, caso não haja manifestação de escolha do usuário.
st.sidebar.markdown( """---""" )   

# a função 'multiselect' cria um filtro multiseleção p/o template (Tipo de pedido)

order_options = st.sidebar.multiselect(                                            #Guardando meu filtro dentro da variável e toda sua função
   'Quais os tipos de pedidos?',                                                   #Frase que aparecerá ao usuário dentro do nosso filtro
   ['Snack', 'Drinks', 'Buffet', 'Meal'], 
   default=['Snack']  )                                                            #Definindo nosso valor padrão, caso não haja manifestação de escolha do usuário.
st.sidebar.markdown( """---""" )                                                   #A função st.sidebar.markdown("""---""") vai determinar uma linha de separação

# a função 'multiselect' cria um filtro multiseleção p/o template (Cidades)

city_options = st.sidebar.multiselect(                                            #Guardando meu filtro dentro da variável e toda sua função
   'Quais as cidades?',                                                           #Frase que aparecerá ao usuário dentro do nosso filtro
   ['Metropolitian', 'Semi-Urban', 'Urban'], 
   default=['Metropolitian']  )                                                   #Definindo nosso valor padrão, caso não haja manifestação de escolha do usuário.
st.sidebar.markdown( """---""" )   
st.sidebar.markdown( 'Powered by COMUNDADE DS')


# LINKANDO FILTROS DENTRO DA NOSSA BARRA LATERAL (sidebar) P/ALTERAREM AO RECEBEREM VALORES --------------------------------------------------------------------------------

#Filtro da Data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de Trafego
linhas_selecionadas = df1['Road_traffic_density'].isin( traffic_options )      # '.isin' é a função que fará uma comparação da seleção da escolha do usuário com as opções
df1 = df1.loc[linhas_selecionadas, :]                                          # definidas dentro da variável traffic_options, da função acima.

#filtro de Pedidos
linhas_selecionadas = df1['Type_of_order'].isin( order_options )
df1 = df1.loc[linhas_selecionadas, :]

#filtro de Cidade
linhas_selecionadas = df1['City'].isin( city_options )
df1 = df1.loc[linhas_selecionadas, :]




#=========================================================================================================================================================================== 
#                                                       CRIANDO O CORPO DO STREAMLIT (função sidebar)
#===========================================================================================================================================================================

# CRIANDO ABAS NO CORPO PRINCIPAL DA TELA DO MEU STREAMLIT -----------------------------------------------------------------------------------------------------------------

#a função st.tabs criará as abas passadas através de uma lista, os nomes das tags que queremos criar
tab1, tab2, tab3 = st.tabs ( ['Visão Gerencial', '_', '_'] )                                              #Criando tres botões de opção

with tab1:
        with st.container():
            col1, col2, col3 = st.columns(3)
        
            with col1:
                delivery_unique = ( len( df1['Delivery_person_ID'].unique() ))
                col1.metric('Entregadores únicos', delivery_unique)
                          
            with col2:
                time_std = Calc_STD( df1, Condition='Yes' )
                col2.metric('Festival - STD', time_std)                                           #col.metric apresentará a informação desejada   
            
            with col3:
                time_mean = Calc_MEAN( df1, Condition='Yes' )
                col3.metric('Festival - MEAN', time_mean)                                         #col.metric apresentará a informação desejada
        
        with st.container():
            col1, col2, col3 = st.columns(3)
            
            with col1:
                distance_mean = Distance_Mediun( df1 )
                col1.metric('Distância Média', distance_mean) 
         
            with col2:
                time_std = Calc_STD( df1, Condition='No' )
                col2.metric('Out_Festival - STD', time_std)
                         
            with col3:
                time_mean = Calc_MEAN( df1, Condition='No' )
                col3.metric('Out_Festival - MEAN', time_mean)                                       #col.metric apresentará a informação desejada 
                   
           
        with st.container():
            st.markdown('## Distância média de entrega por cidade')
            fig = Pie_Distance_Mediun( df1 )
            st.plotly_chart(fig)                                                                    #st.plotly_chart apresentará o gráfico definido acima
           
        with st.container():
            st.markdown("""___""")
            st.markdown('## Tempo Médio e Desvio Padrão - Entrega por Cidade')
            fig = Mean_Std_City_Calc( df1 )
            st.plotly_chart(fig)                                                                    #st.plotly_chart apresentará o gráfico definido acimat.plotly_chart(fig)
            
        with st.container():
            st.markdown("""___""")
            st.markdown('## Tempo médio e Desvio Padrão - Entrega por cidade e tipo de tráfego')
            fig = Mean_Std_City_Traffic_Calc( df1 )
            st.plotly_chart(fig)                                                                    #st.plotly_chart apresentará o gráfico definido acima
         
        with st.container(): 
            st.markdown("""___""")
            st.markdown('## Tempo médio e Desvio Padrão - Entrega por cidade e tipo de Pedido')
            df1_aux = Mean_Std_Order_City_Calc( df1 )
            st.dataframe(df1_aux)
           
            
            
        



    
    
