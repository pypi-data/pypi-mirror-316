from typing import Union, Optional, Annotated
from io import BytesIO
from bs4 import BeautifulSoup

from exceptions import IncorrectCRSException


class Map:
    def __init__(
        self,
        center: Annotated[list, "Coordinates that define the Center of the map"] = [
            0,
            0,
        ],
        zoom: Annotated[int, "Define the initial zoom of the map"] = 10,
        base_layer: Annotated[
            Optional[str], "Base Layer to use in the map"
        ] = "http://mt0.google.com/vt/lyrs=y&hl=en&x={{x}}&y={{y}}&z={{z}}&s=Ga",
        attribution_control: Annotated[
            Optional[bool], "Define if the attribution control will be added to the map"
        ] = True,
        zoom_control: Annotated[
            Optional[bool], "Define if the zoom control will be added to the map"
        ] = True,
        double_click_zoom: Annotated[
            Optional[bool], "Define if the double click will do the zoom works"
        ] = True,
        dragging: Annotated[
            Optional[bool], "Define if the map is draggable or no"
        ] = True,
        scroll_wheel_zoom: Annotated[
            Optional[Union[bool, str]],
            "Define if the scroll wheel zoom is active or no. Possible values: True, False, 'center'(str)",
        ] = True,
        crs: Annotated[
            Optional[Union[str, int]],
            "Define the CRS used on the map. Possible values: 'Earth', '3395', '3857', '4326', 'Base', 'Simple'",
        ] = 3857,
    ):
        self.center = center
        self.zoom = zoom
        self.base_layer = base_layer
        self.attribution_control = "true" if attribution_control else "false"
        self.zoom_control = "true" if zoom_control else "false"
        self.double_click_zoom = "true" if double_click_zoom else "false"
        self.dragging = "true" if dragging else "false"
        self.validate_crs(crs)
        self.crs = f"L.CRS.EPSG{crs}"

        if type(scroll_wheel_zoom) == bool:
            self.scroll_whell_zoom = "true" if scroll_wheel_zoom else "false"
        else:
            self.scroll_whell_zoom = "scroll_wheel_zoom"

        self.map_content = self.get_map_content()

        pass

    def validate_crs(self, crs: Union[int, str]):
        available_crs = ["Earth", "3395", "3857", "4326", "Base", "Simple"]
        if not str(crs) in available_crs:
            self.crs
            raise IncorrectCRSException

    def get_map_content(self) -> str:
        html = f"""
            <!doctype html>
            <html lang="pt-br">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Weedit Map</title>
                    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin="" />
                    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
                    <script src="https://cdn.jsdelivr.net/npm/leaflet-textpath@1.2.3/leaflet.textpath.min.js"></script>
                    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet-side-by-side@2.2.0/layout.min.css">
                    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.1/css/all.min.css" integrity="sha512-5Hs3dF2AEPkpNAR7UiOHba+lRSJNeM2ECkwxUIxC1Q/FLycGTbNapWXB4tP889k5T5Ju8fs4b1P5z/iB4nMfSQ==" crossorigin="anonymous" referrerpolicy="no-referrer" />                <link rel="preconnect" href="https://fonts.googleapis.com">
                    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                    <link href="https://fonts.googleapis.com/css2?family=Lexend:wght@100..900&display=swap" rel="stylesheet">
                </head>
                <style>
                    #map {{ height: 100vh; }}
                </style>
                <body>
                    <div id="map"></div>
                </body>
                <script id="leaflet-script">
                    var map = L.map('map', {{
                        center: [{self.center[0]}, {self.center[1]}],
                        zoom: 13,
                        layers: []
                    }});
                    var baseLayer = L.tileLayer("http://mt0.google.com/vt/lyrs=y&hl=en&x={{x}}&y={{y}}&z={{z}}&s=Ga").addTo(map);
                </script>
            </html>
        """

        return html

    def to_html(
        self,
        file_path: Annotated[Union[str, None], "File path to save the html"] = None,
        bytes_file: Annotated[
            Union[str, None], "Bytes file to save the html content"
        ] = None,
    ) -> None:
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.map_content)

        else:
            html_soup = BeautifulSoup(self.map_content, "html.parser")
            bytes_file.write(html_soup.prettify().encode())
