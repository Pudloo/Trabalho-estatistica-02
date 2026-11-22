# Trabalho II - Probabilidade e Estatística

Alunos: (colocar os nomes)

Funções em Python para intervalos de confiança, testes de hipóteses, erro tipo II (β) e tamanho de amostra.
Não tem menu nem interface: as funções são chamadas direto no código.

## O que foi implementado

**A) Intervalos de confiança**
- média com variância conhecida (Z) e desconhecida (t ou Z, o programa escolhe)
- proporção, com correção de população finita quando N < 20n
- variância (qui-quadrado)
- extra: diferença entre duas médias

**B) Testes de hipóteses** (bilateral, unilateral à esquerda e unilateral à direita)
- uma média contra um valor padrão
- duas médias, com variâncias conhecidas ou desconhecidas
- uma proporção contra um valor padrão e comparação de duas proporções
- uma variância contra um valor padrão e homogeneidade de duas variâncias (teste F)
- extra: médias pareadas

**C) Erro tipo II e tamanho da amostra**
- probabilidade do erro tipo II (β)
- tamanho mínimo da amostra a partir de α e β (média, proporção e variância)
- extra: tamanho da amostra para estimar uma média ou uma proporção

Os intervalos de confiança e os testes ficam em funções separadas.

## Dependências e como rodar

- Python 3.8 ou mais novo
- scipy 1.7 ou mais novo (o numpy já vem junto)

```
pip install -r requirements.txt
python exemplos.py
python verificar_exercicios.py
```

O `exemplos.py` mostra um exemplo de cada função. O `verificar_exercicios.py` confere as funções com os
exercícios resolvidos da lista e com os exemplos dos slides.

## Arquivos

```
estatistica/
    __init__.py
    auxiliares.py             funções de apoio
    intervalos_confianca.py   intervalos de confiança
    testes_hipoteses.py       testes de hipóteses
    erros_e_amostra.py        erro tipo II e tamanho da amostra
exemplos.py
verificar_exercicios.py
requirements.txt
```

## Como usar

A pasta `estatistica` precisa ficar junto do programa que vai chamar as funções.

```python
from estatistica import *

r = ic_media(n=81, media=346, sigma=4.5, confianca=0.95)
print(r["limite_inferior"], r["limite_superior"])
```

Toda função devolve um dicionário, e o valor é pego pela chave, como em `r["limite_inferior"]`.

### Parâmetros que aparecem em várias funções

| parâmetro | significado |
|---|---|
| `confianca` | nível de confiança, entre 0 e 1 (exemplo: `0.95`) |
| `alpha` | nível de significância, entre 0 e 1 (exemplo: `0.05`) |
| `tipo` | `"bilateral"` (padrão), `"esquerda"` ou `"direita"`, que é o lado de H1 |
| `n`, `media` | tamanho e média da amostra |
| `desvio` | desvio padrão da amostra |
| `sigma` | desvio padrão da população, quando é conhecido |
| `variancia_pop` | variância da população, quando é conhecida (no lugar do `sigma`) |
| `dados` | lista com os valores da amostra (no lugar de `n`, `media` e `desvio`) |

Nos intervalos, o `tipo` unilateral devolve só um limite: `"direita"` dá `(limite, +inf)` e `"esquerda"` dá `(-inf, limite)`.

## Funções

### Intervalos de confiança (`intervalos_confianca.py`)

```python
ic_media(n=None, media=None, sigma=None, variancia_pop=None, desvio=None, dados=None,
         confianca=0.95, tipo="bilateral", N=None, forcar_t=False)
```

IC para a média. A distribuição é escolhida assim:

| situação | distribuição |
|---|---|
| sigma (ou variância) conhecido | Z |
| desconhecido e n > 30 | Z, com o desvio da amostra |
| desconhecido e n ≤ 30 | t de Student, com n - 1 graus de liberdade |

`N` é o tamanho da população: se `N < 20n`, o erro padrão é multiplicado por √((N-n)/(N-1)).
Com `forcar_t=True` o programa usa t mesmo com n > 30.

```python
ic_proporcao(x=None, n=None, p=None, confianca=0.95, tipo="bilateral", N=None)
```

IC para a proporção (Z). Pode informar `x` (quantos têm o atributo) ou `p` (a proporção da amostra).
O `N` funciona como na média. Se `n*p` ou `n*(1-p)` for menor ou igual a 5, aparece um `aviso` no retorno.

```python
ic_variancia(n=None, variancia=None, desvio=None, dados=None, confianca=0.95, tipo="bilateral")
```

IC para a variância (qui-quadrado, n - 1 graus de liberdade). Também devolve os limites para o desvio padrão.

```python
ic_diferenca_medias(media1=None, n1=None, media2=None, n2=None,
                    sigma1=None, sigma2=None, variancia_pop1=None, variancia_pop2=None,
                    desvio1=None, desvio2=None, dados1=None, dados2=None,
                    variancias_iguais=None, confianca=0.95, tipo="bilateral", alpha_f=0.05)
```

Extra. IC para μ1 - μ2. Usa Z se os dois sigmas são conhecidos e t nos outros casos
(veja `teste_duas_medias`, que funciona do mesmo jeito).

### Testes de hipóteses (`testes_hipoteses.py`)

```python
teste_media(mu0, n=None, media=None, sigma=None, variancia_pop=None, desvio=None, dados=None,
            alpha=0.05, tipo="bilateral", forcar_t=False)
```

H0: μ = μ0. O `mu0` é o valor padrão. Z ou t são escolhidos pela mesma regra do `ic_media`.

```python
teste_duas_medias(media1=None, n1=None, media2=None, n2=None,
                  sigma1=None, sigma2=None, variancia_pop1=None, variancia_pop2=None,
                  desvio1=None, desvio2=None, dados1=None, dados2=None,
                  variancias_iguais=None, alpha=0.05, tipo="bilateral", alpha_f=0.05)
```

H0: μ1 = μ2. A estatística usa a média 1 menos a média 2, então `tipo="direita"` testa μ1 > μ2.
- Os dois sigmas conhecidos: Z.
- Variâncias desconhecidas: t. Com `variancias_iguais=True` usa a variância combinada (n1 + n2 - 2 graus de liberdade),
  com `False` usa Welch. Se ficar `None`, o programa faz o teste F com `alpha_f` e decide sozinho.

```python
teste_medias_pareadas(dados1=None, dados2=None, media_d=None, desvio_d=None, n=None,
                      alpha=0.05, tipo="bilateral")
```

Extra. H0: μd = 0, com d = grupo 1 menos grupo 2. Informe as duas listas ou então `n`, `media_d` e `desvio_d`.

```python
teste_proporcao(p0, x=None, n=None, p=None, alpha=0.05, tipo="bilateral", metodo="normal")
```

H0: p = p0. O `metodo` pode ser `"normal"` (Z) ou `"exato"` (binomial, precisa do `x`).
Se `n*p0` ou `n*(1-p0)` for menor ou igual a 5, aparece um `aviso`.

```python
teste_duas_proporcoes(x1, n1, x2, n2, alpha=0.05, tipo="bilateral")
```

H0: p1 = p2, com a proporção combinada (Z).

```python
teste_variancia(variancia0=None, desvio0=None, n=None, variancia=None, desvio=None, dados=None,
                alpha=0.05, tipo="bilateral")
```

H0: σ² = σ0². O valor padrão vai em `variancia0` ou `desvio0`. Usa qui-quadrado com n - 1 graus de liberdade.

```python
teste_duas_variancias(n1=None, variancia1=None, desvio1=None, n2=None, variancia2=None, desvio2=None,
                      dados1=None, dados2=None, alpha=0.05, tipo="bilateral")
```

H0: σ1² = σ2² (teste F). No bilateral a maior variância fica em cima, como na aula.
No unilateral, F = variância 1 / variância 2.

### Erro tipo II e tamanho da amostra (`erros_e_amostra.py`)

```python
calcular_beta(mu0, mu_real, sigma=None, n=None, alpha=0.05, tipo="bilateral",
              regiao_aceitacao=None, variancia_pop=None)
```

β = probabilidade de aceitar H0 quando a média verdadeira é `mu_real` (média amostral normal, σ conhecido).
A região de aceitação sai do `alpha` e do `tipo`, ou pode ser informada em `regiao_aceitacao=(inferior, superior)`.

```python
tamanho_amostra_teste_media(mu0, mu_real, alpha=0.05, beta=0.1, tipo="bilateral",
                            sigma=None, variancia_pop=None, desvio=None)
```

Com σ conhecido: n = ((z_α + z_β) · σ / Δ)², com Δ = |mu_real - mu0| (no bilateral usa α/2).
Sem σ, informando o `desvio`, usa t e procura o menor n que atende.

```python
tamanho_amostra_teste_proporcao(p0, p_real, alpha=0.05, beta=0.1, tipo="bilateral")
```

n = ((z_α · √(p0·q0) + z_β · √(p·q)) / Δ)², com p = `p_real`.

```python
tamanho_amostra_teste_variancia(variancia0, variancia_real, alpha=0.05, beta=0.1, tipo="bilateral")
```

Procura o menor n em que o poder do teste (calculado com o qui-quadrado) é pelo menos 1 - β.

```python
tamanho_amostra_media(erro, confianca=0.95, sigma=None, variancia_pop=None, desvio=None, distribuicao="t")
tamanho_amostra_proporcao(erro, confianca=0.95, p=0.5)
```

Extras. Tamanho da amostra para estimar uma média ou uma proporção com um erro máximo dado.
Na média, sem σ, o `desvio` vem do estudo piloto: `distribuicao="t"` (padrão) procura o menor n, e `"z"` usa z direto.
Na proporção, se `p` não for informado, usa 0.5.

## O que as funções retornam

**Intervalos de confiança**

| chave | o que é |
|---|---|
| `estimativa` | estimativa pontual |
| `margem_erro` | margem de erro (na variância é a metade da amplitude do intervalo) |
| `limite_inferior`, `limite_superior` | limites do intervalo |
| `distribuicao`, `gl`, `valor_critico` | o que foi usado no cálculo |
| `erro_padrao` | erro padrão (média e proporção) |
| `correcao_populacao_finita` | `True` se a correção do N foi usada |
| `aviso` | avisos (só na proporção) |
| `interpretacao` | frase com o resultado |

**Testes de hipóteses**

| chave | o que é |
|---|---|
| `H0`, `H1` | as hipóteses, de acordo com o `tipo` |
| `estatistica` | valor da estatística do teste |
| `valores_criticos` | lista com o(s) valor(es) crítico(s) |
| `regiao_rejeicao` | texto com a região de rejeição |
| `p_valor` | p-valor |
| `rejeita_H0` | `True` ou `False` (rejeita quando o p-valor é menor ou igual a alpha) |
| `conclusao` | frase com a conclusão |
| `distribuicao`, `gl`, `aviso` | distribuição usada, graus de liberdade e avisos |

Cada teste também devolve alguns valores extras, como erro padrão e proporções.

**Erro tipo II e tamanho da amostra**
- `calcular_beta`: `beta`, `poder` (1 - β), `regiao_aceitacao`, `z_inferior`, `z_superior`, `H0`, `H1` e `interpretacao`.
- funções de tamanho da amostra: `n_minimo` (já arredondado para cima) e a distribuição usada.

## Exemplos

Os dados são os mesmos das aulas e da lista de exercícios. O `exemplos.py` tem um exemplo de cada função.

### Intervalos de confiança

```python
from estatistica import *

ic_z = ic_media(n=81, media=346, sigma=4.5, confianca=0.95)
ic_t = ic_media(n=15, media=25.31, desvio=1.59, confianca=0.95)
ic_dados = ic_media(dados=[26.7, 25.8, 24.0, 24.9, 26.4], confianca=0.99)
ic_prop = ic_proporcao(x=180, n=300, confianca=0.99)
ic_var = ic_variancia(n=16, variancia=169, confianca=0.95)

print(ic_z["limite_inferior"], ic_z["limite_superior"])
print(ic_var["interpretacao"])
```

Resultados: `ic_z` dá [345.02; 346.98] (margem de 0.98), `ic_t` usa t com 14 graus de liberdade e dá [24.43; 26.19],
`ic_prop` dá [0.5271; 0.6729] e `ic_var` dá [92.22; 404.81].

### Testes de hipóteses

```python
from estatistica import *

teste_z = teste_media(mu0=53, n=30, media=45, sigma=14, alpha=0.01, tipo="esquerda")
teste_t = teste_media(mu0=0.85, n=8, media=0.87, desvio=0.010)
duas_medias = teste_duas_medias(dados1=[12.1, 13.4, 11.8, 14.2], dados2=[10.9, 11.5, 12.3, 10.2], tipo="direita")
prop = teste_proporcao(p0=0.6, x=530, n=1000)
duas_prop = teste_duas_proporcoes(x1=32, n1=80, x2=26, n2=50)
variancia = teste_variancia(desvio0=10, n=16, variancia=169, tipo="direita")
duas_variancias = teste_duas_variancias(dados1=[54, 55, 58, 50, 61], dados2=[51, 54, 55, 52, 53], alpha=0.10)

print(teste_z["H0"], teste_z["H1"], teste_z["estatistica"], teste_z["p_valor"])
print(teste_z["conclusao"])
```

Resultados: `teste_z` dá z = -3.1298 e p-valor = 0.00087 (rejeita H0), `prop` dá z = -4.518 (rejeita H0),
`duas_prop` dá z = -1.339 (não rejeita H0), `variancia` dá qui-quadrado = 25.35 com valor crítico 25.0 (rejeita H0)
e `duas_variancias` dá F = 6.92 com valor crítico 6.39 (rejeita H0).

Saída dos dois `print` acima:

```
H0: mu = 53 H1: mu < 53 -3.1298431857438067 0.0008744982098148672
Rejeita H0. Os dados mostra evidencia a favor de (mu < 53) a nivel de 1% (p-valor = 0.0009).
```

### Erro tipo II e tamanho da amostra

```python
from estatistica import *

beta = calcular_beta(mu0=53, mu_real=56, sigma=4, n=15, alpha=0.05)
n_media = tamanho_amostra_teste_media(mu0=127, mu_real=120, sigma=10, alpha=0.05, beta=0.10, tipo="esquerda")
n_prop = tamanho_amostra_teste_proporcao(p0=0.5, p_real=0.6, alpha=0.05, beta=0.20)
n_var = tamanho_amostra_teste_variancia(variancia0=1, variancia_real=2, alpha=0.05, beta=0.10, tipo="direita")

print(beta["beta"])
print(n_media["n_minimo"], n_prop["n_minimo"], n_var["n_minimo"])
```

Resultados: β = 0.1724 (o poder do teste é 0.8276), e os tamanhos mínimos são 18, 194 e 37.

## Observações

- Para a média, quando σ é desconhecido e n > 30, o programa usa Z com o desvio da amostra, como nos slides das aulas 7 e 10.
  Para usar t sempre, é só passar `forcar_t=True` (a resolução do exercício 2 da lista usa t com n = 36).
- O H0 é rejeitado quando o p-valor é menor ou igual a α. Quando não rejeita, o texto diz "não rejeita H0" e não "aceita H0".
- No exercício 9 da lista, o padrão com t dá n = 96. Com `distribuicao="z"` dá 93, que é a resposta da resolução.
- Alguns valores dos slides estão arredondados, então o `verificar_exercicios.py` usa uma tolerância pequena.
  Como referência foi usada a resolução da lista.
