import pygame


class Button:
    def __init__(self, screen, position_screen:tuple[int,int], text:str, color_button:tuple[int,int,int],
                 color_text:tuple[int,int,int], size:int) -> None:
        self.screen = screen
        self.rec:tuple[int,int,int,int] = position_screen[0],position_screen[1],int (size * 3.5),size
        self.position_text = self.get_position_text()
        self.text = text
        self.color_button = color_button
        self.color_text = color_text
        self.size = size
        font = pygame.font.SysFont("Arial", size // 3)
        self.text_surface = font.render(self.text, True, color_text)

    def draw(self) -> None:
        pygame.draw.rect(self.screen, self.color_button, self.rec)
        self.screen.blit(self.text_surface, self.position_text)

    def get_position_text(self) -> tuple[int,int]:
        return self.rec[0] , self.rec[1] + self.rec[3] // 4
    def click(self) -> bool:
        poz = pygame.mouse.get_pos()
        if not pygame.mouse.get_pressed()[0]:
            return False
        # print(poz)
        # print(self.rec)
        # print(self.rec[0], poz[0], self.rec[0] + self.rec[2])
        # print(self.rec[1], poz[1], self.rec[1] + self.rec[3])
        if self.rec[0] <= poz[0] <= self.rec[0] + self.rec[2]:
            if self.rec[1] <= poz[1] <= self.rec[1] + self.rec[3]:
                return True
        return False