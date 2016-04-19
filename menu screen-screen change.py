import pygame, random, math

# Pygame Setting
pygame.init()
display = pygame.display.set_mode((640, 480))
clock = pygame.time.Clock()

# Font

gameFont = pygame.font.SysFont("Arial", 32)

# Keyboard
keyboard_input = []
keyboard_prev = []


def keyboard_pressed(key):
    # Check if a keyboard button is pressed
    try:
        if not keyboard_prev[key] and keyboard_input[key]:
            return True
        return False
    except IndexError:
        return False


def draw_text(surface, text, x, y, color=(0, 0, 0), h_align=0, v_align=0):
    _txt = gameFont.render(text, True, color)
    text_w, text_h = gameFont.size(text)
    draw_x = x - (text_w/2) - (text_w/2)*(h_align-1)
    draw_y = y - (text_h/2) - (text_h/2)*(v_align-1)
    surface.blit(_txt, (draw_x, draw_y))

# Room Class

current_room = None


class Room(object):
    room_list = []

    def __init__(self, room_speed=60):
        self.instance_list = []
        self.room_speed = room_speed
        Room.room_list.append(self)

    def init(self):
        pass


def room_change(new_room):
    global current_room
    current_room.instance_list = []
    current_room = new_room
    new_room.init()

# Object Class


class Object(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def init(self):
        pass

    def update(self):
        pass

    def destroy(self):
        if self in current_room.instance_list:
            current_room.instance_list.remove(self)


def instance_create(obj, x, y):
    global current_room
    instance = obj(x, y)
    current_room.instance_list.append(instance)
    instance.init()
    return instance

# Setting room and object

# Main menu room


class MainMenu(Room):
    def init(self):
        # Create Menu instance
        instance_create(Menu, 320, 240)


class Menu(Object):
    def init(self):
        self.menu = ["Game Start", "Game Exit"]
        self.cursor_pos = 0

    def update(self):
        # Draw Title
        draw_text(display, "Avoid the Poo", self.x, self.y-100, (200, 100, 0), h_align=1, v_align=1)

        # Draw Menu
        for m in range(len(self.menu)):
            draw_text(display, str(self.menu[m]), self.x, self.y + 40*m, h_align=1, v_align=0)

        # Draw Cursor
        pygame.draw.circle(display, (0, 0, 0), (self.x-100, self.y + 40*self.cursor_pos + 20), 10)

        # Move Cursor
        if keyboard_pressed(pygame.K_UP):
            self.cursor_pos -= 1
            self.cursor_pos = max(self.cursor_pos, 0)

        if keyboard_pressed(pygame.K_DOWN):
            self.cursor_pos += 1
            self.cursor_pos = min(self.cursor_pos, 1)

        # When the player selected menu
        if keyboard_pressed(pygame.K_RETURN):
            if self.menu[self.cursor_pos] == "Game Start":
                # if Game Start is pressed, change the room from room1 to room2
                room_change(room2)
            else:
                # if Game Exit is pressed, exit the game
                pygame.quit()
                quit()

# Game room

# Define Score
score = 0


class Game(Room):
    def init(self):
        # When the game starts, set score to zero
        global score
        score = 0

        # Create GameSystem instance which controls the game
        instance_create(GameSystem, 0, 0)


class GameSystem(Object):
    def init(self):

        # Create Player instance
        instance_create(Player, 320, 440)

        # Set the Timer to 20 tick
        self.timer = 20

    def update(self):

        # Draw the ground
        pygame.draw.line(display, (0, 0, 0), (0, 456), (640, 456))

        # if timer is set
        if self.timer > -1:
            # decrease timer value
            self.timer -= 1
            # if timer is over
            if self.timer == -1:
                # Create the poo instance (1~3) on random x
                for i in range(random.randint(1, 3)):
                    instance_create(Poo, random.randint(0, 640), 0)
                # Set timer to 20 tick
                self.timer = 20

        # Draw score
        draw_text(display, str(score), 320, 20, h_align=1)


class Poo(Object):
    def init(self):
        # Set gravity
        self.gravity = 15

    def update(self):
        # Decrease y value by gravity
        self.y += self.gravity

        # Draw poo
        pygame.draw.circle(display, (0, 0, 0), (self.x, self.y), 16)

        # If it goes over y=480 destroy itself
        if self.y > 480:
            global score
            score += 1
            self.destroy()


class Player(Object):
    def update(self):
        # Draw player
        pygame.draw.rect(display, (255, 0, 0), (self.x-16, self.y-16, 32, 32))

        # Move player
        if keyboard_input[pygame.K_LEFT]:
            self.x -= 10
        if keyboard_input[pygame.K_RIGHT]:
            self.x += 10

        # Check Collision
        for instance in current_room.instance_list:
            if type(instance) == Poo:
                if math.sqrt(pow(self.x-instance.x, 2) + pow(self.y-instance.y, 2)) < 32:
                    room_change(room3)

# Score display Room


class ScoreDisplay(Room):
    def init(self):
        instance_create(score_panel, 0, 0)


class score_panel(Object):
    def update(self):
        draw_text(display, "score: " + str(score), 320, 240, (255, 0, 0), 1, 1)
        draw_text(display, "press enter to return to main menu", 320, 280, (255, 0, 0), 1, 1)
        if keyboard_pressed(pygame.K_RETURN):
            room_change(room1)

# Room Define
room1 = MainMenu()
room2 = Game()
room3 = ScoreDisplay()

# Game Start

if current_room is None:
    current_room = Room.room_list[0]

current_room.init()
while True:
    display.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    global keyboard_input, keyboard_prev
    keyboard_input = pygame.key.get_pressed()

    # Go through instance list of current room and run update method
    for instance in current_room.instance_list:
        instance.update()

    keyboard_prev = keyboard_input

    pygame.display.flip()
    clock.tick(current_room.room_speed)
