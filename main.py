import pygame
import random

#Funções
from recursos.trabalho import inicializarBancoDeDados, limpar_tela, escreverDados, maior_pontuador
from recursos.trabalho import mover_obstaculos
limpar_tela()
inicializarBancoDeDados()
nome_maior, maior_pontos, dataJogada = maior_pontuador()
pygame.init()

while True:
    nome = input("Nickname: ")
    if len(nome) > 0: 
        break
    else:
        print(" Nome Inválido!")
        
tamanho = (1000,700)
pygame.display.set_caption("Iron Man de Pensamento Computacional")
icone  = pygame.image.load("base/icone.webp")
pygame.display.set_icon(icone)
relogio = pygame.time.Clock()
tela = pygame.display.set_mode( tamanho ) 
branco = (255, 255, 255)
preto = (0, 0, 0)

#Telas
fundoBoasVindas = pygame.image.load("base/BoasVindas.png")
fundo = pygame.image.load("base/TelaFundo1000x700.png")
fundoDead = pygame.image.load("base/BackgroundDead.png.png")
fundoDead = pygame.transform.scale(fundoDead, (1000, 700))
fundoStart = pygame.image.load("base/TelaStart.png")

#Personagens e Obstáculos
satelite = pygame.image.load("base/satelite.png")
satelite = pygame.transform.scale(satelite, (80, 40))
superman = pygame.image.load("base/superman.png")
superman = pygame.transform.scale(superman, (120,60))
vilao = pygame.image.load("base/Vilão.webp")
vilao = pygame.transform.scale(vilao, (180,100))
meteorito = pygame.image.load("base/meteorito.png")
meteorito = pygame.transform.scale(meteorito, (70,70))

#Sons
VilaoSound = pygame.mixer.Sound("base/VilaoSound.mp3")
explosaoSound = pygame.mixer.Sound("base/explosao.wav")
pygame.mixer.music.load("base/esperança.mp3")

fonteMenu = pygame.font.SysFont("comicsans",18)

def boas_vindas():
    larguraBotao = 200
    alturaBotao = 50

    while True:
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                quit()

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if startButton.collidepoint(evento.pos):
                    jogar()
                    return

        tela.blit(fundoBoasVindas, (0,0))

        titulo = fonteMenu.render(
            f"Bem-vindo, {nome}!",
            True,
            branco
        )
        tela.blit(titulo, (50, 50))

        explicacao1 = fonteMenu.render(
            "Use W/S ou as setas ↑ ↓ para mover o Superman.",
            True,
            branco
        )
        tela.blit(explicacao1, (50, 120))   

        explicacao2 = fonteMenu.render(
            "Desvie dos meteoritos e do vilao, cada vez desviado o vilão aumenta sua velocidade. Cuidado!!",
            True,
            branco
        )
        tela.blit(explicacao2, (50, 150))

        explicacao3 = fonteMenu.render(
            "Quanto mais tempo sobreviver, mais pontos ganha.",
            True,
            branco
        )
        tela.blit(explicacao3, (50, 180))

        recorde = fonteMenu.render(
            f"Recorde: {nome_maior} - {maior_pontos} pts",
            True,
            branco
        )
        tela.blit(recorde, (50, 250))

        data = fonteMenu.render(
            f"Data: {dataJogada}",
            True,
            branco
        )
        tela.blit(data, (50, 280))

        startButton = pygame.draw.rect(
            tela,
            branco,
            (350, 500, larguraBotao, alturaBotao),
            border_radius=15
        )

        textoBotao = fonteMenu.render(
            "INICIAR PARTIDA",
            True,
            preto
        )

        tela.blit(textoBotao, (380, 515))

        pygame.display.update()
        relogio.tick(60)

def jogar():
    posicaoXPersona = 440
    posicaoYPersona = 60
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

    #Sol
    sol_x = 900
    sol_y = 80
    sol_raio = 40
    sol_crescendo = True
    sol_raio_min = 25
    sol_raio_max = 60

    # Objetos decorativo
    satelite_x = random.randint(0, 920)
    satelite_y = random.randint(0, 660)
    satelite_vel_x = random.choice([-2, -1, 1, 2])
    satelite_vel_y = random.choice([-2, -1, 1, 2])
    contador_mudanca = 0
    pause = False


    texto = fonteMenu.render("Pontos: "+str(pontos), True, branco)
    tela.blit(texto, (700,15))

    textoPause = fonteMenu.render(
        "Press Space to Pause Game",
        True,
        branco
    )
    tela.blit(textoPause, (10, 675))

    for i in range(3):
        obstaculos.append({
            "x": random.randint(-800, -70),
            "y": random.randint(0, 630),
            "velocidade": random.randint(4, 8)
        })
    
    while True:
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                 pygame.quit()
                 quit()

            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP or evento.type == pygame.KEYDOWN and evento.key == pygame.K_w:
                movimentoYPersona = -velocidadeMovPersona
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_DOWN or evento.type == pygame.KEYDOWN and evento.key == pygame.K_s:
                movimentoYPersona = velocidadeMovPersona
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP or evento.type == pygame.KEYUP and evento.key == pygame.K_w:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_DOWN or evento.type == pygame.KEYUP and evento.key == pygame.K_s:
                movimentoYPersona = 0
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
                pause = not pause

        if pause:
            texto_pause = fonteMenu.render("JOGO PAUSADO - Pressione ESPAÇO para continuar", True, branco)

            tela.blit(texto_pause, (300, 350))

            pygame.display.update()
            relogio.tick(60)
            continue
                
                  
        posicaoYPersona = posicaoYPersona + movimentoYPersona 
        player_rect = pygame.Rect(
            posicaoXPersona + 20,
            posicaoYPersona + 10,
            80,
            40
        )


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

        mover_obstaculos(obstaculos)

        tela.fill(branco)
        tela.blit(fundo, (0,0)) 
          
        # Animação do sol
        if sol_crescendo:
            sol_raio += 0.7
            if sol_raio >= 60:
             sol_crescendo = False
        else:
            sol_raio -= 0.7
            if sol_raio <= 25:
                sol_crescendo = True

        pygame.draw.circle(
            tela,
            (255, 255, 0),  # amarelo
            (sol_x, sol_y),
            int(sol_raio)
        )

        tela.blit(satelite, (satelite_x, satelite_y))               
        player_rect = pygame.Rect(posicaoXPersona, posicaoYPersona, 120, 60)

        for obstaculo in obstaculos:

            obstaculo["x"] += obstaculo["velocidade"]

        if obstaculo["x"] > 1000:
                obstaculo["x"] = -70
                obstaculo["y"] = random.randint(0, 630)

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
        textoPause = fonteMenu.render(
            "Pressione ESPACO para pausar",
            True,
            branco
        )

        tela.blit(textoPause, (10, 670))
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
        
        contador_mudanca += 1

        if contador_mudanca >= 60:
            satelite_vel_x = random.choice([-2, -1, 1, 2])
            satelite_vel_y = random.choice([-2, -1, 1, 2])
            contador_mudanca = 0

        satelite_x += satelite_vel_x
        satelite_y += satelite_vel_y

        if satelite_x < 0 or satelite_x > 920:
            satelite_vel_x *= -1

        if satelite_y < 0 or satelite_y > 660:
            satelite_vel_y *= -1
        
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
        tela.blit(fundoBoasVindas, (0,0))
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
           
boas_vindas()