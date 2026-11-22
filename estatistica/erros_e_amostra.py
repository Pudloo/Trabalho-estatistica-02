import math
import scipy.stats as st
from .auxiliares import (checar_tipo, checar_alpha, checar_confianca, pegar_sigma, pegar_z, pegar_t,
                         arredondar_cima, montar_hipoteses)


def calcular_beta(mu0, mu_real, sigma=None, n=None, alpha=0.05, tipo="bilateral",
                  regiao_aceitacao=None, variancia_pop=None):
    checar_alpha(alpha)
    checar_tipo(tipo)
    sigma = pegar_sigma(sigma, variancia_pop)
    if sigma is None or n is None:
        raise ValueError("precisa informar sigma (ou variancia_pop) e n")
    erro_padrao = sigma / math.sqrt(n)

    if regiao_aceitacao is not None:
        inferior, superior = regiao_aceitacao
    elif tipo == "bilateral":
        z = pegar_z(alpha, tipo)
        inferior = mu0 - z * erro_padrao
        superior = mu0 + z * erro_padrao
    elif tipo == "direita":
        z = pegar_z(alpha, tipo)
        inferior = -math.inf
        superior = mu0 + z * erro_padrao
    else:
        z = pegar_z(alpha, tipo)
        inferior = mu0 - z * erro_padrao
        superior = math.inf

    z_inferior = (inferior - mu_real) / erro_padrao
    z_superior = (superior - mu_real) / erro_padrao
    beta = float(st.norm.cdf(z_superior) - st.norm.cdf(z_inferior))

    h0, h1 = montar_hipoteses("mu", mu0, tipo)
    return {
        "H0": h0,
        "H1": h1,
        "mu_real": mu_real,
        "alpha": alpha,
        "tipo": tipo,
        "erro_padrao": erro_padrao,
        "regiao_aceitacao": (inferior, superior),
        "z_inferior": z_inferior,
        "z_superior": z_superior,
        "beta": beta,
        "poder": 1 - beta,
        "interpretacao": f"Se a media verdadeira for {mu_real}, a chance de aceitar H0 por engano (erro tipo II) e {beta:.4f}.",
    }


def tamanho_amostra_teste_media(mu0, mu_real, alpha=0.05, beta=0.1, tipo="bilateral",
                                sigma=None, variancia_pop=None, desvio=None):
    checar_alpha(alpha)
    checar_alpha(beta)
    checar_tipo(tipo)
    if mu0 == mu_real:
        raise ValueError("mu0 e mu_real nao podem ser iguais")
    sigma = pegar_sigma(sigma, variancia_pop)
    delta = abs(mu_real - mu0)
    z_alpha = pegar_z(alpha, tipo)
    z_beta = float(st.norm.ppf(1 - beta))

    if sigma is not None:
        n = arredondar_cima(((z_alpha + z_beta) * sigma / delta) ** 2)
        distribuicao = "Z"
    elif desvio is not None:
        n = max(2, arredondar_cima(((z_alpha + z_beta) * desvio / delta) ** 2))
        while True:
            t_alpha = pegar_t(alpha, n - 1, tipo)
            t_beta = float(st.t.ppf(1 - beta, n - 1))
            precisa = round(((t_alpha + t_beta) * desvio / delta) ** 2, 8)
            if n >= precisa:
                break
            n += 1
        distribuicao = "t"
    else:
        raise ValueError("precisa informar sigma (variancia conhecida) ou o desvio da amostra")

    return {
        "n_minimo": n,
        "distribuicao": distribuicao,
        "delta": delta,
        "z_alpha": z_alpha,
        "z_beta": z_beta,
        "alpha": alpha,
        "beta": beta,
        "poder": 1 - beta,
    }


def tamanho_amostra_teste_proporcao(p0, p_real, alpha=0.05, beta=0.1, tipo="bilateral"):
    checar_alpha(alpha)
    checar_alpha(beta)
    checar_tipo(tipo)
    if p0 == p_real:
        raise ValueError("p0 e p_real nao podem ser iguais")
    z_alpha = pegar_z(alpha, tipo)
    z_beta = float(st.norm.ppf(1 - beta))
    delta = abs(p_real - p0)
    cima = z_alpha * math.sqrt(p0 * (1 - p0)) + z_beta * math.sqrt(p_real * (1 - p_real))
    n = arredondar_cima((cima / delta) ** 2)
    return {
        "n_minimo": n,
        "distribuicao": "Z",
        "delta": delta,
        "z_alpha": z_alpha,
        "z_beta": z_beta,
        "alpha": alpha,
        "beta": beta,
        "poder": 1 - beta,
    }


def tamanho_amostra_teste_variancia(variancia0, variancia_real, alpha=0.05, beta=0.1, tipo="bilateral"):
    checar_alpha(alpha)
    checar_alpha(beta)
    checar_tipo(tipo)
    if variancia0 <= 0 or variancia_real <= 0:
        raise ValueError("as variancias tem que ser maiores que zero")
    if variancia0 == variancia_real:
        raise ValueError("variancia0 e variancia_real nao podem ser iguais")
    if tipo == "direita" and variancia_real < variancia0:
        raise ValueError("no teste a direita a variancia real tem que ser maior que a variancia0")
    if tipo == "esquerda" and variancia_real > variancia0:
        raise ValueError("no teste a esquerda a variancia real tem que ser menor que a variancia0")

    razao = variancia0 / variancia_real
    n = 2
    while n < 50000:
        gl = n - 1
        dist = st.chi2(gl)
        if tipo == "direita":
            poder = float(dist.sf(dist.ppf(1 - alpha) * razao))
        elif tipo == "esquerda":
            poder = float(dist.cdf(dist.ppf(alpha) * razao))
        else:
            poder = float(dist.cdf(dist.ppf(alpha / 2) * razao) + dist.sf(dist.ppf(1 - alpha / 2) * razao))
        if poder >= 1 - beta:
            break
        n += 1
    if n >= 50000:
        raise ValueError("o n ficou grande demais (mais de 50000), confira os valores")

    return {
        "n_minimo": n,
        "distribuicao": "qui-quadrado",
        "alpha": alpha,
        "beta": beta,
        "poder": poder,
    }


def tamanho_amostra_media(erro, confianca=0.95, sigma=None, variancia_pop=None, desvio=None, distribuicao="t"):
    checar_confianca(confianca)
    if erro <= 0:
        raise ValueError("o erro maximo tem que ser maior que zero")
    sigma = pegar_sigma(sigma, variancia_pop)
    alpha = 1 - confianca
    z = pegar_z(alpha, "bilateral")

    if sigma is not None:
        n = arredondar_cima((z * sigma / erro) ** 2)
        usada = "Z"
    elif desvio is not None:
        if distribuicao == "z":
            n = arredondar_cima((z * desvio / erro) ** 2)
            usada = "Z"
        elif distribuicao == "t":
            n = max(2, arredondar_cima((z * desvio / erro) ** 2))
            while n < round((pegar_t(alpha, n - 1, "bilateral") * desvio / erro) ** 2, 8):
                n += 1
            usada = "t"
        else:
            raise ValueError("distribuicao tem que ser 't' ou 'z'")
    else:
        raise ValueError("precisa informar sigma ou o desvio da amostra piloto")

    return {"n_minimo": n, "distribuicao": usada, "confianca": confianca, "erro_maximo": erro}


def tamanho_amostra_proporcao(erro, confianca=0.95, p=0.5):
    checar_confianca(confianca)
    if erro <= 0:
        raise ValueError("o erro maximo tem que ser maior que zero")
    if not 0 <= p <= 1:
        raise ValueError("p tem que ficar entre 0 e 1")
    alpha = 1 - confianca
    z = pegar_z(alpha, "bilateral")
    n = arredondar_cima(z ** 2 * p * (1 - p) / erro ** 2)
    return {"n_minimo": n, "distribuicao": "Z", "confianca": confianca, "erro_maximo": erro, "p_usado": p}
