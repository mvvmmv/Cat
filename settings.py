class Settings():
    """Class to store settings for CatLive game"""
    
    def __init__(self):
        self.bg_color = (230, 230, 230)
        self.screen_width = 700
        self.screen_height = 500
        self.obst_color = (207, 200, 184)
        
        # The cat's features
        self.cat_speed = 100
        self.meow_delay = 20
        # Cat images
        self.cat_images = ['images/cat_0.png', 'images/cat_1.png', \
            'images/cat_inverse_0.png', 'images/cat_inverse_1.png']
        # The borders settings
        self.border_color = (89, 89, 89)
        self.border_width = 100
        
        # Plate's features
        # Delay in fish providing
        self.fish_delay = 5
        # Acceptable range to be around the plate to still get the fish
        # (y axis)
        self.free_y = 15
        self.plate_images = ['images/fish_on_plate.png', 'images/empty_plate.png']