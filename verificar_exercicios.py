import sys
import scipy.stats as st
from estatistica import *

acertos = 0
erros = 0


def conferir(nome, valor, esperado, tolerancia=0.01):
    global acertos, erros
    if abs(valor - esperado) <= tolerancia:
        acertos += 1
        print("ok   ", nome, "->", round(valor, 5))
    else:
        erros += 1
        print("ERRO ", nome, "-> deu", valor, "mas era para dar", esperado)


def conferir_texto(nome, valor, esperado):
    global acertos, erros
    if valor == esperado:
        acertos += 1
        print("ok   ", nome, "->", valor)
    else:
        erros += 1
        print("ERRO ", nome, "-> deu", valor, "mas era para dar", esperado)


print("--- intervalos de confianca (lista) ---")

r = ic_media(n=81, media=346, sigma=4.5)
conferir("ex1 limite inferior", r["limite_inferior"], 345.02)
conferir("ex1 limite superior", r["limite_superior"], 346.98)

r = ic_media(n=36, media=98, desvio=4, confianca=0.99, forcar_t=True)
conferir("ex2a limite inferior", r["limite_inferior"], 96.18)
conferir("ex2a limite superior", r["limite_superior"], 99.82)

r = ic_media(n=36, media=98, desvio=4, confianca=0.99)
conferir_texto("ex2a distribuicao sem forcar t (n > 30)", r["distribuicao"], "Z")

r = ic_proporcao(x=380, n=400, N=500000)
conferir("ex4a limite inferior", r["limite_inferior"], 0.9286, 0.0001)
conferir("ex4a limite superior", r["limite_superior"], 0.9714, 0.0001)
conferir_texto("ex4a correcao de populacao finita", r["correcao_populacao_finita"], False)

r = ic_media(n=20, media=20.01, desvio=1.34)
conferir("ex5 limite inferior", r["limite_inferior"], 19.38)
conferir("ex5 limite superior", r["limite_superior"], 20.64)
conferir_texto("ex5 distribuicao", r["distribuicao"], "t")

r = ic_diferenca_medias(media1=2.538, n1=12, desvio1=0.008, media2=2.520, n2=12, desvio2=0.006,
                        variancias_iguais=True, confianca=0.99)
conferir("ex6 limite inferior", r["limite_inferior"], 0.00986, 0.0001)
conferir("ex6 limite superior", r["limite_superior"], 0.02614, 0.0001)

r = ic_variancia(n=16, variancia=169)
conferir("ex7 limite inferior", r["limite_inferior"], 92.22)
conferir("ex7 limite superior", r["limite_superior"], 404.81)

r = ic_media(n=100, media=65.5, desvio=4.8)
conferir("ex10 limite inferior", r["limite_inferior"], 64.56)
conferir("ex10 limite superior", r["limite_superior"], 66.44)
conferir_texto("ex10 distribuicao", r["distribuicao"], "Z")

r = ic_proporcao(x=42, n=600)
conferir("ex21 limite inferior", r["limite_inferior"], 0.0496, 0.0001)
conferir("ex21 limite superior", r["limite_superior"], 0.0904, 0.0001)

r = ic_diferenca_medias(media1=42, n1=25, desvio1=8, media2=38, n2=25, desvio2=6,
                        variancias_iguais=True)
conferir("ex24 limite inferior", r["limite_inferior"], -0.021, 0.001)
conferir("ex24 limite superior", r["limite_superior"], 8.021, 0.001)


print()
print("--- intervalos de confianca (slides) ---")

potencia = [26.7, 25.8, 24.0, 24.9, 26.4, 25.9, 24.4, 21.7, 24.1, 25.9, 27.3, 26.9, 27.3, 24.8, 23.6]
r = ic_media(dados=potencia)
conferir("aula 7 potencia limite inferior", r["limite_inferior"], 24.43, 0.02)
conferir("aula 7 potencia limite superior", r["limite_superior"], 26.19, 0.02)

r = ic_proporcao(x=180, n=300, confianca=0.99)
conferir("aula 8 proporcao limite inferior", r["limite_inferior"], 0.5270, 0.001)
conferir("aula 8 proporcao limite superior", r["limite_superior"], 0.6730, 0.001)

r = ic_variancia(n=16, variancia=169)
conferir("aula 8 variancia limite superior (slide usa tabela)", r["limite_superior"], 404.95, 0.2)

r = ic_media(n=64, media=142, desvio=24, confianca=0.95, tipo="esquerda")
conferir("aula 10 IC unilateral limite superior", r["limite_superior"], 146.935, 0.01)


print()
print("--- testes de hipoteses (lista) ---")

r = teste_media(mu0=100, n=36, media=98, desvio=4, alpha=0.01, forcar_t=True)
conferir("ex2b estatistica t", r["estatistica"], -3.0)
conferir("ex2b p-valor", r["p_valor"], 0.00495, 0.0001)

r = teste_variancia(desvio0=1, n=20, desvio=1.34)
conferir("ex11 estatistica", r["estatistica"], 34.116, 0.001)
conferir("ex11 p-valor", r["p_valor"], 0.0356, 0.0005)
conferir("ex11 valor critico inferior", r["valores_criticos"][0], 8.907, 0.001)
conferir("ex11 valor critico superior", r["valores_criticos"][1], 32.852, 0.001)
conferir_texto("ex11 rejeita H0", r["rejeita_H0"], True)

r = teste_proporcao(p0=0.5, x=24, n=40)
conferir("ex13 estatistica z", r["estatistica"], 1.265, 0.001)
conferir("ex13 p-valor", r["p_valor"], 0.206, 0.001)
conferir_texto("ex13 rejeita H0", r["rejeita_H0"], False)

r = teste_media(mu0=53, n=30, media=45, sigma=14, alpha=0.01, tipo="esquerda")
conferir("ex14 estatistica z", r["estatistica"], -3.130, 0.001)
conferir("ex14 p-valor", r["p_valor"], 0.00087, 0.00002)
conferir_texto("ex14 rejeita H0", r["rejeita_H0"], True)

r = teste_variancia(desvio0=8, n=20, desvio=10, tipo="direita")
conferir("ex15 estatistica", r["estatistica"], 29.6875, 0.0001)
conferir("ex15 valor critico", r["valores_criticos"][0], 30.144, 0.001)
conferir("ex15 p-valor", r["p_valor"], 0.0559, 0.0005)
conferir_texto("ex15 rejeita H0", r["rejeita_H0"], False)

r = teste_duas_variancias(n1=20, variancia1=10, n2=6, variancia2=40, tipo="esquerda", alpha=0.05)
conferir("ex17 estatistica F", r["estatistica"], 0.25, 0.0001)
conferir("ex17 valor critico", r["valores_criticos"][0], 0.365, 0.001)
conferir("ex17 p-valor", r["p_valor"], 0.0120, 0.0005)
conferir_texto("ex17 rejeita H0", r["rejeita_H0"], True)

r = teste_duas_medias(media1=24000, n1=50, sigma1=2500, media2=26000, n2=40, sigma2=3000, alpha=0.04)
conferir("ex18 estatistica z", r["estatistica"], -3.381, 0.001)
conferir("ex18 p-valor", r["p_valor"], 0.00072, 0.00001)
conferir_texto("ex18 rejeita H0", r["rejeita_H0"], True)

r = teste_media(mu0=120, n=36, media=114, sigma=18, tipo="esquerda")
conferir("ex22 estatistica z", r["estatistica"], -2.0, 0.0001)
conferir("ex22 p-valor", r["p_valor"], 0.0228, 0.0001)

r = teste_duas_proporcoes(30, 200, 18, 180)
conferir("ex23 estatistica z", r["estatistica"], 1.465, 0.001)
conferir("ex23 p-valor", r["p_valor"], 0.143, 0.001)
conferir_texto("ex23 rejeita H0", r["rejeita_H0"], False)

r = teste_variancia(desvio0=10, n=15, desvio=12, tipo="esquerda")
conferir("ex25 estatistica", r["estatistica"], 20.16, 0.001)
conferir("ex25 valor critico", r["valores_criticos"][0], 6.571, 0.001)
conferir("ex25 p-valor", r["p_valor"], 0.875, 0.001)


print()
print("--- testes de hipoteses (slides) ---")

r = teste_media(mu0=0.85, n=8, media=0.87, desvio=0.010)
conferir("aula 10 media estatistica t", r["estatistica"], 5.657, 0.001)
conferir("aula 10 media valor critico", r["valores_criticos"][1], 2.365, 0.001)

r = teste_media(mu0=150, n=64, media=142, desvio=24, alpha=0.05, tipo="esquerda")
conferir("aula 10 API estatistica z", r["estatistica"], -2.667, 0.001)
conferir_texto("aula 10 API distribuicao", r["distribuicao"], "Z")
conferir_texto("aula 10 API rejeita H0", r["rejeita_H0"], True)

r = teste_proporcao(p0=0.6, x=530, n=1000)
conferir("aula 9 mortalidade estatistica z", r["estatistica"], -4.518, 0.001)
conferir_texto("aula 9 mortalidade rejeita H0", r["rejeita_H0"], True)

r = teste_duas_proporcoes(32, 80, 26, 50)
conferir("aula 9 revista estatistica z", r["estatistica"], -1.339, 0.001)
conferir_texto("aula 9 revista rejeita H0", r["rejeita_H0"], False)

r = teste_variancia(desvio0=10, n=16, variancia=169, tipo="direita")
conferir("aula 9 variancia estatistica", r["estatistica"], 25.35, 0.001)
conferir("aula 9 variancia valor critico", r["valores_criticos"][0], 25.0, 0.01)
conferir_texto("aula 9 variancia rejeita H0", r["rejeita_H0"], True)

concreto_x = [54, 55, 58, 50, 61]
concreto_y = [51, 54, 55, 52, 53]
r = teste_duas_variancias(dados1=concreto_x, dados2=concreto_y, alpha=0.1)
conferir("aula 9 concreto estatistica F", r["estatistica"], 6.92, 0.001)
conferir("aula 9 concreto valor critico", r["valores_criticos"][0], 6.39, 0.01)
conferir_texto("aula 9 concreto rejeita H0", r["rejeita_H0"], True)

novo = [22, 21, 28, 30, 33, 33, 26, 24, 31, 22]
antigo = [25, 28, 26, 36, 32, 39, 28, 33, 30, 27]
r = teste_medias_pareadas(dados1=novo, dados2=antigo, alpha=0.05, tipo="esquerda")
conferir("aula 10 pareado estatistica t", r["estatistica"], -2.825, 0.001)
conferir_texto("aula 10 pareado rejeita H0", r["rejeita_H0"], True)

r = teste_proporcao(p0=0.5, x=13, n=14, metodo="exato")
conferir("aula 8 moeda p-valor exato", r["p_valor"], 0.002, 0.0005)


print()
print("--- comparando com o scipy ---")

g1 = [12.1, 13.4, 11.8, 14.2, 13.0, 12.7, 15.1, 12.2]
g2 = [10.9, 11.5, 12.3, 10.2, 11.8, 12.0, 10.7, 11.1, 12.5]
for tipo, alt in [("bilateral", "two-sided"), ("direita", "greater"), ("esquerda", "less")]:
    r = teste_duas_medias(dados1=g1, dados2=g2, variancias_iguais=True, tipo=tipo)
    ref = st.ttest_ind(g1, g2, equal_var=True, alternative=alt)
    conferir("duas medias iguais " + tipo + " estatistica", r["estatistica"], ref.statistic, 1e-9)
    conferir("duas medias iguais " + tipo + " p-valor", r["p_valor"], ref.pvalue, 1e-9)
    r = teste_duas_medias(dados1=g1, dados2=g2, variancias_iguais=False, tipo=tipo)
    ref = st.ttest_ind(g1, g2, equal_var=False, alternative=alt)
    conferir("duas medias welch " + tipo + " estatistica", r["estatistica"], ref.statistic, 1e-9)
    conferir("duas medias welch " + tipo + " p-valor", r["p_valor"], ref.pvalue, 1e-9)
    r = teste_medias_pareadas(dados1=g1, dados2=g2[:8], tipo=tipo)
    ref = st.ttest_rel(g1, g2[:8], alternative=alt)
    conferir("pareado " + tipo + " p-valor", r["p_valor"], ref.pvalue, 1e-9)
    r = teste_media(mu0=12, dados=g1, tipo=tipo)
    ref = st.ttest_1samp(g1, 12, alternative=alt)
    conferir("uma media t " + tipo + " p-valor", r["p_valor"], ref.pvalue, 1e-9)


print()
print("--- erro tipo II e tamanho da amostra ---")

r = calcular_beta(mu0=53, mu_real=56, sigma=4, n=15, alpha=0.05)
conferir("aula 10 beta", r["beta"], 0.17, 0.005)
conferir("aula 10 regiao inferior", r["regiao_aceitacao"][0], 50.975, 0.001)
conferir("aula 10 regiao superior", r["regiao_aceitacao"][1], 55.024, 0.001)

r = calcular_beta(mu0=53, mu_real=56, sigma=4, n=15, regiao_aceitacao=(50.975, 55.024))
conferir("beta com regiao informada", r["beta"], 0.17, 0.005)

r = calcular_beta(mu0=53, mu_real=53, sigma=4, n=15, alpha=0.05)
conferir("beta com mu real igual a mu0 (1 - alpha)", r["beta"], 0.95, 0.0001)

r = tamanho_amostra_teste_media(mu0=127, mu_real=120, sigma=10, alpha=0.05, beta=0.1, tipo="esquerda")
conferir("aula 10 lampadas n minimo", r["n_minimo"], 18, 0)

r = tamanho_amostra_teste_media(mu0=200, mu_real=215, sigma=30, alpha=0.01, beta=0.1, tipo="direita")
conferir("ex16 n minimo", r["n_minimo"], 53, 0)

r = tamanho_amostra_teste_proporcao(p0=0.5, p_real=0.6, alpha=0.05, beta=0.2)
conferir("n minimo teste de proporcao", r["n_minimo"], 194, 0)

r = tamanho_amostra_media(erro=3, confianca=0.90, sigma=20)
conferir("ex8 n minimo", r["n_minimo"], 121, 0)

piloto = [7, 11, 12, 11, 13, 8, 15, 8, 11, 16, 10, 12, 9, 6, 11, 10, 11, 10, 12, 9]
desvio_piloto = st.tstd(piloto)
r = tamanho_amostra_media(erro=0.5, confianca=0.95, desvio=desvio_piloto, distribuicao="z")
conferir("ex9 n minimo com z (resolucao)", r["n_minimo"], 93, 0)
r = tamanho_amostra_media(erro=0.5, confianca=0.95, desvio=desvio_piloto)
conferir("ex9 n minimo com t", r["n_minimo"], 96, 0)

r = tamanho_amostra_proporcao(erro=0.02, confianca=0.95, p=0.10)
conferir("ex3a n minimo", r["n_minimo"], 865, 0)
r = tamanho_amostra_proporcao(erro=0.02, confianca=0.99, p=0.10)
conferir("ex3b n minimo", r["n_minimo"], 1493, 0)
r = tamanho_amostra_proporcao(erro=0.005, confianca=0.99, p=0.95)
conferir("ex4b n minimo", r["n_minimo"], 12607, 0)
r = tamanho_amostra_proporcao(erro=0.04, confianca=0.95)
conferir("ex26 n minimo", r["n_minimo"], 601, 0)
r = tamanho_amostra_proporcao(erro=0.03, confianca=0.95, p=0.1)
conferir("aula 8 fornecedor n minimo", r["n_minimo"], 385, 0)

r = tamanho_amostra_teste_variancia(variancia0=1, variancia_real=2, alpha=0.05, beta=0.1, tipo="direita")
conferir("n minimo teste de variancia (razao 2)", r["n_minimo"], 37, 1)


print()
print("acertos:", acertos, " erros:", erros)
if erros > 0:
    sys.exit(1)
