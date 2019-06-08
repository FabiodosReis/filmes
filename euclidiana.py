
from math import sqrt
from recomendacao import *

#retorna o percentual de similaridade entre duas pessoas
def euclidiana(base,usuario1, usuario2):
    si = {}
    for item in base[usuario1]:
        if item in base[usuario2]: si[item] = 1
    if len(si) == 0: return 0
    soma = sum([pow(base[usuario1][item] - base[usuario2][item], 2)
                for item in base[usuario1] if item in base[usuario2]])
    return 1/(1 + sqrt(soma))

#retorna a similaridade com todas as pessoas baseados nos filmes asistidos
def getSimilares(base,usuario):
    similaridade = [(euclidiana(base,usuario, outro), outro)
                    for outro in base if outro != usuario]
    similaridade.sort()
    similaridade.reverse()
    return similaridade[0:30]

#função de recomendacao, encontra pessos similares e faz indicação de filmes
def getRecomentacao(base,usuario):
    totais = {}
    somaSimilaridade = {}
    for outro in base:
        if outro == usuario: continue
        similaridade = euclidiana(base,usuario,outro)

        if similaridade <= 0: continue

        for item in base[outro]:
            if item not in base[usuario]:
                totais.setdefault(item,0)
                totais[item] += base[outro][item] * similaridade
                somaSimilaridade.setdefault(item,0)
                somaSimilaridade[item] += similaridade

    rankings = [(total / somaSimilaridade[item],item) for item, total in totais.items()]
    rankings.sort()
    rankings.reverse()
    return rankings[0:30]

def carregaMovieLens(path='C:/ml-100k'):
    filmes = {}
    for linha in open(path + '/u.item'):
        (id, titulo) = linha.split('|')[0:2]
        filmes[id] = titulo
    base = {}
    for linha in open(path + '/u.data'):
        (usuario,idFilme,nota,tempo) = linha.split('\t')
        base.setdefault(usuario,{})
        base[usuario][filmes[idFilme]] = float(nota)
    return base

baseMovies = carregaMovieLens()

#calculando a similaridade entre dois usuarios
#print(euclidiana(avaliacoesUsuario,'Adriano','Leonardo'));

#calculando a similaridade entre todos usuarios
#print(getSimilares(avaliacoesUsuario,'Leonardo'));

#Recomendar FIlmes para usuario baseado em outros usuarios
#print(getRecomentacao(avaliacoesUsuario,'Leonardo'))

#Buscar filmes mais semelhantes
#print(getSimilares(avaliacoesFilme,'Star Wars'))


