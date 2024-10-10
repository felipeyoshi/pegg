import base64
import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from utils.mysql_utils import insert_form_data
from utils.llm_utils import ReportGenerator
from utils.smtp_utils import send_email
from utils.score_utils import calcular_score_ontem, calcular_score_amanha

def plot_gauge(score, title, max_val, labels, colors):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': title},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, max_val]},
            'bar': {'color': '#EE7798'},
            'steps': [
                {'range': [labels[i], labels[i+1]], 'color': colors[i]} for i in range(len(labels)-1)
            ]
        }
    ))
    config = {
        'displayModeBar': False
    }
    st.plotly_chart(fig, use_container_width=True, config=config, key=title)
    return fig

def validate_date_format(date_str):
    try:
        datetime.datetime.strptime(date_str, '%d/%m/%Y')
        return True
    except ValueError:
        return False

EMAIL_BODY = """Parabéns!

Você está recebendo o resultado de seu Teste dos Princípios, desenvolvido pela plataforma de Educação para Gentileza e Generosidade, com o mapeamento das suas atitudes de gentileza, generosidade, solidariedade, sustentabilidade, diversidade, respeito e cidadania, mapeadas no seu ontem e planejadas para o seu amanhã, com dicas especiais geradas por inteligência artificial para inspirar suas atitudes e as pessoas ao seu redor!

Lembrete: para mudarmos o mundo é fundamental conhecimento e autoconhecimento!
Para saber mais e conhecer metodologias, materiais e ventos específicos para escolas, famílias, jovens, empresas e organizações, além de estudos e pesquisas, acesse https://www.gentilezagenerosidade.org.br/
"""

openai_key = st.secrets["secrets"]["OPENAI_KEY"]

tabs = st.tabs(['APRESENTAÇÃO', 'AUTOANÁLISE', 'MENSURAÇÃO', 'PONTUAÇÃO', 'PROGRAMAÇÃO', 'COMPROMISSO', 'RELATÓRIO'])

with tabs[0]:
    st.image('./images/pegg_intro_header.png')
    st.title('Desafio do Ontem e do Amanhã')
    st.markdown('### O objetivo deste teste, desenvolvido pela plataforma de Educação para Gentileza e Generosidade (https://gentilezagenerosidade.org.br), é estimular você para um auto desafio, avaliando como você se comporta quando o assunto são os 7 Princípios da Educação para Gentileza, Generosidade, Solidariedade, Sustentabilidade, Diversidade, Respeito e Cidadania.')
    st.markdown('### Tem a fase do ontem, quando você mapeia e reflete sobre o que você já fez; o hoje, para você refletir; e a fase do amanhã, quando você planeja o que pretende fazer. O resultado trará uma análise sociocomportamental das suas atitudes, com recomendações muito especiais preparadas por inteligência artificial, em nome de grandes referências no assunto.')
    st.markdown('### Preparado?**')
    st.markdown('**'+'Clique na seção "AUTOANÁLISE" para começar!'+'**')

with tabs[1]:
    questions_1 = ['EU FUI GENTIL?', 'EU FUI GENEROSO?', 'EU FUI SUSTENTÁVEL?', 'EU FUI RESPEITOSO?', 'EU AGI COM DIVERSIDADE?', 
                 'EU FUI CIDADÃO?', 'EU FUI SOLIDÁRIO?']
    ratings_1 = []
    st.image('./images/pegg_header.png')
    st.subheader('Pensando em suas atitudes durante o dia de ontem, selecione de 0 a 10, em suas respectivas categorias, a quantidade de vezes em que você  colocou em prática, com as pessoas ao seu redor, cada um dos 7PEGG:')
    for q in questions_1:
        ratings_1.append(st.slider("**"+q+"**", min_value=1, max_value=10, step=1))
    df_1 = pd.DataFrame(dict(question=questions_1, rating=ratings_1))
    df_1 = pd.concat([df_1, df_1.iloc[[0]]]).reset_index(drop=True)
    st.markdown('**'+'Clique na seção "MENSURAÇÃO" para continuar!'+'**')

with tabs[2]:
    st.image('./images/pegg_header.png')
    st.subheader('Veja o resultado gerado por suas respostas nesta fase diagnóstica e avalie o formato formado de acordo com a legenda:')
    fig_1 = go.Figure()
    colors = ["#FF0000",'#FFFF00', '#008000']
    ranges = [3, 6, 10]
    for r, color in reversed(list(zip(ranges, colors))):
        fig_1.add_trace(go.Scatterpolar(
            r=[r] * len(df_1),
            theta=df_1['question'],
            fill='toself',
            fillcolor=color,
            line=dict(width=2, color='white'),
            opacity=0.5,
        ))
    fig_1.add_trace(go.Scatterpolar(
        r=df_1['rating'],
        theta=df_1['question'],
        fill='toself',
        line=dict(width=2, color='#EE7798'),
        fillcolor='rgba(0,0,0,0)',
    ))
    fig_1.update_layout(
        polar=dict(
            radialaxis=dict(showline=False, range=[0, 10]),
        ),
        showlegend=False,
        dragmode=False
    )
    st.plotly_chart(fig_1, use_container_width=True, config={'displayModeBar':False}, key='key_1')
    st.subheader('Sobre o desenho: está despontado ou mais equilibrado? Avalie o que está em alta e o que está em baixa e reflita sobre os motivos.')
    col1, col2 = st.columns(2)
    with col1:
        st.image('./images/pegg_disco_1.png')
    with col2:
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('**- Desenhos mais desapontados:** avaliar o que está em alta e o que está em baixa e refletir sobre os motivos.')
        st.markdown('**- Desenhos mais equilibrados:** estou mais equilibrado para o centro do círculo ou para as bordas.')
    st.subheader('Sobre a localização dos pontos no gráfico:')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image('./images/pegg_disco_2.png')
        st.markdown('Preciso repensar a qualidade das minhas atitudes.')
    with col2:
        st.image('./images/pegg_disco_3.png')
        st.markdown('Posso atuar de forma melhor e buscar modelos de inspiração.')
    with col3:
        st.image('./images/pegg_disco_4.png')
        st.markdown('Estou indo bem e preciso me manter assim, inspirando as pessoas ao meu redor.')
    st.markdown('**'+'Clique na seção "PONTUAÇÃO" para continuar!'+'**')

with tabs[3]:
    score_ontem = calcular_score_ontem(df_1)
    st.image('./images/pegg_header.png')

    st.subheader('Confira a qualidade das suas atitudes conferindo a tabela e analisando a sua pontuação.')

    gauge1 = plot_gauge(score_ontem['solidarias'], 'ATITUDES SOLIDÁRIAS', 30, [0, 11, 21, 31], ['#FF0000', '#FFFF00', '#008000'])
    st.text('ATITUDES SOLIDÁRIAS = GENTILEZA + GENEROSIDADE + SOLIDARIEDADE')
    if score_ontem['solidarias'] < 11:
        st.error('Atenção! Você pode mais, muito mais!') 
    elif score_ontem['solidarias'] < 21:
        st.warning('Foco! Não desista de fazer a diferença!')
    elif score_ontem['solidarias'] < 31:
        st.success('Parabéns! Continue inspirado e inspirando!')
    gauge2 = plot_gauge(score_ontem['cidadas'], 'ATITUDES CIDADÃS', 20, [0, 7, 14, 21], ['#FF0000', '#FFFF00', '#008000'])
    st.text('ATITUDES CIDADÃS = RESPEITO + CIDADANIA')
    if score_ontem['cidadas'] < 7:
        st.error('Alerta geral! Melhorar o mundo começa por você!') 
    elif score_ontem['cidadas'] < 14:
        st.warning('Determinação! Quem persiste sempre alcança!')
    elif score_ontem['cidadas'] < 21:
        st.success('Incrível! Continue sempre assim, e além!')
    gauge3 = plot_gauge(score_ontem['inclusivas'], 'ATITUDES INCLUSIVAS', 30, [0, 11, 21, 31], ['#FF0000', '#FFFF00', '#008000'])
    st.text('ATITUDES INCLUSIVAS = DIVERSIDADE + RESPEITO + GENTILEZA')
    if score_ontem['inclusivas'] < 11:
        st.error('Atenção! Você pode mais, muito mais!') 
    elif score_ontem['inclusivas'] < 21:
        st.warning('Foco! Não desista de fazer a diferença!')
    elif score_ontem['inclusivas'] < 31:
        st.success('Parabéns! Continue inspirado e inspirando!')
    gauge4 = plot_gauge(score_ontem['sustentaveis'], 'ATITUDES SUSTENTÁVEIS', 20, [0, 7, 14, 21], ['#FF0000', '#FFFF00', '#008000'])
    st.text('ATITUDES SUSTENTÁVEIS = SUSTENTABILIDADE + CIDADANIA')
    if score_ontem['sustentaveis'] < 7:
        st.error('Alerta geral! Melhorar o mundo começa por você!') 
    elif score_ontem['sustentaveis'] < 14:
        st.warning('Determinação! Quem persiste sempre alcança!')
    elif score_ontem['sustentaveis'] < 21:
        st.success('Incrível! Continue sempre assim, e além!')
    gauge5 = plot_gauge(score_ontem['sociotransformadoras'], 'ATITUDES SOCIOTRANSFORMADORAS', 70, [0, 24, 47, 71], ['#FF0000', '#FFFF00', '#008000'])
    st.text('ATITUDES SOCIOTRANSFORMADORAS = GENTILEZA + GENEROSIDADE + SOLIDARIEDADE +') 
    st.text('+ SUSTENTABILIDADE + DIVERSIDADE + RESPEITO + CIDADANIA')
    if score_ontem['sociotransformadoras'] < 24:
        st.error('Cuidado! Cuidar do próximo é se cuidar também.') 
    elif score_ontem['sociotransformadoras'] < 47:
        st.warning('Muito bom! Siga sempre com força de vontade.')
    elif score_ontem['sociotransformadoras'] < 71:
        st.success('Supreendente! Seu exemplo transforma vidas.')

    gauge1_base64 = base64.b64encode(gauge1.to_image(format="png")).decode('utf-8')
    gauge2_base64 = base64.b64encode(gauge2.to_image(format="png")).decode('utf-8')
    gauge3_base64 = base64.b64encode(gauge3.to_image(format="png")).decode('utf-8')
    gauge4_base64 = base64.b64encode(gauge4.to_image(format="png")).decode('utf-8')
    gauge5_base64 = base64.b64encode(gauge5.to_image(format="png")).decode('utf-8')

    st.markdown('**'+'Clique na seção "PROGRAMAÇÃO" para continuar!'+'**')

with tabs[4]:
    questions_4 = ['EU SEREI GENTIL?', 'EU SEREI GENEROSO?', 'EU SEREI SUSTENTÁVEL?', 'EU SEREI RESPEITOSO?', 'EU AGIREI COM DIVERSIDADE?', 
                 'EU SEREI CIDADÃO?', 'EU SEREI SOLIDÁRIO?']
    ratings_4 = []
    st.image('./images/pegg_header.png')
    st.subheader('Pensando na sua performance de “ontem”, é a vez de olhar para o amanhã e se programar: selecione de 0 a 10, nas respectivas categorias, a quantidade de vezes em que você vai colocar em prática cada um dos 7PEGG:')
    for q in questions_4:
        ratings_4.append(st.slider("**"+q+"**", min_value=1, max_value=10, step=1))
    df_4 = pd.DataFrame(dict(question=questions_4, rating=ratings_4))
    df_4 = pd.concat([df_4, df_4.iloc[[0]]]).reset_index(drop=True)

    st.markdown('**'+'Clique na seção "COMPROMISSO" para finalizar!'+'**')

with tabs[5]:
    fig_4 = go.Figure()
    colors = ["#FF0000", '#FFFF00', '#008000']
    ranges = [3, 6, 10]
    for r, color in reversed(list(zip(ranges, colors))):
        fig_4.add_trace(go.Scatterpolar(
            r=[r] * len(df_4),
            theta=df_4['question'],
            fill='toself',
            fillcolor=color,
            line=dict(width=2, color='white'),
            opacity=0.5,
        ))
    fig_4.add_trace(go.Scatterpolar(
        r=df_4['rating'],
        theta=df_4['question'],
        fill='toself',
        line=dict(width=2, color='#EE7798'),
        fillcolor='rgba(0,0,0,0)',
    ))
    fig_4.update_layout(
        polar=dict(
            radialaxis=dict(showline=False, range=[0, 10]),
        ),
        showlegend=False,
        dragmode=False
    )
    score_amanha = calcular_score_amanha(df_4)
    st.image('./images/pegg_header.png')
    st.subheader('Confira o seu “antes e depois” e coloque em prática estas atitudes no seu dia a dia. Mudanças de hábitos demandam perseverança e disciplina — e você consegue.')
    st.markdown('#### Ontem')
    st.plotly_chart(fig_1, use_container_width=True, config={'displayModeBar':False}, key='key_1')
    st.markdown('#### Amanhã')
    st.plotly_chart(fig_4, use_container_width=True, config={'displayModeBar':False}, key='key_4')
    st.subheader('Precisando de um incentivo maior? Receba uma mensagem gerada por inteligência artificial, em nome de grandes referências no assunto.')
    st.markdown('**'+'Clique na seção "RELATÓRIO" para criar o relatório personalizado!'+'**')

with tabs[6]:
    st.subheader('Preencha o cadastro e receba este relatório em seu e-mail.')
    with st.form("form_relatorio"):
        first_name = st.text_input("* Nome")
        last_name = st.text_input("* Sobrenome")
        main_principle = st.selectbox("Com qual dos 7PEGG você mais se identifica?", ['', 'Gentileza', 'Generosidade', 'Solidariedade', 'Sustentabilidade',
                                                                                       'Diversidade', 'Respeito', 'Cidadania'])
        role = st.text_input("* Profissão / Atividade Exercida")
        email = st.text_input("* Seu melhor email, para receber o resultado do teste e outras novidades")
        birth_date = st.text_input("* Data de Nascimento (DIA/MÊS/ANO)")
        city = st.text_input("* Cidade")
        state = st.text_input("* Estado")
        terms = st.checkbox('Li e aceito os Termos de Uso')
        news = st.checkbox('Eu quero receber novidades e outras informações')
        message_creator = st.selectbox("Quem você gostaria que escrevesse a sua mensagem?", ['',
                                                                                             'Gandhi', 
                                                                                             'Irmã Dulce', 
                                                                                             'Madre Teresa de Calcutá',
                                                                                             'Profeta Gentileza',
                                                                                             'Nelson Mandela',
                                                                                             'Wangari Maathai'],
                                                                                             index = 0)  
        submitted = st.form_submit_button("Enviar!")
    
    with open("./pdf/termos.pdf", "rb") as file:
            btn = st.download_button(
                label="Ler os Termos de Uso",
                data=file,
                file_name="Termos-e-Condicoes-de-Uso_EGG_2023.pdf",
                mime="application/pdf"
                )
            
    if submitted:
        if not (first_name and last_name and main_principle and role and email and birth_date and city and state and terms):
            st.warning("Por favor, preencha todos os campos obrigatórios.")
        elif birth_date and not validate_date_format(birth_date):
            st.error("Formato de Data de Nascimento inválido. Por favor, use DIA/MÊS/ANO.")
        else:
            db_credentials = st.secrets["secrets"]
            insert_form_data(first_name, last_name, main_principle, role, email, birth_date, city, state, terms, news, message_creator, db_credentials)  
            st.success('Dados enviados! Aguarde a finalização do relatório e envio para o seu email. Caso não encontre em alguns minutos, verifique a Caixa de Spam.') 
            with open('./images/pegg_header.png', 'rb') as f:
                header_img = f.read()
            header_base64 = base64.b64encode(header_img).decode('utf-8')
            fig_1_base64 = base64.b64encode(fig_1.to_image(format="png")).decode('utf-8') 
            fig_4_base64 = base64.b64encode(fig_4.to_image(format="png")).decode('utf-8')
            
            score_ontem_text = str(score_ontem).replace('{', '').replace('}', '')
            score_amanha_text = str(score_amanha).replace('{', '').replace('}', '')

            smtp_credentials = st.secrets["secrets"]
            generator = ReportGenerator(openai_key)
            pdf_stream = generator.generate_html(header_base64, fig_1_base64, fig_4_base64, gauge1_base64, gauge2_base64, gauge3_base64, gauge4_base64, gauge5_base64, score_ontem, score_amanha, message_creator)
            smtp_recipient = email
            smtp_title = 'GENTILEZA E GENEROSIDADE - Desafio do Ontem e do Amanhã'
            send_email(smtp_recipient, smtp_title, EMAIL_BODY, smtp_credentials, pdf_stream)
            st.subheader('Felizes com a sua participação e dedicação. Agora é hora de somar as energias e transformar este mundo em um lugar melhor para viver e conviver.')
            st.subheader('Curtiu? Compartilhe o link com quem você sabe que vai gostar ou com quem está precisando se autoanalisar, mas ainda não tinha um teste para isso.')