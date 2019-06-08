#!/usr/bin/python

from flask import Flask, render_template
from flask import jsonify
from math import sqrt
from recomendacao import *

app = Flask(__name__)

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
    return rankings[0:60]

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

@app.route('/filmes', methods=['GET'])
def index():
    return render_template('./index.html')

@app.route('/movies', methods=['GET'])
def movies():
    return jsonify(getRecomentacao(baseMovies,'212'))

@app.route('/movie/<usuario>', methods=['GET'])
def movie(usuario):
    return jsonify(getRecomentacao(baseMovies,usuario))


if __name__ == '__main__':
    app.run(debug=True)