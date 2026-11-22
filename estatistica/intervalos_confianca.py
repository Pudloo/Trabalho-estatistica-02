import math
import scipy.stats as st
from .auxiliares import (resumo_dados, checar_tipo, checar_confianca, pegar_sigma,
                         pegar_variancia, pegar_z, pegar_t, limites, texto_ic,
                         erro_duas_medias)


def ic_media(n=None, media=None, sigma=None, variancia_pop=None, desvio=None, dados=None,
             confianca=0.95, tipo="bilateral", N=None, forcar_t=False):
    checar_confianca(confianca)
    checar_tipo(tipo)
    if dados is not None:
        n, media, desvio = resumo_dados(dados)
    if n is None or media is None:
        raise ValueError("precisa informar n e media ou entao os dados")
    if n < 2:
        raise ValueError("n tem que ser pelo menos 2")
    sigma = pegar_sigma(sigma, variancia_pop)
    alpha = 1 - confianca

    if sigma is not None:
        desvio_usado = sigma
        distribuicao = "Z"
        motivo = "variancia da populacao conhecida"
    elif desvio is not None:
        desvio_usado = desvio
        if forcar_t:
            distribuicao = "t"
            motivo = "variancia desconhecida e t foi forcado"
        elif n > 30:
            distribuicao = "Z"
            motivo = "variancia desconhecida mas n maior que 30 (usa o desvio da amostra)"
        else:
            distribuicao = "t"
            motivo = "variancia desconhecida e n menor ou igual a 30"
    else:
        raise ValueError("precisa informar o sigma ou o desvio da amostra")

    erro_padrao = desvio_usado / math.sqrt(n)
    correcao = False
    if N is not None:
        if N < n:
            raise ValueError("N nao pode ser menor que n")
        if N < 20 * n:
            erro_padrao = erro_padrao * math.sqrt((N - n) / (N - 1))
            correcao = True

    if distribuicao == "Z":
        gl = None
        valor_critico = pegar_z(alpha, tipo)
    else:
        gl = n - 1
        valor_critico = pegar_t(alpha, gl, tipo)

    margem = valor_critico * erro_padrao
    inferior, superior = limites(media, margem, tipo)

    return {
        "parametro": "media",
        "distribuicao": distribuicao,
        "motivo_distribuicao": motivo,
        "gl": gl,
        "confianca": confianca,
        "tipo": tipo,
        "estimativa": media,
        "erro_padrao": erro_padrao,
        "valor_critico": valor_critico,
        "margem_erro": margem,
        "limite_inferior": inferior,
        "limite_superior": superior,
        "correcao_populacao_finita": correcao,
        "interpretacao": texto_ic(confianca, inferior, superior),
    }


def ic_proporcao(x=None, n=None, p=None, confianca=0.95, tipo="bilateral", N=None):
    checar_confianca(confianca)
    checar_tipo(tipo)
    if n is None:
        raise ValueError("precisa informar o n")
    if p is None:
        if x is None:
            raise ValueError("precisa informar x (quantidade com o atributo) ou p")
        p = x / n
    if not 0 <= p <= 1:
        raise ValueError("a proporcao tem que ficar entre 0 e 1")
    alpha = 1 - confianca

    erro_padrao = math.sqrt(p * (1 - p) / n)
    correcao = False
    if N is not None:
        if N < n:
            raise ValueError("N nao pode ser menor que n")
        if N < 20 * n:
            erro_padrao = erro_padrao * math.sqrt((N - n) / (N - 1))
            correcao = True

    aviso = None
    if n * p <= 5 or n * (1 - p) <= 5:
        aviso = "n*p ou n*(1-p) e menor ou igual a 5, a aproximacao normal pode nao ficar boa"

    valor_critico = pegar_z(alpha, tipo)
    margem = valor_critico * erro_padrao
    inferior, superior = limites(p, margem, tipo)

    return {
        "parametro": "proporcao",
        "distribuicao": "Z",
        "gl": None,
        "confianca": confianca,
        "tipo": tipo,
        "estimativa": p,
        "erro_padrao": erro_padrao,
        "valor_critico": valor_critico,
        "margem_erro": margem,
        "limite_inferior": inferior,
        "limite_superior": superior,
        "correcao_populacao_finita": correcao,
        "aviso": aviso,
        "interpretacao": texto_ic(confianca, inferior, superior),
    }


def ic_variancia(n=None, variancia=None, desvio=None, dados=None, confianca=0.95, tipo="bilateral"):
    checar_confianca(confianca)
    checar_tipo(tipo)
    if dados is not None:
        n, media, desvio = resumo_dados(dados)
        variancia = desvio ** 2
    variancia = pegar_variancia(variancia, desvio)
    if n is None or variancia is None:
        raise ValueError("precisa informar n e a variancia (ou o desvio) da amostra")
    if n < 2:
        raise ValueError("n tem que ser pelo menos 2")
    alpha = 1 - confianca
    gl = n - 1

    if tipo == "bilateral":
        q_direita = float(st.chi2.ppf(1 - alpha / 2, gl))
        q_esquerda = float(st.chi2.ppf(alpha / 2, gl))
        inferior = gl * variancia / q_direita
        superior = gl * variancia / q_esquerda
        valores_criticos = [q_esquerda, q_direita]
    elif tipo == "direita":
        q = float(st.chi2.ppf(1 - alpha, gl))
        inferior = gl * variancia / q
        superior = math.inf
        valores_criticos = [q]
    else:
        q = float(st.chi2.ppf(alpha, gl))
        inferior = 0.0
        superior = gl * variancia / q
        valores_criticos = [q]

    if tipo == "bilateral":
        margem = (superior - inferior) / 2
    elif tipo == "direita":
        margem = variancia - inferior
    else:
        margem = superior - variancia

    return {
        "parametro": "variancia",
        "distribuicao": "qui-quadrado",
        "gl": gl,
        "confianca": confianca,
        "tipo": tipo,
        "estimativa": variancia,
        "valores_criticos": valores_criticos,
        "margem_erro": margem,
        "margem_inferior": variancia - inferior,
        "margem_superior": superior - variancia,
        "limite_inferior": inferior,
        "limite_superior": superior,
        "limite_inferior_desvio": math.sqrt(inferior),
        "limite_superior_desvio": math.sqrt(superior),
        "interpretacao": texto_ic(confianca, inferior, superior),
    }


def ic_diferenca_medias(media1=None, n1=None, media2=None, n2=None,
                        sigma1=None, sigma2=None, variancia_pop1=None, variancia_pop2=None,
                        desvio1=None, desvio2=None, dados1=None, dados2=None,
                        variancias_iguais=None, confianca=0.95, tipo="bilateral", alpha_f=0.05):
    checar_confianca(confianca)
    checar_tipo(tipo)
    if dados1 is not None:
        n1, media1, desvio1 = resumo_dados(dados1)
    if dados2 is not None:
        n2, media2, desvio2 = resumo_dados(dados2)
    if n1 is None or n2 is None or media1 is None or media2 is None:
        raise ValueError("precisa informar n e media dos dois grupos ou entao os dados")
    sigma1 = pegar_sigma(sigma1, variancia_pop1)
    sigma2 = pegar_sigma(sigma2, variancia_pop2)
    alpha = 1 - confianca

    info = erro_duas_medias(n1, n2, sigma1, sigma2, desvio1, desvio2, variancias_iguais, alpha_f)
    if info["gl"] is None:
        valor_critico = pegar_z(alpha, tipo)
    else:
        valor_critico = pegar_t(alpha, info["gl"], tipo)

    diferenca = media1 - media2
    margem = valor_critico * info["erro_padrao"]
    inferior, superior = limites(diferenca, margem, tipo)

    return {
        "parametro": "diferenca de medias (mu1 - mu2)",
        "distribuicao": info["distribuicao"],
        "gl": info["gl"],
        "variancias_iguais": info["variancias_iguais"],
        "p_valor_teste_f": info["p_valor_f"],
        "confianca": confianca,
        "tipo": tipo,
        "estimativa": diferenca,
        "erro_padrao": info["erro_padrao"],
        "valor_critico": valor_critico,
        "margem_erro": margem,
        "limite_inferior": inferior,
        "limite_superior": superior,
        "interpretacao": texto_ic(confianca, inferior, superior),
    }
