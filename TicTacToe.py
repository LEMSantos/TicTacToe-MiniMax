import pygame

WIDTH = 500
HEIGHT = 500
FPS = 30
BACKGROUND_COLOR = (20,189,172)
LINE_COLOR = (0,0,50)
CPU_PLAYER = 2
PLAYER = 1
BOARD_SIZE = 3
BOARD = []

pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
clock = pygame.time.Clock()

def MiniMax(node, depth, maximizer):
    if terminal(node) or depth == 0:
        return heuristic(node)
    elif maximizer == False:
        alpha = 10000
        successors = successor(node,maximizer)
        for son in successors:
            alpha = min(alpha,MiniMax(son, depth - 1, True))
        return alpha
    else:
        alpha = -10000
        successors = successor(node,maximizer)
        for son in successors:
            alpha = max(alpha,MiniMax(son, depth - 1, False))
        return alpha

def terminal(node):
    if victory(node, CPU_PLAYER) or victory(node, PLAYER) or draw(node):
        return True
    return False

def draw(node):
    for line in node:
        if 0 in line:
            return False
    return True

def victory(node, player):
    if node[0][0] == player and node[0][1] == player and node[0][2] == player:
        return True
    if node[1][0] == player and node[1][1] == player and node[1][2] == player:
        return True
    if node[2][0] == player and node[2][1] == player and node[2][2] == player:
        return True
    if node[0][0] == player and node[1][0] == player and node[2][0] == player:
        return True
    if node[0][1] == player and node[1][1] == player and node[2][1] == player:
        return True
    if node[0][2] == player and node[1][2] == player and node[2][2] == player:
        return True
    if node[0][0] == player and node[1][1] == player and node[2][2] == player:
        return True
    if node[2][0] == player and node[1][1] == player and node[0][2] == player:
        return True
    return False

def heuristic(node):
    heuristic_sum = 0
    
    points = ()
    # points(diagonal,center,side)
    if PLAYER == 1:
        points = (10,15,5)
    else:
        points = (15,10,5)
    
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if node[i][j] != 0:
                if i == 1 and j == 1:
                    heuristic_sum += (points[1] if node[i][j] == CPU_PLAYER else -points[1])
                elif abs(i-j) == 2 or abs(i-j) == 0:
                    heuristic_sum += (points[0] if node[i][j] == CPU_PLAYER else -points[0])
                else:
                    heuristic_sum += (points[2] if node[i][j] == CPU_PLAYER else -points[2])
                
    if victory(node,CPU_PLAYER):
        heuristic_sum += 100
    elif victory(node, PLAYER):
        heuristic_sum -= 100
    return heuristic_sum

def board_copy(node):
    board_aux = []
    for line in node:
        board_aux.append(line.copy())
    return board_aux

def successor(node, maximizer):
    player = 0
    if maximizer:
        player = CPU_PLAYER
    else:
        player = PLAYER

    successors = []
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if node[i][j] == 0:
                aux = board_copy(node)
                aux[i][j] = player
                successors.append(aux)
    return successors

def inicialize():
    global BOARD
    square_areas = []
    y = 100
    for i in range(BOARD_SIZE):
        x = 100
        for j in range(BOARD_SIZE):
            square_areas.append(pygame.Rect(x,y,100,100))
            x+=100
        y+=100
    for i in range(BOARD_SIZE):
        BOARD.append([])
        for j in range(BOARD_SIZE):
            BOARD[i].append(0)
    return square_areas

def restart_game(cpu_start):
    global BOARD,PLAYER,CPU_PLAYER

    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            BOARD[i][j] = 0
    if not cpu_start:
        PLAYER = 1
        CPU_PLAYER = 2
        return True
    else:
        PLAYER = 2
        CPU_PLAYER = 1
        return False
        
        
    
running = True
playing = True
area = inicialize()
x_sprite = pygame.image.load("sprites/x_sprite.png")
circle_sprite = pygame.image.load("sprites/circle_sprite.png")
restart_sprite = pygame.transform.scale(pygame.image.load("sprites/Restart_sprite.png"),(107,21))
restart = restart_sprite.get_rect(center = (250,450))
auto_start_sprite = pygame.transform.scale(pygame.image.load("sprites/Auto_start_message.png"),(343,21))
auto_start = auto_start_sprite.get_rect(center = (175.5,15.5))
myfont = pygame.font.SysFont('Comic Sans Ms', 30)
winner_message = ''

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(area)):
                if area[i].collidepoint(event.pos) and BOARD[i//3][i%3] == 0:
                    BOARD[i//3][i%3] = PLAYER
                    playing = False
                    break
            if restart.collidepoint(event.pos):
                winner_message = ''
                playing = restart_game(False)
            if auto_start.collidepoint(event.pos):
                winner_message = ''
                playing = restart_game(True)

                
    if victory(BOARD, CPU_PLAYER):
        winner_message = 'CPU Wins'
        playing = False
    elif victory(BOARD, PLAYER):
        winner_message = 'Player Wins'
        playing = False
    elif draw(BOARD):
        playing = False
        winner_message = 'Draw'
    else:
        if not playing:
            index = 0
            successors = successor(BOARD,True)
            max_num = -10000
            for i in range(len(successors)):
                aux = MiniMax(successors[i],4,False)
                if aux > max_num:
                    max_num = aux
                    index = i
            BOARD = successors[index]
            playing = True
    
    screen.fill(BACKGROUND_COLOR)
    for i in range(len(area)):
        pygame.draw.rect(screen,BACKGROUND_COLOR,area[i])
    pygame.draw.rect(screen,LINE_COLOR,[100,198,300,4])
    pygame.draw.rect(screen,LINE_COLOR,[100,298,300,4])
    pygame.draw.rect(screen,LINE_COLOR,[198,100,4,300])
    pygame.draw.rect(screen,LINE_COLOR,[298,100,4,300])
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if BOARD[i][j] == 1:
                screen.blit(x_sprite,(j*100+100+18,i*100+100+18))
            elif BOARD[i][j] == 2:
                screen.blit(circle_sprite,(j*100+100+18,i*100+100+18))

    text_surface = myfont.render(winner_message,False,(255,255,255))
    screen.blit(text_surface,(100, 42))
    screen.blit(restart_sprite,restart)
    screen.blit(auto_start_sprite,auto_start)            
    pygame.display.update()
    clock.tick(FPS)
    
pygame.quit()

