# Open Day Shooting Game - 50th Aniverary Special Edition

## Purpose
The "Open Day Shooting Game" is a Python-based interactive game designed for the Ho Fung College Open Day event, celebrating the 50th anniversary of the college. The game aims to provide entertainment and engage participants through an enjoyable shooting experience.

## Improvement
This year, the "Open Day Shooting Game" has undergone several enhancements compared to last year's version. Key improvements include:
 - New Game Levels: Introduction of two distinct levels, each with unique objectives and challenges. Level 1 focuses on scoring exactly 50 points, while Level 2 involves shooting balloons and avoiding students.
 - Dynamic Target System: The game now includes a variety of targets such as balloons, students, and monsters, making gameplay more engaging and challenging.
 - Enhanced Visuals: Improved graphics and animations, including better scaling of images and more diverse backgrounds.
 - Improved Hand Tracking: Utilization of the Mediapipe library for more accurate hand detection and tracking, enhancing player interaction.
 - User Interface Enhancements: A more intuitive user interface with clear instructions and feedback for players, including score displays and countdown timers.

## Progress
The game is currently in a functional state and offers the following features:
 - Two Game Levels: Complete different challenges in Level 1 and Level 2.
 - Dynamic Gameplay: Shoot various targets while avoiding specific ones to maximize your score.
 - Leaderboard: Track your performance with a top 5 leaderboard for each level.
 - Hand Detection: Control the shooter using hand movements detected through a webcam.
 - Sound Effects: Engaging sound effects accompany gameplay, enhancing the experience.

## Techniques Used
The program utilizes various techniques and technologies, including:
- Pygame: A Python library for game development, used to create the game window, handle graphics, and user input.
- Mediapipe: A cross-platform framework for building multimodal applied ML pipelines, used for hand detection and tracking.
- OpenCV: An open-source computer vision library, used to capture video frames from the webcam for hand detection.
- Shelve: A Python library for object persistence, used to store and retrieve the top 5 scores leaderboard.

## How to Play
1. Launch the program.
2. Press the SPACEBAR to start the game.
3. Control the character's movement by moving your hand in front of the webcam.
4. Use your hand movements to control the shooter and aim at the targets.
5. Complete the objectives for each level to score points.
6. Try to make it into the top 5 leaderboard!

## Installation
To run the program, follow these steps:
1. Clone the repository on your local machine
2. Open `cmd` in the repository floder
3. Type `py -m pip install -r requirements.txt` (or `pip install -r requirements.txt` if you have Python 3.7 or earlier) to install the required libraries
4. (If required) Run https://aka.ms/vs/17/release/vc_redist.x64.exe to imstall the Microsoft Visual C++ Redistributable
5. Run `openDay2024.py` to run current script in terminal

## Details

The `openDay2024.py` program consists of several classes and functions that work together to create the Open Day Shooting Game - 50th Aniverary Special Edition. Let's explore the code and its functionality in more detail:

```python
import pygame as pg
import random
import mediapipe as mp
import cv2
import shelve
import time
```
- **Imports Libraries**: 
  - `pygame`: For game development.
  - `random`: For random number generation.
  - `mediapipe`: For hand tracking.
  - `cv2`: For video capture and image processing.
  - `shelve`: For persistent storage of scores.
  - `time`: For managing timing functions.

```python
AMENDMENT = 0
CONFIDENCE = 0.5
SCORE = 0
LIMIT = 30
```
- **Constants**: 
  - `AMENDMENT`: Used for positioning adjustments.
  - `CONFIDENCE`: Minimum confidence for hand detection in MediaPipe.
  - `SCORE`: Initial score set to zero.
  - `LIMIT`: Time limit for Level 2.

```python
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FONTTYPE = "comicsans"
SIZE = 30
FILE = "src/file"
```
- **Color and Font Settings**:
  - Defines colors using RGB tuples.
  - Sets font type and size for rendering text.
  - Specifies the file path for storing scores.

```python
pg.init()
```
- **Initialize Pygame**: Sets up the Pygame library for use.

```python
FONT = pg.font.SysFont(FONTTYPE, SIZE)
W, H = int(pg.display.Info().current_w*0.9), int(pg.display.Info().current_h*0.9)
```
- **Font and Screen Size**:
  - Creates a font object for rendering text.
  - Sets the width and height of the game window to 90% of the current screen size.

```python
SHOOTER = pg.transform.scale(pg.image.load("assets/shooter.png"), (W//5, W//5))
```
- **Load and Scale Shooter Image**: Loads the shooter image and scales it to one-fifth of the window width.

```python
BGS = [pg.transform.scale(pg.image.load("assets/BGS/%d.png"%i), (W+30, H+100)) for i in range(4)]
```
- **Background Images**: Loads and scales multiple background images for use in the game.

```python
BALLONS = [pg.transform.scale(pg.image.load("assets/BALLONS/%d.png"%i), (W//10, W//10*pg.image.load("assets/BALLONS/%d.png"%i).get_height()//pg.image.load("assets/BALLONS/%d.png"%i).get_width())) for i in range(10)]
```
- **Balloon Images**: Loads and scales balloon images for Level 1.

```python
STUDENTS = [pg.transform.scale(pg.image.load("assets/STUDENTS/%d.png"%i), (W//10, W//10*pg.image.load("assets/STUDENTS/%d.png"%i).get_height()//pg.image.load("assets/STUDENTS/%d.png"%i).get_width())) for i in range(4)]
```
- **Student Images**: Loads and scales student images for Level 2.

```python
MONSTERS = [pg.transform.scale(pg.image.load("assets/MONSTERS/%d.png"%i), (W//10, W//10*pg.image.load("assets/MONSTERS/%d.png"%i).get_height()//pg.image.load("assets/MONSTERS/%d.png"%i).get_width())) for i in range(5)]
```
- **Monster Images**: Loads and scales monster images for Level 2.

```python
LOADS = [pg.transform.scale(pg.image.load("assets/LOADS/%d.png"%i), (W//2, W//2)) for i in range(16)]
```
- **Load Images**: Loads images representing loading screens or effects.

```python
GIFS = [pg.transform.scale(pg.image.load("assets/GIFS/%d.png"%i), (W//10, W//10*pg.image.load("assets/GIFS/%d.png"%i).get_height()//pg.image.load("assets/GIFS/%d.png"%i).get_width())) for i in range(4)]
```
- **GIF Images**: Loads GIF images for animation or effects.

```python
COUNTS = [pg.transform.scale(pg.image.load("assets/COUNTS/monophy_1-%d.png"%i), (W//2, W//2)) for i in range(49)]
```
- **Countdown Images**: Loads images for displaying countdowns.

```python
EXPLODE = pg.transform.scale(pg.image.load("assets/EXPLODE.png"), (W//5, W//5))
```
- **Explosion Image**: Loads an explosion image used when a target is hit.

```python
CRACK = pg.mixer.Sound(file="assets/sound.wav")
BEEP = pg.mixer.Sound(file="assets/BEEP.wav")
BEEPH = pg.mixer.Sound(file="assets/BEEPH.wav")
```
- **Sound Effects**: Loads sound effects for different game events.

```python
MPHANDS = mp.solutions.hands.Hands(
        model_complexity=0,
        min_detection_confidence=CONFIDENCE,
        min_tracking_confidence=CONFIDENCE)
```
- **Hand Tracking Setup**: Initializes MediaPipe's hand tracking solution with specified confidence levels.

```python
CAP = cv2.VideoCapture(0)
```
- **Video Capture**: Initializes the webcam for capturing video input.

```python
CAPTION = "HFC Info Day Shooting Game - 50th Anniversary Special Edition"
RANK = ["1st", "2nd", "3rd", "4th", "5th"]
```
- **Game Title and Ranking**: Sets the caption for the game window and defines the rank labels.

```python
INTRO = [["Level 1: Score EXACTLY 50 points as soon as possible.",
            "Press <SPACE> to start", 
            "Top 5 completing time: "], 
        ["Level 2: For whatever reason, there are some MONSTERS invaded HFC.",
                "Shoot them and DON'T SHOOT the STUDENTS.", 
                "Press <SPACE> to start", 
                "Top 5 Scores: "]]
```
- **Introduction Text**: Contains instructions for each level.

```python
screen = pg.display.set_mode((W,H))
pg.display.set_caption(CAPTION)
```
- **Display Setup**: Creates the game window and sets its title.

### Main Class

```python
class Main:
    def __init__(self):
        self.screen = screen
```
- **Main Class Initialization**: Initializes the main game class and references the game screen.

```python
def main(self):
    self.game = Game().level1()
    if self.game:self.game = Game().level2()
```
- **Main Game Loop**: Starts Level 1 and proceeds to Level 2 if Level 1 is completed.

```python
def printText(self, text, color = BLACK, add = 0):
    for line in text:
        printLine = FONT.render(line, True, color)
        self.screen.blit(printLine, (W // 2 - printLine.get_width()//2, H // 3 +(text.index(line)+1)*30+add))
    pg.display.update()
```
- **Text Rendering**: Renders and displays text on the screen.

```python
def space(self):
    event = pg.event.wait()
    if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: return
    else: self.space()
```
- **Space Key Wait**: Waits for the player to press the spacebar.

```python
def count(self):
    for cnt in range(len(COUNTS)):
        self.screen.blit(BGS[3], (0,0))
        self.screen.blit(COUNTS[cnt], (W//2-COUNTS[cnt%len(COUNTS)].get_width()//2, H//2-COUNTS[cnt%len(COUNTS)].get_height()//2))
        if cnt%len(COUNTS)//5 == 0 or cnt == len(COUNTS): BEEP.play()
        time.sleep(5/len(COUNTS))
        pg.display.update()
```
- **Countdown Display**: Displays a countdown using images and plays a beep sound.

### Game Class

```python
class Game(Main):
    def __init__(self):
        super().__init__()
        try: 
            self.prev = self.prev
            self.level = self.level
        except: 
            self.prev = 0
            self.level = 1
```
- **Game Class Initialization**: Inherits from Main and initializes level and previous position.

```python
def level1(self):
    with shelve.open(FILE) as d: self.tScores = d['tScore1']
    self.screen.blit(BGS[0], (0,0))
    self.printText(INTRO[0])
```
- **Level 1 Setup**: Loads the top scores and displays the introduction for Level 1.

```python
for i in range(5):
    self.screen.blit(FONT.render(RANK[i], True, BLACK), (W//2-200, H//3+120+30*i))
    self.screen.blit(FONT.render(self.tScores[i][0].strip(), True, BLACK), (W//2-100, H//3+120+30*i))
    self.screen.blit(FONT.render("Time: %ds"%self.tScores[i][1], True, BLACK), (W//2+100, H//3+120+30*i)) 
```
- **Display Top Scores**: Renders the top 5 scores on the screen.

```python
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
```
- **Start the Game**: Waits for user input, starts the countdown, initializes player and targets, and begins gameplay.

### Game Logic

```python
def run(self, level):
    self.screen.fill(WHITE)
    self.screen.blit(BGS[3], (0,0))
```
- **Game Loop**: Fills the screen with white and redraws the background.

```python
if random.randint(0, 50) == 1 or self.targets == []:
    self.targets.append(Ballon() if level == 1 else Monster())
```
- **Target Management**: Randomly spawns a new balloon or monster.

```python
if level == 1:
    for target in self.targets: 
        target.update((target.pos[0], target.pos[1]-random.randint(2, 5)))
        if target.pos[1]<-H//4:
            self.targets.remove(target)
            self.targets.append(Ballon())
```
- **Level 1 Target Movement**: Moves balloons down the screen and respawns them if they go off-screen.

```python
results = MPHANDS.process(cv2.cvtColor(CAP.read()[1], cv2.COLOR_BGR2RGB))
if results.multi_hand_landmarks:
    for hand_landmarks in results.multi_hand_landmarks:
        self.player.update([W-(hand_landmarks.landmark[7].x * W), hand_landmarks.landmark[7].y * H+AMENDMENT])
```
- **Hand Tracking**: Processes the video feed to track hand movements and update the shooter's position.

```python
for target in self.targets:
    if target.collide(self.player.pos):
        self.screen.blit(EXPLODE, (target.pos[0]-100, self.player.pos[1]-100))
        CRACK.play()
```
- **Collision Detection**: Checks if the shooter collides with any targets and plays an explosion effect.

### Win/Lose Conditions

```python
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
```
- **Winning Logic**: Displays a congratulatory message and prompts for a name if the player achieves a top score.

```python
with shelve.open(FILE) as d:
    self.tScores.sort(reverse=level-1, key=lambda x: x[1])
    self.tScores.pop()
    d['tScore%d'%level] = self.tScores
```
- **Score Saving**: Updates the shelve database with the new top scores.

### Object Classes

```python
class Object (Game):
    def __init__(self):
        super().__init__()
```
- **Base Object Class**: Inherits from Game and serves as a base for all game objects.

```python
def update(self, fPos):
    self.pos = fPos
    self.rect.center = fPos
    self.screen.blit(self.pic, self.rect)
```
- **Update Position**: Updates the object's position and redraws it on the screen.

```python
def collide(self, pos):
    return self.rect.collidepoint(pos)
```
- **Collision Detection**: Checks if a point collides with the object.

### Shooter and Target Classes

```python
class Shooter(Object):
    def __init__(self):
        self.pic = SHOOTER
        self.pos = [W//2, H//2]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
        super().__init__()
```
- **Shooter Class**: Represents the player character, initialized at the center of the screen.

```python
class Ballon(Object):
    def __init__(self):
        super().__init__()
        self.pos = self.setPos()
        self.num = random.randint(0, 9) if random.randint(0, 9)%2 == 0 else random.randint(1, 3)
        self.pic = BALLONS[self.num]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
```
- **Balloon Class**: Represents balloons in the game with random point values.

```python
class Student(Object):
    def __init__(self):
        super().__init__()
        self.level = 2
        self.pos = self.setPos()
        self.pic = STUDENTS[random.randint(0, 3)]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
```
- **Student Class**: Represents students in Level 2.

```python
class Monster(Object):
    def __init__(self):
        super().__init__()
        self.level = 2
        self.pos = self.setPos()
        self.pic = MONSTERS[random.randint(0, 4)]
        self.rect = self.pic.get_rect()
        self.rect.center = self.pos
```
- **Monster Class**: Represents monsters in Level 2.

```python
with MPHANDS: 
    while True:
        main = Main()
        main.main()
```
- **Game Loop**: Initializes the main game loop and starts the game.

## Reset
The `reset.py` file is a Python script that is used to reset the high score in the game. It utilizes the `shelve` module to store and retrieve data from a persistent dictionary-like object.

## Acknowledgements
This program was developed by Li Tsz Kiu (Kiu-Q) as part of the Ho Fung College Open Day event. Special thanks to the contributors and libraries used in this project.

Background image from <a fref="https://hofung.edu.hk">Ho Fung College</a>

Image by <a href="https://www.freepik.com/free-vector/flat-christmas-background_31962849.htm#from_view=detail_collection#position=23">Freepik</a> and <a href="https://www.irasutoya.com">いらすとや</a>

Sound Effect from <a href="https://pixabay.com/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=83946">Pixabay</a>

## License
This project is licensed under the MIT License. See the `LICENSE.md` file for more details.