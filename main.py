import pygame
import random

#Funções
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from recursos.funcoes import mover_obstaculos
limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()
pygame.init()

while True:
    nome = input("Nickname: ")
    if len(nome) > 0: 
        break
    else:
        print("Nome Inválido!")
        
tamanho = (1000,700)
pygame.display.set_caption("Iron Man de Pensamento Computacional")
icone  = pygame.image.load("assets/icone.webp")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
branco = (255, 255, 255)
preto = (0, 0, 0)

#Telas
fundo = pygame.image.load("assets/TelaFundo1000x700.png")
fundoDead = pygame.image.load("assets/BackgroundDead.png.png")
fundoDead = pygame.transform.scale(fundoDead, (1000, 700))
fundoStart = pygame.image.load("assets/TelaStart.png")

#Personagens e Obstáculos
superman = pygame.image.load("assets/superman.png")
superman = pygame.transform.scale(superman, (120,60))
vilao = pygame.image.load("assets/Vilão.webp")
vilao = pygame.transform.scale(vilao, (180,100))
meteorito = pygame.image.load("assets/meteorito.png")
meteorito = pygame.transform.scale(meteorito, (70,70))

#Sons
VilaoSound = pygame.mixer.Sound("assets/VilaoSound.mp3")
explosaoSound = pygame.mixer.Sound("assets/explosao.wav")
pygame.mixer.music.load("assets/esperança.mp3")

fonteMenu = pygame.font.SysFont("comicsans",18)

def jogar():
    posicaoXPersona = 0
    posicaoYPersona = 60
    movimentoXPersona  = 0
    movimentoYPersona  = 0
    velocidadeMovPersona = 5
    posicaoXVilao = 1000
    posicaoYVilao = random.randint(0, 675)
    velocidadeVilao = 2
    pontos = 0
    pygame.mixer.Sound.play(VilaoSound)
    pygame.mixer.music.play(-1)
    dificuldade = 20
    obstaculos = []
    tempo_spawn = 0
    pause = False

    for i in range(10):
        obstaculos.append({
            "x": random.randint(0, 900),
            "y": random.randint(-400, 0),
            "velocidade": random.randint(3, 8)
        })
    
    while True:
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                quit()
                movimentoXPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP or evento.type == pygame.KEYDOWN and evento.key == pygame.K_w:
                movimentoYPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN or evento.type == pygame.KEYDOWN and evento.key == pygame.K_s:
                movimentoYPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP or evento.type == pygame.KEYUP and evento.key == pygame.K_w:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN or evento.type == pygame.KEYUP and evento.key == pygame.K_s:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT or evento.type == pygame.KEYDOWN and evento.key == pygame.K_d:
                movimentoXPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT or evento.type == pygame.KEYDOWN and evento.key == pygame.K_a:
                movimentoXPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT or evento.type == pygame.KEYUP and evento.key == pygame.K_d:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT or evento.type == pygame.KEYUP and evento.key == pygame.K_a:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pause = not pause

        if pause:
            texto_pause = fonteMenu.render("JOGO PAUSADO - Pressione ESPAÇO para continuar", True, branco)

            tela.blit(texto_pause, (300, 350))

            pygame.display.update()
            relogio.tick(60)
            continue
                
        
        posicaoXPersona = posicaoXPersona + movimentoXPersona          
        posicaoYPersona = posicaoYPersona + movimentoYPersona 
        player_rect = pygame.Rect(
            posicaoXPersona + 20,
            posicaoYPersona + 10,
            80,
            40
        )

        if posicaoXPersona < 0:
            posicaoXPersona = 0
        elif posicaoXPersona > 880:   # 1000 - 116
            posicaoXPersona = 880

        if posicaoYPersona < 0:
            posicaoYPersona = 0
        elif posicaoYPersona > 640:   # 700 - 51
            posicaoYPersona = 640
            
        posicaoXVilao = posicaoXVilao - velocidadeVilao
        if posicaoXVilao < -180:
            pygame.mixer.Sound.play(VilaoSound)
            posicaoXVilao = 1000
            pontos = pontos + 1
            velocidadeVilao += 1
            posicaoYVilao = random.randint(0,600)

        tempo_spawn += 1

        if tempo_spawn > 30:
            obstaculos.append({
            "x": random.randint(0, 900),
            "y": -50,
            "velocidade": random.randint(4, 10)
        })
        tempo_spawn = 0
        mover_obstaculos(obstaculos)
                            
        tela.fill(branco)
        tela.blit(fundo, (0,0) )
        player_rect = pygame.Rect(posicaoXPersona, posicaoYPersona, 120, 60)

        for obstaculo in obstaculos:
                obstaculo["velocidade"] += 0.002

                meteor_rect = pygame.Rect(
                    obstaculo["x"] + 15,
                    obstaculo["y"] + 15,
                    50,
                    50
                )

        tela.blit(meteorito, (obstaculo["x"], obstaculo["y"]))
        if player_rect.colliderect(meteor_rect):
            escreverDados(nome, pontos)
            dead()
            return
            
        tela.blit(superman, (posicaoXPersona,posicaoYPersona))
        tela.blit(vilao, (posicaoXVilao, posicaoYVilao) )
        texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
        tela.blit(texto, (700,15))
            
        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona+116))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona+51))
        pixelsVilaoX = list(range(posicaoXVilao, posicaoXVilao + 180))
        pixelsVilaoY = list(range(posicaoYVilao, posicaoYVilao + 100))
        if  len( list( set(pixelsVilaoY).intersection(set(pixelsPersonaY))) ) > dificuldade:
            if len( list( set(pixelsVilaoX).intersection(set(pixelsPersonaX))   ) )  > dificuldade:
                escreverDados(nome, pontos)
                dead()
                return
                
            else:
                print("Ainda Vivo, mas por pouco!")
        else:
            print("Ainda Vivo")
        
        
        
        pygame.display.update()
        relogio.tick(60)

def dead():
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()

                    pygame.mixer.music.stop()
                    pygame.mixer.music.load("Bases/esperança.mp3")
                    pygame.mixer.music.play(-1)
                    
                    jogar()
                    return
            
        tela.fill(branco)
        tela.blit(fundoDead, (0,0))
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))


        pygame.display.update()
        relogio.tick(60)



def start():
    larguraButtonStart = 150
    alturaButtonStart  = 40
    larguraButtonQuit = 150
    alturaButtonQuit  = 40
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    larguraButtonStart = 140
                    alturaButtonStart  = 35
                if quitButton.collidepoint(evento.pos):
                    larguraButtonQuit = 140
                    alturaButtonQuit  = 35

                
            elif evento.type == pygame.MOUSEBUTTONUP:
                # Verifica se o clique foi dentro do retângulo
                if startButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonStart = 150
                    alturaButtonStart  = 40
                    jogar()
                if quitButton.collidepoint(evento.pos):
                    #pygame.mixer.music.play(-1)
                    larguraButtonQuit = 150
                    alturaButtonQuit  = 40
                    quit()
            
        tela.fill(branco)
        tela.blit(fundoStart, (0,0))
        startButton = pygame.draw.rect(tela, branco, (10,10, larguraButtonStart, alturaButtonStart), border_radius=15)
        startTexto = fonteMenu.render("Iniciar Game", True, preto)
        tela.blit(startTexto, (25,12))
        
        quitButton = pygame.draw.rect(tela, branco, (10,60, larguraButtonQuit, alturaButtonQuit), border_radius=15)
        quitTexto = fonteMenu.render("Sair do Game", True, preto)
        tela.blit(quitTexto, (25,62))
        texto = fonteMenu.render(f"The Best - {nome_maior} - {maior_pontos} - { dataJogada} ", True, branco)
        tela.blit(texto, (480,15))
        

        pygame.display.update()
        relogio.tick(60)
           
start()