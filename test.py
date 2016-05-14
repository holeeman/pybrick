from pybrick import *
import random

spr_char = Sprite("player.png", 32, 32, True)


class StartingRoom(Room):
    def init(self):
        print "start"
        room_change(NextRoom)


class NextRoom(Room):
    def init(self):
        print "next"
        for i in xrange(1):
            instance_create(Player, 100+random.randint(-50, 50), 100+random.randint(-50, 50))


class Player(Object):
    def init(self):
        self.sprite_index = spr_char

    def update(self):
        self.x += (keyboard_button(K_RIGHT)- keyboard_button(K_LEFT)) * 10
        self.y += (keyboard_button(K_DOWN)- keyboard_button(K_UP)) * 10
        draw_sprite_ext(self.sprite_index, self.x, self.y, 64, 64, Room.current_room.current_frame, 0.5)

new_font = pygame.font.SysFont("Arial", 20, 1)


def game_init():
    draw_set_font(new_font)
    display_resize(640, 480)


def game_update():
    draw_text(fps_get(), 10, 10)

game_start(game_init, game_update)