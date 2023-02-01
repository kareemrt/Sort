from exif import Image

class Picture:
    def __init__(self, Image):
        self.image = Image
        self.Latitude = 0
        self.Longitude = 0
        self.Date = 0
        self.Model = ""

    def set_traits(self):
        try: 
            self.Latitude = self.image.gps_latitude
            self.Longitude = self.image.gps_longitude
        except AttributeError: 
            print("The picture does not have GPS information")
            self.Latitude = 0
            self.Longitude = 0
        try: self.Date = self.image.datetime
        except AttributeError: 
            print("The picture does not have datetime information")
            self.Date = None
        try: self.Model = self.image.model
        except AttributeError: 
            print("The picture does not have model information")
            self.Model = None

    def get_coord(self):
        return "{}, {}".format(self.Latitude, self.Longitude)

    def __lt__(self, other):
        return self.datetime < other.datetime
    def __gt__(self, other):
        return self.datetime > other.datetime