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

class CarAiApp:

    def __init__(self, root):
        # Loading the photo assets
        icon = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/car.png'))
        track_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/track.png'))
        start_lane_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/startLane.png'))
        car_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/car.png'))
       
        # Setting up the canvas
        self.root = root
        self.root.title('Autonomous Car Reinforcement Learning AI Demo')
        self.root.wm_iconphoto(True, icon)

        self.canvas = tkinter.Canvas(height=720, width = 1080)
        self.canvas.pack()

        # Loading the images
        self.canvas.create_image((540, 360), image = track_img)
        self.canvas.create_image(start_coords, image = start_lane_img)
        self.Car = self.canvas.create_image(car_coords, image = car_img)

        # Start the simulation
        self.tick()

    def tick(self):

        # Algorithm to identify keystrokes and accordingly change the tire direction and speed of the car
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

        # Applying the calculated physics change to the car itself
        rotation += wheel_rotation/2
        move_x = math.sin(rotation)*speed
        move_y = math.cos(rotation)*speed
        self.canvas.move(self.Car, move_x, move_y)

        self.root.after(16, self.tick)

# Starting the execution process and end of the canvas loop
root = tkinter.Tk()
app = CarAiApp(root)
root.mainloop()