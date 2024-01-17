def gather_line_distances(track_source, car_rotation, car_position_x, car_position_y, car_speed, car_wheel_rotation):

    import math

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