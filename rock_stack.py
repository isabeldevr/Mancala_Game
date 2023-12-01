import os
import random
from PIL import Image, ImageDraw, ImageFont

class RockStack:
    def __init__(self):
        self.rocks_path = "img\\rocks"
        self.rock_components_path = self.rocks_path + "\\base"
        self.canvas_width = 110
        self.canvas_height = 110
        self.rocks_file_list = []
        for filename in os.listdir(self.rock_components_path):
            if os.path.isfile(os.path.join(self.rock_components_path, filename)):
                self.rocks_file_list.append(f"{self.rock_components_path}\\{filename}")
        pass

    def stack_number_on_image(self, image, number):
        image = image.convert('RGBA')
        draw = ImageDraw.Draw(image)

        font = ImageFont.load_default()
        text_position = (self.canvas_height/2, self.canvas_width/2)
        text_color = (255, 255, 255, 255)  # White
        draw.text(text_position, str(number), font=font, fill=text_color)
        return image


    def scale_image(self, image, scale_factor):
        new_width = int(image.width * scale_factor)
        new_height = int(image.height * scale_factor)
        return image.resize((new_width, new_height))

    def stack_images(self, amount: int, row: int, col: int) -> str:
        final_image = Image.new('RGBA', (self.canvas_height, self.canvas_width), (0, 0, 0, 0))

        for _ in range(amount):
            selected_image_filename = random.choice(self.rocks_file_list)
            selected_image = Image.open(selected_image_filename).convert('RGBA')

            rotation_angle = random.randint(0, 360)
            selected_image = selected_image.rotate(rotation_angle)
            scale_factor = float("{0:.2f}".format(random.uniform(0.80, 1.10)))
            selected_image = self.scale_image(selected_image, scale_factor)

            if final_image is None:
                final_image = selected_image
            else:
                final_image.paste(selected_image, (0, 0), selected_image)

        final_image = self.stack_number_on_image(final_image, amount)
        final_image.save(f'{self.rocks_path}\\stacked_rocks_{col}_{row}.png')
        return f'rocks\\stacked_rocks_{col}_{row}.png'

# Example usage
if __name__ == '__main__':
    rockStack = RockStack()
    # rockStack.stack_images(random.randint(1, 5), 0, 0)
    rockStack.stack_images(0, 0, 0)