import tkinter
from PIL import Image, ImageTk
import simulation_input as input
import neat
import ai
import car

# Setting up variables
start_coords = list((540, 666))

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
        self.Car = self.canvas.create_image(self.car_coords, image = self.car_img)

        # Start the simulation
        self.tick()

# Starting the execution process
root = tkinter.Tk()
app = CarAiApp(root)

# Loading the AI training
if __name__ == '__main__':
    config_path = 'examples/reinforcement learning/config-feedforward.txt'
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    # Adding the core evolution algorithm class
    p = neat.Population(config)

    # Add reporter for fancy statistical result
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    # Run NEAT
    p.run(ai.run_simulation, 1000)

# End of the canvas loop
root.mainloop()