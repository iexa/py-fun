from typing import List
from random import randint
import time
import turtle



class Snake:
    WIDTH = HEIGHT = 600
    FONT_BASE = ("Courier", 20, "bold")
    __instance: 'Snake' = None


    def __init__(self):
        if Snake.__instance is not None:
            raise Exception("The Snake can only be started once.")
        else:
            Snake.__instance = self
            self.delay: float = 0.1
            self.score: int = 0
            self.high_score: int = 0
            self.scr = turtle.Screen()
            self.snake_head = turtle.Turtle()
            self.snake_dir = 'stop'
            self.snake_parts: List[turtle.Turtle] = []
            self.food = turtle.Turtle()
            self.pen = turtle.Turtle()  
            self.scr.title('Snake')
            self.scr.bgcolor('black')
            self.scr.setup(width=self.WIDTH, height=self.HEIGHT)
            self.scr.tracer(0)

            self.reset_game()
            self.game_loop()
            self.scr.mainloop()
            

    def reset_game(self):
        self.score = 0
        self.delay = 0.1
        self.snake_head.speed(0) # no anim whatsoever
        self.snake_head.shape('circle')
        self.snake_head.color('green')
        self.snake_head.penup()
        self.snake_head.goto(0, 0)
        self.snake_dir = 'stop'
        for part in self.snake_parts: # remove from screen
            part.goto(9999,9999)
        self.snake_parts.clear()

        self.food.speed(0)        
        self.food.shape('triangle')
        self.food.setheading(90)
        self.food.color('red')
        self.food.penup()
        self.food.goto(self.WIDTH // 4, self.HEIGHT // 4)

        self.pen.speed(0)
        self.pen.shape('square')
        self.pen.color('olive')
        self.pen.penup()     
        self.pen.hideturtle()
        self.pen.goto(0, self.HEIGHT // 2 - 2*20)
        self.write_score()

        self.scr.listen() # set focus
        self.scr.onkeypress(self.go_up, 'Up')
        self.scr.onkeypress(self.go_up, 'w')
        self.scr.onkeypress(self.go_down, 'Down')
        self.scr.onkeypress(self.go_down, 's')
        self.scr.onkeypress(self.go_left, 'Left')
        self.scr.onkeypress(self.go_left, 'a')
        self.scr.onkeypress(self.go_right, 'Right')
        self.scr.onkeypress(self.go_right, 'd')
        self.scr.onkeypress(self.scr.bye, 'Escape')


    def write_score(self):
        self.pen.clear()
        self.pen.write(f'Score: {self.score} - High score: {self.high_score}',
                        align='center', font=self.FONT_BASE)


    # go_* disable 180 degree turns
    def go_up(self):
        if self.snake_dir != 'down':
            self.snake_dir = 'up'
    def go_down(self):
        if self.snake_dir != 'up':
            self.snake_dir = 'down'
    def go_left(self):
        if self.snake_dir != 'right':
            self.snake_dir = 'left'
    def go_right(self):
        if self.snake_dir != 'left':
            self.snake_dir = 'right'


    def move(self):
        if self.snake_dir == 'up':
            self.snake_head.sety(self.snake_head.ycor() + 20 )
        if self.snake_dir == 'down':
            self.snake_head.sety(self.snake_head.ycor() - 20 )
        if self.snake_dir == 'left':
            self.snake_head.setx(self.snake_head.xcor() - 20 )
        if self.snake_dir == 'right':
            self.snake_head.setx(self.snake_head.xcor() + 20 )
        

    def game_loop(self):
        while True:
            self.scr.update()
            # check if out of bounds
            if self.snake_head.xcor() > self.WIDTH // 2 - 10 \
            or self.snake_head.xcor() < -(self.WIDTH // 2 - 10) \
            or self.snake_head.ycor() > self.HEIGHT // 2 - 10 \
            or self.snake_head.ycor() < -(self.HEIGHT // 2 - 10):
                time.sleep(1.5)
                self.reset_game()
            # picked up food
            if self.snake_head.distance(self.food) < 20:
                print(self.snake_head.distance(self.food))
                pos_x = self.WIDTH // 2 - 10
                pos_y = self.HEIGHT // 2 - 10
                self.food.goto(randint(-pos_x, pos_x), randint(-pos_y, pos_y))
                new_part = turtle.Turtle()
                new_part.speed(0)
                new_part.shape('circle')
                # TODO: change colors to be a gradient as added?
                new_part.color('darkgreen')
                new_part.penup()
                self.snake_parts += [new_part]
                if self.delay > 0:
                    self.delay -= 0.001
                self.score += 10
                if self.score > self.high_score:
                    self.high_score = self.score
                self.write_score()
            for idx in range(len(self.snake_parts)-1, 0, -1):
                self.snake_parts[idx].goto(
                    self.snake_parts[idx-1].xcor(), self.snake_parts[idx-1].ycor()
                )
            if len(self.snake_parts):
                self.snake_parts[0].goto(self.snake_head.xcor(), self.snake_head.ycor())
            self.move()
            for part in self.snake_parts:
                if part.distance(self.snake_head) < 20:
                    time.sleep(1.5)
                    self.reset_game()
            time.sleep(self.delay)


Snake()