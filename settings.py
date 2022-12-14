class Settings():
    """Class to store settings for CatLive game"""
    
    def __init__(self):
        self.bg_color = (230, 230, 230)
        self.screen_width = 550
        self.screen_border_width = 50
        self.screen_height = 400
        self.screen_border_height = 100
        self.obst_color = (207, 200, 184)
        
        # The cat's features
        self.cat_speed = 1
        
        # Cat images
        self.cat_images = ['images/cat_0.png', 'images/cat_1.png',
            'images/cat_inverse_0.png', 'images/cat_inverse_1.png',
            'images/cat_sleep.png']
        self.cat_bed_image = ['images/cat_bed.png']
        self.ball_image = ['images/ball.png']
        
        # The borders settings
        self.border_color = (89, 89, 89)
        self.border_width = 100
        
        # Plate's features
        # Delay in fish providing
        self.fish_delay = 5
        # Acceptable range to be around the plate to still get the fish
        # (y axis)
        self.plate_images = ['images/fish_on_plate.png', 
                             'images/empty_plate.png']
        
        # Buttons
        self.images_of_button = ['images/mute.png',
                                 'images/un_mute.png']
        self.mb_pos = (10,60)
        
        # time to start random roaming if no user input
        self.afk_delay = 10
        
        # time to keep cat's random direction in seconds (when roaming)
        self.keep_random_direction_time = 10
        
        # Time for a ball to keep moving after kick
        self.kicked_time = 1