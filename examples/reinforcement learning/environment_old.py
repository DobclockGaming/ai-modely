import tkinter
from PIL import Image, ImageTk
import time
import keyboard
import math

# Setting up variables
start_coords = list((540, 666))
car_coords = list((start_coords[0]-20, start_coords[1]))
speed = 0
wheel_rotation = 0
rotation = 0
speed_change = 1
rotation_change = 0.25
max_wheel_rotation = 30

# Initialise drawing canvas
root = tkinter.Tk()
root.title('Autonomous Car Reinforcement Learning AI Demo')
icon = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/car.png'))
root.wm_iconphoto(True, icon)
canvas = tkinter.Canvas(height=720, width = 1080)

# Draw track and start line
track_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/track.png'))
canvas.create_image((540, 360), image = track_img)
start_lane_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/startLane.png'))
canvas.create_image(start_coords, image = start_lane_img)

# Draw the car
car_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/car.png'))
canvas.create_image(car_coords, image = car_img, tag = 'car')

canvas.pack()

# Main game timer (currently set to 60 FPS)
while True:
    time.sleep(1/60)

    # Simple physics for determining the speed of vehicle and rotation of wheels + their change after keystrokes
    try:
        if keyboard.is_pressed('w'):
            speed += speed_change
            print('Pressed W key')
        elif speed > 0: 
            speed -= speed_change/2
        elif speed < 0:
            speed += speed_change/2
        elif speed_change/2 > speed > 0:
            speed = 0
        elif 0 > speed > -speed_change/2:
            speed = 0

        if keyboard.is_pressed('s'):
            speed += 1.5*speed_change
            print('Pressed S key')
        elif speed > 0: 
            speed -= speed_change/2
        elif speed < 0:
            speed += speed_change/2
        elif speed_change/2 > speed > 0:
            speed = 0
        elif 0 > speed > -speed_change/2:
            speed = 0
        
        if keyboard.is_pressed('a'):
            wheel_rotation += rotation_change
            print('Pressed A key')
        elif keyboard.is_pressed('d'):
            wheel_rotation -= rotation_change
            print('Pressed D key')
        elif wheel_rotation > 0:
            wheel_rotation -= rotation_change/2
        elif wheel_rotation < 0:
            wheel_rotation += rotation_change/2
        elif rotation_change/2 > wheel_rotation > 0:
            wheel_rotation = 0
        elif 0 > wheel_rotation > -rotation_change/2:
            wheel_rotation = 0
        break

    except:

        if speed > 0: 
            speed -= speed_change/2
        elif speed < 0:
            speed += speed_change/2
        elif speed_change/2 > speed > 0:
            speed = 0
        elif 0 > speed > -speed_change/2:
            speed = 0

        if wheel_rotation > 0:
            wheel_rotation -= rotation_change/2
        elif wheel_rotation < 0:
            wheel_rotation += rotation_change/2
        elif rotation_change/2 > wheel_rotation > 0:
            wheel_rotation = 0
        elif 0 > wheel_rotation > -rotation_change/2:
            wheel_rotation = 0
            
    if wheel_rotation > max_wheel_rotation:
        wheel_rotation = max_wheel_rotation
    elif wheel_rotation < -max_wheel_rotation:
        wheel_rotation = -max_wheel_rotation

    # Determining the change of position with changed variables from the previous algorithm and changing the position of car
    rotation += wheel_rotation/2
    car_coords[0] += math.sin(rotation)*speed
    car_coords[1] += math.cos(rotation)*speed
    car_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/car.png'))
    canvas.create_image(car_coords, image = car_img, tag = 'car')
    canvas.update()
    

root.mainloop()