import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
SCREEN_TITLE = 'WWDW'
GRAVITY = 3
JUMP = 50
CEILING = SCREEN_HEIGHT - 50
FLOOR = 20
CACTUS_SPEED = 0
CLOUD_SPEED = 2


class Dinocowboy(arcade.Sprite):
    pose = 0
    dino_time = 0

    def jump(self):
        if self.bottom == FLOOR:
            self.change_y = JUMP

    def multijump(self):
        self.change_y = JUMP

    def cowpoke(self, delta_time):
        self.center_y += self.change_y
        self.change_y -= GRAVITY

        self.dino_time += delta_time
        if self.dino_time > 0.1:

            self.pose += 1
            if self.pose == 3:
                self.pose = 0
            self.set_texture(self.pose)
            self.dino_time = 0

        if self.bottom < FLOOR:
            self.bottom = FLOOR

        if self.top > CEILING:
            self.top = CEILING


class Cactus(arcade.Sprite):
    def move(self):
        self.center_x -= CACTUS_SPEED
        if self.right < 0:
            self.left = SCREEN_WIDTH
            window.score += 1


class Cloud(arcade.Sprite):
    def move(self):
        self.center_x -= CLOUD_SPEED
        if self.right < 0:
            self.left = SCREEN_WIDTH


class Game(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        self.Cmod = False
        self.stategame = True
        self.dinocowboy = Dinocowboy("images/dino1.png")
        self.dinocowboy.append_texture(arcade.load_texture("images/dino2.png"))
        self.dinocowboy.append_texture(arcade.load_texture("images/dino3.png"))
        self.bg = arcade.load_texture("images/bg.png")
        self.bg2 = arcade.load_texture("images/game_over.png")
        self.dinocowboy.center_x = SCREEN_WIDTH / 2
        self.dinocowboy.bottom = FLOOR
        self.cactus = Cactus("images/cactus2.png")
        self.cactus.bottom = FLOOR
        self.cactus.center_x = SCREEN_WIDTH
        self.cloud = Cloud("images/cloud.png")
        self.cloud.top = SCREEN_HEIGHT
        self.cloud.center_x = SCREEN_WIDTH
        self.score = 0
        self.game_time = 0

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            if self.Cmod == True:
                self.dinocowboy.multijump()
            else:
                self.dinocowboy.jump()
        if symbol == arcade.key.C:
            self.Cmod = True
            print("Cmod enabled")
        if symbol == arcade.key.V:
            self.Cmod = False
            print("Cmod disabled")

    def on_key_release(self, symbol: int, modifiers: int):  # отпускание клавиш
        pass

    def on_draw(self):
        self.clear()
        if self.stategame == False:
            arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg2)
            return
        arcade.draw_texture_rectangle(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT, self.bg)
        self.cactus.draw()
        self.cloud.draw()
        self.dinocowboy.draw()
        arcade.draw_text(f"SCORE {self.score}", 200, 600)
        arcade.draw_text(f"TIME {self.game_time}", 200, 550)

    def update(self, delta_time: float):
        self.game_time = self.game_time + delta_time
        self.dinocowboy.cowpoke(delta_time)
        self.cactus.move()
        self.cloud.move()
        if arcade.check_for_collision(self.dinocowboy, self.cactus):
            self.stategame = False


window = Game(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
arcade.run()
