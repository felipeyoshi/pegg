import os
#import pdfkit
#from BytesIO import BytesIO

def generate_pdf(header_base64, fig1_base64, fig2_base64):
    html = f'''
    <html>
        <body>
            <img src="data:image/png;base64, {header_base64}" width="700">
            <h2 style="text-align: center;">Como fui ontem?</h2>
            <img src="data:image/png;base64, {fig1_base64}" width="700">
            <h2 style="text-align: center;">Como serei amanhã?</h2>
            <img src="data:image/png;base64, {fig2_base64}" width="700">
            <h2 style="text-align: center;">Mensagem</h2>
        </body>
    </html>
    '''
    return html