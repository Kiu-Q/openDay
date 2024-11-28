import pygame as pg
import random
import mediapipe as mp
import cv2
import shelve
import time

pg.init()

test = False

AMD = 0
SCORE = 0
LIMIT = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0 ,0)
    
font = pg.font.SysFont("comicsans", 30)

w, h = pg.display.Info().current_w-30, pg.display.Info().current_h-100
screen = pg.display.set_mode((w,h))

file = "src/file"
    
shooter = pg.transform.scale(pg.image.load("assets/shooter.png"), (w//5, w//5))
bgs = [pg.transform.scale(pg.image.load("assets/bg/%d.png"%i), (w+30, h+100)) for i in range(4)]
ballons = [pg.transform.scale(pg.image.load("assets/ballons/%d.png"%i), (w//10, w//10*pg.image.load("assets/ballons/%d.png"%i).get_height()//pg.image.load("assets/ballons/%d.png"%i).get_width())) for i in range(10)]
students = [pg.transform.scale(pg.image.load("assets/students/%d.png"%i), (w//10, w//10*pg.image.load("assets/students/%d.png"%i).get_height()//pg.image.load("assets/students/%d.png"%i).get_width())) for i in range(4)]
monsters = [pg.transform.scale(pg.image.load("assets/monsters/%d.png"%i), (w//10, w//10*pg.image.load("assets/monsters/%d.png"%i).get_height()//pg.image.load("assets/monsters/%d.png"%i).get_width())) for i in range(5)]
loads = [pg.transform.scale(pg.image.load("assets/load/%d.png"%i), (w//2, w//2)) for i in range(16)]
gifs = [pg.transform.scale(pg.image.load("assets/gifs/%d.png"%i), (w//10, w//10*pg.image.load("assets/gifs/%d.png"%i).get_height()//pg.image.load("assets/gifs/%d.png"%i).get_width())) for i in range(4)]
loadings = [pg.transform.scale(pg.image.load("assets/loading/%d.png"%i), (w//5, w//5*pg.image.load("assets/loading/%d.png"%i).get_height()//pg.image.load("assets/loading/%d.png"%i).get_width())) for i in range(4)]
count = [pg.transform.scale(pg.image.load("assets/count/monophy_1-%d.png"%i), (w//2, w//2)) for i in range(49)]
explode = pg.transform.scale(pg.image.load("assets/explode.png"), (w//5, w//5))
carck = pg.mixer.Sound(file="assets/sound.wav")
beep = pg.mixer.Sound(file="assets/beep.wav")
beeph = pg.mixer.Sound(file="assets/beeph.wav")

rank= ["1st", "2nd", "3rd", "4th", "5th"]

pg.display.set_caption("HFC Info Day Shooting Game - 50th Aniversary Special Edition")

mpHands = mp.solutions.hands

targets = []

prev = 0