from enum import Enum
import pygame,  colors
import random
from ui import Button,UI_TextElement,Switch,UI_Manager,WIDTH,HEIGHT, FONTS 
from GameLogic import Logic,Node

class GameState(Enum):
    MAIN_MENU = 1
    PLAYING = 2
    ENDSCREEN = 3

class Game():
    def __init__(self):
        self.UI_Manager = UI_Manager()
        self.Logic_Manager = None
        self.running = True
        self.game_state = GameState.MAIN_MENU

        self.buttons = None
        self.PairSelectionButtons = None

        self.start_numberlength = 20
        self.start_useMinmax = True
        self.start_playerfirst = True

        self.ai_search_depth = 3

    def game_loop(self):   
        self.UI_Manager.Setup_Main_Menu(self.start_numberlength)
        self.create_buttons()
        while self.running:
            change_cursor_to_hover_mode = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  
                    self.running = False
                if event.type == pygame.USEREVENT:
                    if (not self.Logic_Manager.CurrentNode.player_turn and self.game_state == GameState.PLAYING and len(self.Logic_Manager.CurrentNode.string) > 1):
                        start_time = pygame.time.get_ticks()
                        if(self.start_useMinmax):
                            self.Logic_Manager.AI_Play(self.ai_search_depth,True)
                        else:
                            self.Logic_Manager.AI_Play(self.ai_search_depth,False)
                        self.SetUpPairSelectionButtons(len(self.Logic_Manager.CurrentNode.string))
                        self.CheckWinner()
                        self.UpdateUI()
                        think_time = (pygame.time.get_ticks() - start_time)/1000
                        print("AI thought for : ",think_time, "seconds.")
                if(self.buttons):    
                    for btn in self.buttons:
                        btn.handle_event(event)
                if(self.game_state == GameState.PLAYING and self.PairSelectionButtons and self.Logic_Manager.CurrentNode.player_turn): # dont let the player choose if it is not their turn.
                    for btn in self.PairSelectionButtons:
                        btn.handle_event(event)
                
            self.UI_Manager.Draw_UI(self.buttons,self.PairSelectionButtons)

            if(self.buttons):
                for btn in self.buttons:
                    if(btn.hovered):
                        change_cursor_to_hover_mode = True
            if(self.PairSelectionButtons):
                for btn in self.PairSelectionButtons:
                    if(btn.hovered):
                        change_cursor_to_hover_mode = True

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND if change_cursor_to_hover_mode else pygame.SYSTEM_CURSOR_ARROW)
        pygame.quit()

    def start_game(self):
        print("Start Button Clicked!")
        self.SwitchState(GameState.PLAYING)
        pygame.time.set_timer(pygame.USEREVENT, 1)  


        self.UpdateUI()

    def quit_game(self):
        print("Quit Button Clicked!")
        if(self.Logic_Manager):
            self.Logic_Manager.printTree()
        self.running = False

    def increment_numberLength(self,amount):
        desiredLength = self.start_numberlength + amount
        if 15 <= desiredLength <= 25:
            self.start_numberlength = desiredLength
            self.UI_Manager.texts[7].text = ""
            self.UI_Manager.texts[6].text = f"{desiredLength}"

        if desiredLength == 15 or desiredLength ==  25:
            self.start_numberlength = desiredLength
            self.UI_Manager.texts[7].text = "The number can only be between 15 and 25"

    def UpdateUI(self): # Updates the texts in ui according to game data
        self.UI_Manager.texts[0].text = " ".join(self.Logic_Manager.CurrentNode.string)
        print(self.Logic_Manager.CurrentNode.player_turn,"ActiveString:","".join(self.Logic_Manager.CurrentNode.string), self.Logic_Manager.CurrentNode.p1, self.Logic_Manager.CurrentNode.p2)
        self.UI_Manager.texts[3].text = f"{self.Logic_Manager.CurrentNode.p1}" # Text list is at the ui.py file, need to manually set ids to what text you want to update.
        self.UI_Manager.texts[4].text = f"{self.Logic_Manager.CurrentNode.p2}"
     

    def GenerateRandomNumberWithNDigits(self,N):
    # random int between [(10^3),((10^4)-1)] = [100,999] , used stringlength = 4 for this example
        return list(str( random.randint(10**(N-1), 10**N - 1 )))

    def SwitchState(self,state):
        self.game_state = state
        if(state == GameState.MAIN_MENU):
            self.UI_Manager.Setup_Main_Menu(self.start_numberlength)
            self.PairSelectionButtons = []
            self.create_buttons()
        elif(state == GameState.PLAYING):
            self.Logic_Manager = Logic(Node('A1', self.GenerateRandomNumberWithNDigits(self.start_numberlength), 0, 0, 1,self.start_playerfirst))
            #self.Logic_Manager = Logic(Node('A1', list("26719"), 1, 1, 1,self.start_playerfirst))

            self.UI_Manager.Setup_Playing()
            self.create_buttons()


    def ToggleAlgorithm(self):
        self.start_useMinmax = not self.start_useMinmax
        print("Use Minmax toggled to :",self.start_useMinmax)

    def TogglePlayerTurn(self):
        self.start_playerfirst = not self.start_playerfirst
        print("player turn toggled to :",self.start_playerfirst)
    
    def SetUpPairSelectionButtons(self,n):
        self.PairSelectionButtons = []
        buttonwidth = 41
        for i in range(1,n):
            PairSelectionButton = Button(((((WIDTH//2)-i*buttonwidth)-buttonwidth/2+float(n/2)*buttonwidth), HEIGHT//3-44.5, buttonwidth, 87.5), colors.GREEN, f"", FONTS[0], lambda i=i: self.SelectPair(n-i))# n-i because the buttons are created right to left
            self.PairSelectionButtons.append(PairSelectionButton)

    def SelectPair(self, selected_pair_id):
        moves = self.Logic_Manager.get_possible_moves(self.Logic_Manager.CurrentNode)
        self.Logic_Manager.CurrentNode = moves[selected_pair_id-1]
        self.SetUpPairSelectionButtons(len(self.Logic_Manager.CurrentNode.string))
        self.UpdateUI()
        pygame.time.set_timer(pygame.USEREVENT, 1) 
        self.CheckWinner()

    def CheckWinner(self):
        if(len(self.Logic_Manager.CurrentNode.string)<2):
            if(self.Logic_Manager.CurrentNode.p1>self.Logic_Manager.CurrentNode.p2):
                print("Winner is the Player(p1) !")
                self.UI_Manager.texts.append(UI_TextElement("Winner is the Player !",colors.GREEN,FONTS[0],(WIDTH // 2, HEIGHT // 6))) 
            elif(self.Logic_Manager.CurrentNode.p1==self.Logic_Manager.CurrentNode.p2):
                self.UI_Manager.texts.append(UI_TextElement("Game is Draw !",colors.YELLOW,FONTS[0],(WIDTH // 2, HEIGHT // 6)))
            else:
                print("Winner is the Computer(p2) !")
                self.UI_Manager.texts.append(UI_TextElement("Winner is the Computer !",colors.RED,FONTS[0],(WIDTH // 2, HEIGHT // 6)))
            return True
        return False
    
    def create_buttons(self):
        if(self.game_state == GameState.MAIN_MENU):    
            self.buttons = [
                Button(((WIDTH//3)-100, HEIGHT-(HEIGHT//2), 200, 50), colors.BLUE, "Start", FONTS[0], self.start_game),
                Button((2*(WIDTH//3)-100, HEIGHT-(HEIGHT//2),200,50), colors.RED, "Quit", FONTS[0], self.quit_game),
                
                Switch(((WIDTH//2)-25, HEIGHT-(HEIGHT//2)+112, 50, 25), colors.GRAY,  self.ToggleAlgorithm,self.start_useMinmax,[self.UI_Manager.texts[1],self.UI_Manager.texts[2]]),
                Switch(((WIDTH//2)-25, HEIGHT-(HEIGHT//2)+162, 50, 25), colors.GRAY,  self.TogglePlayerTurn,self.start_playerfirst,[self.UI_Manager.texts[3],self.UI_Manager.texts[4]]),

                Button(((WIDTH//2)-75, HEIGHT-(HEIGHT//5), 50, 50), colors.GRAY, "-", FONTS[0], lambda : self.increment_numberLength(-1)),
                Button(((WIDTH//2)+25, HEIGHT-(HEIGHT//5), 50, 50), colors.GRAY, "+", FONTS[0], lambda : self.increment_numberLength(1))
                ]
        elif(self.game_state == GameState.PLAYING):
            self.buttons = [                
                Button(((WIDTH//2)-100, HEIGHT-(HEIGHT//5), 200, 50), colors.YELLOW, "Main Menu", FONTS[0], lambda: self.SwitchState(GameState.MAIN_MENU)),
                ]
            self.SetUpPairSelectionButtons(self.start_numberlength)   
