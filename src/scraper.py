from bs4 import BeautifulSoup
import requests
from datetime import datetime
from db import WellRepository

class WellPageScraper:
    """
    Class to scrape well page of a given API number.
    """
    def __init__(self, api: str):
        self.api = api.strip()
        self._base_span_id = "ctl00_ctl00__main_main_ucGeneralWellInformation_"
        self._url = f"https://wwwapps.emnrd.nm.gov/OCD/OCDPermitting/Data/WellDetails.aspx?api={self.api}"
        self._soup = BeautifulSoup(self._get_src(), "html.parser")

    def _get_src(self) -> bytes:
        response = requests.get(self._url)
        if response.status_code == 200:
            return response.content
        
        raise Exception(f"Failed to get page source for API: {self.api}/n{response.text}")
    
    @staticmethod
    def _parse_bool(value: str) -> bool:
        """
        Helper method to parse boolean values from string.
        """
        if value:
            return value.lower() in ["yes", "true"]
        return None

    @staticmethod
    def _format_date(date: str) -> str:
        """
        Helper method to format the date string from MM/DD/YYYY to YYYY-MM-DD for SQLite storage.
        """
        if date:
            return datetime.strptime(date, "%m/%d/%Y").strftime("%Y-%m-%d")
        return None

    def _get_span(self, key: str, dtype=str):
        """
        Return the text of the span tag with the given `key` as the HTML tag's `id`
        prefixed with `self._base_span_id`.
        """
        try:
            value = self._soup.find("span", id=self._base_span_id + key).text
            if dtype == bool:
                return self._parse_bool(value)
            elif dtype == datetime:
                return self._format_date(value)

            return dtype(value) if value else None
        except AttributeError:
            return None
    
    def _get_surface_location(self) -> str:
        """
        Helper function to return concatenated surface location.
        """
        location = [
            self._get_span("Location_lblLocation"), 
            self._get_span("Location_lblLot"),
            self._get_span("Location_lblFootageNSH"),
            self._get_span("Location_lblFootageEW")
        ]

        return " ".join([x.strip() for x in location if x])

    def _get_coords(self) -> dict:
        coords = {
            "Latitude": None,
            "Longitude": None,
            "CRS": None
        }

        # coords_str is of the form "35.1234,-104.1234 NAD83"
        coords_str = self._get_span("Location_lblCoordinates")
        if coords_str:
            # CRS is the last value in the string after the " "
            coords["CRS"] = coords_str.split(" ")[-1] if len(coords_str.split(" ")) > 1 else None

            # Latitude and Longitude are the first two values in the string before the CRS
            coords["Latitude"], coords["Longitude"] = [float(x) for x in coords_str.split(" ")[0].split(",")]

        return coords
        
    def run(self) -> dict:
        """
        Run the scraper and return the parsed model as a dictionary.
        """
        model = {
            "API":                          self.api,
            "Operator":                     self._get_span("lblOperator"),
            "Status":                       self._get_span("lblStatus"),
            "Well Type":                    self._get_span("lblWellType"),
            "Work Type":                    self._get_span("lblWorkType"),
            "Directional Status":           self._get_span("lblDirectionalStatus"),
            "Multi-Lateral":                self._get_span("lblMultiLateral", bool),
            "Mineral Owner":                self._get_span("lblMineralOwner"),
            "Surface Owner":                self._get_span("lblSurfaceOwner"),
            "GL Elevation":                 self._get_span("lblGLElevation", float),
            "KB Elevation":                 self._get_span("lblKBElevation", float),
            "DF Elevation":                 self._get_span("lblDFElevation", float),
            "Single/Multiple Completion":   self._get_span("lblCompletions"),
            "Potash Waiver":                self._get_span("lblPotashWaiver", bool),
            "Spud Date":                    self._get_span("lblSpudDate", datetime),
            "Last Inspection":              self._get_span("lblLastInspectionDate", datetime),
            "TVD":                          self._get_span("lblTrueVerticalDepth", float),
            "Surface Location":             self._get_surface_location(),
        }

        coords = self._get_coords()
        model.update(coords)

        return model

def main():
    repo = WellRepository()
    with open("apis_pythondev_test.csv", "r") as f:
        apis = f.read().split("\n")[1:]  # skip header

    # network bound operation - would benefit from multi threading
    for api in apis:
        try:
            if api.strip() == "":
                continue

            scraper = WellPageScraper(api)
            
            # scrape the model from the page and insert into db
            model = scraper.run()
            repo.insert(model)

            print(f"{api} inserted successfully!")

        except Exception as e:
            print(f"Failed to ingest {api} - {e}")

if __name__ == '__main__':
    main()
