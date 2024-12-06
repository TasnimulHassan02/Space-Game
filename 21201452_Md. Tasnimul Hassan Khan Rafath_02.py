from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from numpy import random


width = 1200
height = 750
space_x, space_y = width//2 - 50, 50
bullets = []
bullet_speed = 5
enemys = []
enemy_speed = 0.2
sp_enemys = []
sp_enemy_speed = 0.2
valid_x = list(range(100, width - 100, 100))
valid_x2 = list(range(100, width - 100, 100))
score = 0
injury = 0
miss = 0
game_over = False
states = True
dec = True


def draw_points(x, y):
    glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x,y)
    glEnd()

def FindZone(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    if dx == 0:  
        if dy > 0:
            return 1 
        else:
            return 5
    elif dy == 0:
        if dx > 0:
            return 0  
        else:
            return 4
    if abs(dx) > abs(dy):
        if dx > 0 and dy > 0:
            return 0
        elif dx < 0 and dy > 0:
            return 3
        elif dx < 0 and dy < 0:
            return 4
        elif dx > 0 and dy < 0:
            return 7
    else:
        if dx > 0 and dy > 0:
            return 1
        elif dx < 0 and dy > 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        elif dx > 0 and dy < 0:
            return 6

def ConvertMtoZero(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (y, -x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (-y, x)
    elif zone == 7:
        return (x, -y)

def ConvertZeroToM(x, y, zone):
    if zone == 0:
        return (x, y)
    elif zone == 1:
        return (y, x)
    elif zone == 2:
        return (-y, x)
    elif zone == 3:
        return (-x, y)
    elif zone == 4:
        return (-x, -y)
    elif zone == 5:
        return (-y, -x)
    elif zone == 6:
        return (y, -x)
    elif zone == 7:
        return (x, -y)

def MidpointLine(x1, y1, x2, y2, zone):
    dx = x2 - x1
    dy = y2 - y1
    E  = 2 * dy
    NE = 2 * (dy - dx)
    d = 2 * dy - dx 
    x = x1
    y = y1
    cx, cy = ConvertZeroToM(x, y, zone)
    draw_points(cx, cy)
    while (x <= x2):
        if d <= 0:
            d = d + E
            x = x + 1
        else:
            d = d + NE
            x = x + 1
            y = y + 1      
        cx, cy = ConvertZeroToM(x, y, zone)
        draw_points(cx, cy)

def MidpointLineEightway(x1, y1, x2, y2):
    zone = FindZone(x1, y1, x2, y2)
    x1, y1 = ConvertMtoZero(x1, y1, zone)
    x2, y2 = ConvertMtoZero(x2, y2, zone)
    MidpointLine(x1, y1, x2, y2, zone)

def CirclePoints(x, y, cx, cy):
    draw_points( x + cx,  y + cy)
    draw_points( y + cx,  x + cy)  
    draw_points( y + cx, -x + cy) 
    draw_points( x + cx, -y + cy) 
    draw_points( -x + cx, -y + cy) 
    draw_points( -y + cx, -x + cy) 
    draw_points( -y + cx,  x + cy) 
    draw_points( -x + cx,  y + cy)

def MidpointCircle(radius, cx, cy):
    d = 1 - radius
    x = 0                       
    y = radius
    CirclePoints(x, y, cx, cy)
    while x < y:
        if d < 0:
            d = d + 2*x + 3 
            x = x + 1
        else:
            d = d + 2*x - 2*y + 5
            x = x + 1
            y = y - 1
        CirclePoints(x, y, cx, cy)

def spaceship(x,y):
    glColor3f(1.0, 1.0, 0)
    MidpointLineEightway(x+1, y, x+1, y+100)
    MidpointLineEightway(x+79, y, x+79, y+100)
    MidpointLineEightway(x-50, y, x, y+50)
    MidpointLineEightway(x+130, y, x+80, y+50)
    MidpointLineEightway(x+1, y+100, x+78, y+100)
    MidpointLineEightway(x+1, y+100, x+39, y+150)
    MidpointLineEightway(x+79, y+100, x+40, y+150)
    MidpointLineEightway(x-50, y, x+129, y)
    MidpointLineEightway(x+22, y-15, x+22, y-40)
    MidpointLineEightway(x+42, y-15, x+42, y-40)
    MidpointLineEightway(x+62, y-15, x+62, y-40)

def bullet():
    global bullets, miss, height, game_over
    new_bullets = []
    glColor3f(1.0, 0, 0)
    for b in bullets:
        if b[1] < height:
            MidpointCircle(7, b[0], b[1])
            new_bullets.append((b[0], b[1]+ bullet_speed))
        else:
            miss += 1
            print("Missed Enemy:", miss)
            if miss == 3 and not game_over:
                game_over = True
                print("Game Over!\nFinal Score:", score)
                bullets.clear()
                enemys.clear()
    bullets = new_bullets

def enemy():
    global enemys, enemy_speed, injury, game_over, score
    glColor3f(1.0, 0, 1.0)
    if game_over:
        return None
    new_enemys = []
    for e in enemys:
        MidpointCircle(e[0], e[1], e[2])
        e[2] -= enemy_speed
        if e[2] + e[0] > 0:
            new_enemys.append(e)
        else:
            injury += 1
            print("Life Remaining:", 3-injury)
            if injury == 3 and not game_over:
                game_over = True
                print("Game Over!\nFinal Score:", score)
                bullets.clear()
                enemys.clear()  
    enemys = new_enemys

def enemy_incomming(value):
    global enemys, valid_x
    radius = random.randint(20, 40)
    x = random.choice(valid_x) 
    enemys.append([radius, x, height - 50 - radius])
    glutTimerFunc(1700, enemy_incomming, 0)

def collision():
    global space_x, space_y, enemys, bullets, score, game_over, sp_enemys, enemy_speed, sp_enemy_speed
    if game_over:
        return None
    for e in enemys:
        for b in bullets:
            hit = b[0]-10 < (e[1]+e[0]) and (b[0]+10 > e[1]-e[0]) and b[1] < (e[2]+e[0]) and (b[1]+10 > e[2]-e[0])
            if hit:
                enemys.remove(e)
                bullets.remove(b)
                score += 1
                print("Score:", score)
                print("Life Remaining:", 3-injury)
                print("Missed Enemy:", miss)
                if score % 10 == 0:
                    enemy_speed += 0.1
                    sp_enemy_speed += 0.1
                    print("Level Increased")
        crash = space_x < (e[1]+e[0]) and (space_x+80 > e[1]-e[0]) and space_y < (e[2]+e[0]) and (space_y+150 > e[2]-e[0])
        if crash and not game_over:
            game_over = True
            print("Game Over!\nFinal Score:", score)
            bullets.clear() 
            enemys.clear()
    for e in sp_enemys:
        for b in bullets:
            hit = b[0]-10 < (e[1]+e[0]) and (b[0]+10 > e[1]-e[0]) and b[1] < (e[2]+e[0]) and (b[1]+10 > e[2]-e[0])
            if hit:
                sp_enemys.remove(e)
                bullets.remove(b)
                score += 3
                print("Score:", score)
                print("Life Remaining:", 3-injury)
                print("Missed Enemy:", miss)
        crash = space_x < (e[1]+e[0]) and (space_x+80 > e[1]-e[0]) and space_y < (e[2]+e[0]) and (space_y+150 > e[2]-e[0])
        if crash and not game_over:
            game_over = True
            print("Game Over!\nFinal Score:", score)
            bullets.clear() 
            sp_enemys.clear()

def control():
    glColor3f(0, 1.0, 1.0)
    MidpointLineEightway(20, 720, 35, 735)
    MidpointLineEightway(20, 720, 60, 720)
    MidpointLineEightway(20, 720, 35, 705)
    glColor3f(.2, .5, .2)
    MidpointLineEightway(580, 705, 580, 735)
    MidpointLineEightway(610, 705, 610, 735)
    glColor3f(1.0, 0, 0)
    MidpointLineEightway(1150, 705, 1180, 735)
    MidpointLineEightway(1180, 705, 1150, 735)

def special_enemy():
    global sp_enemys, sp_enemy_speed, injury, game_over, dec
    glColor3f(0, 1.0, 0)
    if game_over:
        return None
    new_enemys = []
    for e in sp_enemys:
        MidpointCircle(e[0], e[1], e[2])
        if dec:
            e[0] -= 1
            if e[0] == 1:
                dec = not dec
        if not dec:
            e[0] += 1
            if e[0] == 20:
                dec = not dec
        e[2] -= sp_enemy_speed
        if e[2] + e[0] > 0:
            new_enemys.append(e)
        else:
            injury += 1
            print("Life Remaining:", 3-injury)
            if injury == 3 and not game_over:
                game_over = True
                print("Game Over!\nFinal Score:", score)
                bullets.clear()
                sp_enemys.clear()  
    sp_enemys = new_enemys

def sp_enemy_incomming(value):
    global sp_enemys, valid_x2
    radius = random.randint(15, 20)
    x = random.choice(valid_x) 
    sp_enemys.append([radius, x, height - 50 - radius])
    glutTimerFunc(10000, sp_enemy_incomming, 0)

def iterate():
    glViewport(0, 0, 1200, 750)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1200, 0.0, 750, 0.0, 1.0)
    glMatrixMode (GL_MODELVIEW)
    glLoadIdentity()

def showScreen():
    global space_x, space_y
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    iterate()
    spaceship(space_x, space_y)
    bullet()
    enemy()
    special_enemy()
    collision()
    control()
    glutSwapBuffers()

def mouseListener(button, state, x, y):
    global score, miss, injury, width, height, space_x, space_y, bullets, enemys, states, sp_enemys
    y = height - y
    if button==GLUT_LEFT_BUTTON:
        if(state == GLUT_DOWN):
            if 20<x<60 and 705<y<735:
                score, miss, injury = 0, 0, 0
                space_x, space_y = width//2 - 50, 50
                bullets = []
                enemys = []
                sp_enemys = []
                print("Starting Over!")
            if 580<x<610 and 705<y<735:
                states = not states
                if states:
                    glutIdleFunc(showScreen) 
                    print("Game Resumed")
                else:
                    glutIdleFunc(None)
                    print("Game Paused")         
            if 1150<x<1180 and 705<y<735:
                print("Goodbye!\nFinal Score:", score)
                glutLeaveMainLoop() 
    glutPostRedisplay()
          

def keyboardListener(key, x, y):
    global space_x, bullets, game_over
    if game_over:
        return None
    if key==b'a':
        if 50<space_x<width:
            space_x-=10
    if key==b'd':
        if 50<=space_x<width-130:
            space_x+=10
    if key == b' ':
        bullets.append((space_x + 40, space_y + 150))
        print("Firing Bullet")
    glutPostRedisplay()
print("Game Started!")
print("Score:", score)    
print("Life:", 3-injury)
print("Miss:", miss)

glutInit()
glutInitDisplayMode(GLUT_RGBA)
glutInitWindowSize(1200, 750)
glutInitWindowPosition(150, 0)
wind = glutCreateWindow(b"Shoot The Circles!")
glutDisplayFunc(showScreen)
glutKeyboardFunc(keyboardListener)
glutMouseFunc(mouseListener)
glutIdleFunc(showScreen)
glutTimerFunc(1700, enemy_incomming, 0)
glutTimerFunc(10000, sp_enemy_incomming, 0)
glutMainLoop()