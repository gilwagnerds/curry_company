import streamlit as st
from PIL import Image                        #biblioteca usada para se importar as imagens das páginas

st.set_page_config(                          #esta função unirá as páginas buscando-as na página 'pages'
    page_title="Home")

#Trazendo a imagem da nossa logo para a junção da nossa página

#image_path = '/Users/usuario 1/gilwagner/repos/ftc_programacao_python/'     
image = Image.open( 'alvo2.jpg' )                               
st.sidebar.image( image, width=230 )

#Aqui determinamos as mesmas medidas da página lateral feita por nós nas très páginas anteriores, sem os filtros
st.sidebar.markdown( '# Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown( """---""" )  

st.write( '# Curry Company Growth Dashboard')                            #Aqui estamos colocando um título na nossa apresentação inicial da página

st.markdown(                                  #Aqui trazemos as instruções para uso da página e suas funcionalidades. 
    """
    Growth Dashboard foi construído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão geográfica: Insights de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurantes:
        - Indicadores semanais de crescimento dos restaurantes
    ### Ask for Help
    - Time de Data Science no Discord
        -@gillgner
    """ )