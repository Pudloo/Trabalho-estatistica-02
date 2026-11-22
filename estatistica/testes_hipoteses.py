import math
import scipy.stats as st
from .auxiliares import (resumo_dados, checar_tipo, checar_alpha, pegar_sigma, pegar_variancia,
                         montar_hipoteses, fazer_teste, montar_resultado, erro_duas_medias)


def teste_media(mu0, n=None, media=None, sigma=None, variancia_pop=None, desvio=None, dados=None,
                alpha=0.05, tipo="bilateral", forcar_t=False):
    checar_alpha(alpha)
    checar_tipo(tipo)
    if dados is not None:
        n, media, desvio = resumo_dados(dados)
    if n is None or media is None:
        raise ValueError("precisa informar n e media ou entao os dados")
    if n < 2:
        raise ValueError("n tem que ser pelo menos 2")
    sigma = pegar_sigma(sigma, variancia_pop)

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
    estatistica = (media - mu0) / erro_padrao

    if distribuicao == "Z":
        gl = None
        dist = st.norm()
    else:
        gl = n - 1
        dist = st.t(gl)

    h0, h1 = montar_hipoteses("mu", mu0, tipo)
    resultado = fazer_teste("media contra um valor padrao", h0, h1, distribuicao, gl,
                            estatistica, dist, alpha, tipo)
    resultado["motivo_distribuicao"] = motivo
    resultado["media_amostra"] = media
    resultado["erro_padrao"] = erro_padrao
    return resultado


def teste_duas_medias(media1=None, n1=None, media2=None, n2=None,
                      sigma1=None, sigma2=None, variancia_pop1=None, variancia_pop2=None,
                      desvio1=None, desvio2=None, dados1=None, dados2=None,
                      variancias_iguais=None, alpha=0.05, tipo="bilateral", alpha_f=0.05):
    checar_alpha(alpha)
    checar_tipo(tipo)
    if dados1 is not None:
        n1, media1, desvio1 = resumo_dados(dados1)
    if dados2 is not None:
        n2, media2, desvio2 = resumo_dados(dados2)
    if n1 is None or n2 is None or media1 is None or media2 is None:
        raise ValueError("precisa informar n e media dos dois grupos ou entao os dados")
    sigma1 = pegar_sigma(sigma1, variancia_pop1)
    sigma2 = pegar_sigma(sigma2, variancia_pop2)

    info = erro_duas_medias(n1, n2, sigma1, sigma2, desvio1, desvio2, variancias_iguais, alpha_f)
    estatistica = (media1 - media2) / info["erro_padrao"]

    if info["gl"] is None:
        dist = st.norm()
    else:
        dist = st.t(info["gl"])

    h0, h1 = montar_hipoteses("mu1", "mu2", tipo)
    resultado = fazer_teste("comparacao de duas medias", h0, h1, info["distribuicao"], info["gl"],
                            estatistica, dist, alpha, tipo)
    resultado["diferenca_medias"] = media1 - media2
    resultado["erro_padrao"] = info["erro_padrao"]
    resultado["variancias_iguais"] = info["variancias_iguais"]
    resultado["p_valor_teste_f"] = info["p_valor_f"]
    return resultado


def teste_medias_pareadas(dados1=None, dados2=None, media_d=None, desvio_d=None, n=None,
                          alpha=0.05, tipo="bilateral"):
    checar_alpha(alpha)
    checar_tipo(tipo)
    if dados1 is not None and dados2 is not None:
        if len(dados1) != len(dados2):
            raise ValueError("os dois grupos tem que ter o mesmo tamanho")
        diferencas = [a - b for a, b in zip(dados1, dados2)]
        n, media_d, desvio_d = resumo_dados(diferencas)
    elif n is None or media_d is None or desvio_d is None:
        raise ValueError("informe os dois grupos ou entao n, media_d e desvio_d")

    erro_padrao = desvio_d / math.sqrt(n)
    estatistica = media_d / erro_padrao
    gl = n - 1

    h0, h1 = montar_hipoteses("mu_d", 0, tipo)
    resultado = fazer_teste("media de amostras pareadas (d = grupo1 - grupo2)", h0, h1,
                            "t de Student", gl, estatistica, st.t(gl), alpha, tipo)
    resultado["media_diferencas"] = media_d
    resultado["erro_padrao"] = erro_padrao
    return resultado


def teste_proporcao(p0, x=None, n=None, p=None, alpha=0.05, tipo="bilateral", metodo="normal"):
    checar_alpha(alpha)
    checar_tipo(tipo)
    if n is None:
        raise ValueError("precisa informar o n")
    if not 0 < p0 < 1:
        raise ValueError("p0 tem que ficar entre 0 e 1")
    if p is None:
        if x is None:
            raise ValueError("precisa informar x (quantidade com o atributo) ou p")
        p = x / n

    h0, h1 = montar_hipoteses("p", p0, tipo)

    if metodo == "exato":
        if x is None:
            raise ValueError("no metodo exato precisa informar o x")
        alternativa = {"bilateral": "two-sided", "direita": "greater", "esquerda": "less"}[tipo]
        p_valor = float(st.binomtest(int(x), n, p0, alternative=alternativa).pvalue)
        resultado = montar_resultado("proporcao contra um valor padrao (binomial exata)", h0, h1,
                                     "binomial", None, x, alpha, tipo, p_valor, None,
                                     "nao se aplica, o p-valor vem direto da binomial")
        resultado["proporcao_amostra"] = p
        return resultado

    if metodo != "normal":
        raise ValueError("metodo tem que ser normal ou exato")

    aviso = None
    if n * p0 <= 5 or n * (1 - p0) <= 5:
        aviso = "n*p0 ou n*(1-p0) e menor ou igual a 5, a aproximacao normal pode nao ficar boa (veja metodo='exato')"

    erro_padrao = math.sqrt(p0 * (1 - p0) / n)
    estatistica = (p - p0) / erro_padrao
    resultado = fazer_teste("proporcao contra um valor padrao", h0, h1, "Z", None,
                            estatistica, st.norm(), alpha, tipo, aviso)
    resultado["proporcao_amostra"] = p
    resultado["erro_padrao"] = erro_padrao
    return resultado


def teste_duas_proporcoes(x1, n1, x2, n2, alpha=0.05, tipo="bilateral"):
    checar_alpha(alpha)
    checar_tipo(tipo)
    p1 = x1 / n1
    p2 = x2 / n2
    p_junto = (x1 + x2) / (n1 + n2)
    if p_junto == 0 or p_junto == 1:
        raise ValueError("a proporcao junta nao pode ser 0 nem 1")

    erro_padrao = math.sqrt(p_junto * (1 - p_junto) * (1 / n1 + 1 / n2))
    estatistica = (p1 - p2) / erro_padrao

    aviso = None
    if min(n1 * p_junto, n1 * (1 - p_junto), n2 * p_junto, n2 * (1 - p_junto)) <= 5:
        aviso = "alguma quantidade esperada (n*p) e menor ou igual a 5, a aproximacao normal pode nao ficar boa"

    h0, h1 = montar_hipoteses("p1", "p2", tipo)
    resultado = fazer_teste("comparacao de duas proporcoes", h0, h1, "Z", None,
                            estatistica, st.norm(), alpha, tipo, aviso)
    resultado["proporcao_1"] = p1
    resultado["proporcao_2"] = p2
    resultado["proporcao_junta"] = p_junto
    resultado["erro_padrao"] = erro_padrao
    return resultado


def teste_variancia(variancia0=None, desvio0=None, n=None, variancia=None, desvio=None, dados=None,
                    alpha=0.05, tipo="bilateral"):
    checar_alpha(alpha)
    checar_tipo(tipo)
    if dados is not None:
        n, media, desvio = resumo_dados(dados)
        variancia = desvio ** 2
    variancia = pegar_variancia(variancia, desvio)
    variancia0 = pegar_variancia(variancia0, desvio0)
    if n is None or variancia is None:
        raise ValueError("precisa informar n e a variancia (ou o desvio) da amostra")
    if variancia0 is None:
        raise ValueError("precisa informar variancia0 ou desvio0")
    if n < 2:
        raise ValueError("n tem que ser pelo menos 2")

    gl = n - 1
    estatistica = gl * variancia / variancia0

    h0, h1 = montar_hipoteses("sigma2", variancia0, tipo)
    resultado = fazer_teste("variancia contra um valor padrao", h0, h1, "qui-quadrado", gl,
                            estatistica, st.chi2(gl), alpha, tipo)
    resultado["variancia_amostra"] = variancia
    return resultado


def teste_duas_variancias(n1=None, variancia1=None, desvio1=None, n2=None, variancia2=None, desvio2=None,
                          dados1=None, dados2=None, alpha=0.05, tipo="bilateral"):
    checar_alpha(alpha)
    checar_tipo(tipo)
    if dados1 is not None:
        n1, media1, desvio1 = resumo_dados(dados1)
        variancia1 = desvio1 ** 2
    if dados2 is not None:
        n2, media2, desvio2 = resumo_dados(dados2)
        variancia2 = desvio2 ** 2
    variancia1 = pegar_variancia(variancia1, desvio1)
    variancia2 = pegar_variancia(variancia2, desvio2)
    if n1 is None or n2 is None or variancia1 is None or variancia2 is None:
        raise ValueError("precisa informar n e variancia (ou desvio) dos dois grupos")
    if variancia1 <= 0 or variancia2 <= 0:
        raise ValueError("as variancias tem que ser maiores que zero")

    h0, h1 = montar_hipoteses("sigma1^2", "sigma2^2", tipo)

    if tipo == "bilateral":
        if variancia1 >= variancia2:
            estatistica = variancia1 / variancia2
            gl_cima = n1 - 1
            gl_baixo = n2 - 1
        else:
            estatistica = variancia2 / variancia1
            gl_cima = n2 - 1
            gl_baixo = n1 - 1
        dist = st.f(gl_cima, gl_baixo)
        critico = float(dist.ppf(1 - alpha / 2))
        p_valor = min(1.0, 2 * float(dist.sf(estatistica)))
        regiao = f"F > {critico:.4f} (maior variancia sobre a menor)"
        resultado = montar_resultado("homogeneidade de duas variancias (teste F)", h0, h1, "F",
                                     (gl_cima, gl_baixo), estatistica, alpha, tipo, p_valor,
                                     [critico], regiao)
        return resultado

    estatistica = variancia1 / variancia2
    gl = (n1 - 1, n2 - 1)
    dist = st.f(gl[0], gl[1])
    return fazer_teste("homogeneidade de duas variancias (teste F)", h0, h1, "F", gl,
                       estatistica, dist, alpha, tipo)
