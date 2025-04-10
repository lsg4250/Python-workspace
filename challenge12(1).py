from random import *
import turtle, time

screen = turtle.Screen()
image1 = "lab도전문제/img/front.GIF"
image2 = "lab도전문제/img/back.GIF"
screen.addshape(image1)
screen.addshape(image2)

t1 = turtle.Turtle()
t1.speed(0)
coin = randrange(2)

flipping = True
current_side = "heads"
count = 0

t1.shape("lab도전문제/img/front.GIF")

answer = turtle.textinput("동전 던지기", "동전을 던지시겠습니까?(Yes/No)")

if answer == 'y' or answer == 'yes':
    while flipping:
        if current_side == "heads":
            t1.shape("lab도전문제/img/back.GIF")
            current_side = "tails"
        else:
            t1.shape("lab도전문제/img/front.GIF")
            current_side = "heads"
        
        screen.update()
        turtle.delay(50)
        count += 1

        if count >= 60:
            flipping = False

    t1.hideturtle()
    screen.update()
    t1.write("결과는?", align="center", font=("Arial", 48, "bold"))
    time.sleep(1)

    if coin == 0:
        t1.shape(image1)
        t1.clear()
        t1.stamp()
        t1.penup()
        t1.goto(0, -120)
        t1.write("앞", align="center", font=("Arial", 30, 'bold'))

    else:
        t1.shape(image2)
        t1.clear()
        t1.stamp()
        t1.penup()
        t1.goto(0, -120)
        t1.write("뒤", align="center", font=("Arial", 30, 'bold'))

    t1.goto(0,0)
    screen.update()

    time.sleep(3)
    t1.clear()
    screen.update()

t1.hideturtle()
screen.update()
t1.write("동전 던지기 프로그램을 종료합니다.", align='center', font=("Arial", 30, 'bold'))
time.sleep(1)
turtle.bye()
exit()
