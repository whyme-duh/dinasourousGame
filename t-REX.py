import  pygame, random
pygame.init()
pygame.font.init()

W, H = 800, 400
win = pygame.display.set_mode((W, H))
pygame.display.set_caption("T REX")
clock = pygame.time.Clock()

# image
standing = pygame.image.load('trex1.png')
dino = [pygame.image.load('rex1.png'),pygame.image.load('rex2.png'),pygame.image.load('rex3.png'),pygame.image.load('rex4.png')]
base = pygame.image.load('base.png')
background = pygame.image.load('back.jpg')
obstacle = [pygame.image.load('o1.png'),pygame.image.load('o2.png'),pygame.image.load('o3.png'),pygame.image.load('o4.png'),pygame.image.load('o5.png'),pygame.image.load('o6.png')]
choose = random.randint(0, 6)
dragon = [pygame.image.load('d1.png'),pygame.image.load('d2.png'),pygame.image.load('d1.png'),pygame.image.load('d2.png') ]
game_over = pygame.image.load('over.png')
replay = pygame.image.load('replay.png')
duck = [pygame.image.load('duck1.png'),pygame.image.load('duck2.png'),pygame.image.load('duck1.png'),pygame.image.load('duck2.png')]
# variables
vel = 10
class Dino:
    def __init__(self,x ,y , width, height):
        self.x = x
        self.y = y
        self.width= width
        self.height = height
        self.standing =True
        self.jump_count = 8
        self.is_jump = False
        self.walk_count = 0
        self.img = dino[0]
        self.right = False
        self.duck = False
        self.duck_count = 0


    def draw(self,win):

        if self.walk_count + 1 > 8:
            self.walk_count = 0
        if not(self.standing):
            if not(self.duck):
                win.blit(dino[self.walk_count//2] , (self.x, self.y))
                self.walk_count += 1
        else:
            win.blit(standing, (self.x ,self.y))

        if self.duck_count + 1> 8:
            self.duck_count = 0
        if self.duck:
            win.blit(duck[self.duck_count//2],(self.x, self.y))
            self.duck_count += 1
    def get_mask(self):

        return pygame.mask.from_surface(self.img)

class Obstacle():


    def __init__(self, x,y):
        self.x = x
        self.y = y
        self.block = obstacle[random.randint(0,5)]
        self.passed = False
        self.top = 0

    def move(self):
        self.x -= vel

    def draw(self,win):
        self.move()
        win.blit(self.block, (self.x, self.y))

    def collide(self, rex):
        rex_mask = rex.get_mask()
        block_mask = pygame.mask.from_surface(self.block)
        block_offset = (round(self.x - rex.x ), round(self.y - rex.y) - 5)

        b_point = block_mask.overlap(rex_mask, block_offset)

        if b_point:
            return True
        return False

class Dragon:
    def __init__(self,x  ):
        self.x = x
        self.y = random.randint(230, 250)
        self.img = dragon[0]
        self.fly_count = 0
        self.passed = False
        self.enable = False
    def move(self):

        self.x -= vel

    def draw(self,win):
        self.move()
        if self.fly_count + 1 > 8:
            self.fly_count = 0

        win.blit(dragon[self.fly_count// 3], (self.x ,self.y))
        self.fly_count += int(1)

    def collide1(self, rex):
        rex_mask = rex.get_mask()
        BEAST_MASK = pygame.mask.from_surface(self.img)
        offset = (round(self.x - rex.x)+2, round(self.y - rex.y)+2)
        t_point = rex_mask.overlap(BEAST_MASK , offset)
        if t_point:
            return True
        return False

class Background:
    IMG = background
    width = background.get_width()
    def __init__(self, y):
        self.y = y
        self.x1= 0
        self.x2 = self.width
        self.back_move = False

    def move(self):
        self.x1 -= vel
        self.x2 -= vel
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self,win):
        if self.back_move:
            self.move()
        win.blit(self.IMG ,(self.x1, self.y))
        win.blit(self.IMG, (self.x2 , self.y))

class Base:

    width = base.get_width()
    IMG =base

    def __init__(self,y):
        self.y = y
        self.x1 = 0
        self.x2 = self.width

        self.base_move = False

    def move(self):
        self.x1 -= vel
        self.x2 -= vel
        if self.x1 + self.width < 0:
            self.x1 = self.x2 + self.width

        if self.x2 + self.width < 0:
            self.x2 = self.x1 + self.width

    def draw(self,win):
        if self.base_move:
            self.move()

        win.blit(self.IMG ,(self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))
score = 0
def draw():
    win.fill((255,255,255))
    fnt = pygame.font.Font("Pokemon_GB.ttf", 14)
    text = fnt.render(f'Score : {score}', 1, (0,0,0))
    text1 = fnt.render(f'Highscore : {score}', 1, (148,148,148))
    sky.draw(win)
    win.blit(text, (590, 20))
    base.draw(win)
    for beast in beasts:
        if beast.enable:
            beast.draw(win)
    rex.draw(win)
    for block in blocks:
        block.draw(win)
    if block.collide(rex):
        win.blit(text1, (320, 20))
    pygame.display.update()


def message():

    flag = True
    while flag:
        global run
        win.blit(game_over, (300, 200))
        win.blit(replay, (350, 250))
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                flag = False
                pygame.quit()
            if ev.type == pygame.MOUSEBUTTONDOWN:
                a, b = pygame.mouse.get_pos()
                if a > 350 and a < 350 + replay.get_width():
                    if b > 250 and b < 250 + replay.get_height():

                        main()


        pygame.display.update()





rex = Dino(100 ,300, 64,64)
base = Base(340)
sky = Background(0)
beasts = [Dragon(5000)]
blocks = [Obstacle(700 ,320)]


def main():
    run = True
    while run:

        global score, vel
        FPS = 30
        clock.tick(FPS)
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False
        key = pygame.key.get_pressed()
        if key[pygame.K_RIGHT]:
            rex.standing = False
            base.base_move = True
            sky.back_move = True
            rex.right = True
            rex.duck = False
        if rex.right:
            score += 1

        if key[pygame.K_DOWN]:
            rex.standing= False
            rex.duck = True
            rex.right = False
            rex.standing = False

        if not(rex.is_jump):
            if key[pygame.K_UP]:
                rex.is_jump= True
                rex.walk_count = 0
                rex.duck= False

        else:
            if rex.jump_count >= -8:
                neg = 1
                if rex.jump_count < 0:
                    neg = -1
                rex.y -= (rex.jump_count ** 2) * 0.5 * neg

                rex.jump_count -= 1
            else:
                rex.is_jump = False
                rex.jump_count = 8


        # adding obstacles

        rem = []
        add_block = False
        for block in blocks:
            if block.collide(rex):
                run = False

            if block.x + block.block.get_width() < 0:
                rem.append(block)
            if not block.passed and block.x < rex.x:
                block.passed = True
                add_block = Trueaaaa

        if add_block:

            blocks.append(Obstacle(800, 320))
            if score > 40:
                vel += 0.2

        for r in rem:
            blocks.remove(r)

        cut = []
        add_beast = False
        for beast in beasts:
            if beast.collide1(rex):
                print("ok")
            if beast.x + beast.img.get_width() < 0:
                cut.append(beast)
            if not beast.passed and beast.x < rex.x:
                beast.passed =True
                add_beast = True

        if add_beast:
            beasts.append(Dragon(5700))

        draw()

main()

pygame.quit()
