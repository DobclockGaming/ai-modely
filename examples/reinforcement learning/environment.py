import tkinter
from PIL import Image, ImageTk
import keyboard
import math
import simulation_input as input

# Setting up variables
start_coords = list((540, 666))
car_coords = list((start_coords[0]-20, start_coords[1]))
speed = 0
wheel_rotation = 0
rotation = 0
speed_change = 0.25
rotation_change = 0.0125
max_wheel_rotation = 0.5

class CarAiApp:

    def __init__(self, root):
        # Loading the photo assets
        self.track_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/track.png'))
        self.start_lane_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/startLane.png'))
        self.car_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/car.png'))
       
        # Setting up the canvas
        self.root = root
        self.root.title('Autonomous Car Reinforcement Learning AI Demo')
        self.root.wm_iconphoto(True, self.car_img)

        self.canvas = tkinter.Canvas(height=720, width = 1080)
        self.canvas.pack()

        # Loading the images
        self.canvas.create_image((540, 360), image = self.track_img)
        self.canvas.create_image(start_coords, image = self.start_lane_img)
        self.Car = self.canvas.create_image(car_coords, image = self.car_img)

        # Start the simulation
        self.tick()

    def tick(self):

        global start_coords, car_coords, speed, wheel_rotation, rotation, speed_change, max_wheel_rotation

        # Algorithm to identify keystrokes and accordingly change the tire direction and speed of the car

        # Identifying the keystrokes of w and s and changing speed attribute
        if keyboard.is_pressed('w'):
            speed += speed_change
        elif keyboard.is_pressed('s') and speed > 0:
            speed -= speed_change*1.5
        elif keyboard.is_pressed('s') and speed <= 0:
            speed -= speed_change/2
        elif speed > 0:
            speed -= speed_change/2
        elif speed < 0:
            speed += speed_change/2

        # Rounding the speed to 0 during very slow speeds
        if -speed_change/4 < speed < speed_change/4:
            speed = 0

        # Identifying the keystrokes of a and d and changinge the wheel_rotation attribute
        if speed != 0:
            if keyboard.is_pressed('a'):
                wheel_rotation += rotation_change
                speed -= speed_change                                                       # Just for making an award system easier
            elif keyboard.is_pressed('d'):
                wheel_rotation -= rotation_change
                speed -= speed_change                                                       # Just for making an award system easier
            elif wheel_rotation > 0:
                wheel_rotation -= rotation_change*2
            elif wheel_rotation < 0:
                wheel_rotation += rotation_change*2
        
        # Rounding the rotation to 0 during very small rotations
        if -rotation_change < wheel_rotation < rotation_change:
            wheel_rotation = 0
            
        if wheel_rotation > max_wheel_rotation:
            wheel_rotation = max_wheel_rotation
        elif wheel_rotation < -max_wheel_rotation:
            wheel_rotation = -max_wheel_rotation

        # Applying the calculated physics change to the car itself
        if speed != 0:
            rotation += wheel_rotation/2
        self.rotated_car_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/car.png').rotate(rotation*57.2958)) # Rotation is multiplied because of it being counted in radians
        car_coords[0] += math.cos(-rotation)*speed
        car_coords[1] += math.sin(-rotation)*speed
        self.canvas.delete(self.Car)
        self.Car = self.canvas.create_image(car_coords, image = self.rotated_car_img)

        print(input.gather_line_distances(Image.open('examples/reinforcement learning/assets/track.png').convert('RGB'), rotation, car_coords[0], car_coords[1], speed, wheel_rotation))

        self.root.after(3, self.tick)

# Starting the execution process and end of the canvas loop
root = tkinter.Tk()
app = CarAiApp(root)
root.mainloop()