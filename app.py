import base64
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
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
    df_1 = pd.concat([df_1, df_1.iloc[[0]]]).reset_index(drop=True)
    st.text('Clique na seção "2.MENSURAÇÃO" para visualizar a sua autoanálise sobre o ontem!')

with tabs[1]:
    st.image('./images/pegg_header.png')
    st.image('./images/pegg_etapa_2.png')
    fig_1 = go.Figure()
    colors = ["red", "blue", "yellow"]
    ranges = [3, 6, 10]
    for r, color in reversed(list(zip(ranges, colors))):
        fig_1.add_trace(go.Scatterpolar(
            r=[r] * len(df_1),
            theta=df_1['question'],
            fill='toself',
            fillcolor=color,
            line=dict(width=2, color='white'),  # Adding white circular contour
            opacity=0.5,
        ))
    fig_1.add_trace(go.Scatterpolar(
        r=df_1['rating'],
        theta=df_1['question'],
        fill='toself',
        line=dict(width=2, color='#FF1493'),
        fillcolor='rgba(0,0,0,0)',  # Making the fill transparent
    ))
    fig_1.update_layout(
        polar=dict(
            radialaxis=dict(showline=False, range=[0, 10]),
        ),
        showlegend=False
    )
    st.subheader('RESULTADO DA AUTOANÁLISE')
    st.plotly_chart(fig_1, use_container_width=True, config={'displayModeBar':False})

    st.text('Clique na seção "3.PONTUAÇÃO" para conferir o seu resultado!')

with tabs[2]:
    score_ontem = calcular_score_ontem(df_1)
    st.image('./images/pegg_header.png')
    st.image('./images/pegg_etapa_3.png')

    st.subheader('PONTUAÇÃO OBTIDA')
    col1, col2 = st.columns(2)

    with col1:
      st.metric('**'+'ATITUDES SOLIDÁRIAS'+'**', score_ontem['solidarias'])
      if score_ontem['solidarias'] < 11:
          st.error('Atenção! Você pode mais, muito mais!') 
      elif score_ontem['solidarias'] < 21:
          st.info('Foco! Não desista de fazer a diferença!')
      elif score_ontem['solidarias'] < 31:
          st.warning('Parabéns! Continue inspirado e inspirando!')

    with col2:
      st.metric('**'+'ATITUDES CIDADÃS'+'**', score_ontem['cidadas'])
      if score_ontem['cidadas'] < 7:
          st.error('Alerta geral! Melhorar o mundo começa por você!') 
      elif score_ontem['cidadas'] < 14:
          st.info('Determinação! Quem persiste sempre alcança!')
      elif score_ontem['cidadas'] < 21:
          st.warning('Incrível! Continue sempre assim, e além!')

    col1, col2 = st.columns(2)

    with col1:
      st.metric('**'+'ATITUDES INCLUSIVAS'+'**', score_ontem['inclusivas'])
      if score_ontem['inclusivas'] < 11:
          st.error('Atenção! Você pode mais, muito mais!') 
      elif score_ontem['inclusivas'] < 21:
          st.info('Foco! Não desista de fazer a diferença!')
      elif score_ontem['inclusivas'] < 31:
          st.warning('Parabéns! Continue inspirado e inspirando!')

    with col2:
      st.metric('**'+'ATITUDES SUSTENTÁVEIS'+'**', score_ontem['sustentaveis'])
      if score_ontem['sustentaveis'] < 7:
          st.error('Alerta geral! Melhorar o mundo começa por você!') 
      elif score_ontem['sustentaveis'] < 14:
          st.info('Determinação! Quem persiste sempre alcança!')
      elif score_ontem['sustentaveis'] < 21:
          st.warning('Incrível! Continue sempre assim, e além!')

    col1, col2 = st.columns(2)
    
    with col1:
        st.metric('**'+'ATITUDES SOCIOTRANSFORMADORAS'+'**', score_ontem['sociotransformadoras'])
        if score_ontem['sociotransformadoras'] < 24:
            st.error('Cuidado! Cuidar do próximo é se cuidar também.') 
        elif score_ontem['sociotransformadoras'] < 47:
            st.info('Muito bom! Siga sempre com força de vontade.')
        elif score_ontem['sociotransformadoras'] < 71:
            st.warning('Supreendente! Seu exemplo transforma vidas.')

    st.text('Clique na seção "4.PROGRAMAÇÃO" para planejar o seu amanhã!')

with tabs[3]:
    questions_4 = ['EU SEREI GENTIL?', 'EU SEREI GENEROSO?', 'EU SEREI SUSTENTÁVEL?', 'EU SEREI RESPEITOSO?', 'EU AGIREI COM DIVERSIDADE?', 
                 'EU SEREI CIDADÃO?', 'EU SEREI SOLIDÁRIO?']
    ratings_4 = []
    st.image('./images/pegg_header.png')
    st.image('./images/pegg_etapa_4.png')
    for q in questions_4:
        ratings_4.append(st.slider("**"+q+"**", min_value=1, max_value=10, step=1))
    df_4 = pd.DataFrame(dict(question=questions_4, rating=ratings_4))
    df_4 = pd.concat([df_4, df_4.iloc[[0]]]).reset_index(drop=True)

    fig_4 = go.Figure()
    colors = ["red", "blue", "yellow"]
    ranges = [3, 6, 10]
    for r, color in reversed(list(zip(ranges, colors))):
        fig_4.add_trace(go.Scatterpolar(
            r=[r] * len(df_4),
            theta=df_4['question'],
            fill='toself',
            fillcolor=color,
            line=dict(width=2, color='white'),  # Adding white circular contour
            opacity=0.5,
        ))
    fig_4.add_trace(go.Scatterpolar(
        r=df_4['rating'],
        theta=df_4['question'],
        fill='toself',
        line=dict(width=2, color='#FF1493'),
        fillcolor='rgba(0,0,0,0)',  # Making the fill transparent
    ))
    fig_4.update_layout(
        polar=dict(
            radialaxis=dict(showline=False, range=[0, 10]),
        ),
        showlegend=False
    )
    st.subheader('RESULTADO DA PROGAMAÇÃO')
    st.plotly_chart(fig_4, use_container_width=True, config={'displayModeBar':False})

    st.text('Clique na seção "5.COMPROMISSO" para comparar o seu ontem com o seu amanhã!')

with tabs[4]:
    st.image('./images/pegg_header.png')

    st.subheader('COMO FUI ONTEM?')
    st.plotly_chart(fig_1, use_container_width=True, config={'displayModeBar':False})
    st.subheader('COMO SEREI AMANHÃ?')
    st.plotly_chart(fig_4, use_container_width=True, config={'displayModeBar':False})

    st.text('Clique na seção "6.RELATÓRIO" caso queira gerar um resultado personalizado!')

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