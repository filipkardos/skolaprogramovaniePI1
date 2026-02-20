h = 800
w = 800

import colorsys as cs
import turtle as t

t.setup(1000, 1000)
#turtle.turtlesize(1)
t.width(1)
t.speed(0)
t.bgcolor("black")
for i in range(25):
    for j in range(15):
        t.color(cs.hsv_to_rgb(j/15, i/25, 1))
        t.right(90)
        t.circle(200 - i * 4, 90)
        t.left(90)
        t.circle(200 - i * 4, 90)
        t.right(180)
        t.circle(50, 24)
t.hideturtle()

t.done()