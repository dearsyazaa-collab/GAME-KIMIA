import sys
try:
    import pygame
    import cv2
    import mediapipe
except ImportError as e:
    print(f"MISSING: {e}")
    sys.exit(0)

pygame.init()
pygame.display.set_mode((100,100), pygame.HIDDEN)

from main import *
from engine.camera_tracker import CameraTracker
from engine.physics import PhysicsEngine
from entities.player import Player
from entities.enemies import Enemy
from entities.items import Item, QuestionBlock
from levels.level_manager import LevelManager
from ui.dashboard import Dashboard
from ui.quiz_system import QuizSystem

print("Instantiating objects...")
ct = CameraTracker(device_index=-1)
pe = PhysicsEngine()
pl = Player(0,0)
en = Enemy(0,0)
it = Item(0,0)
qb = QuestionBlock(0,0)
lm = LevelManager(100, 100)
db = Dashboard()
qs = QuizSystem()

print("ALL GOOD!")
pygame.quit()
