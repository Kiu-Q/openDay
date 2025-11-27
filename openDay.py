import pygame as pg
import random
import mediapipe as mp
import cv2
import shelve
import time
import math

AMENDMENT = 0
CONFIDENCE = 0.2
SPEED = 5
CLEVER = 2
LIMIT = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0 ,0)
BLUE = (0, 0, 255)

FONTTYPE = "comicsans"
SIZE = 30
FILE = "src/file"
TSCORE = 'tScore'

pg.init()
FONT = pg.font.SysFont(FONTTYPE, SIZE)

W, H = int(pg.display.Info().current_w*0.9), int(pg.display.Info().current_h*0.9)

SHOOTER = pg.transform.scale(pg.image.load("assets/shooter.png"), (W//5, W//5))
COMPUTER = pg.transform.scale(pg.image.load("assets/shooter.png"), (W//20, W//20))
BGS = [pg.transform.scale(pg.image.load("assets/BGS/%d.png"%i), (W+30, H+100)) for i in range(4)]
STUDENTS = [pg.transform.scale(pg.image.load("assets/STUDENTS/%d.png"%i), (W//12, W//12*pg.image.load("assets/STUDENTS/%d.png"%i).get_height()//pg.image.load("assets/STUDENTS/%d.png"%i).get_width())) for i in range(4)]
MONSTERS = [pg.transform.scale(pg.image.load("assets/MONSTERS/%d.png"%i), (W//10, W//10*pg.image.load("assets/MONSTERS/%d.png"%i).get_height()//pg.image.load("assets/MONSTERS/%d.png"%i).get_width())) for i in range(5)]
THUNDER = pg.transform.scale(pg.image.load("assets/THUNDER.png"), (W//8, W//8*pg.image.load("assets/THUNDER.png").get_height()//pg.image.load("assets/THUNDER.png").get_width()))
COUNTS = [pg.transform.scale(pg.image.load("assets/COUNTS/monophy_1-%d.png"%i), (W//2, W//2)) for i in range(49)]
EXPLODE = pg.transform.scale(pg.image.load("assets/EXPLODE.png"), (W//5, W//5))
NO = pg.transform.scale(pg.image.load("assets/NO.png"), (W//10, W//10))
THN = pg.transform.scale(pg.image.load("assets/THN.png"), (W//10, W//10))

BEEP = pg.mixer.Sound(file="assets/BEE.wav")
BEEPH = pg.mixer.Sound(file="assets/BEEP.wav")
CRACK = pg.mixer.Sound(file="assets/sound.wav")
THU = pg.mixer.Sound(file="assets/thunder.wav")

mpHands = mp.solutions.hands.Hands(
    model_complexity=1,
    min_detection_confidence=CONFIDENCE,
    min_tracking_confidence=CONFIDENCE+0.5)

CAP = cv2.VideoCapture(0)
CAPTION = "HFC Info Day - Thunder Challenge"
RANK = ["1st", "2nd", "3rd", "4th", "5th"]

INTRO = [["Thunder Challenge: 30 SECOND SURVIVAL vs COMPUTER.",
         "Monsters come from ALL directions!",
         "Beat the CPU score within 30 seconds to WIN!",
         "Collect THUNDER power-up to weaken CPU!",
         "Press SPACE to start",
         "Top 5 Scores: "]]

screen = pg.display.set_mode((W,H))
pg.display.set_caption(CAPTION)

class Main:
    def __init__(self):
        self.screen = screen

    def main(self):
        Game().thunderChallenge()

    def printText(self, text, color = BLACK, add = 0):
        for line in text:
            printLine = FONT.render(line, True, color)
            self.screen.blit(printLine, (W // 2 - printLine.get_width()//2, H // 3 +(text.index(line)+1)*30+add))
        pg.display.update()

    def space(self):
        try:
            event = pg.event.wait()
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: 
                return
            else: 
                self.space()
        except RecursionError:
            self.space()

    def count(self):
        total_frames = len(COUNTS)
        play_times = 4
        interval = max(1, total_frames // play_times)
        for cnt in range(total_frames):
            self.screen.blit(BGS[3], (0,0))
            frame = COUNTS[cnt]
            self.screen.blit(frame, (W//2-frame.get_width()//2, H//2-frame.get_height()//2))
            if (cnt % interval == 0) or (cnt == total_frames - 1): BEEP.play()
            time.sleep(1/total_frames)
            pg.display.update()

class Game(Main):
    def __init__(self):
        super().__init__()
        self.compClev = 0.0
        self.cleverness_multiplier = 1.0
        self.win_reason = None

    def thunderChallenge(self):
        with shelve.open(FILE) as d: 
            self.tScores = d[TSCORE]
        
        self.screen.blit(BGS[0], (0,0))
        self.printText(INTRO[0])
        
        for i in range(5):
            screen.blit(FONT.render(RANK[i], True, BLACK), (W//2-200, H//3+210+30*i))
            screen.blit(FONT.render(self.tScores[i][0].strip(), True, BLACK), (W//2-100, H//3+210+30*i))
            screen.blit(FONT.render("Score: %d"%self.tScores[i][1], True, BLACK), (W//2+100, H//3+210+30*i))
        
        pg.display.update()
        self.space()
        self.count()
        BEEPH.play()

        self.start = pg.time.get_ticks()
        self.score = 0
        self.compScore = 0
        self.level = 3
        self.cleverness_multiplier = 1.0
        self.player = Shooter()
        self.computer = Computer(gameInst=self)
        self.targets = [Monster(level=3)]
        self.result = self.run()

        if self.result:
            return self.win()
        else:
            return self.lose()

    def run(self):
        self.screen.fill(WHITE)
        self.screen.blit(BGS[3], (0,0))

        # Calculate time elapsed
        timeElapsed = (pg.time.get_ticks() - self.start) / 1000
        timeRemaining = LIMIT - int(timeElapsed)
        
        # Dynamic spawn threshold that decreases over time (increases frequency)
        # Starts at 10, decreases to 3 as time progresses
        baseSpawnThresh = max(3, int(10 - (timeElapsed / LIMIT) * 7))
        spawnThresh = baseSpawnThresh

        # Spawn monsters and students with increasing frequency
        if random.randint(0, spawnThresh) == 1 or self.targets == []:
            if random.randint(0, 30) > 1:
                self.targets.append(Monster(level=3))
            else:
                self.targets.append(Student(level=3))

        # Thunder spawn logic - appears at 5+ score
        if self.score >= 5:
            hasThunder = any(isinstance(t, Thunder) for t in self.targets)
            if not hasThunder and random.randint(0, 100) < 3:  # 3% chance
                self.targets.append(Thunder(level=3))

        # Update target positions
        for target in self.targets:
            newX = target.pos[0] + target.vel[0]
            newY = target.pos[1] + target.vel[1]
            target.update((newX, newY))
            
            # Remove off-screen targets
            if (newX < -W//2 or newX > W + W//2 or 
                newY < -H//2 or newY > H + H//2):
                if target in self.targets:
                    self.targets.remove(target)

        # Display game info
        time_color = RED if timeRemaining <= 5 else (RED if timeRemaining <= 10 else BLACK)
        self.screen.blit(FONT.render(f"Time: {timeRemaining}s", True, time_color), (10, 10))
        self.screen.blit(FONT.render(f"P: {self.score} vs CPU: {self.compScore}", True, BLACK), (10, 40))
        self.screen.blit(FONT.render(f"CPU Cleverness: {self.compClev:.2f}", True, BLUE), (10, 70))

        # Check if time is up
        if timeRemaining <= 0:
            return self.checkWinner()

        # Get player position from hand tracking
        plrPos = None
        results = mpHands.process(cv2.cvtColor(CAP.read()[1], cv2.COLOR_BGR2RGB))
        
        if results.multi_hand_landmarks:
            plrPos = [0, 0]
            for handLMs in results.multi_hand_landmarks:
                if plrPos == [0, 0] or handLMs.landmark[7].y * H < plrPos[1]:
                    plrPos = [W-(handLMs.landmark[7].x * W), handLMs.landmark[7].y * H+AMENDMENT]
            self.player.update(plrPos)

        # Update computer AI
        if plrPos: self.computer.updateAi(self.targets, timeElapsed, plrPos)
        else: self.computer.updateAi(self.targets, timeElapsed, self.player.pos)

        # Check computer collisions
        for target in self.targets[:]:
            if isinstance(target, Thunder): 
                continue  # CPU cannot detect Thunder
                
            if target.collide(self.computer.pos):
                self.screen.blit(EXPLODE, (target.pos[0]-100, target.pos[1]-100))
                CRACK.play()
                
                if isinstance(target, Monster):
                    self.compScore += 1
                    if target in self.targets:
                        self.targets.remove(target)
                elif isinstance(target, Student):
                    self.screen.blit(NO, (target.pos[0], target.pos[1]))
                    pg.display.update()
                    time.sleep(1)
                    self.win_reason = "cpu_hit_student"
                    return True

        # Check player collisions
        if results.multi_hand_landmarks:
            for target in self.targets[:]:
                if target.collide(self.player.pos):
                    CRACK.play()
                    
                    if isinstance(target, Thunder):
                        self.screen.blit(EXPLODE, (target.pos[0]-100, target.pos[1]-100))
                        THU.play()
                        # Permanent cleverness reduction
                        self.cleverness_multiplier /= 1.1
                        self.cleverness_multiplier = max(0.05, self.cleverness_multiplier)
                        
                        # Kill all monsters on screen
                        monstersToRemove = [t for t in self.targets if isinstance(t, Monster)]
                        self.screen.blit(THN, (W//3, 0))
                        self.screen.blit(THN, (W-W//3, 0))
                        for monster in monstersToRemove:
                            self.score += 1
                            if monster in self.targets:
                                self.screen.blit(EXPLODE, (monster.pos[0]-W//20, monster.pos[1]-W//20))
                                self.screen.blit(THN, (monster.pos[0]-50, monster.pos[1]-monster.pic.get_height()))
                                self.targets.remove(monster)
                        
                        # Remove thunder
                        if target in self.targets:
                            self.targets.remove(target)
                            
                    elif isinstance(target, Monster):
                        self.screen.blit(EXPLODE, (target.pos[0]-W//20, target.pos[1]-W//20))
                        self.score += 1
                        if target in self.targets:
                            self.targets.remove(target)
                            
                    elif isinstance(target, Student):
                        self.screen.blit(NO, (plrPos[0]-W//20, plrPos[1]-W//20))
                        pg.display.update()
                        time.sleep(1)
                        self.win_reason = "player_hit_student"
                        return False
        pg.display.update()
        time.sleep(0.01)
        return self.run()

    def checkWinner(self):
        if self.score > self.compScore:
            self.win_reason = "score_higher"
            return True  # Player wins
        else:
            self.win_reason = "score_lower"
            return False  # Player loses

    def win(self):
        self.screen.blit(BGS[0], (0,0))
        plrFinalScore = self.score
        
        # Determine win message based on reason
        if self.win_reason == "cpu_hit_student":
            win_msg = "YOU WIN! CPU hit a student!"
        elif self.win_reason == "score_higher":
            win_msg = "YOU WIN! Your score beats the CPU!"
                    
        with shelve.open(FILE) as d:
            self.tScores = d.get(TSCORE, [["CPU", 50], ["User1", 40], ["User2", 30], ["User3", 20], ["User4", 10]])
            
            # Check if player made it to top 5
            if plrFinalScore > self.tScores[4][1]:
                self.tScores.append(["", plrFinalScore])
                
                while True:
                    HIGH = [f"Player: {plrFinalScore} | CPU: {self.compScore}",
                           win_msg,
                           "Congratulations! You made it to Top 5!",
                           "Enter your name (max 10 characters)",
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
                    d[TSCORE] = self.tScores
            else:
                MSG = [f"Player Score: {plrFinalScore} | Computer Score: {self.compScore}",
                      win_msg,
                      "Press SPACE to restart"]
                self.printText(MSG, BLACK, 60)
                self.space()
        
        return True

    def lose(self):
        self.screen.blit(BGS[0], (0,0))
        plrFinalScore = self.score
        
        # Determine lose message based on reason
        if self.win_reason == "player_hit_student":
            lose_msg = "YOU LOSE! You hit a student!"
        elif self.win_reason == "score_lower":
            lose_msg = "YOU LOSE! CPU score is higher!"
        else:
            lose_msg = "YOU LOSE!"
        
        LOSE = ["GAME OVER",
               f"Player Score: {plrFinalScore} | Computer Score: {self.compScore}",
               lose_msg,
               "Press SPACE to restart"]
        
        self.printText(LOSE, RED, 60)
        self.space()
        return False

class Object(Game):
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
        baseClev = 0.5 + (CLEVER-0.5) * (x**2 / (x**2 + 5**2))
        
        # Apply permanent cleverness multiplier (affected by Thunder)
        currentClev = baseClev * self.game.cleverness_multiplier
        self.game.compClev = currentClev
        self.spd = 15 * currentClev + 5
        
        moveX, moveY = 0, 0
        targetMns = None
        minD = float('inf')
        stds = []
        
        for t in targets:
            if isinstance(t, Thunder):
                stds.append(t)  # CPU cannot detect Thunder
            
            if isinstance(t, Monster):
                dSq = (t.pos[0] - self.pos[0])**2 + (t.pos[1] - self.pos[1])**2
                if dSq < minD:
                    minD = dSq
                    targetMns = t
            elif isinstance(t, Student):
                stds.append(t)
        
        # Move towards nearest monster
        if targetMns:
            dx = targetMns.pos[0] - self.pos[0]
            dy = targetMns.pos[1] - self.pos[1]
            dist = (dx**2 + dy**2)**0.5
            if dist != 0:
                moveX += (dx / dist) * 1.0
                moveY += (dy / dist) * 1.0
        
        # Avoid students
        AVOID_RAD = 250
        REPUL_WT = 6.0
        for std in stds:
            dx = self.pos[0] - std.pos[0]
            dy = self.pos[1] - std.pos[1]
            dist = (dx**2 + dy**2)**0.5
            if dist < AVOID_RAD and dist != 0:
                force = (1 - (dist / AVOID_RAD)) * REPUL_WT
                moveX += (dx / dist) * force
                moveY += (dy / dist) * force
        
        # Avoid player
        PLR_AVOID_RAD = 200
        PLR_REPUL_WT = 4.0
        dx = self.pos[0] - plrPos[0]
        dy = self.pos[1] - plrPos[1]
        dist = (dx**2 + dy**2)**0.5
        if dist < PLR_AVOID_RAD and dist != 0:
            force = (1 - (dist / PLR_AVOID_RAD)) * PLR_REPUL_WT
            moveX += (dx / dist) * force
            moveY += (dy / dist) * force
        
        # Apply movement with error margin
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
        lbl = FONT.render("CPU", True, BLUE)
        self.screen.blit(lbl, (self.pos[0], self.pos[1]-40))

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
        spd = random.randint(SPEED, SPEED + 5) *3
        self.vel = (math.cos(angle) * spd, math.sin(angle) * spd)

class Monster(Object):
    def __init__(self, level=3):
        super().__init__()
        self.level = level
        self.pos = self.setPos(level)
        self.pic = MONSTERS[random.randint(0, 4)]
        randSize = random.randint(W//12, W//8)
        self.pic = pg.transform.scale(self.pic, (randSize, randSize*self.pic.get_height()//self.pic.get_width()))
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
        
        centerX, centerY = W//2, H//2
        angle = math.atan2(centerY - self.pos[1], centerX - self.pos[0])
        angle += random.uniform(-0.5, 0.5)
        spd = random.randint(SPEED, SPEED + 5)
        self.vel = (math.cos(angle) * spd, math.sin(angle) * spd)

class Thunder(Object):
    def __init__(self, level=3):
        super().__init__()
        self.level = level
        self.pos = self.setPos(level)
        self.pic = THUNDER
        spd = random.randint(SPEED * 5, SPEED * 5 + 50)
        self.pic = pg.transform.scale(self.pic, (spd*4, spd*4*self.pic.get_height()//self.pic.get_width()))
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
        
        centerX, centerY = W//2, H//2
        angle = math.atan2(centerY - self.pos[1], centerX - self.pos[0])
        angle += random.uniform(-0.5, 0.5)
        self.vel = (math.cos(angle) * spd, math.sin(angle) * spd)

# Main game loop
with mpHands:
    while True:
        try:
            main = Main()
            main.main()
        except RecursionError:
            continue
