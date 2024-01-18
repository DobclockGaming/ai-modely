import tkinter
from PIL import Image, ImageTk
import neat
import math
import os


global start_coords, car_coords
start_coords = list((540, 666))
car_coords = list((start_coords[0]-20, start_coords[1]))

class Car:
    def __init__(self):

        # Setting up the variables
        self.speed = 0
        self.wheel_rotation = 0
        self.rotation = 0
        self.distance = 0
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False

        # Variables to change the behaviour of the car
        self.speed_change = 0.25
        self.rotation_change = 0.0125
        self.max_wheel_rotation = 0.5

    def check_collision(self):
        self.keep_alive = True
        radars = self.gather_line_distances(Image.open('examples/reinforcement learning/assets/track.png').convert('RGB'), self.rotation, self.car_coords[0], self.car_coords[1], self.speed, self.wheel_rotation)
        if radars == 'Null':
            self.keep_alive = False

    def gather_line_distances(track_source, car_rotation, car_position_x, car_position_y, car_speed, car_wheel_rotation):

        # Set up the angles of detection lines
        lines = list((0, 45, 90, 135, 180, 225, 270, 315))

        output = list((0, 0, 0, 0, 0, 0, 0, 0))

        # If car is already on the grass, cancel the whole process
        if track_source.getpixel((car_position_x, car_position_y)) == (34, 177, 76):
            output = 'Null'

        # If car is on the road, compute the distances
        if output != 'Null':
            
            for i in range(8):
                pixel_distance = 1

                x = int(car_position_x + (math.cos(math.radians(360 - (car_rotation + lines[i])))) * pixel_distance)
                y = int(car_position_y + (math.sin(math.radians(360 - (car_rotation + lines[i])))) * pixel_distance)

                while not track_source.getpixel((x, y)) == (34, 177, 76) and pixel_distance <= 100:
                    pixel_distance += 1
                    x = int(car_position_x + (math.cos(math.radians(360 - (car_rotation + lines[i])))) * pixel_distance)
                    y = int(car_position_y + (math.sin(math.radians(360 - (car_rotation + lines[i])))) * pixel_distance)
                    
                # Feed the distances into the output list
                output[i] = (pixel_distance-1)/100

            # Appending speed and rotation for future ease
            output.append(car_speed)
            output.append(car_wheel_rotation)

        return output
    
    def update(self):

        # Algorithm to identify keystrokes and accordingly change the tire direction and speed of the car

        # Identifying the keystrokes of w and s and changing speed attribute
        if self.forward:
            speed += self.speed_change
        elif self.backward and speed > 0:
            speed -= self.speed_change*1.5
        elif self.backward and speed <= 0:
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
            if self.left:
                wheel_rotation += self.rotation_change
                speed -= self.speed_change                                                       # Just for making an award system easier
            elif self.right:
                wheel_rotation -= self.rotation_change
                speed -= self.speed_change                                                       # Just for making an award system easier
            elif wheel_rotation > 0:
                wheel_rotation -= self.rotation_change*2
            elif wheel_rotation < 0:
                wheel_rotation += self.rotation_change*2
            
        self.forward = False
        self.backward = False
        self.left = False
        self.right = False
        
        # Rounding the rotation to 0 during very small rotations
        if -self.rotation_change < wheel_rotation < self.rotation_change:
            wheel_rotation = 0
            
        if wheel_rotation > self.max_wheel_rotation:
            wheel_rotation = self.max_wheel_rotation
        elif wheel_rotation < -self.max_wheel_rotation:
            wheel_rotation = -self.max_wheel_rotation

        self.check_collision(self)

        self.distance += speed

        return None
    
    def draw(self):

        if self.speed != 0:
            rotation += self.wheel_rotation/2
        self.rotated_car_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/car.png').rotate(rotation*57.2958)) # Rotation is multiplied because of it being counted in radians
        self.car_coords[0] += math.cos(-rotation)*self.speed
        self.car_coords[1] += math.sin(-rotation)*self.speed
    
def run_simulation(genomes, config):

    # Loading the photo assets
    track_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/track.png'))
    start_lane_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/startLane.png'))
    car_img = ImageTk.PhotoImage(Image.open('examples/reinforcement learning/assets/car.png'))
       
    # Setting up the canvas
    Car.root = root
    Car.root.title('Autonomous Car Reinforcement Learning AI Demo')
    Car.root.wm_iconphoto(True, car_img)

    Car.canvas = tkinter.Canvas(height=720, width = 1080)
    Car.canvas.pack()

    # Loading the images
    Car.canvas.create_image((540, 360), image = track_img)
    Car.canvas.create_image(start_coords, image = start_lane_img)
    Car.Car = Car.canvas.create_image(car_coords, image = car_img)

    # Initialise NEAT
    nets = []
    cars = []

    for id in genomes:
        net = neat.nn.FeedForwardNetwork.create(id, config)
        nets.append(net)
        id.fitness = 0

    global generation
    generation += 1

    # Input my data and get result from network
    for index, car in enumerate(cars):
        output = nets[index].activate(car.get_data())
        i = output.index(max(output))
        if i == 0:
            car.forward = True
        elif i == 1:
            car.backward = True
        elif i == 2:
            car.left = True
        else:
            car.right = True

    # Update car and fitness
    remain_cars = 0
    for i, car in enumerate(cars):
        if car.get_alive():
            remain_cars += 1
            car.update(map)
            genomes[i][1].fitness += Car.distance

    # check
    if remain_cars == 0:
        os.Exit()

    # Drawing
    for car in cars:
        if car.keep_alive():
            car.draw(Car)

# Starting the execution process
root = tkinter.Tk()

if __name__ == "__main__":
    # Set configuration file
    config_path = "./config-feedforward.txt"
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Create core evolution algorithm class
    p = neat.Population(config)

    # Add reporter for fancy statistical result
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT
    p.run(run_simulation, 1000)

# End of the canvas loop
root.mainloop()