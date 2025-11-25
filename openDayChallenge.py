import pygame as pg
import random
import mediapipe as mp
import cv2
import shelve
import time
import math

AMENDMENT = 0
CONFIDENCE = 0.5
SPEED = 15
CLEVER = 10

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0 ,0)
BLUE = (0, 0, 255)
FONTTYPE = "comicsans"
SIZE = 30
FILE = "src/file"
T_SCORE_KEY = 'tScore4'

pg.init()

FONT = pg.font.SysFont(FONTTYPE, SIZE)
W, H = int(pg.display.Info().current_w*0.9), int(pg.display.Info().current_h*0.9)

SHOOTER = pg.transform.scale(pg.image.load("assets/shooter.png"), (W//5, W//5))
COMPUTER = pg.transform.scale(pg.image.load("assets/shooter.png"), (W//5, W//5)) 

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

mpHands = mp.solutions.hands.Hands(
        model_complexity=0,
        min_detection_confidence=CONFIDENCE,
        min_tracking_confidence=CONFIDENCE)
CAP = cv2.VideoCapture(0)

CAPTION = "HFC Info Day Shooting Game - Challenge Level"
RANK = ["1st", "2nd", "3rd", "4th", "5th"]
INTRO = [["Challenge Level: SURVIVAL MODE vs COMPUTER.",
                "Monsters come from ALL directions!",
                "Beat the computer score. Don't shoot students!",
                "Press <SPACE> to start",
                "Top 5 Scores: "]]

screen = pg.display.set_mode((W,H))
pg.display.set_caption(CAPTION)

class Main:
    def __init__(self):
        self.screen = screen
    def main(self):
        Game().challengeLevel()
    def printText(self, text, color = BLACK, add = 0):
        for line in text:
            printLine = FONT.render(line, True, color)
            self.screen.blit(printLine, (W // 2 - printLine.get_width()//2, H // 3 +(text.index(line)+1)*30+add))
        pg.display.update()
    def space(self):
        try:
            event = pg.event.wait()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: return
            else: self.space()
        except RecursionError:
            self.space()
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
            self.compClev = 0.0
        except: 
            self.compClev = 0.0
    
    def challengeLevel(self):
        with shelve.open(FILE) as d: self.tScores = d.get(T_SCORE_KEY, [["CPU", 100], ["User1", 50], ["User2", 30], ["User3", 20], ["User4", 10]])
        self.screen.blit(BGS[0], (0,0))
        self.printText(INTRO[0])
        for i in range(5):
            screen.blit(FONT.render(RANK[i], True, BLACK), (W//2-200, H//3+180+30*i))
            screen.blit(FONT.render(self.tScores[i][0].strip(), True, BLACK), (W//2-100, H//3+180+30*i))
            screen.blit(FONT.render("Score: %d"%self.tScores[i][1], True, BLACK), (W//2+100, H//3+180+30*i))
        pg.display.update()
        self.space()
        self.count()
        BEEPH.play()
        
        self.start = pg.time.get_ticks()
        self.score = 0
        self.compScore = 0
        self.level = 3
        
        self.player = Shooter()
        self.computer = Computer(gameInst=self) 
        
        self.targets = [Monster(level=3)]
        
        self.result = self.run()
        if self.result: return self.win()
        else: return self.lose()
        
    def run(self):
        self.screen.fill(WHITE)
        self.screen.blit(BGS[3], (0,0))
        
        spawnThresh = 15 
        if random.randint(0, spawnThresh) == 1 or self.targets == []:
            if random.randint(0, 10) > 2:
                self.targets.append(Monster(level=3))
            else:
                self.targets.append(Student(level=3))

        for target in self.targets:
            newX = target.pos[0] + target.vel[0]
            newY = target.pos[1] + target.vel[1]
            target.update((newX, newY))
            
            if (newX < -W//2 or newX > W + W//2 or 
                newY < -H//2 or newY > H + H//2):
                if target in self.targets:
                    self.targets.remove(target)

        self.timeUsed = (pg.time.get_ticks() - self.start) // 1000
        self.screen.blit(FONT.render(f"Time Elapsed: {self.timeUsed}s", True, BLACK), (10, 10))
        self.screen.blit(FONT.render(f"P: {self.score} vs CPU: {self.compScore}", True, BLUE), (10, 40))
        self.screen.blit(FONT.render(f"CPU Cleverness: {self.compClev:.2f}", True, RED), (10, 70))


        plrPos = None 
        results = mpHands.process(cv2.cvtColor(CAP.read()[1], cv2.COLOR_BGR2RGB))
        if results.multi_hand_landmarks:
            for handLMs in results.multi_hand_landmarks:
                plrPos = [W-(handLMs.landmark[7].x * W), handLMs.landmark[7].y * H+AMENDMENT]
                self.player.update(plrPos)

        timeElapsed = (pg.time.get_ticks() - self.start) / 1000
        if plrPos:
            self.computer.updateAi(self.targets, timeElapsed, plrPos)
        else:
            self.computer.updateAi(self.targets, timeElapsed, self.player.pos)
        
        for target in self.targets:
            if target.collide(self.computer.pos):
                self.screen.blit(EXPLODE, (target.pos[0]-100, target.pos[1]-100))
                CRACK.play()
                if isinstance(target, Monster):
                    self.compScore += 1
                    if target in self.targets: self.targets.remove(target)
                elif isinstance(target, Student):
                    return True 
                
        if results.multi_hand_landmarks: 
            for target in self.targets:
                if target.collide(self.player.pos):
                    self.screen.blit(EXPLODE, (target.pos[0]-100, target.pos[1]-100))
                    CRACK.play()
                    
                    if isinstance(target, Monster):
                        self.score += 1
                        if target in self.targets: self.targets.remove(target)
                    elif isinstance(target, Student): 
                        return False 

        time.sleep(0.02)
        pg.display.update()
        return self.run()

    def win(self):
        self.screen.blit(BGS[0], (0,0))
        
        plrFinalScore = self.score
        with shelve.open(FILE) as d: self.tScores = d.get(T_SCORE_KEY, [["CPU", 100], ["User1", 50], ["User2", 30], ["User3", 20], ["User4", 10]])
        
        if self.compScore > plrFinalScore:
            MSG = [["GAME OVER",
                   f"Player Score: {plrFinalScore} | Computer Score: {self.compScore}",
                   "The computer won by hitting a student! YOU WIN!",
                   "Press <SPACE> to restart"]]
            self.printText(MSG[0], BLACK, 60)
            self.space()
            return True

        if plrFinalScore > self.tScores[4][1]:
            self.tScores.append(["", plrFinalScore])
            
            while True:
                HIGH = [f"GAME OVER: Player Score: {plrFinalScore} | CPU Score: {self.compScore}", 
                    "Congratulations, your score gets into Top 5 Scores!", 
                    "Please enter your name (At most 10 charachters) to have a cool record",
                    f"Name: {self.tScores[5][0]} |"]
                event = pg.event.wait()
                self.screen.blit(BGS[0], (0,0))
                self.printText(HIGH, BLACK, 60)
                
                if event.type == pg.KEYDOWN and event.key == pg.K_RETURN:
                    break
                elif event.type == pg.KEYDOWN and event.key == pg.K_BACKSPACE:
                    self.tScores[5][0] = self.tScores[5][0][:-1]
                elif event.type == pg.KEYDOWN and len(self.tScores[5][0]) < 10:
                    self.tScores[5][0] += event.unicode
            
            with shelve.open(FILE) as d:
                self.tScores.sort(reverse=True, key=lambda x: x[1]) 
                self.tScores.pop()
                d[T_SCORE_KEY] = self.tScores
        else:
            MSG = [["GAME OVER",
                   f"Player Score: {plrFinalScore} | Computer Score: {self.compScore}",
                   "You outscored the CPU! YOU WIN!",
                   "Press <SPACE> to restart"]]
            self.printText(MSG[0], BLACK, 60)
            self.space()
            
        return True
            
    def lose(self):
        self.screen.blit(BGS[0], (0,0))
        LOSE = [["You shoot the student! You Lose.",
                       "Press <SPACE> to restart"]]
        self.printText(LOSE[0], RED, 60)
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
    def setPos(self, level=3):
        side = random.choice(['top', 'bottom', 'left', 'right'])
        if side == 'top':
            return [random.randint(0, W), -50]
        elif side == 'bottom':
            return [random.randint(0, W), H + 50]
        elif side == 'left':
            return [-50, random.randint(0, H)]
        elif side == 'right':
            return [W + 50, random.randint(0, H)]
        return [W//2, H//2]

class Shooter(Object):
    def __init__(self):
        self.pic = SHOOTER
        self.pos = [W//2, H//2]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
        super().__init__()

class Computer(Object):
    def __init__(self, gameInst):
        self.game = gameInst 
        self.pic = COMPUTER
        self.pos = [W//2, H//2]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
        self.spd = 10 
        super().__init__()
    def updateAi(self, targets, timeElap, plrPos):
        x = timeElap
        currentClev = 0.2 + 1.8 * (x**2 / (x**2 + CLEVER**2))

        self.game.compClev = currentClev

        self.spd = 15 * currentClev + 5

        moveX, moveY = 0, 0

        targetMns = None
        minD = float('inf')
        stds = []
        
        for t in targets:
            if isinstance(t, Monster):
                dSq = (t.pos[0] - self.pos[0])**2 + (t.pos[1] - self.pos[1])**2
                if dSq < minD:
                    minD = dSq
                    targetMns = t
            elif isinstance(t, Student):
                stds.append(t)
        
        if targetMns:
            dx = targetMns.pos[0] - self.pos[0]
            dy = targetMns.pos[1] - self.pos[1]
            dist = (dx**2 + dy**2)**0.5
            
            if dist != 0:
                moveX += (dx / dist) * 1.0
                moveY += (dy / dist) * 1.0
        
        AVOID_RAD = 250  
        REPUL_WT = 4.0 

        for std in stds:
            dx = self.pos[0] - std.pos[0]
            dy = self.pos[1] - std.pos[1]
            dist = (dx**2 + dy**2)**0.5

            if dist < AVOID_RAD and dist != 0:
                force = (1 - (dist / AVOID_RAD)) * REPUL_WT
                moveX += (dx / dist) * force
                moveY += (dy / dist) * force

        PLR_AVOID_RAD = 200 
        PLR_REPUL_WT = 15.0 

        dx = self.pos[0] - plrPos[0]
        dy = self.pos[1] - plrPos[1]
        dist = (dx**2 + dy**2)**0.5

        if dist < PLR_AVOID_RAD and dist != 0:
            force = (1 - (dist / PLR_AVOID_RAD)) * PLR_REPUL_WT
            moveX += (dx / dist) * force
            moveY += (dy / dist) * force

        finalMag = (moveX**2 + moveY**2)**0.5
            
        if finalMag != 0:
            normX = moveX / finalMag
            normY = moveY / finalMag

            errorMarg = (1 - currentClev) * 20
            
            stepX = normX * self.spd + random.uniform(-errorMarg, errorMarg)
            stepY = normY * self.spd + random.uniform(-errorMarg, errorMarg)
            
            self.pos[0] += stepX
            self.pos[1] += stepY
        
        self.pos[0] = max(0, min(W, self.pos[0]))
        self.pos[1] = max(0, min(H, self.pos[1]))

        self.rect.center = self.pos
        self.screen.blit(self.pic, self.rect)
        lbl = FONT.render("CPU", True, RED)
        self.screen.blit(lbl, (self.pos[0], self.pos[1]-40))
                        
class Ballon(Object):
    def __init__(self):
        super().__init__()
        self.level = 1
        self.pos = self.setPos(3)
        self.num = random.randint(0, 9) if random.randint(0, 9)%2 == 0 else random.randint(1, 3)
        self.pic = BALLONS[self.num]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
        
class Student(Object):
    def __init__(self, level=3):
        super().__init__()
        self.level = level
        self.pos = self.setPos(level)
        self.pic = STUDENTS[random.randint(0, 3)]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
        
        centerX, centerY = W//2, H//2
        angle = math.atan2(centerY - self.pos[1], centerX - self.pos[0])
        angle += random.uniform(-0.5, 0.5)
        spd = random.randint(SPEED, SPEED + 5)
        self.vel = (math.cos(angle) * spd, math.sin(angle) * spd)
            
class Monster(Object):
    def __init__(self, level=3):
        super().__init__()
        self.level = level
        self.pos = self.setPos(level)
        self.pic = MONSTERS[random.randint(0, 4)]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos

        centerX, centerY = W//2, H//2
        angle = math.atan2(centerY - self.pos[1], centerX - self.pos[0])
        angle += random.uniform(-0.5, 0.5)
        spd = random.randint(SPEED, SPEED + 5)
        self.vel = (math.cos(angle) * spd, math.sin(angle) * spd)

with mpHands: 
    while True:
        try:
            main = Main()
            main.main()
        except RecursionError: continue