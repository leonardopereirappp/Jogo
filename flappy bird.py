import pygame  # Biblioteca de jogos
import os  # Biblioteca de integração de arquivos
import random  # Biblioteca que escolhe algo aleatoriamente

largura, altura = 500, 800

# Definir os sprites do jogo:
imagem_cano, imagem_chao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png'))), pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png'))),
imagem_background, imagens_passaro = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png'))), [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
                                                                                                    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
                                                                                                    pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))]
# O método transform.scale2x, multiplica a imagem em 2 em x e y, imagino eu!
# O bird possuem 3 imagens para dar a sensação de movimento do pássaro, mas para isso é preciso passar uma lista python que contenha as 3 imagens

pygame.font.init()
fonte_pontos = pygame.font.SysFont(name="Comic-sans", size=50, bold=True)
fonte_gameover = pygame.font.SysFont(name="Arial", size=50, bold=False)


class Passaro:
    IMGS = imagens_passaro
    rotacao_maxima, velocidade_rotacao, tempo_animacao = 25, 15, 5  # Aquela animação que o gemaplys aplica no Super_Chicken_Jumper para o obj_bird ficar dinâmico

    def __init__(self, x, y):  # Tu tem que dizer em que lugar da tela ele vai nascer
        self.x = x
        self.y = y
        self.angulo = 0  # Ângulo do pássaro
        self.velocidade = 0  # Velocidade de rotação do pássaro
        self.altura = self.y
        self.tempo = 0  # Tempo de animação do pássaro  No caso teria de usar aquela equação do S= So + Vo.t + at²/2 , aquela do ensino médio
        self.contagem_imagem = 0  # Saber qual das imagens (1,2,3) está se utilizando
        self.imagem = self.IMGS[0]  # Saber qual das imagens o pássaro vai iniciar no jogo

    def pular(self):
        self.velocidade = -10.5  # É importante ressaltar que o Pygame começa o plano cartesiano na esquerda superior, nada intuitivo, mas é assim que fizeram
        self.tempo = 0  # Na verdade, pode ser intuitivo se você pensar no lançamento vertical, quando se joga um corpo contra a gravidade, está se negativando o valor da resultante ( Y )
        self.altura = self.y  # Já o X, é igual ao plano cartesiano de origem matemática, pois começa na esquerda e para a direita aumenta

    def mover(self):
        # Calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo**2) + self.velocidade * self.tempo  # S= So + Vo.t + at²/2
        # Restringir o deslocamento
        if deslocamento > 12:
            deslocamento = 12
        elif deslocamento < 0:
            deslocamento -= 1  # Essa linha de código serve para o pássaro na hora de subir, subir um pouco mais do que já sobe para ajudar o player, porque o pássaro tende a cair mais rápido que subir

        self.y += deslocamento
        # Ângulo do pássaro
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotacao_maxima:
                self.angulo = self.rotacao_maxima
        else:
            if self.angulo > -30:
                self.angulo -= self.velocidade_rotacao

    def desenhar(self, tela):
        # Definir qual a imagem do pássaro vai se utilizar
        self.contagem_imagem += 1
        if self.contagem_imagem < self.tempo_animacao:
            self.imagem = self.IMGS[0]
        elif self.contagem_imagem < self.tempo_animacao * 2:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem < self.tempo_animacao * 3:
            self.imagem = self.IMGS[2]
        elif self.contagem_imagem < self.tempo_animacao * 4:
            self.imagem = self.IMGS[1]
        elif self.contagem_imagem >= self.tempo_animacao * 4 + 1:
            self.imagem = self.IMGS[0]
            self.contagem_imagem = 0

        # Se o pássaro tiver caindo, não bate a asa
        if self.angulo <= -80:
            self.imagem = self.IMGS[1]
            self.contagem_imagem = self.tempo_animacao * 2

        # Desenhar a imagem
        imagem_rotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        pos_centro_imagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagem_rotacionada.get_rect(center=pos_centro_imagem)  # Imagino que essa linha de código seja a hit-box
        tela.blit(imagem_rotacionada, retangulo.topleft)

    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)  # Basicamente a hitbox que diz: o pássaro e o chão, ou cano, tem um pixel em comum? Ou seja, houve colisão? Se sim, you lose


class Cano:
    distancia, velocidade = 200, 5  # Distância que o pássaro tem para passar e a velocidade no qual ele se movimenta para <- -X

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.pos_topo = 0
        self.pos_base = 0
        self.cano_topo = pygame.transform.flip(imagem_cano, False, True)  # Flip => Flipar no eixo x? False, Flipar no eixo y? True
        self.cano_base = imagem_cano
        self.passou = False  # O cano já passou do pássaro?
        self.definir_altura()  # A função init vai chamar a outra função que está abaixo

    def definir_altura(self):
        self.altura = random.randrange(50, 450)
        self.pos_topo = self.altura - self.cano_topo.get_height()  # Para pegar o ponto esquerdo superior da imagem como referência, porque o pygame pega o ponto esquerdo sup. como ref pra tudo
        self.pos_base = self.altura + self.distancia

    def mover(self):
        self.x -= self.velocidade

    def desenhar(self, tela):
        tela.blit(self.cano_topo, (self.x, self.pos_topo))
        tela.blit(self.cano_base, (self.x, self.pos_base))

    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.cano_topo)  # Criado a coliosão do cano do topo
        base_mask = pygame.mask.from_surface(self.cano_base)  # Criado a coliosão do cano da base
        distancia_topo = (self.x - passaro.x, self.pos_topo - round(passaro.y))  # O round arredonda o número do pássaro
        distancia_base = (self.x - passaro.x, self.pos_base - round(passaro.y))
        topo_ponto = passaro_mask.overlap(topo_mask, distancia_topo)  # Retorna um Boolean de T ou F para a pergunta: Colidiu no cano de cima?:
        base_ponto = passaro_mask.overlap(base_mask, distancia_base)  # Retorna um Boolean de T ou F para a pergunta: Colidiu no cano de baixo?:

        if base_ponto or topo_ponto:
            return True
        else:
            return False

class Chao:
    velocidade = 5
    largura = imagem_chao.get_width()
    imagem = imagem_chao

    def __init__(self, y):  # O eixo y serve para definir o x do primeiro chão e do segundo chão
        self.y = y
        self.x0 = 0  # X do chão 1
        self.x1 = self.largura  # X do chão 2 # O selfx0 é igual a 0 mas para entender a lógica, deixei esse cara na fórmula.
        # Quando o jogo começar, vão existir dois chãos, um colado no outro

    def mover(self):
        self.x0 -= self.velocidade
        self.x1 -= self.velocidade

        if self.x0 + self.largura < 0:  # Se o cara saiu da tela
            self.x0 = self.x1 + self.largura  # Coloca ele atrás do chão 2
        if self.x1 + self.largura < 0:
            self.x1 = self.x0 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x0, self.y))
        tela.blit(self.imagem, (self.x1, self.y))


class Background:
    velocidade = 2
    largura = imagem_background.get_width()
    imagem = imagem_background

    def __init__(self, y):  # O eixo y serve para definir o x do primeiro chão e do segundo chão
        self.y = y
        self.bg0 = 0  # X do chão 1
        self.bg1 = self.largura  # X do chão 2 # O self.bg0 é igual a 0 mas para entender a lógica, deixei esse cara na fórmula.
        # Quando o jogo começar, vão existir dois chãos, um colado no outro

    def mover(self):
        self.bg0 -= self.velocidade
        self.bg1 -= self.velocidade
        if self.bg0 + self.largura < 0:  # Se o cara saiu da tela
            self.bg0 = self.bg1 + self.largura  # Coloca ele atrás do chão 2
        if self.bg1 + self.largura < 0:
            self.bg1 = self.bg0 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.bg0, self.y))
        tela.blit(self.imagem, (self.bg1, self.y))

def desenhar_tela(tela, fundo, passaros, canos, chao, pontuacao):
    fundo.desenhar(tela)
    for passaro in passaros:
        passaro.desenhar(tela)
    for cano in canos:
        cano.desenhar(tela)

    texto = fonte_pontos.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))  # O 1 é para ficar bonito e não pixelado  o (255,255,255) é o RGB da cor branca
    tela.blit(texto, (largura - 10 - texto.get_width(), 10))
    chao.desenhar(tela)
    pygame.display.update()

def main():
    background = Background(0)
    passaros = [Passaro(230, 350)]
    chao = Chao(730)
    canos = [Cano(700)]
    tela = pygame.display.set_mode((largura, altura))
    ponto = 0
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        # Quantidade de FPS a serem plotados pelo jogo
        relogio.tick(30)  # ESSA PORRA AQUI, SE MODIFICADO ELEVA A VELOCIDADE DO JOGO PACARALHO
        # Interação do usuário com o game
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    for passaro in passaros:
                        passaro.pular()

        # Mover os objetos
        for passaro in passaros:
            passaro.mover()
        chao.mover()
        background.mover()

        adicionar_cano = False
        remover_canos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                if not cano.passou and passaro.x > cano.x:  # Ou seja, se o pássaro já passou do cano
                    cano.passou = True
                    adicionar_cano = True
            cano.mover()
            if cano.x + cano.cano_topo.get_width() < 0:
                remover_canos.append(cano)
        if adicionar_cano:
            ponto += 1
            canos.append(Cano(600))
        for cano in remover_canos:
            canos.remove(cano)

        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)

        desenhar_tela(tela, background, passaros, canos, chao, ponto)


if __name__ == '__main__':
    main()
