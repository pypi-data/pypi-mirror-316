class IncorrectCRSException(Exception):
    def __init__(self, crs_value: str):
        self.type = "IncorrectCRSException"
        self.message = f"The value {crs_value} is invalid to map CRS"
        super().__init__(self.type, self.message)


class MissingTileLayerException(Exception):
    def __init__(self):
        self.type = "MissingTileLayerException"
        self.message = f"You need to pass a tile url to create a tile layer"
        super().__init__(self.type, self.message)
