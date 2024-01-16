import math

def gather_line_distances(track_source, car_rotation, car_position_x, car_position_y, car_speed, car_wheel_rotation):

    # Set up the angles of detection lines
    lines = list((0, 45, 90, 135, 180, 225, 270, 315))

    output = list((0, 0, 0, 0, 0, 0, 0, 0))

    # If car is already on the grass, cancel the whole process
    if track_source.getpixel((car_position_x, car_position_y)) == (34, 177, 76):
        output = 'Null'

    if output != 'Null':
        
        for i in range(8):
            colour = ''
            pixel_distance = 1
            line_rotation = math.tan((lines[i]+car_rotation)/57.2958)
            print(line_rotation)

            while colour != 'found':
                point_x = car_position_x + pixel_distance
                if line_rotation != 0:
                    point_y = round(car_position_y + pixel_distance/line_rotation)
                else:
                    point_y = car_position_y

                if track_source.getpixel((point_x, point_y)) == (34, 177, 76):
                    colour = 'found'
                else:
                    pixel_distance += 1

            output[i] = round(((point_x - car_position_x)+(point_y-car_position_y)**1/2)/100, 2)

        for a in range(8):
            if output[a] > 1:
                output[a] = 1
        
        output.append(car_speed)
        output.append(car_wheel_rotation)

    return output