import pygame
from pygame.locals import *

pygame.init() 
pygame.mixer.init()
screen_width=600
screen_hieght=500
screen =pygame.display.set_mode((screen_width,screen_hieght)) 
pygame.display.set_caption('Ping Pong by supro') 
fpsClock=pygame.time.Clock()


#define font 
font= pygame.font.SysFont('Constantia',30) 

#define game variables
margin= 50
cpu_score=0
player_score=0 
fps=60
winner =0
live_ball=False
speed_increase=0
sound1 = pygame.mixer.Sound('Bouncing on paddle.wav')
sound1.set_volume(200)
sound2= pygame.mixer.Sound('Bouncy Ball.mp3')
sound3=pygame.mixer.Sound('Pong wall.mp3')
#define colours
bg=(50,25,50)
white=(255,255,255) 
def draw_board():
    screen.fill(bg)
    pygame.draw.line(screen,white,(0,margin),(screen_width,margin))  

def draw_text(text,font,text_col,x,y): 
    img= font.render(text,True,text_col)
    screen.blit(img,(x,y))

#paddle class
class paddle(): 
    def __init__(self,x,y):
        self.x=x
        self.y=y
        self.rect=Rect(self.x,self.y,20,100) 
        self.speed=5 
    def move(self): 
        key=pygame.key.get_pressed()
        if key[pygame.K_UP] and self.rect.top> margin :
            self.rect.move_ip(0,-1*self.speed)
        if key[pygame.K_DOWN] and self.rect.bottom<screen_hieght:
            self.rect.move_ip(0,1*self.speed)
    def draw(self): 
        pygame.draw.rect(screen,white,self.rect)
    def ai(self):  
        #ai to move paddle automatically
        #move down
        if self.rect.centery<pong.rect.top and self.rect.bottom<screen_hieght:
            self.rect.move_ip(0,self.speed) 
        if self.rect.centery>pong.rect.bottom and self.rect.top> margin: 
            self.rect.move_ip(0,-1*self.speed)             
sound1 = pygame.mixer.Sound('Bouncing on paddle.wav')
#ball class
class ball(): 
    def __init__(self,x,y):
        self.reset(x,y)      
        
    def draw(self):
        pygame.draw.circle(screen,white,(self.rect.x+self.ball_rad, self.rect.y+self.ball_rad),self.ball_rad)
    def move(self):
        #collision detection
        #check with top margin 
        if self.rect.top<margin:
            self.speed_y*=-1
            sound2.play()  
        #check with bottom margin 
        if self.rect.bottom>screen_hieght:
            self.speed_y*=-1
            sound2.play() 
        #check for collision with paddles 
        if self.rect.colliderect(player_paddle) or self.rect.colliderect(cpu_paddle):
            self.speed_x *=-1
            sound1.play()  # Play the sound.
        #check for out of bounds
        if self.rect.left<0:
            self.winner=1
            sound3.play()
        if self.rect.right>screen_width:
            self.winner=-1
            sound3.play ()
        #update ball pos.
        self.rect.x+=self.speed_x
        self.rect.y+=self.speed_y

        return self.winner 
    def reset(self,x,y): 
        self.x=x
        self.y=y
        self.ball_rad=8
        self.rect=Rect(self.x,self.y,self.ball_rad*2,self.ball_rad*2)  
        self.speed_x=-4  
        self.speed_y=4
        self.winner=0 #1 means player has scored  #-1 means CpU has scored 

  
#create instances of paddles
player_paddle=paddle(screen_width-40,screen_hieght//2)
cpu_paddle=paddle(20,screen_hieght//2)           
#create instances of ball
pong=ball(screen_width-60,screen_hieght//2+50) 

#game loop and event handler
run=True 
while run: 
    fpsClock.tick(fps)
    draw_board()
    draw_text('CPU: '+ str(cpu_score),font,white,20,15 ) 
    draw_text('P1: '+ str(player_score),font,white,screen_width-100,15)
    draw_text('BALL SPEED '+ str(abs(pong.speed_x)), font, white, screen_width//2-100,15) 
    #draw paddles
    player_paddle.draw()
    cpu_paddle.draw()
    cpu_paddle.ai() 


    
    if live_ball== True: 
        #speed_increase 
        speed_increase+=1 
        #move ball
        winner=pong.move()
        if winner==0: 

          #move paddle
          player_paddle.move()

          #draw the ball
          pong.draw()
        else:
            live_ball=False
            if winner ==1:
                player_score +=1
            elif winner ==-1:
                cpu_score +=1

    #print player instruction 
    if live_ball== False:
        if winner==0:
            draw_text('CLICK ANYWHERE TO START', font , white,100,screen_hieght//2-100)
        if winner==1:
            draw_text('YOU SCORED!!', font , white,220,screen_hieght//2-100)
            draw_text('CLICK ANYWHERE TO START', font , white,100,screen_hieght//2-50) 
        if winner==-1: 
            draw_text('CPU SCORED!!', font , white,220,screen_hieght//2-100)
            draw_text('CLICK ANYWHERE TO START', font , white,100,screen_hieght//2-50) 


    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            run=False
        if event.type==pygame.MOUSEBUTTONDOWN and live_ball ==False:
            live_ball=True 
            pong.reset(screen_width-60,screen_hieght//2+50)
    pygame.display.update()

    if speed_increase>500: 
        speed_increase=0
        if pong.speed_x <0:
            pong.speed_x-=1
        if pong.speed_x >0:
            pong.speed_x+=1
    
        if pong.speed_y <0:
            pong.speed_y-=1
        if pong.speed_y >0:
            pong.speed_y+=1     

     
pygame.quit(); 


