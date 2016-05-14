from setting import *
from classes import *
from constants import *
import math


def draw_text(text, x, y, color=(0, 0, 0), h_align=A_LEFT, v_align=A_TOP, font=None):
    if font is None:
        font = gameFont
    _txt = font.render(str(text), True, color)
    text_w, text_h = gameFont.size(str(text))
    draw_x = x - (text_w/2) - (text_w/2)*(h_align-1)
    draw_y = y - (text_h/2) - (text_h/2)*(v_align-1)
    surface.blit(_txt, (draw_x, draw_y))


def draw_set_font(font):
    global gameFont
    gameFont = font


def draw_sprite(sprite, x, y, index):
    surface.blit(sprite.get_image(index), (x, y))


def draw_sprite_animated(sprite, x, y, speed):
    current_image_index = int(Room.current_room.current_frame * speed % sprite.image_count)
    surface.blit(sprite.get_image(current_image_index), (x, y))


def draw_sprite_ext(sprite, x, y, width, height, angle, animate_speed):
    current_image_index = int(Room.current_room.current_frame * animate_speed % sprite.image_count)
    image = sprite.get_image(current_image_index)
    image = pygame.transform.scale(image, (width, height))
    rot_image = pygame.transform.rotate(image, angle)
    delta_w = rot_image.get_rect().w-image.get_rect().w
    delta_h = rot_image.get_rect().h-image.get_rect().h
    surface.blit(rot_image, (x - delta_w/2, y - delta_h/2))


def draw_sprite_rotated(sprite, x, y, angle, index=0):
    rot_image = pygame.transform.rotate(sprite.get_image(index), angle)
    delta_w = rot_image.get_rect().w-sprite.get_image(index).get_rect().w
    delta_h = rot_image.get_rect().h-sprite.get_image(index).get_rect().h
    surface.blit(rot_image, (x - delta_w/2, y - delta_h/2))


def draw_line(x1, y1, x2, y2, width=1, color=BLACK):
    # Draws Rectangle
    pygame.draw.line(surface, color, (x1, y1), (x2, y2), width)


def draw_rectangle(x1, y1, x2, y2, width=0, color=BLACK):
    # Draws Rectangle
    pygame.draw.rect(surface, color, (x1, y1, x2 - x1, y2 - y1), width)


def draw_circle(x, y, radius, width=0, color=BLACK):
    # Draws Rectangle
    pygame.draw.circle(surface, color, (int(x), int(y)), int(radius), width)


def display_get_width():
    # Get width of display
    return screenResolution[0]


def display_get_height():
    # Get height of display
    return screenResolution[1]


def display_resize(width, height):
    # Reset the size of display
    global screenResolution
    global surface
    screenResolution = (width, height)
    surface = pygame.display.set_mode(screenResolution)


def display_set_screen(state):
    global surface
    if state:
        surface = pygame.display.set_mode(screenResolution, pygame.FULLSCREEN)
    else:
        surface = pygame.display.set_mode(screenResolution)


def display_set_background_color(color):
    global gameBackgroundColor
    gameBackgroundColor = color


def fps_get(precise=False):
    if precise:
        return clock.get_fps()
    else:
        return int(clock.get_fps())


def keyboard_button(key):
    # Check if a keyboard button is on hold
    try:
        if keyboardInput[key]:
            return True
        return False
    except IndexError:
        return False


def keyboard_released(key):
    # Check if a keyboard button is released
    try:
        if keyboardPrev[key] and not keyboardInput[key]:
            return True
        return False
    except IndexError:
        return False


def keyboard_pressed(key):
    # Check if a keyboard button is pressed
    try:
        if not keyboardPrev[key] and keyboardInput[key]:
            return True
        return False
    except IndexError:
        return False


def mouse_button(key):
    # Check if a mouse button is on hold
    try:
        if mouseInput[key]:
            return True
        return False
    except IndexError:
        return False


def mouse_released(key):
    # Check if a mouse button is released
    try:
        if mousePrev[key] and not mouseInput[key]:
            return True
        return False
    except IndexError:
        return False


def mouse_pressed(key):
    # Check if a mouse button is pressed
    try:
        if not mousePrev[key] and mouseInput[key]:
            return True
        return False
    except IndexError:
        return False


def mouse_x():
    # Get x position of mouse
    return mousePos[0]


def mouse_y():
    # Get y position of mouse
    pos = pygame.mouse.get_pos()
    return mousePos[1]


def instance_create(obj, x, y):
    instance = obj(x, y)
    Room.current_room.instance_list.append(instance)
    instance.init()
    return instance


def instance_get_list(obj):
    # Get list of instance
    return [ins for ins in Room.current_room.instance_list if type(ins) is obj]


def point_distance(x1, y1, x2, y2):
    # Return distance between to points
    return math.sqrt(pow(x2-x1, 2) + pow(y2-y1, 2))


def point_direction(x1, y1, x2, y2, in_degree=True):
    # Return direction from one point to another
    if in_degree:
        return math.degrees(math.atan2(-(y2-y1), (x2-x1)))
    else:
        return math.atan2(-(y2-y1), (x2-x1))


def length_direction_x(length, direction):
    return math.cos(math.radians(direction)) * length


def length_direction_y(length, direction):
    return math.sin(math.radians(-direction)) * length


def collision_rectangle(box1, box2):
    b1 = list(box1)
    b2 = list(box2)
    if b1[2] < 0:
        b1[0] += b1[2]
        b1[2] *= -1
    if b2[2] < 0:
        b2[0] += b2[2]
        b2[2] *= -1
    # Rectangular collision check
    if b2[0] > b1[0] + b1[2]:
        return False
    if b1[0] > b2[0] + b2[2]:
        return False
    if b1[1] > b2[1] + b2[3]:
        return False
    if b2[1] > b1[1] + b1[3]:
        return False
    return True


def room_change(new_room):
    Room.current_room.instance_list = []
    Room.current_room = Room.rooms[new_room]
    Room.current_room.current_frame = 0
    Room.rooms[new_room].init()


def room_current():
    return Room.current_room


def game_end():
    # Game End
    pygame.quit()
    quit()


def game_start(game_init=None, game_update=None, room_list=None):
    # Start game loop
    if room_list:
        for room in room_list:
            Room.rooms.update([(room, room())])
    else:
        for room in Room.__subclasses__():
            Room.rooms.update([(room, room())])

    if game_init:
        game_init()

    if Room.current_room is None:
        Room.current_room = Room.rooms[Room.rooms.keys()[0]]

    Room.current_room.init()

    while True:
        surface.fill(gameBackgroundColor)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end()

            global keyboardInput, mouseInput, mousePos
            keyboardInput = pygame.key.get_pressed()
            mouseInput = pygame.mouse.get_pressed()
            mousePos = pygame.mouse.get_pos()
        pygame.event.pump()

        if game_update:
            game_update()

        for instance in Room.current_room.instance_list:
            if instance in Room.current_room.instance_list:
                instance.update()

        Room.current_room.current_frame += 1

        global keyboardPrev, mousePrev
        keyboardPrev = keyboardInput
        mousePrev = mouseInput
        pygame.display.flip()
        clock.tick(Room.current_room.room_speed)
