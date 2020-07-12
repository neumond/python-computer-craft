from cc import is_turtle, turtle

if not is_turtle():
    print('Turtle required!')
    exit()

for _ in range(4):
    turtle.forward()
    turtle.turnLeft()
