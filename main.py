import pygame
import timeit
import progressbar
from PIL import Image


class ImageRenderer():

    def __init__(self, width, height, color_command, save_file_as="image", save_file_to="", frames=1, frames_per_second=30) -> None:
        self.width = width
        self.height = height
        self.color_command = color_command
        self.save_file_as = save_file_as
        self.save_file_to = save_file_to
        self.frames = frames
        self.frames_per_second = frames_per_second
    
        self.bar = progressbar.ProgressBar(max_value=(frames if frames > 1 else height), widgets=[
                ' [',
                progressbar.Timer(format= 'elapsed time: %(elapsed)s'),
                '] ',
                progressbar.Bar('*'),' (',
                progressbar.ETA(), ') ',
            ]).start()
        
        self.images = []
    
    def generate(self):
        for frame in range(self.frames):
            if self.frames > 1:
                self.bar.update(frame)
            
            current_image = Image.new(mode="RGB", size=(self.width, self.height), color="black") 
            current_map = current_image.load()
            
            for y in range(self.height):
                if self.frames <= 1:
                    self.bar.update(self.height)
                for x in range(self.width):
                    color = self.color_command(x, y, frame)
                    current_map[x, y] = (int(255*color[0]), int(255*color[1]), int(255*color[2]))
        
            self.images.append(current_image)
    
        if self.frames > 1:
            self.images[0].save(self.save_file_to+self.save_file_as+".gif", save_all=True, append_images=self.images[1:], optimize=False, duration=1000/self.frames_per_second,loop=0)
        else:
            self.images[0].save(self.save_file_to+self.save_file_as+".png")


class PixelRenderer():

    def __init__(self, surface, width, height, color_command, pixel_size=1):
        self.surface = surface
        self.width = width
        self.height = height
        self.color_command = color_command
        
        self.pixel_rows = []
        for i in range(height):
            row = []
            for j in range(width):
                row.append(Pixel(surface, i, j, color_command, size=pixel_size))
            self.pixel_rows.append(row)


    def update(self, time=0):
        self.set_colors(time)
        self.draw()


    def set_colors(self, time=0):
        for row in self.pixel_rows:
            for pixel in row:
                pixel.set_color(time)


    def draw(self):
        for row in self.pixel_rows:
            for pixel in row:
                pixel.draw()


class Pixel():

    def __init__(self, surface, x, y, color_command, size=1):
        self.surface = surface
        self.x = x
        self.y = y
        self.color_command = color_command
        self.size = size

        self.color = (0, 0, 0)

    def set_color(self, time=0):
        color = self.color_command(self.x, self.y, time)
        color = [max(0, min(c, 1))*255 for c in color]
        self.color = color
        
    def draw(self):
        # print(self.color)
        pygame.draw.rect(self.surface, self.color, [self.x*self.size, self.y*self.size, self.size, self.size])
    

def color_test(x, y, time=0):
    # striped = 255*(x%2)
    # return (striped, striped, striped)

    if "grid_size" in globals():
        grid_size = globals()['grid_size']
    else:
        grid_size = 256

    checkered = (x%2)^(y%2)
    # return (255*checkered, 255*checkered, 255*checkered)
    return (x/(grid_size-1)*checkered, y/(grid_size-1)*checkered, time/31*checkered)

    # return (x, y, 0)


def get_time():
    setup="from main import color_test"
    code = lambda: {color_test(1, 1)}

    time = timeit.timeit(code, setup=setup, number=26215)*10
    return time


def start():
    # renderer = PixelRenderer(window, grid_size, grid_size, color_test, pixel_size=512//grid_size)
    renderer = ImageRenderer(grid_size, grid_size, color_test, save_file_as='checkered', save_file_to='gif_outputs/', frames=32, frames_per_second=15)

    # print("start")
    # start_time = time.time()
    renderer.generate()
    # end_time = time.time()
    # process_time = end_time - start_time
    # print(f"finished in {process_time}s\tfps of {1/process_time:.4f}")

    # print(get_time())


# def update():
#     check_events()
    # pygame.display.update()

if __name__ == '__main__':
    grid_size = 256
    start()


# def check_events():
#     global run

#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             run = False


# if __name__ == '__main__':
#     window = pygame.display.set_mode((1000, 800), pygame.RESIZABLE)
#     clock = pygame.time.Clock()
    
#     pygame.init()
#     pygame.display.set_caption("Pixel Simulation")

#     grid_size = 256

#     start()
#     # main loop
#     run = True
#     while run:
#         clock.tick(30)
#         update()

#     pygame.quit()
