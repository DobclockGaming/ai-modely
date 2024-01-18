class Car:
    def __init__(self, start_coords):
        from PIL import Image, ImageTk

        self.car_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/car.png'))
        self.car_coords = list((start_coords[0]-20, start_coords[1]))
        self.speed = 0
        self.wheel_rotation = 0
        self.rotation = 0
        self.speed_change = 0.25
        self.rotation_change = 0.0125
        self.max_wheel_rotation = 0.5
        self.keep_alive = True
        self.distance = 0

    def tick(self):

        import keyboard
        from PIL import Image, ImageTk
        import math
        import simulation_input as input

        # Algorithm to identify keystrokes and accordingly change the tire direction and speed of the car

        # Identifying the keystrokes of w and s and changing speed attribute
        if keyboard.is_pressed('w'):
            speed += self.speed_change
        elif keyboard.is_pressed('s') and speed > 0:
            speed -= self.speed_change*1.5
        elif keyboard.is_pressed('s') and speed <= 0:
            speed -= self.speed_change/2
        elif speed > 0:
            speed -= self.speed_change/2
        elif speed < 0:
            speed += self.speed_change/2

        # Rounding the speed to 0 during very slow speeds
        if -self.speed_change/4 < speed < self.speed_change/4:
            speed = 0

        # Identifying the keystrokes of a and d and changinge the wheel_rotation attribute
        if speed != 0:
            if keyboard.is_pressed('a'):
                wheel_rotation += self.rotation_change
                speed -= self.speed_change                                                       # Just for making an award system easier
            elif keyboard.is_pressed('d'):
                wheel_rotation -= self.rotation_change
                speed -= self.speed_change                                                       # Just for making an award system easier
            elif wheel_rotation > 0:
                wheel_rotation -= self.rotation_change*2
            elif wheel_rotation < 0:
                wheel_rotation += self.rotation_change*2
        
        # Rounding the rotation to 0 during very small rotations
        if -self.rotation_change < wheel_rotation < self.rotation_change:
            wheel_rotation = 0
            
        if wheel_rotation > self.max_wheel_rotation:
            wheel_rotation = self.max_wheel_rotation
        elif wheel_rotation < -self.max_wheel_rotation:
            wheel_rotation = -self.max_wheel_rotation

        # Applying the calculated physics change to the car itself
        if speed != 0:
            rotation += wheel_rotation/2
        self.rotated_car_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/car.png').rotate(rotation*57.2958)) # Rotation is multiplied because of it being counted in radians
        self.car_coords[0] += math.cos(-rotation)*speed
        self.car_coords[1] += math.sin(-rotation)*speed
        self.canvas.delete(self.Car)
        self.Car = self.canvas.create_image(self.car_coords, image = self.rotated_car_img)

        radars = input.gather_line_distances(Image.open('examples/reinforcement learning/assets/track.png').convert('RGB'), rotation, self.car_coords[0], self.car_coords[1], speed, wheel_rotation)

        self.root.after(1, self.tick)