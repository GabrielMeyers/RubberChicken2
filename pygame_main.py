__author__ = 'yournamehere'  # put your name here!!!

import pygame, sys, traceback, random
from pygame.locals import *

GAME_MODE_MAIN = 0
GAME_MODE_TITLE_SCREEN = 1

# import your classFiles here.
from ClownFile import Clown
from ChickenFile import Chicken
from PieFile import Pie
from CarFile import Car
from playsound import playsound
# =====================  setup()
def setup():
    """
    This happens once in the program, at the very beginning.
    """
    global canvas, objects_on_screen, objects_to_add, bg_color, game_mode, pie_list, the_chicken, the_clown, score, ammo, car_list, hits, misses
    canvas = pygame.display.set_mode((600, 600))
    objects_on_screen = []  # this is a list of all things that should be drawn on screen.
    objects_to_add = [] #this is a list of things that should be added to the list on screen. Put them here while you
                        #   are in the middle of the loop, and they will be added in later in the loop, when it is safe
                        #   to do so.
    bg_color = pygame.Color(128,128,128)  # you can find a list of color names at https://goo.gl/KR7Pke
    game_mode = GAME_MODE_MAIN
    car_list = []
    # Add any other things you would like to have the program do at startup here.
    reference_car = Car(0,0)
    left_car = Car(-300, 300+reference_car.height/2)
    right_car = Car(300, 300 - reference_car.height / 2)
    car_list.append(left_car)
    car_list.append(right_car)
    objects_on_screen.append(left_car)
    objects_on_screen.append(right_car)
    the_clown = Clown()
    objects_on_screen.append(the_clown)
    pie_list = []
    the_chicken = Chicken()
    objects_on_screen.append(the_chicken)
    pygame.mouse.set_visible(False)

    score = 0
    ammo = 10
    hits = 0
    misses = 0
# =====================  loop()
def loop(delta_T):
    """
     this is what determines what should happen over and over.
     delta_T is the time (in seconds) since the last loop() was called.
    """
    canvas.fill(bg_color) # wipe the screen with the background color.
    if game_mode == GAME_MODE_MAIN:
        animate_objects(delta_T)

        # place any other code to test interactions between objects here. If you want them to
        # disappear, set them so that they respond True to isDead(), and they will be deleted next. If you want to put
        # more objects on screen, add them to the global variable objects_to_add, and they will be added later in this
        # loop.


        clear_dead_objects()
        add_new_objects()
        draw_objects()
        check_pie_clown_collision()
        check_pie_car_collision()
        calc_misses()
        show_stats(delta_T) #optional. Comment this out if it annoys you.
        the_end_game()
    #if game_mode == GAME_MODE_OVER
    pygame.display.flip()  # updates the window to show the latest version of the buffer.




# =====================  animate_objects()
def animate_objects(delta_T):
    """
    tells each object to "step"...
    """
    global objects_on_screen
    for object in objects_on_screen:
        if object.is_dead(): #   ...but don't bother "stepping" the dead ones.
            continue
        object.step(delta_T)


# =====================  clear_dead_objects()
def clear_dead_objects():
    """
    removes all objects that are dead from the "objectsOnScreen" list
    """
    global objects_on_screen
    i = 0
    for object in objects_on_screen[:]:
        if object.is_dead():
            objects_on_screen.pop(i) # removes the ith object and pulls everything else inwards, so don't advance "i"
                                     #      ... they came back to you.
        else:
            i += 1
    i = 0
    for pie in pie_list[:]:
        if pie.is_dead():
            pie_list.pop(i)  # removes the ith object and pulls everything else inwards, so don't advance "i"
            #      ... they came back to you.
        else:
            i += 1

# =====================  add_new_objects()
def add_new_objects():
    """
    Adds all the objects in the list "objects to add" to the list of "objects on screen" and then clears the "to add" list.
    :return: None
    """
    global objects_to_add, objects_on_screen
    objects_on_screen.extend(objects_to_add)
    objects_to_add.clear()

# =====================  draw_objects()
def draw_objects():
    """
    Draws each object in the list of objects.
    """
    for object in objects_on_screen:
        object.draw_self(canvas)

# =====================  show_stats()
def show_stats(delta_T):
    """
    draws the frames-per-second in the lower-left corner and the number of objects on screen in the lower-right corner.
    Note: the number of objects on screen may be a bit misleading. They still count even if they are being drawn off the
    edges of the screen.
    :param delta_T: the time since the last time this loop happened, used to calculate fps.
    :return: None
    """
    white_color = pygame.Color(255,255,255)
    stats_font = pygame.font.SysFont('Arial', 10)

    score_string = f"SCORE: {score}"
    score_text_surface = stats_font.render(score_string, True, white_color)  # this makes a transparent box with text
    score_text_rect = score_text_surface.get_rect()  # gets a copy of the bounds of the transparent box
    score_text_rect.left = 10  # now relocate the box to the left side top
    score_text_rect.top = canvas.get_rect().top + 10
    canvas.blit(score_text_surface, score_text_rect)  # ... and copy it to the buffer at the location of the box



    ammo_string = f"AMMO: {ammo}"
    ammo_text_surface = stats_font.render(ammo_string, True, white_color)  # this makes a transparent box with text
    ammo_text_rect = ammo_text_surface.get_rect()  # gets a copy of the bounds of the transparent box
    ammo_text_rect.right = canvas.get_rect().right - 10  # now relocate the box to the left side top
    ammo_text_rect.top = canvas.get_rect().top + 10
    canvas.blit(ammo_text_surface, ammo_text_rect)  # ... and copy it to the buffer at the location of the box

    fps_string = f"FPS: {(1.0/delta_T):3.1f}" #build a string with the calculation of FPS. (The 3.1f means a number with 1 decimal place after the decimal.)
    fps_text_surface = stats_font.render(fps_string,True,white_color) #this makes a transparent box with text
    fps_text_rect = fps_text_surface.get_rect()   # gets a copy of the bounds of the transparent box
    fps_text_rect.left = 10  # now relocate the box to the lower left corner
    fps_text_rect.bottom = canvas.get_rect().bottom - 10
    canvas.blit(fps_text_surface, fps_text_rect) #... and copy it to the buffer at the location of the box

    objects_string = f"Objects: {(len(objects_on_screen)):5d} {len(pie_list)}" #build a string with the number of objects
                            # (the 5d means an integer (d) with spaces so that it is always at least 5 characters wide.)
    objects_text_surface = stats_font.render(objects_string,True,white_color)
    objects_text_rect = objects_text_surface.get_rect()
    objects_text_rect.right = canvas.get_rect().right - 10 # move this box to the lower right corner
    objects_text_rect.bottom = canvas.get_rect().bottom - 10
    canvas.blit(objects_text_surface, objects_text_rect)

    hits_string = f"HITS: {hits}"
    hits_text_surface = stats_font.render(hits_string, True, white_color)  # this makes a transparent box with text
    hits_text_rect = hits_text_surface.get_rect()  # gets a copy of the bounds of the transparent box
    hits_text_rect.left = 10  # now relocate the box to the left side top
    hits_text_rect.top = canvas.get_rect().top + 20
    canvas.blit(hits_text_surface, hits_text_rect)

    misses_string = f"MISSES: {misses}"
    misses_text_surface = stats_font.render(misses_string, True, white_color)  # this makes a transparent box with text
    misses_text_rect = misses_text_surface.get_rect()  # gets a copy of the bounds of the transparent box
    misses_text_rect.left = 10  # now relocate the box to the left side top
    misses_text_rect.top = canvas.get_rect().top + 30
    canvas.blit(misses_text_surface, misses_text_rect)
def check_pie_clown_collision():
    global score, hits
    for pie in pie_list:
        if abs(pie.x - the_clown.x) < (pie.width/2 +the_clown.width/2) and \
            abs(pie.y - the_clown.y) < (pie.height / 2 + the_clown.height / 2):
            pie.die()
            print("HIT")
            score += 50
            hits += 1
            pygame.mixer.music.load('sounds/Smashingsound.mp3')
            pygame.mixer.music.play(1)
            # playsound('sounds/Smashingsound.mp3')


def check_pie_car_collision():
    global score
    for pie in pie_list:
        for car in car_list:
            if abs(pie.x - car.x) < (pie.width/2 +car.width/2) and \
                abs(pie.y - car.y) < (pie.height / 2 + car.height / 2):
                pie.die()
                print("Oops")
                score -= 50
                pygame.mixer.music.load('sounds/engineer_no01.mp3')
                pygame.mixer.music.play(1)

def shoot_pie():
    global ammo
    if len(pie_list) == 0 and ammo > 0:
        temp_pie = Pie(the_chicken.x,the_chicken.y)
        pie_list.append(temp_pie)
        objects_to_add.append(temp_pie)
        ammo -= 1

def calc_misses():
    global misses
    misses = 10-ammo - hits

def the_end_game():
    global pie, clown, chicken, left_car, right_car
    if ammo == 0:
        canvas.fill(pygame.Color("black"))
        gameover_font = pygame.font.SysFont("Arial", 96)
        gameover_color = pygame.Color("yellow")

        gameover_surface = gameover_font.render("Game Over", True, gameover_color)
        gameover_rectangle = gameover_surface.get_rect()

        canvas.blit(gameover_surface, (300 - gameover_rectangle.width / 2, 300 - gameover_rectangle.height / 2))

        score_font = pygame.font.SysFont("Arial", 96)
        score_color = pygame.Color("yellow")

        score_surface = score_font.render(f'SCORE:{score} ', True, score_color)
        score_rectangle = score_surface.get_rect()

        canvas.blit(score_surface, (300 - score_rectangle.width / 2, 500 - score_rectangle.height / 2))
          #


# =====================  read_events()
def read_events():
    """
    checks the list of events and determines whether to respond to one.
    """
    events = pygame.event.get()  # get the list of all events since the last time
    for evt in events:
        if evt.type == QUIT:
            pygame.quit()
            raise Exception("User quit the game")
            # You may decide to check other events, like the mouse
            # or keyboard here.
        if evt.type == MOUSEMOTION:
            the_chicken.x = evt.pos[0]
            the_chicken.y = evt.pos[1]
        if evt.type == MOUSEBUTTONDOWN:
            shoot_pie()



# program start with game loop - this is what makes the loop() actually loop.
pygame.init()
try:
    setup()
    fpsClock = pygame.time.Clock()  # this will let us pass the deltaT to loop.
    while True:
        time_since_last_loop = fpsClock.tick(60) / 1000.0 # we set this to go up to as much as 60 fps, probably less.
        loop(time_since_last_loop)
        read_events()

except Exception as reason: # If the user quit, exit gracefully. Otherwise, explain what happened.
    if len(reason.args)>0 and reason.args[0] == "User quit the game":
        print ("Game Over.")
    else:
        traceback.print_exc()
