import pygame


# Data Type
class Map(object):
    def __init__(self, items=None):
        self.key = []
        self.value = []
        self.dict = {}

        if items:
            for item in items:
                key, value = item
                self.key.append(key)
                self.value.append(value)
                self.dict.update({key:value})

    def __getitem__(self, item):
        return self.dict[item]

    def __repr__(self):
        return "Map[("+str('), ('.join([str(key)+", "+str(self.dict[key]) for key in self.key]))+")]"

    def update(self, items):
        for item in items:
            key, value = item
            if key in self.key:
                self.value[self.key.index(key)] = value
            else:
                self.key.append(key)
                self.value.append(value)
            self.dict.update({key:value})

    def keys(self):
        return self.key


class Room(object):
    rooms = Map()
    current_room = None

    def __init__(self, room_speed=60):
        self.instance_list = []
        self.room_speed = room_speed
        self.current_frame = 0

    def init(self):
        pass


class Object(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def init(self):
        pass

    def update(self):
        pass

    def destroy(self):
        if self in Room.current_room.instance_list:
            Room.current_room.instance_list.remove(self)


class Sprite(object):
    # Sprite class

    def __init__(self, file_name, width=0, height=0, alpha=True):
        if alpha:
            self.sprite_sheet = pygame.image.load(file_name).convert_alpha()
        else:
            self.sprite_sheet = pygame.image.load(file_name).convert()
        self.sprite = []
        self.mask = []
        self.center_x, self.center_y = (0, 0)
        self.file_name = file_name
        self.sheet_width = self.sprite_sheet.get_size()[0]
        self.sheet_height = self.sprite_sheet.get_size()[1]
        self.image_count = 0
        if width == 0 or height == 0:
            width = self.sheet_width
            height = self.sheet_height
        self.image_width = width
        self.image_height = height
        for yy in xrange(self.sheet_height/height):
            for xx in xrange(self.sheet_width/width):
                image = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                image.blit(self.sprite_sheet, (0, 0), (xx*width, yy*height, width, height))
                self.sprite.append(image)
                self.mask.append(pygame.mask.from_surface(image))
                self.image_count += 1

    def get_image(self, index=0):
        try:
            return self.sprite[index]
        except IndexError:
            return self.sprite[0]

    def get_mask(self, index=0):
        try:
            return self.mask[index]
        except IndexError:
            return self.mask[0]

    def set_center(self, center_x, center_y):
        self.center_x, self.center_y = center_x, center_y
