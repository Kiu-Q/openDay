import pygame as pg
import random
import mediapipe as mp
import cv2
import shelve
import time

AMENDMENT = 0
CONFIDENCE = 0.5
SCORE = 0
LIMIT = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0 ,0)
FONTTYPE = "comicsans"
SIZE = 30
FILE = "src/file"

pg.init()

FONT = pg.font.SysFont(FONTTYPE, SIZE)
W, H = int(pg.display.Info().current_w*0.9), int(pg.display.Info().current_h*0.9)

SHOOTER = pg.transform.scale(pg.image.load("assets/shooter.png"), (W//5, W//5))
BGS = [pg.transform.scale(pg.image.load("assets/BGS/%d.png"%i), (W+30, H+100)) for i in range(4)]
BALLONS = [pg.transform.scale(pg.image.load("assets/BALLONS/%d.png"%i), (W//10, W//10*pg.image.load("assets/BALLONS/%d.png"%i).get_height()//pg.image.load("assets/BALLONS/%d.png"%i).get_width())) for i in range(10)]
STUDENTS = [pg.transform.scale(pg.image.load("assets/STUDENTS/%d.png"%i), (W//10, W//10*pg.image.load("assets/STUDENTS/%d.png"%i).get_height()//pg.image.load("assets/STUDENTS/%d.png"%i).get_width())) for i in range(4)]
MONSTERS = [pg.transform.scale(pg.image.load("assets/MONSTERS/%d.png"%i), (W//10, W//10*pg.image.load("assets/MONSTERS/%d.png"%i).get_height()//pg.image.load("assets/MONSTERS/%d.png"%i).get_width())) for i in range(5)]
LOADS = [pg.transform.scale(pg.image.load("assets/LOADS/%d.png"%i), (W//2, W//2)) for i in range(16)]
GIFS = [pg.transform.scale(pg.image.load("assets/GIFS/%d.png"%i), (W//10, W//10*pg.image.load("assets/GIFS/%d.png"%i).get_height()//pg.image.load("assets/GIFS/%d.png"%i).get_width())) for i in range(4)]
COUNTS = [pg.transform.scale(pg.image.load("assets/COUNTS/monophy_1-%d.png"%i), (W//2, W//2)) for i in range(49)]
EXPLODE = pg.transform.scale(pg.image.load("assets/EXPLODE.png"), (W//5, W//5))
CRACK = pg.mixer.Sound(file="assets/sound.wav")
BEEP = pg.mixer.Sound(file="assets/BEEP.wav")
BEEPH = pg.mixer.Sound(file="assets/BEEPH.wav")

MPHANDS = mp.solutions.hands.Hands(
        model_complexity=0,
        min_detection_confidence=CONFIDENCE,
        min_tracking_confidence=CONFIDENCE)
CAP = cv2.VideoCapture(0)

CAPTION = "HFC Info Day Shooting Game - 50th Aniversary Special Edition"
RANK = ["1st", "2nd", "3rd", "4th", "5th"]
INTRO = [["Level 1: Score EXACTLY 50 points as soon as possible.",
            "Press <SPACE> to start", 
            "Top 5 completing time: "], 
        ["Level 2: For whatever reason, there are some MONSTERS invaded HFC.",
                "Shoot them and DON'T SHOOT the STUDENTS.", 
                "Press <SPACE> to start", 
                "Top 5 Scores: "]]

screen = pg.display.set_mode((W,H))
pg.display.set_caption(CAPTION)

class Main:
    def __init__(self):
        self.screen = screen
                
    def main(self):
        self.game = Game().level1()
        if self.game:self.game = Game().level2()
        
    def printText(self, text, color = BLACK, add = 0):
        for line in text:
            printLine = FONT.render(line, True, color)
            self.screen.blit(printLine, (W // 2 - printLine.get_width()//2, H // 3 +(text.index(line)+1)*30+add))
        pg.display.update()
            
    def space(self):
        event = pg.event.wait()
        if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: return
        else: self.space()
        
    def count(self):
        for cnt in range(len(COUNTS)):
            self.screen.blit(BGS[3], (0,0))
            self.screen.blit(COUNTS[cnt], (W//2-COUNTS[cnt%len(COUNTS)].get_width()//2, H//2-COUNTS[cnt%len(COUNTS)].get_height()//2))
            if cnt%len(COUNTS)//5 == 0 or cnt == len(COUNTS): BEEP.play()
            time.sleep(5/len(COUNTS))
            pg.display.update()

class Game(Main):
    def __init__(self):
        super().__init__()
        try: 
            self.prev = self.prev
            self.level = self.level
        except: 
            self.prev = 0
            self.level = 1
                            
    def level1(self):
        with shelve.open(FILE) as d: self.tScores = d['tScore1']
        self.screen.blit(BGS[0], (0,0))
        self.printText(INTRO[0])
        for i in range(5):
            self.screen.blit(FONT.render(RANK[i], True, BLACK), (W//2-200, H//3+120+30*i))
            self.screen.blit(FONT.render(self.tScores[i][0].strip(), True, BLACK), (W//2-100, H//3+120+30*i))
            self.screen.blit(FONT.render("Time: %ds"%self.tScores[i][1], True, BLACK), (W//2+100, H//3+120+30*i)) 
        pg.display.update()
        self.space()
        self.count()
        BEEPH.play()
        self.start = pg.time.get_ticks()
        self.score = SCORE
        self.level = 1
        self.player = Shooter()
        self.targets = [Ballon()]
        self.prev = self.targets[0].pos[0]
        self.result = self.run(1)
        if self.result: return self.win(1)
        else: return self.lose(1)
    
    def level2(self):
        with shelve.open(FILE) as d: self.tScores = d['tScore2']
        self.screen.blit(BGS[0], (0,0))
        self.printText(INTRO[1])
        for i in range(5):
            screen.blit(FONT.render(RANK[i], True, BLACK), (W//2-200, H//3+150+30*i))
            screen.blit(FONT.render(self.tScores[i][0].strip(), True, BLACK), (W//2-100, H//3+150+30*i))
            screen.blit(FONT.render("Score: %d"%self.tScores[i][1], True, BLACK), (W//2+100, H//3+150+30*i)) 
        pg.display.update()
        self.space()
        self.count()
        BEEPH.play()
        self.start = pg.time.get_ticks()
        self.score = SCORE
        self.times = LIMIT
        self.level = 2
        self.player = Shooter()
        self.targets = [Monster()]
        self.prev = self.targets[0].pos[1]
        self.result = self.run(2)
        if self.result: return self.win(2)
        else: return self.lose(2)
        
    def run(self, level):
        self.screen.fill(WHITE)
        self.screen.blit(BGS[3], (0,0))
        if random.randint(0, 50) == 1 or self.targets == []:
            self.targets.append(Ballon() if level == 1 else Monster())
        if level == 1:
            for target in self.targets: 
                target.update((target.pos[0], target.pos[1]-random.randint(2, 5)))
                if target.pos[1]<-H//4:
                    self.targets.remove(target)
                    self.targets.append(Ballon())
        elif level == 2:
            for target in self.targets: 
                target.update((target.pos[0]-random.randint(2, 5), target.pos[1]))
                if target.pos[0]<0-W//10:
                    self.targets.remove(target)
                    self.targets.append(Ballon())
       
        self.timeUsed = (pg.time.get_ticks() - self.start) // 1000 if level == 1 else self.times - (pg.time.get_ticks() - self.start) // 1000

        self.screen.blit(FONT.render("Time Used: " + str(self.timeUsed), True, BLACK), (10, 40)) if level == 1 else self.screen.blit(FONT.render("Time Remaining: " + str(self.timeUsed), True, BLACK if self.timeUsed > 5 else RED), (10, 40))

        results = MPHANDS.process(cv2.cvtColor(CAP.read()[1], cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                self.player.update([W-(hand_landmarks.landmark[7].x * W), hand_landmarks.landmark[7].y * H+AMENDMENT])
            for target in self.targets:
                if target.collide(self.player.pos):
                    self.screen.blit(EXPLODE, (target.pos[0]-100, self.player.pos[1]-100))
                    CRACK.play()
                    if isinstance(target, Ballon) or isinstance(target, Monster):
                        self.score += target.num if level == 1 else 1
                        self.targets.remove(target)
                        randSeed = random.randint(0, 4)
                        if randSeed != 1 and randSeed%2 == 0:
                            self.targets.append(Ballon() if level == 1 else Monster())
                        elif randSeed == 1:
                            self.targets.append(Ballon() if level == 1 else Student())
                    else: return False
        
        time.sleep(0.02)
        if level == 1:
            if self.score == 50:
                return True
            elif self.score>50:
                return False
            else:
                self.screen.blit(FONT.render("Score: " + str(self.score)+" / 50", True, BLACK), (10, 10))
                pg.display.update()
                return self.run(level)        
        else:
            if self.timeUsed <= 0:
                return True
            else:
                screen.blit(FONT.render("Score: " + str(self.score), True, BLACK), (10, 10))
                pg.display.update()
                return self.run(level)

    def win(self, level):
        self.screen.blit(BGS[0], (0,0))
        if (self.timeUsed < self.tScores[4][1] if level ==1 else self.score > self.tScores[4][1]):
            self.tScores.append(["", self.timeUsed if level ==1 else self.score])
            while True:
                HIGH = [["50 points scored! Time used: %ds"%self.timeUsed, 
                    "Congratulations, your score gets into Top 5 completeing time!", 
                    "Please enter your name (At most 10 charachters) to have a cool record",
                    "Name: %s |"%self.tScores[5][0]], 
                    ["Time's Up! Final Score: %d"%self.score, 
                    "Congratulations, your score gets into Top 5 Scores!", 
                    "Please enter your name (At most 10 charachters) to have a cool record",
                    "Name: %s |"%self.tScores[5][0]]]
                event = pg.event.wait()
                self.screen.blit(BGS[0], (0,0))
                self.printText(HIGH[level-1], BLACK, 60)
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    break
                elif event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
                    self.tScores[5][0] = self.tScores[5][0][:-1]
                elif event.type == pg.KEYDOWN and len(self.tScores[5][0]) < 10:
                    self.tScores[5][0] += event.unicode
            with shelve.open(FILE) as d:
                self.tScores.sort(reverse=level-1, key=lambda x: x[1])
                self.tScores.pop()
                d['tScore%d'%level] = self.tScores
        else:
            WIN = [["50 points scored! Time used: %ds"%self.timeUsed,
                    "Press <SPACE> to Level 2"], 
                    ["Time's Up! Final Score: %d"%self.score if self.score < 30 else "Time's Up! Final Score %d higher than 30!"%self.score,
                    "Press <SPACE> to restart"]]
            self.printText(WIN[level-1], BLACK, 60)
            self.space()
        return True
            
    def lose(self, level):
        self.screen.blit(BGS[0], (0,0))
        LOSE = [["Over 50 points scored! You Lose.",
                        "Press <SPACE> to restart"], 
                ["You shoot the student! You Lose.",
                       "Press <SPACE> to restart"]]
        self.printText(LOSE[level-1], RED, 60)
        self.space()
        return False

class Object (Game):
    def __init__(self):
        super().__init__()
        
    def update(self, fPos):
        self.pos = fPos
        self.rect.center = fPos
        self.screen.blit(self.pic, self.rect)
    
    def collide(self, pos):
        return self.rect.collidepoint(pos)
    
    def setPos(self):
        if self.level == 1:
            xPos = random.randint(W//10, W-W//10)
            if xPos in range(self.prev-W//10, self.prev): yPos -=W//10
            elif xPos in range(self.prev, self.prev+W//10): yPos +=W//10
            self.prev = xPos
            return [xPos, H+H//5]
        elif self.level == 2:
            yPos = random.randint(H//5, H-H//5)
            if yPos in range(self.prev-H//5, self.prev): yPos -=H//5
            elif yPos in range(self.prev, self.prev+H//5):  yPos +=H//5
            self.prev = yPos
            return [W+W//10, yPos]

class Shooter(Object):
    def __init__(self):
        self.pic = SHOOTER
        self.pos = [W//2, H//2]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
        super().__init__()
                        
class Ballon(Object):
    def __init__(self):
        super().__init__()
        self.pos = self.setPos()
        self.num = random.randint(0, 9) if random.randint(0, 9)%2 == 0 else random.randint(1, 3)
        self.pic = BALLONS[self.num]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
        
class Student(Object):
    def __init__(self):
        super().__init__()
        self.level = 2
        self.pos = self.setPos()
        self.pic = STUDENTS[random.randint(0, 3)]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos

            
class Monster(Object):
    def __init__(self):
        super().__init__()
        self.level = 2
        self.pos = self.setPos()
        self.pic = MONSTERS[random.randint(0, 4)]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos

with MPHANDS: 
    while True:
        main = Main()
        main.main()