"""
Title: Tap the boxes
Purpose: Create a game where you can tap boxes
Creator: Orlando
"""

import pygame
from pygame import mixer
from pydub import AudioSegment

# Song can be switched by placing a different music file, however the edge threshholds should be changed based on the song
song = AudioSegment.from_file("WeAreN1.wav")

# Size of segments to break song into for volume calculations
SEGMENT_MS = 50

# dBFS is decibels relative to the maximum possible loudness
volume = [segment.dBFS for segment in song[::SEGMENT_MS]]

# Minimum volume necessary to be considered a note
VOLUME_THRESHOLD = -1000

# The increase from one sample to the next required
# to be considered a note (Instead of background)
EDGE_THRESHOLD = -1

# Throw out any additional notes found in this window
MIN_MS_BETWEEN = 40
predicted_starts = []
for i in range(1, len(volume)):
    if (
        volume[i] > VOLUME_THRESHOLD and
        volume[i] - volume[i - 1] > EDGE_THRESHOLD
    ):
        ms = i * SEGMENT_MS
        # Ignore any too close together
        if (
            len(predicted_starts) == 0 or
            ms - predicted_starts[-1] >= MIN_MS_BETWEEN
        ):
            predicted_starts.append(ms)

# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load('background.jpg')


# Caption and Icon
pygame.display.set_caption("Tap the box")

# Boxes
red_square = pygame.image.load('redsquare.png')
blue_square = pygame.image.load('bluesquare.png')

# Arrow
arrow_image = pygame.image.load('arrow.dms')
arrow_image = pygame.transform.scale(arrow_image, (100, 100))

# Starting the mixer
mixer.init()

# Loading the song
mixer.music.load("WeAreN1.wav")

# Setting the volume
mixer.music.set_volume(0.5)


# Music info
array = predicted_starts
arrowX = [0] * len(array)
arrowY = [0] * len(array)
arrowStart = [0] * len(array)

# Score
global score
score = 0


# Displays the controllable ship
def player(direction):

    # Will scale the image and rotate it according to the angle
    red = pygame.transform.scale(red_square, (100, 100))
    blue = pygame.transform.scale(blue_square, (100, 100))

    if direction == "None":
        screen.blit(blue, (140, 400))
        screen.blit(red, (560, 400))

    elif direction == "Left":
        screen.blit(pygame.transform.rotate(blue, 180), (140, 400))
        screen.blit(red, (560, 400))

    elif direction == "Right":
        screen.blit(blue, (140, 400))
        screen.blit(pygame.transform.rotate(red, 180), (560, 400))

# Displays arrow
def arrow(arrowX, arrowY):
    if arrowY == 0:
        screen.blit(arrow_image, (140, arrowX))
    if arrowY == 1:
        screen.blit(arrow_image, (560, arrowX))

# Registers the tap of the user
def taparrow(direction):

    global score

    for x in range(len(array)):

        # Determines whether the right side has been clicked
        if direction == "Left":

            # ArrayY[x] is assigned to determine whether a note is left or right
            if arrowY[x] == 0:

                if arrowX[x] < 450 and arrowX[x] > 300:

                    # Stops the function and registers the click
                    arrowX[x] = 0
                    arrowStart[x] = 0
                    score += 1
                    return

        elif direction == "Right":

            if arrowY[x] == 1:

                if arrowX[x] < 450 and arrowX[x] > 300:
                    # Stops the function and registers the click
                    arrowX[x] = 0
                    arrowStart[x] = 0
                    score += 1
                    return

        score -= 1/len(array)

# Displays the score
def displayscore(score):
    disscore = pygame.font.Font('freesansbold.ttf', 32).render("Your Score : " + str(int(score)), True, (0, 0, 0))
    screen.blit(disscore, (30, 30))

def main():

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                intro = False
        screen.fill((255, 255, 255))
        start_text = pygame.font.Font('freesansbold.ttf', 32).render("Press a key to play:", True, (0, 0, 0))
        screen.blit(start_text, (250, 200))
        pygame.display.update()

    # Start playing the song
    mixer.music.play()

    time = 0
    direction = "None"
    tap = "None"
    total_time = 0

    running = True
    while running:

        # RGB = Red, Green, Blue
        screen.fill((255, 255, 255))

        # The game's timer
        total_time += 1.75

        # Receives any clicks
        for event in pygame.event.get():

            # Stops the loop if pygame is quit
            if event.type == pygame.QUIT:
                running = False

            # If keystroke is pressed, will rotate or fire a bullet
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_LEFT:

                    if tap == "None":

                        # Registers click
                        direction = "Left"
                        taparrow(direction)

                if event.key == pygame.K_RIGHT:

                    if tap == "None":

                        # Registers click
                        direction = "Right"
                        taparrow(direction)

            # When the user lifts up their finger, the ship will stop moving
            if event.type == pygame.KEYUP:

                # If the user lets go of the key, everything will be set to default
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:

                    direction = "None"
                    tap = "None"
                    time = 0

        # If the button has been clicked for too long, everything will be reset
        if direction == "Right" or direction == "Left":

            time += 1

            if time >= 50:

                direction = "None"
                tap = "YES"

        # Displays the clicked button
        player(direction)

        # Goes through the array and determines whether it is time of a note
        for x in range(len(array)):

            # Determines if a note is in action yet
            if array[x] <= total_time + 54 and array[x] >= total_time + 52:

                # Every note alternates between right and left
                if x%2 == 0:

                    arrowX[x] = 0

                    # Arroy[x] = 1 means it is on the right side
                    arrowY[x] = 1

                    # Means that the arrow will start to be displayed
                    arrowStart[x] = 1

                else:

                    arrowX[x] = 0

                    # Arroy[x] = 1 means left
                    arrowY[x] = 0
                    arrowStart[x] = 1

            # If the arrow is determined to be in action, the arrow will move
            if arrowStart[x] == 1:

                arrowX[x] += 1.4
                arrow(arrowX[x], arrowY[x])

        displayscore(score)
        pygame.display.update()

if __name__ == '__main__':
    main()