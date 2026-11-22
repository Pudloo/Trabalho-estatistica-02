from estatistica import *


def mostrar(titulo, resultado):
    print("=" * 60)
    print(titulo)
    print("=" * 60)
    for chave in resultado:
        print(chave, ":", resultado[chave])
    print()


print("----- A) INTERVALOS DE CONFIANCA -----")
print()

r = ic_media(n=81, media=346, sigma=4.5, confianca=0.95)
mostrar("IC para media com sigma conhecido (Z)", r)

r = ic_media(n=15, media=25.31, desvio=1.59, confianca=0.95)
mostrar("IC para media com sigma desconhecido e n pequeno (t)", r)

potencia = [26.7, 25.8, 24.0, 24.9, 26.4, 25.9, 24.4, 21.7, 24.1, 25.9, 27.3, 26.9, 27.3, 24.8, 23.6]
r = ic_media(dados=potencia, confianca=0.95)
mostrar("IC para media passando a lista de dados", r)

r = ic_media(n=100, media=65.5, desvio=4.8, confianca=0.95)
mostrar("IC para media com sigma desconhecido e n > 30 (Z)", r)

r = ic_media(n=64, media=142, desvio=24, confianca=0.95, tipo="esquerda")
mostrar("IC unilateral para media", r)

r = ic_proporcao(x=180, n=300, confianca=0.99)
mostrar("IC para proporcao", r)

r = ic_proporcao(x=60, n=100, confianca=0.95, N=1500)
mostrar("IC para proporcao com populacao pequena (N < 20n)", r)

r = ic_variancia(n=16, variancia=169, confianca=0.95)
mostrar("IC para variancia", r)

r = ic_diferenca_medias(media1=42, n1=25, desvio1=8, media2=38, n2=25, desvio2=6, confianca=0.95)
mostrar("IC para diferenca de medias (extra)", r)


print("----- B) TESTES DE HIPOTESES -----")
print()

r = teste_media(mu0=0.85, n=8, media=0.87, desvio=0.010, alpha=0.05, tipo="bilateral")
mostrar("Teste para uma media (t)", r)

r = teste_media(mu0=53, n=30, media=45, sigma=14, alpha=0.01, tipo="esquerda")
mostrar("Teste para uma media com sigma conhecido (Z)", r)

r = teste_duas_medias(media1=24000, n1=50, sigma1=2500, media2=26000, n2=40, sigma2=3000,
                      alpha=0.04, tipo="bilateral")
mostrar("Duas medias com variancias conhecidas (Z)", r)

grupo1 = [12.1, 13.4, 11.8, 14.2, 13.0, 12.7, 15.1, 12.2]
grupo2 = [10.9, 11.5, 12.3, 10.2, 11.8, 12.0, 10.7, 11.1, 12.5]
r = teste_duas_medias(dados1=grupo1, dados2=grupo2, alpha=0.05, tipo="direita")
mostrar("Duas medias com variancias desconhecidas (escolhe sozinho iguais ou diferentes)", r)

novo = [22, 21, 28, 30, 33, 33, 26, 24, 31, 22]
antigo = [25, 28, 26, 36, 32, 39, 28, 33, 30, 27]
r = teste_medias_pareadas(dados1=novo, dados2=antigo, alpha=0.05, tipo="esquerda")
mostrar("Teste para medias pareadas (extra)", r)

r = teste_proporcao(p0=0.6, x=530, n=1000, alpha=0.05, tipo="bilateral")
mostrar("Teste para uma proporcao", r)

r = teste_duas_proporcoes(x1=32, n1=80, x2=26, n2=50, alpha=0.05, tipo="bilateral")
mostrar("Comparacao de duas proporcoes", r)

r = teste_variancia(desvio0=10, n=16, variancia=169, alpha=0.05, tipo="direita")
mostrar("Teste para uma variancia", r)

r = teste_duas_variancias(dados1=[54, 55, 58, 50, 61], dados2=[51, 54, 55, 52, 53], alpha=0.10,
                          tipo="bilateral")
mostrar("Homogeneidade de duas variancias (teste F)", r)


print("----- C) ERRO TIPO II E TAMANHO DA AMOSTRA -----")
print()

r = calcular_beta(mu0=53, mu_real=56, sigma=4, n=15, alpha=0.05, tipo="bilateral")
mostrar("Probabilidade do erro tipo II (beta)", r)

r = calcular_beta(mu0=53, mu_real=56, sigma=4, n=15, regiao_aceitacao=(50.975, 55.024))
mostrar("Beta com a regiao de aceitacao informada", r)

r = tamanho_amostra_teste_media(mu0=127, mu_real=120, sigma=10, alpha=0.05, beta=0.10, tipo="esquerda")
mostrar("Tamanho minimo da amostra (media)", r)

r = tamanho_amostra_teste_proporcao(p0=0.5, p_real=0.6, alpha=0.05, beta=0.20, tipo="bilateral")
mostrar("Tamanho minimo da amostra (proporcao)", r)

r = tamanho_amostra_teste_variancia(variancia0=1, variancia_real=2, alpha=0.05, beta=0.10, tipo="direita")
mostrar("Tamanho minimo da amostra (variancia)", r)

r = tamanho_amostra_media(erro=0.5, confianca=0.95, desvio=2.458)
mostrar("Tamanho da amostra para estimar uma media (extra)", r)

r = tamanho_amostra_proporcao(erro=0.04, confianca=0.95)
mostrar("Tamanho da amostra para estimar uma proporcao (extra)", r)
