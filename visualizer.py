import turtle
window = turtle.Screen()

turt = turtle.pen(fillcolor="black", pencolor="red", pensize=10)

#turtle.right(50)



def createBox(x, y):
    turtle.setx(x)
    turtle.sety(y)
    if(turtle.isdown != True):
        turtle.pendown()
    for i in range(4):
        turtle.setheading(i*90)
        turtle.forward()

turtle.exitonclick()
