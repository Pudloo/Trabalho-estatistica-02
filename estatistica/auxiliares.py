import math
import statistics
import scipy.stats as st


def resumo_dados(dados):
    n = len(dados)
    if n < 2:
        raise ValueError("precisa de pelo menos 2 dados")
    media = statistics.mean(dados)
    desvio = statistics.stdev(dados)
    return n, media, desvio


def checar_tipo(tipo):
    if tipo not in ("bilateral", "esquerda", "direita"):
        raise ValueError("tipo tem que ser bilateral, esquerda ou direita")


def checar_alpha(alpha):
    if not 0 < alpha < 1:
        raise ValueError("alpha tem que ser um numero entre 0 e 1, exemplo 0.05")


def checar_confianca(confianca):
    if not 0 < confianca < 1:
        raise ValueError("confianca tem que ser um numero entre 0 e 1, exemplo 0.95")


def pegar_sigma(sigma, variancia_pop):
    if sigma is not None:
        return sigma
    if variancia_pop is not None:
        return math.sqrt(variancia_pop)
    return None


def pegar_variancia(variancia, desvio):
    if variancia is not None:
        return variancia
    if desvio is not None:
        return desvio ** 2
    return None


def pegar_z(alpha, tipo):
    if tipo == "bilateral":
        return float(st.norm.ppf(1 - alpha / 2))
    return float(st.norm.ppf(1 - alpha))


def pegar_t(alpha, gl, tipo):
    if tipo == "bilateral":
        return float(st.t.ppf(1 - alpha / 2, gl))
    return float(st.t.ppf(1 - alpha, gl))


def arredondar_cima(x):
    return math.ceil(round(x, 8))


def limites(estimativa, margem, tipo):
    if tipo == "bilateral":
        return estimativa - margem, estimativa + margem
    if tipo == "direita":
        return estimativa - margem, math.inf
    return -math.inf, estimativa + margem


def texto_ic(confianca, inferior, superior):
    return f"Com {confianca * 100:g}% de confianca, o parametro esta entre {inferior:.4f} e {superior:.4f}."


def montar_hipoteses(simbolo, valor, tipo):
    h0 = f"H0: {simbolo} = {valor}"
    if tipo == "bilateral":
        h1 = f"H1: {simbolo} != {valor}"
    elif tipo == "direita":
        h1 = f"H1: {simbolo} > {valor}"
    else:
        h1 = f"H1: {simbolo} < {valor}"
    return h0, h1


def pegar_criticos(dist, alpha, tipo):
    if tipo == "bilateral":
        return [float(dist.ppf(alpha / 2)), float(dist.ppf(1 - alpha / 2))]
    if tipo == "direita":
        return [float(dist.ppf(1 - alpha))]
    return [float(dist.ppf(alpha))]


def texto_regiao(criticos, tipo):
    if tipo == "bilateral":
        return f"estatistica < {criticos[0]:.4f} ou estatistica > {criticos[1]:.4f}"
    if tipo == "direita":
        return f"estatistica > {criticos[0]:.4f}"
    return f"estatistica < {criticos[0]:.4f}"


def pegar_p_valor(estatistica, dist, tipo):
    esquerda = float(dist.cdf(estatistica))
    direita = float(dist.sf(estatistica))
    if tipo == "bilateral":
        return min(1.0, 2 * min(esquerda, direita))
    if tipo == "direita":
        return direita
    return esquerda


def texto_p(p):
    if p < 0.0001:
        return "< 0.0001"
    return f"= {p:.4f}"


def montar_conclusao(rejeita, h1, alpha, p):
    h1_sem_nome = h1.replace("H1: ", "")
    if rejeita:
        return f"Rejeita H0. Os dados mostra evidencia a favor de ({h1_sem_nome}) a nivel de {alpha * 100:g}% (p-valor {texto_p(p)})."
    return f"Nao rejeita H0. Nao tem evidencia suficiente a favor de ({h1_sem_nome}) a nivel de {alpha * 100:g}% (p-valor {texto_p(p)})."


def montar_resultado(nome, h0, h1, distribuicao, gl, estatistica, alpha, tipo, p_valor, criticos, regiao, aviso=None):
    rejeita = p_valor <= alpha
    return {
        "teste": nome,
        "H0": h0,
        "H1": h1,
        "alpha": alpha,
        "tipo": tipo,
        "distribuicao": distribuicao,
        "gl": gl,
        "estatistica": float(estatistica),
        "valores_criticos": criticos,
        "regiao_rejeicao": regiao,
        "p_valor": p_valor,
        "rejeita_H0": rejeita,
        "conclusao": montar_conclusao(rejeita, h1, alpha, p_valor),
        "aviso": aviso,
    }


def fazer_teste(nome, h0, h1, distribuicao, gl, estatistica, dist, alpha, tipo, aviso=None):
    p_valor = pegar_p_valor(estatistica, dist, tipo)
    criticos = pegar_criticos(dist, alpha, tipo)
    regiao = texto_regiao(criticos, tipo)
    return montar_resultado(nome, h0, h1, distribuicao, gl, estatistica, alpha, tipo, p_valor, criticos, regiao, aviso)


def comparar_variancias(n1, desvio1, n2, desvio2):
    razao = desvio1 ** 2 / desvio2 ** 2
    dist = st.f(n1 - 1, n2 - 1)
    return min(1.0, 2 * min(float(dist.cdf(razao)), float(dist.sf(razao))))


def erro_duas_medias(n1, n2, sigma1, sigma2, desvio1, desvio2, variancias_iguais, alpha_f=0.05):
    if sigma1 is not None and sigma2 is not None:
        erro = math.sqrt(sigma1 ** 2 / n1 + sigma2 ** 2 / n2)
        return {"erro_padrao": erro, "gl": None, "distribuicao": "Z",
                "variancias_iguais": None, "p_valor_f": None}
    if sigma1 is not None or sigma2 is not None:
        raise ValueError("informe os dois sigmas ou nenhum dos dois")
    if desvio1 is None or desvio2 is None:
        raise ValueError("faltou o desvio padrao das amostras")
    p_f = None
    if variancias_iguais is None:
        p_f = comparar_variancias(n1, desvio1, n2, desvio2)
        variancias_iguais = p_f > alpha_f
    if variancias_iguais:
        gl = n1 + n2 - 2
        sp2 = ((n1 - 1) * desvio1 ** 2 + (n2 - 1) * desvio2 ** 2) / gl
        erro = math.sqrt(sp2 * (1 / n1 + 1 / n2))
        nome = "t de Student (variancias iguais)"
    else:
        a = desvio1 ** 2 / n1
        b = desvio2 ** 2 / n2
        erro = math.sqrt(a + b)
        gl = (a + b) ** 2 / (a ** 2 / (n1 - 1) + b ** 2 / (n2 - 1))
        nome = "t de Student (variancias diferentes)"
    return {"erro_padrao": erro, "gl": gl, "distribuicao": nome,
            "variancias_iguais": variancias_iguais, "p_valor_f": p_f}
