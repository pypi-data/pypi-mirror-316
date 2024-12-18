from typing import Annotated, Union, Optional
from bs4 import BeautifulSoup
import random
import string

from exceptions import MissingTileLayerException


class TileLayer:
    def __init__(
        self,
        tile_layer_url: Annotated[
            Union[str, None], "The tile url to add in the map"
        ] = None,
        min_zoom: Annotated[
            Optional[int], "Set the minimum zoom value to the tile layer"
        ] = 1,
        max_zoom: Annotated[
            Optional[int], "Set the maximum zoom value to the tile layer"
        ] = 10,
        pane: Annotated[
            Optional[str], "Set the pane that the layer will be added"
        ] = "overlayPane",
    ):
        if not tile_layer_url:
            raise MissingTileLayerException

        self.tile_layer = tile_layer_url
        self.min_zoom = min_zoom
        self.max_zoom = max_zoom
        self.pane = pane

    def add_to(self, map) -> None:
        html_soup = BeautifulSoup(map.map_content, "html.parser")

        script = html_soup.find("script", {"id": "leaflet-script"})
        old_script = script

        random_id = "".join(random.choices(string.ascii_letters + string.digits, k=12))
        javascript_var = f"var tile_layer_{random_id}"
        layer_code = f"""
            {javascript_var} = L.tileLayer("{self.tile_layer}").addTo(map);
        """

        old_script.extract()
        script.append(layer_code)
        html_soup.body.append(script)

        map.map_content = html_soup.prettify()
        self.var_name = javascript_var
