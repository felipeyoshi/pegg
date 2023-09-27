from prompts.mensagem import PROMPT_MENSAGEM
from utils.openai_utils import LLM
import io
import pdfkit

class ReportGenerator:

    def __init__(self, openai_key):
        self.openai_key = openai_key

    def generate_message(self, score_ontem, score_amanha, message_creator):
        prompt_mensagem_final = PROMPT_MENSAGEM.format(score_ontem, score_amanha, message_creator)
        agent = "Você é um especialista em gentileza e generosidade."
        llm = LLM(self.openai_key)
        message = llm.get_prompt(agent, prompt_mensagem_final)
        mensagem_final = llm.get_completion(message)
        return mensagem_final

    def generate_html(self, header_base64, fig1_base64, fig2_base64, gauge1_base64, gauge2_base64, gauge3_base64, gauge4_base64, gauge5_base64, score_ontem, score_amanha, message_creator):
        message_content = self.generate_message(score_ontem, score_amanha, message_creator)
        html = f'''
        <html>
            <head>
                <style>
                    body, h2, p {{
                        font-family: "Arial", sans-serif;
                    }}
                    h2 {{
                        text-align: center;
                    }}
                    .figures-container, .gauges-container {{
                        display: flex;
                    }}
                    .figure, .gauge {{
                        margin: 0 10px;
                        text-align: center; 
                    }}            
                </style>
            </head>
            <body>
                <img src="data:image/png;base64, {header_base64}" width="980">
                
                <div class="figures-container">
                    <div class="figure">
                        <h2>Como fui ontem?</h2>
                        <img src="data:image/png;base64, {fig1_base64}" width="450">
                    </div>

                    <div class="figure">
                        <h2>Como serei amanhã?</h2>
                        <img src="data:image/png;base64, {fig2_base64}" width="450">
                    </div>
                </div>
                <h2>Como estão as minhas atitudes?</h2>
                <div class="gauges-container">
                    <div class="gauge">
                        <img src="data:image/png;base64, {gauge1_base64}" width="300">
                        <p>ATITUDES SOLIDÁRIAS = GENTILEZA + GENEROSIDADE + SOLIDARIEDADE</p>
                    </div>
                    <div class="gauge">
                        <img src="data:image/png;base64, {gauge2_base64}" width="300">
                        <p>ATITUDES CIDADÃS = RESPEITO + CIDADANIA</p>
                    </div>
                    <div class="gauge">
                        <img src="data:image/png;base64, {gauge3_base64}" width="300">
                        <p>ATITUDES INCLUSIVAS = DIVERSIDADE + RESPEITO + GENTILEZA</p>
                    </div>
                </div>
                <div class="gauges-container">
                    <div class="gauge">
                        <img src="data:image/png;base64, {gauge4_base64}" width="300">
                        <p>ATITUDES SUSTENTÁVEIS = SUSTENTABILIDADE + CIDADANIA</p>
                    </div>
                    <div class="gauge">
                        <img src="data:image/png;base64, {gauge5_base64}" width="300">
                        <p>ATITUDES SOCIOTRANSFORMADORAS = GENTILEZA + GENEROSIDADE + SOLIDARIEDADE + SUSTENTABILIDADE + DIVERSIDADE + RESPEITO + CIDADANIA</p>
                    </div>
                </div>
                <br>
                <br>
                <br>
                <h2>Mensagem</h2>
                <p>{message_content}</p>
                <footer>
                    <p>Nota: A mensagem neste documento foi gerada pelo ChatGPT da OpenAI. Ela é produto de uma inteligência artificial e representa uma criação simulada baseada nos parâmetros fornecidos.</p>
                </footer>
            </body>
        </html>
        '''
        pdf_options = {
            'encoding': 'UTF-8'
        }
        pdf_data = pdfkit.from_string(html, False, options=pdf_options)
        pdf_stream = io.BytesIO(pdf_data)
        return pdf_stream
