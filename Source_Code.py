import arcade
import numpy as np
import copy, sys

width, height = arcade.window_commands.get_display_size()
ROW_COUNT = 10
COLUMN_COUNT = 10
WIDTH = 60
HEIGHT = 60
MARGIN = 3
SCREEN_WIDTH = width
SCREEN_HEIGHT = height - 28
SPRITE_SCALING_PLAYER = 0.5
SCREEN_TITLE = "SNALIS Game"

class MenuView(arcade.View):
    def on_show(self):
        #arcade.set_background_color(arcade.color.WHITE)
        self.background = arcade.load_texture("menu.jpeg")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)
        # arcade.draw_text("Menu Screen", SCREEN_WIDTH/2, SCREEN_HEIGHT/2,
        #                  arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", 680, 550,
                         arcade.color.RED, font_size=50, anchor_x="center")

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        instructions_view = InstructionView()
        self.window.show_view(instructions_view)


class InstructionView(arcade.View):
    def on_show(self):
        # arcade.set_background_color(arcade.color.ORANGE_PEEL)
        self.background = arcade.load_texture("background2.jfif")

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0,0,SCREEN_WIDTH,SCREEN_HEIGHT,self.background)
        arcade.draw_text("Instructions Screen", 400, 650, arcade.color.BLACK, font_size=50)
        arcade.draw_text("1: 2D Snail game has total hundred number of grids.", 170, 600, arcade.color.BLACK, font_size=20)
        arcade.draw_text("2: Initial position of 1st player will be at the bottom left but inside the specified grid.", 170, 560, arcade.color.BLACK, font_size=20)
        arcade.draw_text("3: Initial position of 2nd player will be at the top right but inside the specifies grid.", 170, 520, arcade.color.BLACK, font_size=20)
        arcade.draw_text("4: A player can move one step in single turn and step can be towards left, right, up or down.", 170, 480, arcade.color.BLACK, font_size=20)
        arcade.draw_text("5: A player can't move diagonally.", 170, 440, arcade.color.BLACK, font_size=20)
        arcade.draw_text("6: A player can't jump from one position to other. Instead of jumping, it has to cover all the position to reach that specific position.", 170, 400, arcade.color.BLACK, font_size=20)
        arcade.draw_text("7: A player can't move to position or splash of opponent. ", 170, 360, arcade.color.BLACK, font_size=20)
        arcade.draw_text("8: A player can move on its own splashes but it will slip to last splash towards moving side. ", 170, 320, arcade.color.BLACK, font_size=20)
        arcade.draw_text("9: A player can use mouse to click to move its sprite. ", 170, 280, arcade.color.BLACK, font_size=20)
        arcade.draw_text("10: A player can lose its turn by clicking on opponent's position.", 170, 240, arcade.color.BLACK, font_size=20)
        arcade.draw_text("11: Both players have to cover maximum position to win the game.", 170, 200, arcade.color.BLACK, font_size=20)
        arcade.draw_text("12: When there is be no position or box of grid, the game will be ended.", 170, 160, arcade.color.BLACK, font_size=20)
        arcade.draw_text("13: Each legal turn and filling of empty position will add a point to total points of that player.", 170, 120, arcade.color.BLACK, font_size=20)
        arcade.draw_text("14: A player with maximum number of covered position will win the game.", 170, 80, arcade.color.BLACK, font_size=20)

        arcade.draw_text("Click to advance", 500,40,arcade.color.GRAY, font_size=30)

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        game_view = GameView()
        self.window.show_view(game_view)


class GameView(arcade.View):

    def __init__(self):
        super().__init__()
        
        
        self.grid = None
        # print(self.grid)
        self.player_list = None
        self.player1_sprite = None
        self.player2_sprite = None
        self.player1_sprite_splash = None
        self.player2_sprite_splash = None
        self.Background = None
        self.vs  = None
        self.count = 2
        self.scoreA = 0
        self.scoreB = 0        
        self.player_list = arcade.SpriteList()
        self.player1_list = arcade.SpriteList()        
        self.player1_previous_x = None
        self.player1_previous_y = None
        self.player2_previous_x = None
        self.player2_previous_y = None
        self.snailD = None
        self.counter1 = 0
        self.setup()
        self.initialize_grid()

    def initialize_grid(self):
        self.grid=np.zeros((10,10))
        self.grid[0][0] = 1
        self.grid[9][9] = 2


    def setup(self):
        
        img = "sprite2.png"
        self.player2_sprite = arcade.Sprite(img, 0.22)
        self.player2_sprite.center_x = 600
        self.player2_sprite.center_y = 602
        self.player1_list.append(self.player2_sprite)
        self.Background = arcade.load_texture("back4.jpg")
        self.vs = arcade.load_texture("vslogo.png")

        img = "sprite1.png"
        self.player1_sprite = arcade.Sprite(img, 0.13)
        self.player1_sprite.center_x = 33
        self.player1_sprite.center_y = 33
        self.player1_list.append(self.player1_sprite)

        img1 = "snailDesign.png"
        self.snailD = arcade.Sprite(img1, 0.5)
        self.snailD.center_x = 970
        self.snailD.center_y = 250
        self.player1_list.append(self.snailD)

    
    def on_draw(self):  

        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.Background)
        for x in range(0, 631, 63):
            arcade.draw_line(x, 0, x, 630, arcade.color.WHITE, 1.5)
        for y in range(0, 631, 63):
            arcade.draw_line(0, y, 630, y, arcade.color.WHITE, 1.5) 

        arcade.draw_text("SNAILS Game", 530, 663, arcade.color.WHITE, 40,bold=True,font_name="ALGERIAN")

        arcade.draw_text("Player Turn: A", 700, 510, arcade.color.WHITE, 22,bold=True,font_name="ALGERIAN")
        arcade.draw_text("Player Turn: B", 1050, 510, arcade.color.WHITE, 22,bold=True,font_name="ALGERIAN")
        if self.count % 2 == 0:        
            arcade.draw_text("Player Turn: A", 700, 510, arcade.color.CYAN, 22,bold=True,font_name="ALGERIAN")
        else:
            arcade.draw_text("Player Turn: B", 1050, 510, arcade.color.CYAN, 22,bold=True,font_name="ALGERIAN")
        # arcade.draw_text("Player A Score:", 700, 470, arcade.color.YELLOW, 20)
        # arcade.draw_text("Player B Score:", 1050, 470, arcade.color.YELLOW, 20)
        arcade.draw_text(str(self.scoreA), 800, 450, arcade.color.WHITE, 25,bold=True,font_name="ALGERIAN")
        arcade.draw_text(str(self.scoreB), 1150, 450, arcade.color.WHITE, 25,bold=True,font_name="ALGERIAN")
        if self.count % 2 == 0:
            arcade.draw_text(str(self.scoreA), 800, 450, arcade.color.CYAN, 25, bold=True,font_name="ALGERIAN")
        else:
            arcade.draw_text(str(self.scoreB), 1150, 450, arcade.color.CYAN, 25,bold=True,font_name="ALGERIAN")

        arcade.draw_texture_rectangle(992, 510, 180, 120, self.vs)
        # self.snailD.draw()


        self.player_list.draw()
        self.player1_list.draw()
        

    def is_Legal_Move(self,x,y):
        num1 = x - self.player1_sprite.center_x
        num2 = y - self.player1_sprite.center_y
        num3 = x - self.player2_sprite.center_x
        num4 = y - self.player2_sprite.center_y

        res = False

        column = int(x // (WIDTH + MARGIN))
        row = int(y // (HEIGHT + MARGIN))

        x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
        y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4

        # print(num2)
        if self.count % 2 == 0:
            # if num1 < 30:
            #     return False
            if num1 > 90:
                res = False
            elif  num2 > 88:
                res = False
            elif num1 < -94:
                res = False
            elif num2 < -99:
                res = False
            elif num1 > 28 and num2 > 25:
                res = False
            elif num1 < -32 and num2 < -34:
                res = False
            elif num1 < -32 and num2 > 25:
                res = False
            elif num1 > 28 and num2 < -35:
                res = False
            else:
                res = True
            if res ==  True:
                if row < ROW_COUNT and column < COLUMN_COUNT:
                    if self.grid[row][column] == 0:
                        self.grid[row][column] = 1                    
                        self.player1_sprite.center_x = x
                        self.player1_sprite.center_y = y
                        column1 = int(self.player1_previous_x // (WIDTH + MARGIN))
                        row1 = int(self.player1_previous_y // (HEIGHT + MARGIN))
                        img = "sprite1_splash.png"
                        self.player1_sprite_splash = arcade.Sprite(img, 0.06)
                        self.player1_sprite_splash.center_x = self.player1_previous_x
                        self.player1_sprite_splash.center_y = self.player1_previous_y
                        self.player_list.append(self.player1_sprite_splash)            
                        self.grid[row1][column1] = 11
                        self.count = self.count + 1
                        self.scoreA = self.scoreA + 1

                    elif self.grid[row][column] == 11:
                        column1 = int(self.player1_previous_x // (WIDTH + MARGIN))
                        row1 = int(self.player1_previous_y // (HEIGHT + MARGIN))

                        if row == row1 and column < column1:
                            self.left_slip(1,row,column,row1,column1)
                        elif row == row1 and column > column1:
                            self.right_slip(1,row,column,row1,column1)
                        elif row > row1 and column == column1:
                            self.upward_slip(1,row,column,row1,column1)
                        elif row < row1 and column == column1:
                            self.downward_slip(1,row,column,row1,column1)
            elif res == False:
                self.count = self.count + 1


    def left_slip(self,turn,row,column,row1,column1):
        msg = False
        if turn == 1:
            while self.grid[row][column] == 11:
                if column == 0:
                    msg = True
                    break

                column = column - 1 
            
            if msg is True:            
                img = "sprite1_splash.png"
                self.player1_sprite_splash = arcade.Sprite(img, 0.06)
                self.player1_sprite_splash.center_x = self.player1_previous_x
                self.player1_sprite_splash.center_y = self.player1_previous_y
                self.player_list.append(self.player1_sprite_splash)            
                self.grid[row1][column1] = 11
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row][column] = 1
                self.player1_sprite.center_x = x
                self.player1_sprite.center_y = y
                self.count = self.count + 1
            else:
                img = "sprite1_splash.png"
                self.player1_sprite_splash = arcade.Sprite(img, 0.06)
                self.player1_sprite_splash.center_x = self.player1_previous_x
                self.player1_sprite_splash.center_y = self.player1_previous_y
                self.player_list.append(self.player1_sprite_splash)    
                        
                self.grid[row1][column1] = 11
                x = (column+1) * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row][column+1] = 1
                self.player1_sprite.center_x = x
                self.player1_sprite.center_y = y
                self.count = self.count + 1

        elif turn == 2:
            while self.grid[row][column] == 22:
                if column == 0:
                    msg = True
                    break

                column = column - 1
            if msg is True:
                img = "sprite2_splash.png"
                self.player2_sprite_splash = arcade.Sprite(img, 0.06)
                self.player2_sprite_splash.center_x = self.player2_previous_x
                self.player2_sprite_splash.center_y = self.player2_previous_y
                self.player_list.append(self.player2_sprite_splash)            
                self.grid[row1][column1] = 22
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row][column] = 2
                self.player2_sprite.center_x = x
                self.player2_sprite.center_y = y
                self.count = self.count + 1

            else:

                img = "sprite2_splash.png"
                self.player2_sprite_splash = arcade.Sprite(img, 0.06)
                self.player2_sprite_splash.center_x = self.player2_previous_x
                self.player2_sprite_splash.center_y = self.player2_previous_y
                self.player_list.append(self.player2_sprite_splash)            
                self.grid[row1][column1] = 22
                x = (column+1) * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row][column+1] = 2
                self.player2_sprite.center_x = x
                self.player2_sprite.center_y = y
                self.count = self.count + 1



    def right_slip(self,turn,row,column,row1,column1):
        msg = False
        
        if turn == 1:
            while self.grid[row][column] == 11:
                if column == 9:
                    msg = True
                    break                           
                column = column + 1

        
            if msg is True:

                img = "sprite1_splash.png"
                self.player1_sprite_splash = arcade.Sprite(img, 0.06)
                self.player1_sprite_splash.center_x = self.player1_previous_x
                self.player1_sprite_splash.center_y = self.player1_previous_y
                self.player_list.append(self.player1_sprite_splash)            
                self.grid[row1][column1] = 11
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row][column] = 1
                self.player1_sprite.center_x = x
                self.player1_sprite.center_y = y
                self.count = self.count + 1
            else:
                img = "sprite1_splash.png"
                self.player1_sprite_splash = arcade.Sprite(img, 0.06)
                self.player1_sprite_splash.center_x = self.player1_previous_x
                self.player1_sprite_splash.center_y = self.player1_previous_y
                self.player_list.append(self.player1_sprite_splash)            
                self.grid[row1][column1] = 11
                x = (column-1) * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row][column-1] = 1
                self.player1_sprite.center_x = x
                self.player1_sprite.center_y = y 
                self.count = self.count + 1

        elif turn == 2:
            while self.grid[row][column] == 22:
                if column == 9:
                    msg = True
                    break                           
                column = column + 1
            if msg is True:
                img = "sprite2_splash.png"
                self.player2_sprite_splash = arcade.Sprite(img, 0.06)
                self.player2_sprite_splash.center_x = self.player2_previous_x
                self.player2_sprite_splash.center_y = self.player2_previous_y
                self.player_list.append(self.player2_sprite_splash)            
                self.grid[row1][column1] = 22
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row][column] = 2
                self.player2_sprite.center_x = x
                self.player2_sprite.center_y = y
                self.count = self.count + 1
            else:
                img = "sprite2_splash.png"
                self.player2_sprite_splash = arcade.Sprite(img, 0.06)
                self.player2_sprite_splash.center_x = self.player2_previous_x
                self.player2_sprite_splash.center_y = self.player2_previous_y
                self.player_list.append(self.player2_sprite_splash)            
                self.grid[row1][column1] = 22
                x = (column-1) * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row][column-1] = 2
                self.player2_sprite.center_x = x
                self.player2_sprite.center_y = y
                self.count = self.count + 1



    def upward_slip(self,turn,row,column,row1,column1):

        msg = False
        if turn == 1:
        
            while self.grid[row][column] == 11:
                if row == 9:
                    msg = True
                    break                           
                row = row + 1   

            if msg is True:
            
                img = "sprite1_splash.png"
                self.player1_sprite_splash = arcade.Sprite(img, 0.06)
                self.player1_sprite_splash.center_x = self.player1_previous_x
                self.player1_sprite_splash.center_y = self.player1_previous_y
                self.player_list.append(self.player1_sprite_splash)            
                self.grid[row1][column1] = 11
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row][column] = 1
                self.player1_sprite.center_x = x
                self.player1_sprite.center_y = y
                self.count = self.count + 1
            else:
                img = "sprite1_splash.png"
                self.player1_sprite_splash = arcade.Sprite(img, 0.06)
                self.player1_sprite_splash.center_x = self.player1_previous_x
                self.player1_sprite_splash.center_y = self.player1_previous_y
                self.player_list.append(self.player1_sprite_splash)            
                self.grid[row1][column1] = 11
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = (row-1) * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row-1][column] = 1
                self.player1_sprite.center_x = x
                self.player1_sprite.center_y = y
                self.count = self.count + 1

        elif turn == 2:
            while self.grid[row][column] == 22:
                if row == 9:
                    msg = True
                    break                      
                row = row + 1

            if msg is True:

                img = "sprite2_splash.png"
                self.player2_sprite_splash = arcade.Sprite(img, 0.06)
                self.player2_sprite_splash.center_x = self.player2_previous_x
                self.player2_sprite_splash.center_y = self.player2_previous_y
                self.player_list.append(self.player2_sprite_splash)            
                self.grid[row1][column1] = 22
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row][column] = 2
                self.player2_sprite.center_x = x
                self.player2_sprite.center_y = y
                self.count = self.count + 1
            else:
                img = "sprite2_splash.png"
                self.player2_sprite_splash = arcade.Sprite(img, 0.06)
                self.player2_sprite_splash.center_x = self.player2_previous_x
                self.player2_sprite_splash.center_y = self.player2_previous_y
                self.player_list.append(self.player2_sprite_splash)            
                self.grid[row1][column1] = 22
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = (row-1) * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row-1][column] = 2
                self.player2_sprite.center_x = x
                self.player2_sprite.center_y = y
                self.count = self.count + 1




    def downward_slip(self,turn,row,column,row1,column1):
        msg = False
        if turn == 1:
            while self.grid[row][column] == 11:
                if row == 0:
                    msg = True
                    break                            
                row = row - 1
            if msg is True: 

                img = "sprite1_splash.png"
                self.player1_sprite_splash = arcade.Sprite(img, 0.06)
                self.player1_sprite_splash.center_x = self.player1_previous_x
                self.player1_sprite_splash.center_y = self.player1_previous_y
                self.player_list.append(self.player1_sprite_splash)            
                self.grid[row1][column1] = 11
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row][column] = 1
                self.player1_sprite.center_x = x
                self.player1_sprite.center_y = y
                self.count = self.count + 1

            else:
                img = "sprite1_splash.png"
                self.player1_sprite_splash = arcade.Sprite(img, 0.06)
                self.player1_sprite_splash.center_x = self.player1_previous_x
                self.player1_sprite_splash.center_y = self.player1_previous_y
                self.player_list.append(self.player1_sprite_splash)            
                self.grid[row1][column1] = 11
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = (row + 1) * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row+1][column] = 1
                self.player1_sprite.center_x = x
                self.player1_sprite.center_y = y
                self.count = self.count + 1
        elif turn == 2:
            while self.grid[row][column] == 22:
                if row == 0:
                    msg = True
                    break                  
                row = row - 1 
            if msg is True:
        
                img = "sprite2_splash.png"
                self.player2_sprite_splash = arcade.Sprite(img, 0.06)
                self.player2_sprite_splash.center_x = self.player2_previous_x
                self.player2_sprite_splash.center_y = self.player2_previous_y
                self.player_list.append(self.player2_sprite_splash)            
                self.grid[row1][column1] = 22
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = row * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row][column] = 2
                self.player2_sprite.center_x = x
                self.player2_sprite.center_y = y
                self.count = self.count + 1
            else:
                img = "sprite2_splash.png"
                self.player2_sprite_splash = arcade.Sprite(img, 0.06)
                self.player2_sprite_splash.center_x = self.player2_previous_x
                self.player2_sprite_splash.center_y = self.player2_previous_y
                self.player_list.append(self.player2_sprite_splash)            
                self.grid[row1][column1] = 22
                x = column * (WIDTH + MARGIN) + (WIDTH / 2 + MARGIN)
                y = (row+1) * (HEIGHT + MARGIN) + (HEIGHT / 2 + MARGIN) + 4
                self.grid[row+1][column] = 2
                self.player2_sprite.center_x = x
                self.player2_sprite.center_y = y
                self.count = self.count + 1
    
        

    def on_mouse_press(self, x, y, button, modifiers):

        self.player1_previous_x = self.player1_sprite.center_x
        self.player1_previous_y = self.player1_sprite.center_y
        self.player2_previous_x = self.player2_sprite.center_x
        self.player2_previous_y = self.player2_sprite.center_y
        prev_scoreA = self.scoreA
        prev_scoreB = self.scoreB

        self.is_Legal_Move(x,y)

        self.check_state(prev_scoreA,prev_scoreB)

        bot_pos = self.current_position(self.grid, False)
        bot_pos = copy.deepcopy(bot_pos)
        legal_move, slipped_move = list(self.findBestMove())
      
        if slipped_move is False:            
            self.scoreB = self.scoreB + 1
            ress =  self.current_position(self.grid, False)

            self.grid[legal_move[0]][legal_move[1]] = 2
            self.grid[bot_pos[0]][bot_pos[1]] = 22

            
            self.bot_position = copy.deepcopy(legal_move)
            self.player2_sprite.center_x = (MARGIN + WIDTH) * (legal_move[1]) + MARGIN + WIDTH // 2
            self.player2_sprite.center_y = (MARGIN + HEIGHT) * (legal_move[0]) + MARGIN + HEIGHT // 2

            img = "sprite2_splash.png"
            self.player2_sprite_splash = arcade.Sprite(img, 0.06)
            self.player2_sprite_splash.center_x = (MARGIN + WIDTH) * (bot_pos[1]) + MARGIN + WIDTH // 2
            self.player2_sprite_splash.center_y = (MARGIN + WIDTH) * (bot_pos[0]) + MARGIN + WIDTH // 2
            self.player_list.append(self.player2_sprite_splash)   
            self.count = self.count + 1
        elif slipped_move is True:
            bot_pos = self.current_position(self.grid, False)
            if legal_move[0] == bot_pos[0] and legal_move[1] < bot_pos[1]:
                self.left_slip(2,legal_move[0],legal_move[1],bot_pos[0],bot_pos[1])
            elif legal_move[0] == bot_pos[0] and legal_move[1] > bot_pos[1]:
                self.right_slip(2,legal_move[0],legal_move[1],bot_pos[0],bot_pos[1])
            elif legal_move[0] > bot_pos[0] and legal_move[1] == bot_pos[1]:
                self.upward_slip(2,legal_move[0],legal_move[1],bot_pos[0],bot_pos[1])
            elif legal_move[0] < bot_pos[0] and legal_move[1] == bot_pos[1]:
                self.downward_slip(2,legal_move[0],legal_move[1],bot_pos[0],bot_pos[1])
                     
        print(self.grid[::-1])


    def current_position(self,board,human):
        if human:
            for x in range(len(board)):
                for y in range(len(board[x])):
                    if board[x][y] == 1:
                        return [x,y]
        else:
            for x in range(len(board)):
                for y in range(len(board[x])):
                    if board[x][y] == 2:
                        return [x,y]

    
    def check_state(self,prev_scoreA,prev_scoreB):

    # If any of the two players done with 50 scores first....Stoping Criteria 1

        if self.scoreA == 50 or self.scoreB == 50:
            self.result()


    # If there is no changing in state...Sprite gets stuck in slippery surface ....Stoping Criteria 2

        if self.scoreA == prev_scoreA and self.scoreB == prev_scoreB:
            self.counter1 = self.counter1 + 1
        
        if self.scoreA > prev_scoreA or self.scoreB > prev_scoreB:
            self.counter1 = 0

        if self.counter1 == 12:
            self.result()

    def result(self):

        if self.scoreA > self.scoreB:
            state = 1
            gameover = GameOverView(state,self.scoreA)
            self.window.show_view(gameover)
        elif self.scoreA < self.scoreB:
            state = 2
            gameover = GameOverView(state,self.scoreB)
            self.window.show_view(gameover)
        elif self.scoreA == self.scoreB:
            state = 0
            gameover = GameOverView(state,self.scoreA)
            self.window.show_view(gameover)


    def findBestMove(self):
        copied_board = copy.deepcopy(self.grid)
        best_value = -10000

        
        bot_pos = self.current_position(copied_board, False)

        best_move = copy.deepcopy(bot_pos)

        zero_boxes, slipped_boxes = self.legal_moves(bot_pos, copied_board, 0)
        bot_pos = copy.deepcopy(bot_pos)
        
        if len(zero_boxes) == 0:
            for x in slipped_boxes:
                if x[0] == bot_pos[0] and x[1] < bot_pos[1]:
                    result = self.left_slip_check(x[0], x[1])

                elif x[0] == bot_pos[0] and x[1] > bot_pos[1]:
                    result = self.right_slip_check(x[0], x[1])

                elif x[0] > bot_pos[0] and x[1] == bot_pos[1]:
                    result = self.upward_slip_check(x[0], x[1])

                elif x[0] < bot_pos[0] and x[1] == bot_pos[1]:
                    result = self.downward_slip_check(x[0], x[1])

                value = self.calculate_sorrounding_zeros(copied_board,result)
              
                if value > best_value:
                    best_value = value
                    best_move[0] = x[0]
                    best_move[1] = x[1]
            return best_move, True

        if len(zero_boxes) != 0:
            
            for x in zero_boxes:
                copied_board[x[0]][x[1]] = 2
                prev_mov = copy.deepcopy(x)
                copied_board[bot_pos[0]][bot_pos[1]] = 22
                bot_pos[0] = x[0]
                bot_pos[1] = x[1]
                
                # This BOT_POS will be used by MINIMAX and its subs
                value = self.minimax(copied_board,0,8,False)
                
                # Undo the move and restore the place

                copied_board[prev_mov[0]][prev_mov[1]] = 0
                copied_board[bot_pos[0]][bot_pos[1]] = 2
                bot_pos = copy.deepcopy(bot_pos)
                if value >= best_value :
                    best_value = value
                    best_move[0] = x[0]
                    best_move[1] = x[1]
        
        return best_move, False


    def evalboard(self,board):
        player_score = 0
        bot_score = 0
        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] == 0:
                    return 0
                elif board[row][col] == 1 or board[row][col] == 11 :
                    player_score += 1
                elif board[row][col] == 2 or board[row][col] == 22 :
                    bot_score += 1
        
        if bot_score == player_score:
            return 0
        elif bot_score > player_score:
            return 1
        elif player_score > bot_score:
            return -1

        
    def minimax(self, board, depth, max_depth, is_max):
        win = 1
        draw = 0
        lose = -1

        result = self.evalboard(board)

        if result == lose or result == win or result == draw or depth == 7:
            return result + self.heuristic(board)

        if isAgentTurn:
            best = -1000

            bot_pos = self.current_position(board, False)
            zero_boxes , slipped_boxes = self.legal_moves(self.BOT_POS, board, 0)
            if len(zero_boxes) != 0:
                for x in zero_boxes:       
                    board[x[0]][x[1]] = 2
                    board[bot_pos[0]][bot_pos[1]] = 22
                    bot_places.append(bot_pos)
                    bot_pos = copy.deepcopy(x)
                    best = max(best, self.minimax(board, depth+1, 8, False))
                    board[x[0]][x[1]] = 0
                    pos = list(bot_places.pop())
                    bot_pos = copy.deepcopy(pos)
                    board[pos[0]][pos[1]] = 2
            
            elif len(zero_boxes) == 0:
                temp = []
                for x in slipped_boxes:
                    if x[0] == player_pos[0] and x[1] < player_pos[1]:
                        result = self.left_slip_check(x[0], x[1])

                    elif x[0] == player_pos[0] and x[1] > player_pos[1]:
                        result = self.right_slip_check(x[0], x[1])

                    elif x[0] > player_pos[0] and x[1] == player_pos[1]:
                        result = self.upward_slip_check(x[0], x[1])

                    elif x[0] < player_pos[0] and x[1] == player_pos[1]:
                        result = self.downward_slip_check(x[0], x[1])
                    temp.append(bot_pos)
                    board[bot_pos[0]][bot_pos[1]] = 22
                    board[result[0]][result[1]] = 2
                    bot_pos[0] = result[0]
                    bot_pos[1] = result[1]
                    best = max(best,self.minimax(board, depth+1, 8, False))
                    board[result[0]][result[1]] = 22
                    pos = list(temp.pop())
                    bot_pos = copy.deepcopy(pos)
                    board[pos[0]][pos[1]] = 2
            return best

        else:
            best = 1000

            player_pos = self.current_position(board, True)
            zero_boxes , slipped_boxes = self.legal_moves(player_pos, board, 1)

            if len(zero_boxes) == 0:
                temp1 = []
                for x in slipped_boxes:
                    if x[0] == player_pos[0] and x[1] < player_pos[1]:
                        result = self.left_slip_check(x[0], x[1])

                    elif x[0] == player_pos[0] and x[1] > player_pos[1]:
                        result = self.right_slip_check(x[0], x[1])

                    elif x[0] > player_pos[0] and x[1] == player_pos[1]:
                        result = self.upward_slip_check(x[0], x[1])

                    elif x[0] < player_pos[0] and x[1] == player_pos[1]:
                        result = self.downward_slip_check(x[0], x[1])
                    temp1.append(player_pos)
                    board[player_pos[0]][player_pos[1]] = 11
                    board[result[0]][result[1]] = 1
                    player_pos[0] = result[0]
                    player_pos[1] = result[1]
                    best = min(best,self.minimax(board, depth+1, 7, True))
                    board[result[0]][result[1]] = 11
                    pos = list(temp1.pop())
                    player_pos = copy.deepcopy(pos)
                    board[pos[0]][pos[1]] = 1

            elif len(zero_boxes) != 0:
                for x in zero_boxes:
                    board[x[0]][x[1]] = 1
                    board[player_pos[0]][player_pos[1]] = 11
                    player_places.append(player_pos)
                    player_pos = copy.deepcopy(x)
                    best = min(best,self.minimax(board, depth+1, 8, True))
                    board[x[0]][x[1]] = 0
                    pos = list(player_places.pop())
                    player_pos = copy.deepcopy(pos)
                    board[pos[0]][pos[1]] = 1
            return best


    def heuristic(self,board):
        wining_chances = 0
        # 1st Condition
        for x in range(len(board)):
            for y in range(len(board[x])):
                if board[x][y] == 22 :
                    wining_chances += 1 

        # 2nd condition
        bot_pos = self.current_position(board, False)
        chance = self.calculate_sorrounding_zeros(board,bot_pos)        
        wining_chances += chance


        #3rd Condition       
        
        if bot_pos[0] in range(3,7) and bot_pos[1] in range(3,7):
            wining_chances += 10 


        # 4th condition
        player_pos = self.current_position(board, True)
        chance = 250
        
        dx = abs(player_pos[0] - bot_pos[0])
        dy = abs(player_pos[1] - bot_pos[1])
        import math
        result = int(math.sqrt((dx*dx)+ (dy*dx)))
     
        if result == 0:
            result = 1
            
        chance = int(chance / result)
        
        wining_chances += chance
        
              
        return wining_chances
    

    def legal_moves(self,location,board,turn):
       
       
        pos = copy.deepcopy(location)
        row , column = list(pos)

        temp = []        
      
        if (row > 0 and row < 9) and (column > 0 and column < 9):
            temp.append([row,column-1]) 
            temp.append([row,column+1])
            temp.append([row-1,column])
            temp.append([row+1,column])
        
        elif row == 0:
            if column == 0:
                temp.append([row+1,column])
                temp.append([row,column+1])
            elif column == 9:
                temp.append([row+1,column])
                temp.append([row,column-1])
            elif column > 0 and column < 9:
                temp.append([row,column+1])
                temp.append([row,column-1])
                temp.append([row+1,column])
        elif row == 9:
            if column == 0:
                temp.append([row-1,column])
                temp.append([row,column+1])
            elif column == 9:
                temp.append([row-1,column])
                temp.append([row,column-1])
            elif column > 0 and column < 9:
                temp.append([row,column+1])
                temp.append([row,column-1])
                temp.append([row-1,column])
        elif row < 9 and column == 9:
            temp.append([row,column-1])
            temp.append([row-1,column])
            temp.append([row+1,column])
        elif (row > 0 and row < 9) and column == 0:
            temp.append([row,column+1])
            temp.append([row-1,column])
            temp.append([row+1,column])
          
        legal = []
        slipped = []        
        for i in temp:
            if board[i[0]][i[1]] == 0: 
                legal.append(i)
            elif board[i[0]][i[1]] == 22:
                slipped.append(i)
        return legal,slipped


    def calculate_sorrounding_zeros(self,board,postion):
        x,y = postion
        chances = 0
        if x == 0:
            if y == 0:
                if board[x][y+1] == 0 or board[x+1][y] == 0:
                    for row in range(x, 4):
                        for col in range(y, 4):
                            if board[row][col] == 0:
                                chances += 1
            elif y == 9:
                if board[x][y-1] == 0 or board[x+1][y] == 0:
                    for row in range(x, 4):
                        for col in range(5, y):
                            if board[row][col] == 0:
                                chances += 1
            else:
                if board[x][y+1] == 0 or board[x+1][y] == 0 or board[x][y-1] == 0 :
                    for row in range(x, 4):
                        for col in range(y, 4):
                            if col > 9 :
                                break
                            if board[row][col] == 0:
                                chances += 1
                    for row in range(x, 4):
                        for col in range(y-4, y):
                            if col < 0  :
                                break
                            if board[row][col] == 0:
                                chances += 1
        elif x == 9:
            if y == 0:
                if board[x][y+1] == 0 or board[x-1][y] == 0:
                    for row in range(x-4, x):
                        for col in range(y, 4):
                            if board[row][col] == 0:
                                chances += 1
            elif y == 9:
                if board[x][y-1] == 0 or board[x-1][y] == 0:
                    for row in range(x-5, x):
                        for col in range(y-4, y):
                            if board[row][col] == 0:
                                chances += 1
            else:
                if board[x][y+1] == 0 or board[x-1][y] == 0 or board[x][y-1] == 0 :
                    for row in range(x-4, x):
                        for col in range(y, y+4):
                            if col > 9 :
                                break
                            if board[row][col] == 0:
                                chances += 1
                    for row in range(x-4, x):
                        for col in range(y-4, y):
                            if col < 0  :
                                break
                            if board[row][col] == 0:
                                chances += 1
        
        elif y == 0 and (x > 0 or x < 9):
            if board[x][y+1] == 0 or board[x+1][y] == 0 or board[x-1][y] == 0:
                for row in range(x-4, x):
                    for col in range(y, 5):
                        if row < 0 :
                            break
                        if board[row][col] == 0:
                            chances += 1
                for row in range(x, 4):
                    for col in range(y, 5):
                        if row > 9 :
                            break
                        if board[row][col] == 0:
                            chances += 1

        elif  y == 9 and (x > 0 or x < 9):
            if board[x][y-1] == 0 or board[x+1][y] == 0 or board[x-1][y] == 0:
                for row in range(x-4, x):
                    for col in range(5, y):
                        if row < 0 :
                            break
                        if board[row][col] == 0:
                            chances += 1
                for row in range(x, 4):
                    for col in range(5, y):
                        if row > 9 :
                            break
                        if board[row][col] == 0:
                            chances += 1
        else:
            if board[x][y+1] == 0 or board[x][y-1] == 0 or board[x+1][y] == 0 or board[x-1][y+1] == 0:
                for row in range(x, 4):
                    for col in range(y, 4):
                        if row > 9 or col > 9 :
                            break
                        if board[row][col] == 0:
                            chances += 1
                for row in range(x, 4):
                    for col in range(y-4, y):
                        if row > 9 or col < 0 :
                            break
                        if board[row][col] == 0:
                            chances += 1

                for row in range(x-4, x):
                    for col in range(y, 4):
                        if row < 0 or col > 9 :
                            break
                        if board[row][col] == 0:
                            chances += 1
                for row in range(x-4, x):
                    for col in range(y-4, y):
                        if row < 0 or col < 0 :
                            break
                        if board[row][col] == 0:
                            chances += 1    
        return chances


    def left_slip_check(self,row,column):
        msg = False
        
        while self.grid[row][column] == 22:
            if column == 0:
                msg = True
                break

            column = column - 1 
            
        if msg is True:            
            return [row,column]
            
            
        else:
            return [row,column+1]


    def right_slip_check(self,row,column):
        msg = False
        
        
        while self.grid[row][column] == 22:
            if column == 9:
                msg = True
                break                           
            column = column + 1

    
        if msg is True:

        
            return [row,column]
        
        else:
            return [row,column-1]

    def upward_slip_check(self, row, column):
        msg = False
        
        while self.grid[row][column] == 22:
            if row == 9:
                msg = True
                break                           
            row = row + 1   

        if msg is True:
        
            return [row,column]
        else:
            return [row-1,column]

                
    def downward_slip_check(self, row, column):
        msg = False
    
        while self.grid[row][column] == 22:
            if row == 0:
                msg = True
                break                            
            row = row - 1
        if msg is True: 

            return [row,column]

        else:
            return [row+1,column]



class GameOverView(arcade.View):
    

    def __init__(self,state,score):
       
        super().__init__()
        self.state = state
        self.score = score
        self.texture = arcade.load_texture("back3.png")

    def on_draw(self):
        
        arcade.start_render()
        if self.state == 1:
            message = "Congrats..Human Won"
        elif self.state == 2:
            message = "OOPS...BOT Won"
        elif self.state == 0:
            message = "Draw..!"

        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT)
        
        arcade.draw_text("Game Over", SCREEN_WIDTH/2, SCREEN_HEIGHT - 150, arcade.color.RED, font_size=70, anchor_x="center")

        if self.state == 0:
            arcade.draw_text(f"{message}", SCREEN_WIDTH/2, SCREEN_HEIGHT - 250, arcade.color.BLACK, font_size=50, anchor_x="center")
        else:
            arcade.draw_text(f"{message}", 650, 450, arcade.color.BLACK, font_size=50, anchor_x="center")
            arcade.draw_text(f"Scores: {self.score}", 650, 400, arcade.color.BLACK, font_size=30, anchor_x="center")
        arcade.draw_text(f"Click To Close the Screen", SCREEN_WIDTH/2, SCREEN_HEIGHT - 450, arcade.color.WHITE, font_size=30, anchor_x="center")
        snail = arcade.Sprite("game_over_snail.png")
        snail.scale = 0.4
        snail.center_x = 670
        snail.center_y = 165
        snail.draw()

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        arcade.close_window()
          

                
def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_view = MenuView()
    window.show_view(menu_view)
    arcade.run()

if __name__ == "__main__":
    main()