from prompts.mensagem import PROMPT_MENSAGEM
from utils.openai_utils import LLM
import io
import pdfkit

class PDFGenerator:

    def __init__(self, openai_key):
        self.openai_key = openai_key

    def generate_message(self, score_ontem, score_amanha, message_creator):
        prompt_mensagem_final = PROMPT_MENSAGEM.format(score_ontem, score_amanha, message_creator)
        agent = "Você é um especialista em gentileza e generosidade."
        llm = LLM(self.openai_key)
        message = llm.get_prompt(agent, prompt_mensagem_final)
        mensagem_final = llm.get_completion(message)
        return mensagem_final

    def generate_pdf(self, header_base64, fig1_base64, fig2_base64, score_ontem, score_amanha, message_creator):
        message_content = self.generate_message(score_ontem, score_amanha, message_creator)
        html = f'''
        <html>
            <head>
                <style>
                    body, h2, p {{
                        font-family: "Arial", sans-serif;
                    }}
                    .figures-container {{
                        display: flex;
                        justify-content: space-between;
                    }}
                    .figure {{
                        margin: 0 10px; /* Add some spacing between the images */
                        text-align: center; /* Center the heading relative to the image */
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
