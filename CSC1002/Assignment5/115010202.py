# Revise the coding to add:
# (1) Clear the cell index text as they are only for your design stage.
# (2) Check if the snake bites itself. If it does, stop motion. Show 'Snake bites itself!' and the final length in
#  Label.
# (3) Check if the snake gets out of the boundary. If it does, stop motion. Show 'Snake gets out of the window!' and
#  the final length in Label.
# (4) In the current coding, there is possiblity that the food will be generated randomly onto the snake body. Revise
#  the coding to prevent from this.


import random
from tkinter import *

WINDOW_WIDTH = 15
WINDOW_HEIGHT = 10
CELL_WIDTH = 40
CELL_HEIGHT = 40
keep_on_moving = True
SNAKE_INITIAL_SEGMENT = [[WINDOW_HEIGHT // 2, WINDOW_WIDTH // 2]]
# The approximate center point as the snake initial position
directionArray = [[-1, 0], [0, 1], [1, 0], [0, -1]]


class Snake(object):
    def __init__(self, length=1, body_segment=SNAKE_INITIAL_SEGMENT, direction='N'):
        self.__length = length
        self.__body_segment = body_segment
        self.__direction = direction

    def get_length(self):
        return self.__length

    def get_body_segment(self):
        return self.__body_segment

    def get_direction(self):
        return self.__direction

    def set_direction(self, direction):
        self.__direction = direction

    def add_body_segment(self, additional_segment):
        self.__body_segment.insert(0, additional_segment)
        self.__length += 1

    def move(self):
        direction_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}[self.__direction]
        additional_segment = [self.__body_segment[0][0] + directionArray[direction_index][0],
                              self.__body_segment[0][1] + directionArray[direction_index][1]]
        # if additional_segment in self.__body_segment:
        global keep_on_moving
        if additional_segment[0] < 0 or additional_segment[0] > WINDOW_HEIGHT-1 or additional_segment[1] < 0 or \
           additional_segment[1] > WINDOW_WIDTH-1:
            print('Stop')
            labelText.configure(text='Snake gets out of the window! Final Length: %s ' % self.get_length())
            keep_on_moving = False
        elif additional_segment in self.__body_segment:
            print('Self overlay')
            keep_on_moving = False
            labelText.configure(text='Snake bites itself! Final Length: %s ' % self.get_length())
        else:
            self.__body_segment.insert(0, additional_segment)
            self.__body_segment.pop()


def draw_background():
    """
    Refresh the background to all yellow.
    """
    for i in range(WINDOW_HEIGHT):
        for j in range(WINDOW_WIDTH):
            labelArray[i][j].configure(bg='yellow')


def draw_snake():
    """
    Draw the snake in the background.
    """
    for segment in snake.get_body_segment():
        labelArray[segment[0]][segment[1]].configure(bg='brown')


def draw_food():
    """
    Draw the food
    """
    food_image = PhotoImage(file='apple.gif')
    labelArray[food[0]][food[1]].configure(image=food_image)
    labelArray[food[0]][food[1]].photo = food_image


def go_go_go():
    """
    Continously movement of the snake
    """
    global food
    if keep_on_moving:
        if is_food_in_way():
            snake.add_body_segment(food)
            labelText.configure(text='Snake Length: %s' % snake.get_length())
            labelArray[food[0]][food[1]].configure(image='')
            while True:
                food = [random.randint(1, WINDOW_HEIGHT - 2), random.randint(1, WINDOW_WIDTH - 2)]
                print(food.__repr__())
                if food not in snake.get_body_segment():
                    break
        snake.move()
        draw_background()
        draw_food()
        draw_snake()
        if keep_on_moving:  # Hint: this is related to question (2) and (3)
            root.after(200, go_go_go)


def is_food_in_way():
    """
    If food is in the next position ahead, return True. Otherwise, return False.
    """
    direction_index = {'N': 0, 'E': 1, 'S': 2, 'W': 3}[snake.get_direction()]
    body_segment = snake.get_body_segment()
    head = body_segment[0]
    next_head = [head[0] + directionArray[direction_index][0], head[1] + directionArray[direction_index][1]]
    if food == next_head:
        return True
    else:
        return False


snake = Snake()
food = [5, 10]  # Initial position of food
root = Tk()
root.title('Snake')
root.geometry('%sx%s+50+50' % (WINDOW_WIDTH * CELL_WIDTH, WINDOW_HEIGHT * CELL_HEIGHT + 40))
labelText = Label(root, text='Snake Length: %s' % snake.get_length(), font=('Times New Roman', 16))
labelText.place(x=0, y=0, width=CELL_WIDTH * WINDOW_WIDTH, height=CELL_HEIGHT)
labelArray = []
for i in range(WINDOW_HEIGHT):
    labelRow = []
    for j in range(WINDOW_WIDTH):
        # labelRow.append(Label(root, text='%s,%s' % (i, j), bg='yellow'))
        labelRow.append(Label(root, bg='yellow'))
        labelRow[j].place(x=j * CELL_WIDTH, y=i * CELL_HEIGHT + CELL_HEIGHT, width=CELL_WIDTH, height=CELL_HEIGHT)
    labelArray.append(labelRow[:])
draw_background()
draw_snake()
go_go_go()

root.bind("<KeyRelease-Up>", lambda x: snake.set_direction('N'))
root.bind("<KeyRelease-Down>", lambda x: snake.set_direction('S'))
root.bind("<KeyRelease-Left>", lambda x: snake.set_direction('W'))
root.bind("<KeyRelease-Right>", lambda x: snake.set_direction('E'))

root.mainloop()
