import pygame
import colors
import weakref

WIDTH, HEIGHT = 1100, 700
FONTS = []

def init_fonts():
    global FONTS
    FONTS.append(pygame.font.Font(None, 36))
    FONTS.append(pygame.font.Font(None,72))
    
class UI_Manager:
    def __init__(self):
        init_fonts()
        self.window = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("The Number")
        self.texts=[]


    def DrawTexts(self):
        for text in self.texts:
            text.draw(self.window)

    def Draw_UI(self, buttons, PairSelectionButtons):
        self.window.fill(colors.DARK_GRAY)  
        pygame.draw.rect(self.window, colors.GREEN, (0,(HEIGHT//2)-(HEIGHT//4.3),WIDTH,HEIGHT//8))
        if(buttons):
            for button in buttons:
                button.draw(self.window)
        if (PairSelectionButtons):
            for PairSelectionButton in PairSelectionButtons:
                PairSelectionButton.draw(self.window)

        self.DrawTexts()
        pygame.display.update()
    

    def Setup_Main_Menu(self,numberlength):
        self.texts = [
        UI_TextElement("T H E   N U M B E R",colors.WHITE,FONTS[0],(WIDTH // 2, HEIGHT // 3)),
        UI_TextElement("Min-Max",  colors.GRAY, FONTS[0], ((WIDTH//3), HEIGHT-(HEIGHT//2)+125)),
        UI_TextElement("Alpha-Beta", colors.GRAY, FONTS[0],(2*(WIDTH//3), HEIGHT-(HEIGHT//2)+125)),
        UI_TextElement("Player Starts",colors.GRAY, FONTS[0], ((WIDTH//3), HEIGHT-(HEIGHT//2)+175)),
        UI_TextElement("AI Starts", colors.GRAY, FONTS[0],(2*(WIDTH//3), HEIGHT-(HEIGHT//2)+175)),
        UI_TextElement("Number Length", colors.WHITE, FONTS[0],((WIDTH//3), HEIGHT-(HEIGHT//6))),
        UI_TextElement(f"{numberlength}", colors.WHITE, FONTS[0],((WIDTH//2), HEIGHT-(HEIGHT//6))),
        UI_TextElement("", colors.GRAY, FONTS[0],((WIDTH//2), 15*HEIGHT//16))
        ]

        
    def Setup_Playing(self):
        self.texts =[ UI_TextElement("",colors.WHITE,FONTS[1],(WIDTH // 2, HEIGHT // 3)), # The number (since it updates frequently anyway we dont need to assign a text)
                      UI_TextElement("PLAYER SCORE",colors.GRAY,FONTS[0],(WIDTH // 5, HEIGHT // 6)),
                      UI_TextElement("AI SCORE",colors.GRAY,FONTS[0],(4*WIDTH // 5, HEIGHT // 6)),
                      UI_TextElement("",colors.WHITE,FONTS[1],(WIDTH // 5, HEIGHT // 6)), # Player Score (since it updates frequently anyway we dont need to assign a text)
                      UI_TextElement("",colors.WHITE,FONTS[1],(4*WIDTH // 5, HEIGHT // 6)) # AI Score (since it updates frequently anyway we dont need to assign a text)
                     ]

class UI_TextElement:
    def __init__(self, text, color, font, position):
        self.text = text
        self.color = color
        self.font = font
        self.position = position

    def draw(self,window):
        text_surface = self.font.render(self.text, True, self.color)
        text_rect = text_surface.get_rect()
        text_rect.center = self.position
        window.blit(text_surface,text_rect)

    def set_color(self,color):
        self.color = color

class Button():
    def __init__(self, rect, color, text, font, action):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.hover_color = (min(255, color[0]+50),min(255, color[1]+50),min(255, color[2]+50))
        self.action = action
        self.hovered = False        
        self.text = text
        self.font = font

    def draw(self, window):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        button_color = self.hover_color if self.hovered == True else self.color
        pygame.draw.rect(window, button_color, self.rect)


        text_surface = self.font.render(self.text, True, colors.WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        window.blit(text_surface, text_rect)
        

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            if self.rect.collidepoint(event.pos) :
                self.action() 
         

class Switch():
    def __init__(self, rect,color,action,state,referancedtext):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.hover_color = (min(255, color[0]+50),min(255, color[1]+50),min(255, color[2]+50))
        self.action = action
        self.hovered = False        
        self.current_state = state
        self.referancedtext = referancedtext  # a referance to the text object so we can change states of that exact text object within the class member functions
        self.updatereferances()

    def draw(self, window):
        mouse_pos = pygame.mouse.get_pos()
        self.hovered = self.rect.collidepoint(mouse_pos)
        button_color = self.hover_color if self.hovered else self.color

        pygame.draw.rect(window, button_color, self.rect)
        
        self.color = colors.GRAY if self.current_state else colors.GRAY
        switchposrect = (self.rect.x + (2*self.rect.width/24) if self.current_state else  (self.rect.x +5 * self.rect.width/8)+self.rect.width/16,self.rect.y+self.rect.height/8 ,  self.rect.width/4, 3*self.rect.height/4) 
        pygame.draw.rect(window, colors.DARK_GRAY,switchposrect)

    def updatereferances(self):
        if self.referancedtext[0] and self.referancedtext[1]:
            self.referancedtext[0].color = colors.WHITE if self.current_state else colors.GRAY
            self.referancedtext[1].color = colors.WHITE if not self.current_state else colors.GRAY

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  
            if self.rect.collidepoint(event.pos) :
                self.action()
                self.current_state = not self.current_state 
                self.updatereferances()
     
        

