def calcular_score_ontem(df):
    score = {}
    
    gentileza = int(df[df['question']=='EU FUI GENTIL?']['rating'].iloc[0])
    generosidade = int(df[df['question']=='EU FUI GENEROSO?']['rating'].iloc[0])
    sustentabilidade = int(df[df['question']=='EU FUI SUSTENTÁVEL?']['rating'].iloc[0])
    respeitabilidade = int(df[df['question']=='EU FUI RESPEITOSO?']['rating'].iloc[0])
    diversidade = int(df[df['question']=='EU AGI COM DIVERSIDADE?']['rating'].iloc[0])
    cidadania = int(df[df['question']=='EU FUI CIDADÃO?']['rating'].iloc[0])
    solidariedade = int(df[df['question']=='EU FUI SOLIDÁRIO?']['rating'].iloc[0])

    solidarias = gentileza + generosidade + solidariedade
    cidadas = respeitabilidade + cidadania 
    inclusivas = diversidade + respeitabilidade + gentileza
    sustentaveis = sustentabilidade + cidadania
    sociotransformadoras = gentileza + generosidade + sustentabilidade + respeitabilidade + diversidade + cidadania + solidariedade

    score['solidarias'] = solidarias
    score['cidadas'] = cidadas
    score['inclusivas'] = inclusivas
    score['sustentaveis'] = sustentaveis
    score['sociotransformadoras'] = sociotransformadoras

    return score

def calcular_score_amanha(df):
    score = {}
    
    gentileza = int(df[df['question']=='EU SEREI GENTIL?']['rating'].iloc[0])
    generosidade = int(df[df['question']=='EU SEREI GENEROSO?']['rating'].iloc[0])
    sustentabilidade = int(df[df['question']=='EU SEREI SUSTENTÁVEL?']['rating'].iloc[0])
    respeitabilidade = int(df[df['question']=='EU SEREI RESPEITOSO?']['rating'].iloc[0])
    diversidade = int(df[df['question']=='EU AGIREI COM DIVERSIDADE?']['rating'].iloc[0])
    cidadania = int(df[df['question']=='EU SEREI CIDADÃO?']['rating'].iloc[0])
    solidariedade = int(df[df['question']=='EU SEREI SOLIDÁRIO?']['rating'].iloc[0])

    solidarias = gentileza + generosidade + solidariedade
    cidadas = respeitabilidade + cidadania 
    inclusivas = diversidade + respeitabilidade + gentileza
    sustentaveis = sustentabilidade + cidadania
    sociotransformadoras = gentileza + generosidade + sustentabilidade + respeitabilidade + diversidade + cidadania + solidariedade

    score['solidarias'] = solidarias
    score['cidadas'] = cidadas
    score['inclusivas'] = inclusivas
    score['sustentaveis'] = sustentaveis
    score['sociotransformadoras'] = sociotransformadoras

    return score