import pygame
import random
from recursos.funcoes import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador

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

fundo = pygame.image.load("assets/TelaFundo1000x700.png")
fundoDead = pygame.image.load("assets/BackgroundDead.png.png")
fundoDead = pygame.transform.scale(fundoDead, (1000, 700))
fundoStart = pygame.image.load("assets/TelaStart.png")

superman = pygame.image.load("assets/superman.png")
superman = pygame.transform.scale(superman, (116,51))
vilao = pygame.image.load("assets/Vilão.webp")
vilao = pygame.transform.scale(vilao, (180,100))
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
                
        
        posicaoXPersona = posicaoXPersona + movimentoXPersona          
        posicaoYPersona = posicaoYPersona + movimentoYPersona 

        if posicaoXPersona < 0:
            posicaoXPersona = 0
        elif posicaoXPersona > 884:   # 1000 - 116
            posicaoXPersona = 884

        if posicaoYPersona < 0:
            posicaoYPersona = 0
        elif posicaoYPersona > 649:   # 700 - 51
            posicaoYPersona = 649
            
        posicaoXVilao = posicaoXVilao - velocidadeVilao
        if posicaoXVilao < -180:
            pygame.mixer.Sound.play(VilaoSound)
            posicaoXVilao = 1000
            pontos = pontos + 1
            velocidadeVilao += 1
            posicaoYVilao = random.randint(0,600)
                            
        tela.fill(branco)
        tela.blit(fundo, (0,0) )
        
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