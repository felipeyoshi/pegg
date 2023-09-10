import base64
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
from pdf_utils import generate_pdf
from score import calcular_score_ontem, calcular_score_amanha

tabs = st.tabs(['1.AUTOANÁLISE', '2.MENSURAÇÃO', '3.PONTUAÇÃO', '4.PROGRAMAÇÃO', '5.COMPROMISSO', '6.RELATÓRIO'])

with tabs[0]:
    questions_1 = ['EU FUI GENTIL?', 'EU FUI GENEROSO?', 'EU FUI SUSTENTÁVEL?', 'EU FUI RESPEITOSO?', 'EU AGI COM DIVERSIDADE?', 
                 'EU FUI CIDADÃO?', 'EU FUI SOLIDÁRIO?']
    ratings_1 = []
    st.image('./images/pegg_header.png')
    st.image('./images/pegg_etapa_1.png')
    for q in questions_1:
        ratings_1.append(st.slider("**"+q+"**", min_value=1, max_value=10, step=1))
    df_1 = pd.DataFrame(dict(question=questions_1, rating=ratings_1))

with tabs[1]:
    st.image('./images/pegg_header.png')
    st.image('./images/pegg_etapa_2.png')
    fig_1 = px.line_polar(df_1, r='rating', theta='question', line_close=True)
    fig_1.update_layout(polar = dict(radialaxis = dict(range = [1, 10])))
    fig_1.update_traces(line_width=1,line_color='#FF1493',fillcolor='rgba(255, 20, 147, 1)')
    st.title('RESULTADO DA AUTOANÁLISE')
    st.plotly_chart(fig_1, use_container_width=True)

with tabs[2]:
    score_ontem = calcular_score_ontem(df_1)
    st.image('./images/pegg_header.png')
    st.image('./images/pegg_etapa_3.png')

    st.title('PONTUAÇÃO OBTIDA')
    col1, col2 = st.columns(2)

    with col1:
      st.metric('SOLIDÁRIAS', score_ontem['solidarias'])
      if score_ontem['solidarias'] < 11:
          st.error('Atenção! Você pode mais, muito mais!') 
      elif score_ontem['solidarias'] < 21:
          st.warning('Foco! Não desista de fazer a diferença!')
      elif score_ontem['solidarias'] < 31:
          st.info('Parabéns! Continue inspirado e inspirando!')

    with col2:
      st.metric('CIDADÃS', score_ontem['cidadas'])
      if score_ontem['cidadas'] < 7:
          st.error('Alerta geral! Melhorar o mundo começa por você!') 
      elif score_ontem['cidadas'] < 14:
          st.warning('Determinação! Quem persiste sempre alcança!')
      elif score_ontem['cidadas'] < 21:
          st.info('Incrível! Continue sempre assim, e além!')

    col1, col2 = st.columns(2)

    with col1:
      st.metric('INCLUSIVAS', score_ontem['inclusivas'])
      if score_ontem['inclusivas'] < 11:
          st.error('Atenção! Você pode mais, muito mais!') 
      elif score_ontem['inclusivas'] < 21:
          st.warning('Foco! Não desista de fazer a diferença!')
      elif score_ontem['inclusivas'] < 31:
          st.info('Parabéns! Continue inspirado e inspirando!')

    with col2:
      st.metric('SUSTENTÁVEIS', score_ontem['sustentaveis'])
      if score_ontem['sustentaveis'] < 7:
          st.error('Alerta geral! Melhorar o mundo começa por você!') 
      elif score_ontem['sustentaveis'] < 14:
          st.warning('Determinação! Quem persiste sempre alcança!')
      elif score_ontem['sustentaveis'] < 21:
          st.info('Incrível! Continue sempre assim, e além!')

    col1, col2 = st.columns(2)
    
    with col1:
        st.metric('SOCIOTRANSFORMADORAS', score_ontem['sociotransformadoras'])
        if score_ontem['sociotransformadoras'] < 24:
            st.error('Cuidado! Cuidar do próximo é se cuidar também.') 
        elif score_ontem['sociotransformadoras'] < 47:
            st.warning('Muito bom! Siga sempre com força de vontade.')
        elif score_ontem['sociotransformadoras'] < 71:
            st.info('Supreendente! Seu exemplo transforma vidas.')

with tabs[3]:
    questions_4 = ['EU SEREI GENTIL?', 'EU SEREI GENEROSO?', 'EU SEREI SUSTENTÁVEL?', 'EU SEREI RESPEITOSO?', 'EU AGIREI COM DIVERSIDADE?', 
                 'EU SEREI CIDADÃO?', 'EU SEREI SOLIDÁRIO?']
    ratings_4 = []
    st.image('./images/pegg_header.png')
    st.image('./images/pegg_etapa_4.png')
    for q in questions_4:
        ratings_4.append(st.slider("**"+q+"**", min_value=1, max_value=10, step=1))
    df_4 = pd.DataFrame(dict(question=questions_4, rating=ratings_4))

with tabs[4]:
    st.image('./images/pegg_header.png')
    fig_4 = px.line_polar(df_4, r='rating', theta='question', line_close=True)
    fig_4.update_layout(polar = dict(radialaxis = dict(range = [1, 10])))
    fig_4.update_traces(line_width=1,line_color='#FF1493',fillcolor='rgba(255, 20, 147, 1)')

    st.title('COMO FUI ONTEM?')
    st.plotly_chart(fig_1, use_container_width=True)
    st.title('COMO SEREI AMANHÃ?')
    st.plotly_chart(fig_4, use_container_width=True)

with tabs[5]:
    with st.form("form_relatorio"):
        name = st.text_input("Nome")
        email = st.text_input("Email")  
        submitted = st.form_submit_button("Enviar")
    
    if submitted:
        st.success("Dados enviados!")
        with open('./images/pegg_header.png', 'rb') as f:
            header_img = f.read()
        header_base64 = base64.b64encode(header_img).decode('utf-8')
        fig_1_base64 = base64.b64encode(fig_1.to_image(format="png")).decode('utf-8') 
        fig_4_base64 = base64.b64encode(fig_4.to_image(format="png")).decode('utf-8')
        relatorio = generate_pdf(header_base64, fig_1_base64, fig_4_base64)
        st.components.v1.html(relatorio, height=500, scrolling=True)