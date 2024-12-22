import os
import requests
import json
import logging
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from typing import Optional, Dict


# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("BaseFetcher")


class BaseFetcher:
    """
    A base class for API interactions.
    """
    base_url = "https://api.encar.com"
    headers = {
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "en-ID,en;q=0.9,ru-ID;q=0.8,ru;q=0.7,id;q=0.6",
        "Connection": "keep-alive",
        "DNT": "1",
        "Origin": "http://www.encar.com",
        "Referer": "http://www.encar.com/",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"macOS"',
    }

    def __init__(self, output_dir: str):
        """
        Initializes the base fetcher.

        Args:
            output_dir (str): Directory for saving fetched data.
        """
        self.output_dir = output_dir
        self.session = self.create_session()
        self.create_output_directory()

    def create_output_directory(self):
        """Creates the output directory if it doesn't exist."""
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            logger.info(f"Output directory created: {self.output_dir}")

    def create_session(self) -> requests.Session:
        """
        Creates an HTTP session with retry settings.

        Returns:
            requests.Session: Configured HTTP session.
        """
        session = requests.Session()
        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("https://", adapter)
        return session

    def fetch_data(self, endpoint: str, params: dict) -> dict:
        """
        Performs a REST API request.

        Args:
            endpoint (str): API endpoint relative to the base URL.
            params (dict): Query parameters for the request.

        Returns:
            dict: JSON response data, or None if an error occurs.
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.info(f"Fetching data from {url} with params: {params}")
        try:
            response = self.session.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ Error fetching data from {url}: {e}")
            return None

    def save_data(self, data: dict, file_name: str):
        """
        Saves the data to a JSON file.

        Args:
            data (dict): Data to save.
            file_name (str): Output file name.
        """
        file_path = os.path.join(self.output_dir, file_name)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"✅ Data saved to {file_path}")
        except Exception as e:
            logger.error(f"❌ Error saving data to {file_path}: {e}")


class CarListingParser(BaseFetcher):
    """
    Class for parsing car listings from the API.
    """

    def __init__(self, output_dir="data/list", items_per_page=12):
        """
        Initializes the parser.

        Args:
            output_dir (str): Directory for saving data.
            items_per_page (int): Number of items per page.
        """
        super().__init__(output_dir)
        self.items_per_page = items_per_page

    def fetch_page(self, page_num: int) -> dict:
        """
        Fetches a single page of car listings.

        Args:
            page_num (int): The page number to fetch.

        Returns:
            dict: JSON response data.
        """
        start = page_num * self.items_per_page
        query = (
            "(And."
            "(And.Hidden.N._.CarType.Y.)_."
            "(Or.ServiceMark.EncarDiagnosisP0._.ServiceMark.EncarDiagnosisP1._.ServiceMark.EncarDiagnosisP2.)"
            ")"
        )
        params = {
            "count": "true",
            "q": query,
            "sr": f"|ExtendWarranty|{start}|{self.items_per_page}",
        }
        return self.fetch_data("search/car/list/general", params)

    def parse_pages(self, max_pages: int):
        """
        Fetches and saves multiple pages of car listings.

        Args:
            max_pages (int): Maximum number of pages to fetch.
        """
        for page_num in range(max_pages):
            data = self.fetch_page(page_num)
            if data:
                file_name = f"page_{page_num}.json"
                self.save_data(data, file_name)
            else:
                logger.error(f"❌ Stopping at page {page_num} due to error or no data.")
                break



class VehicleMainFetcher(BaseFetcher):
    """
    Class for fetching detailed vehicle data.
    """
    def __init__(self, input_dir: str, output_dir: str):
        """
        Initializes the vehicle data fetcher.

        Args:
            input_dir (str): Directory containing listing JSON files.
            output_dir (str): Directory to save vehicle data.
        """
        super().__init__(output_dir)
        self.input_dir = input_dir

    def fetch_vehicle_data(self, vehicle_id: str) -> Optional[Dict]:
        """
        Fetches detailed data for a specific vehicle ID.

        Args:
            vehicle_id (str): The ID of the vehicle to fetch.

        Returns:
            dict: Vehicle details or None if an error occurs.
        """
        endpoint = f"v1/readside/vehicle/{vehicle_id}"
        params = {
            "include": "ADVERTISEMENT,CATEGORY,CONDITION,CONTACT,MANAGE,OPTIONS,PHOTOS,SPEC,PARTNERSHIP,CENTER",
        }
        return self.fetch_data(endpoint, params)

    def save_data_in_vehicle_folder(self, vehicle_id: str, data: dict):
        """
        Saves the data in a folder named after the vehicle ID.

        Args:
            vehicle_id (str): The ID of the vehicle.
            data (dict): Data to be saved.
        """
        vehicle_folder = os.path.join(self.output_dir, str(vehicle_id))
        
        # Create a folder with vehicle ID if it doesn't exist
        if not os.path.exists(vehicle_folder):
            os.makedirs(vehicle_folder)
            logger.info(f"Created folder for vehicle ID {vehicle_id} at {vehicle_folder}")
        
        file_path = os.path.join(vehicle_folder, "main.json")  # Save as main.json
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            logger.info(f"Data for vehicle {vehicle_id} saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving data for vehicle {vehicle_id}: {e}")

    def process_file(self, file_path: str):
        """
        Processes a single listing file to fetch and save vehicle details.

        Args:
            file_path (str): Path to the JSON file containing vehicle listings.
        """
        logger.info(f"Processing file: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            vehicles = data.get("SearchResults", [])
            for vehicle in vehicles:
                vehicle_id = vehicle.get("Id")
                if vehicle_id:
                    vehicle_data = self.fetch_vehicle_data(vehicle_id)
                    if vehicle_data:
                        self.save_data_in_vehicle_folder(vehicle_id, vehicle_data)
                else:
                    logger.warning(f"Missing vehicle ID in file: {file_path}")
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")

    def process_all_files(self):
        """
        Processes all listing files in the input directory.
        """
        for root, _, files in os.walk(self.input_dir):
            for file in files:
                if file.endswith(".json"):
                    file_path = os.path.join(root, file)
                    self.process_file(file_path)


class VehicleDataFetcher(BaseFetcher):
    """
    Class for fetching vehicle data, including history, performance inspection, and diagnosis.
    """
    def __init__(self, output_dir: str):
        """
        Initializes the vehicle data fetcher.

        Args:
            output_dir (str): Directory to save vehicle data.
        """
        super().__init__(output_dir)

    def fetch_vehicle_history(self, vehicle_id: str, vehicle_no: str) -> Optional[Dict]:
        endpoint = f"v1/readside/record/vehicle/{vehicle_id}/open"
        params = {"vehicleNo": vehicle_no}
        return self.fetch_data(endpoint, params)

    def fetch_performance_inspection(self, vehicle_id: str) -> Optional[Dict]:
        endpoint = f"v1/readside/inspection/vehicle/{vehicle_id}"
        return self.fetch_data(endpoint, {})

    def fetch_diagnosis_data(self, vehicle_id: str) -> Optional[Dict]:
        endpoint = f"v1/readside/diagnosis/vehicle/{vehicle_id}"
        return self.fetch_data(endpoint, {})

    def fetch_clean_encar(self, vehicle_id: str) -> Optional[Dict]:
        endpoint = f"v1/readside/clean-encar/vehicle/{vehicle_id}"
        return self.fetch_data(endpoint, {})

    def fetch_vehicle_options(self, vehicle_id: str) -> Optional[Dict]:
        endpoint = f"v1/readside/vehicles/car/{vehicle_id}/options/choice"
        return self.fetch_data(endpoint, {})

    def fetch_extend_warranty(self, vehicle_id: str) -> Optional[Dict]:
        endpoint = f"v1/readside/extend-warrant/vehicle/{vehicle_id}"
        return self.fetch_data(endpoint, {})

    def fetch_vehicle_category(self, manufacturer_cd: str, model_cd: str) -> Optional[Dict]:
        """
        Fetches the vehicle category data using manufacturerCd and modelCd.

        Args:
            manufacturer_cd (str): The manufacturer code.
            model_cd (str): The model code.

        Returns:
            dict: Vehicle category data.
        """
        endpoint = f"v1/readside/vehicle/category?manufacturerCd={manufacturer_cd}&modelCd={model_cd}"
        return self.fetch_data(endpoint, {})

    def save_data_in_vehicle_folder(self, vehicle_id: str, data: dict, file_name: str):
        """
        Saves data into a folder named after the vehicle ID.

        Args:
            vehicle_id (str): The ID of the vehicle.
            data (dict): The data to be saved.
            file_name (str): The name of the file.
        """
        vehicle_folder = os.path.join(self.output_dir, str(vehicle_id))
        
        # Ensure the folder exists but do not overwrite any existing files
        if not os.path.exists(vehicle_folder):
            os.makedirs(vehicle_folder)
            logger.info(f"Created folder for vehicle ID {vehicle_id} at {vehicle_folder}")

        file_path = os.path.join(vehicle_folder, file_name)
        if not os.path.exists(file_path):  # Only save if the file doesn't exist
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                logger.info(f"{file_name} for vehicle {vehicle_id} saved to {file_path}")
            except Exception as e:
                logger.error(f"Error saving {file_name} for vehicle {vehicle_id}: {e}")
        else:
            logger.info(f"{file_name} for vehicle {vehicle_id} already exists, skipping fetch.")

    def process_vehicle_data(self, listing_id: str):
        """
        Process the vehicle data based on the listing ID, extracts the `vehicleId` and `vehicleNo` from the corresponding `main.json`,
        and fetches and saves history, inspection, diagnosis data, and vehicle category data.

        Args:
            listing_id (str): The listing ID to locate the `main.json` file.
        """
        vehicle_folder = os.path.join(self.output_dir, str(listing_id))

        # Check if the main.json file exists for the given listing_id
        main_file_path = os.path.join(vehicle_folder, "main.json")
        if not os.path.exists(main_file_path):
            logger.error(f"Main file for listing ID {listing_id} does not exist!")
            return

        # Load vehicleId, vehicleNo, manufacturerCd, and modelCd from main.json
        with open(main_file_path, "r", encoding="utf-8") as f:
            main_data = json.load(f)

        vehicle_id = main_data.get("vehicleId")
        vehicle_no = main_data.get("vehicleNo")
        manufacturer_cd = main_data.get("category", {}).get("manufacturerCd")
        model_cd = main_data.get("category", {}).get("modelCd")

        if not vehicle_id or not vehicle_no:
            logger.error(f"Invalid vehicle data in main.json for listing {listing_id}. Missing vehicleId or vehicleNo.")
            return

        if not manufacturer_cd or not model_cd:
            logger.error(f"Invalid vehicle data in main.json for listing {listing_id}. Missing manufacturerCd or modelCd.")
            return

        # Fetch data for vehicle history, inspection, diagnosis, and vehicle category
        history_data = self.fetch_vehicle_history(vehicle_id, vehicle_no)
        inspection_data = self.fetch_performance_inspection(vehicle_id)
        diagnosis_data = self.fetch_diagnosis_data(vehicle_id)
        clean_encar_data = self.fetch_clean_encar(vehicle_id)
        vehicle_options = self.fetch_vehicle_options(vehicle_id)
        extend_warranty_data = self.fetch_extend_warranty(vehicle_id)

        # Fetch vehicle category data using manufacturerCd and modelCd
        vehicle_category_data = self.fetch_vehicle_category(manufacturer_cd, model_cd)

        # Save data if it's fetched (not None)
        self.save_data_in_vehicle_folder(listing_id, history_data, "history.json")
        self.save_data_in_vehicle_folder(listing_id, inspection_data, "inspection.json")
        self.save_data_in_vehicle_folder(listing_id, diagnosis_data, "diagnosis.json")
        self.save_data_in_vehicle_folder(listing_id, clean_encar_data, "clean_encar.json")
        self.save_data_in_vehicle_folder(listing_id, vehicle_options, "vehicle_options.json")
        self.save_data_in_vehicle_folder(listing_id, extend_warranty_data, "extend_warranty.json")
        self.save_data_in_vehicle_folder(listing_id, vehicle_category_data, "vehicle_category.json")


if __name__ == "__main__":    

    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    dir_data_list = os.path.join(ROOT_DIR, "data/list")
    dir_data_vehicles = os.path.join(ROOT_DIR, "data/vehicles")

    parser = CarListingParser(output_dir=dir_data_list, items_per_page=5)
    parser.parse_pages(3)

    fetcher = VehicleMainFetcher(input_dir=dir_data_list, output_dir=dir_data_vehicles)
    fetcher.process_all_files()

    with open(os.path.join(dir_data_list, "page_0.json"), "r", encoding="utf-8") as f:
        data = json.load(f)

        for item in data.get("SearchResults", []):
            listing_id = item.get("Id")

            print(f"Processing vehicle data for listing ID: {listing_id}")
            vehicle_data_fetcher = VehicleDataFetcher(output_dir=dir_data_vehicles)
            vehicle_data_fetcher.process_vehicle_data(listing_id)

            break

    print("Vehicle data processing completed.")





