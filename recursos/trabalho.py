import os, time
import json
import random
from datetime import datetime

def limpar_tela():
    os.system("cls")
    
def aguarde(segundos):
    time.sleep(segundos)
    
def inicializarBancoDeDados():
    # r - read, w - write, a - append
    try:
        banco = open("log.dat.atitus","r")
    except:
        print("Banco de Dados Inexistente. Criando...")
        banco = open("log.dat.atitus","w")
    
def escreverDados(nome, pontos):
    # INI - inserindo no arquivo
    banco = open("log.dat.atitus","r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}
        
def escreverDados(nome, pontos):
    # INI - inserindo no arquivo
    banco = open("log.dat.atitus","r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}

    data_br = datetime.now().strftime("%d/%m/%Y")
    hora = datetime.now().strftime("%H:%M:%S")
    dadosDict[nome] = [pontos, data_br, hora]

    banco = open("log.dat.atitus","w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
    banco = open("log.dat.atitus","w")
    banco.write(json.dumps(dadosDict))
    banco.close()
    
    # END - inserindo no arquivo
    
def maior_pontuador():
    banco = open("log.dat.atitus","r")
    dados = banco.read()
    banco.close()
    if dados != "":
        dadosDict = json.loads(dados)
    else:
        dadosDict = {}

    nome_maior = None
    dataJogada =  None
    maior_pontos = -1

    for nome, info in dadosDict.items():

        pontos = info[0]
        
        if pontos > maior_pontos:
            maior_pontos = pontos
            nome_maior = nome
            dataJogada = info[1]            

    return nome_maior, maior_pontos, dataJogada


def mover_obstaculos(obstaculos):
    for obstaculo in obstaculos:
        obstaculo["x"] += obstaculo["velocidade"]

        if obstaculo["x"] > 1000:
            obstaculo["x"] = -70
            obstaculo["y"] = random.randint(0, 630)