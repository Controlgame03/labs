import math
import matplotlib.pyplot as plt

def get_components(image, filename, position, start_pos, width, height):
    step = 0
    store_image = [[]]
    component_pos = 0
    for i in range(start_pos, len(image)):
        cur_height = len(store_image) - 1
        if position != step:
            image[i] = 0
        else:
            store_image[cur_height].append(image[i])
            component_pos = component_pos + 1
        if (component_pos == width and cur_height + 1 != height):
            store_image.append([])
            component_pos = 0
        step = (step + 1) % 3
    imageFile = open(filename, 'wb')
    imageFile.write(bytes(image))
    imageFile.close()

    return store_image

def get_r(image1, image2):
    mean1 = sum(sum(image1, [])) / (len(image1) * len(image1[0]))
    mean2 = sum(sum(image2, [])) / (len(image2) * len(image2[0]))
    cov = sum([(image1[i][j] - mean1) * (image2[i][j] - mean2) for i in range(len(image1)) for j in range(len(image1[0]))]) / (len(image2) * len(image2[0]))
    std1 = math.sqrt(sum([(image1[i][j] - mean1) ** 2 for i in range(len(image1)) for j in range(len(image1[0]))]) / (len(image2) * len(image2[0]) - 1))
    std2 = math.sqrt(sum([(image2[i][j] - mean2) ** 2 for i in range(len(image2)) for j in range(len(image2[0]))]) / (len(image2) * len(image2[0]) - 1))
    corr = cov / (std1 * std2)

    return corr

def get_r_auto(full_image, delta_x, delta_y):
    image1 = [[]]
    image2 = [[]]
    current_row = 0

    def correct_x(x):
        res = x
        if x < 0:
            res = 0
        elif x > len(full_image):
            res = len(full_image)
        return res

    def correct_y(y):
        res = y
        if y < 0:
            res = 0
        elif y > len(full_image[0]):
            res = len(full_image[0])
        return res

    first_start_row = correct_x(0 + delta_x)
    first_start_column = correct_y(0 + delta_y)
    first_end_row = correct_x(len(full_image) + delta_x)
    first_end_column = correct_y(len(full_image[0]) + delta_y)

    second_start_row = correct_x(0 - delta_x)
    second_start_column = correct_y(0 - delta_y)
    second_end_row = correct_x(len(full_image) - delta_x)
    second_end_column = correct_y(len(full_image[0]) - delta_y)


    for i in range(first_start_row, first_end_row):
        current_column = 0
        image1.insert(current_row, [])
        for j in range(first_start_column, first_end_column):
            image1[current_row].insert(current_column, full_image[i][j])
            current_column += 1
        current_row += 1
    if len(image1) > 0:
        image1.pop(len(image1) - 1)

    current_row = 0
    for i in range(second_start_row, second_end_row):
        current_column = 0
        image2.insert(current_row, [])
        for j in range(second_start_column, second_end_column):
            image2[current_row].insert(current_column, full_image[i][j])
            current_column += 1
        current_row += 1
    if len(image2) > 0:
        image2.pop(len(image2) - 1)


    return get_r(image1, image2)

def show_graphics(image, title):
    all_x = []
    max_check_points = 400
    all_x.insert(0,math.floor((-0.5) * max_check_points))

    for i in range(1, max_check_points):
        all_x.insert(i, i - (max_check_points / 2))
        all_x[i] = int(math.floor(all_x[i]))
    all_y = [-10, -5, 0, 5, 10]

    def auto_correlation(all_x, current_y):
        result = []
        for current_x in all_x:
            result.append(get_r_auto(image, current_x, current_y))
        return result

    plt.figure()
    for y in all_y:
        plt.title(title)
        plt.plot(all_x, auto_correlation(all_x, y), label='$y = %i$'%y)
        plt.legend()

    plt.show()

with open('kodim15.bmp', 'rb') as f:
    header = f.read(54)
    pixel_offset = int.from_bytes(header[10:14], byteorder='little')
    width = int.from_bytes(header[18:22], byteorder='little')
    height = int.from_bytes(header[22:26], byteorder='little')

    f.seek(0)
    full_image = bytearray(f.read())

    image_r = get_components(full_image.copy(), 'red.bmp', 2, pixel_offset, width, height)
    image_g = get_components(full_image.copy(), 'green.bmp', 1, pixel_offset, width, height)
    image_b = get_components(full_image.copy(), 'blue.bmp', 0, pixel_offset, width, height)

print(get_r(image_r, image_g))
print(get_r(image_r, image_b))
print(get_r(image_b, image_g))

show_graphics(image_r, "image_r")
show_graphics(image_b, "image_b")
show_graphics(image_g, "image_g")
