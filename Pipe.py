class Pipe:
    def __init__(self, left_down:int, left_up:int, width:int, left_x:int):
        self.left_down = left_down
        self.left_up = left_up
        self.width = width
        self.left_y = left_x

    def collides_with(self, poz_x:int, poz_y:int, distance:int) -> bool:
        if (self.left_y <= poz_y <= self.left_y + self.width) or (self.left_y <= poz_y + distance <= self.left_y + self.width):
            if (self.left_down >= poz_x >= self.left_up) and (self.left_down >= poz_x + distance >= self.left_up):
                return False
            return True
        return False
