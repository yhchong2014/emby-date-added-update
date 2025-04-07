import json
import threading
import os
from datetime import datetime
from typing import Optional, List, Dict
import requests

lock = threading.Lock()
DEFAULT_HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; GitHubActions; +https://github.com/)"}

class EmbyDateUpdater:
    def __init__(self, emby_host: str, emby_api_key: str, emby_user_id: str):
        self.emby_host = emby_host.rstrip('/') + '/'
        self.emby_host = self.emby_host if self.emby_host.startswith("http") else "http://" + self.emby_host
        self.api_key = emby_api_key
        self.user_id = emby_user_id
        self.processed_items = set()
        self.correct_count = 0
        self.stop_processing = False

    def update_date_added_for_libraries(self, library_ids: List[str]):
        if not library_ids:
            print("No library IDs configured.")
            return
        
        for library_id in library_ids:
            self.stop_processing = False
            self.correct_count = 0
            self.processed_items.clear()
            print(f"Processing library: {library_id}")
            self.update_date_added(library_id)
            print(f"Completed processing library: {library_id}\n")

    def update_date_added(self, library_id: str):
        items = self.get_library_items(library_id)
        if not items:
            print(f"No items found in library {library_id}.")
            return
        
        for item in items:
            if self.stop_processing:
                break
            self.process_item(item)

    def process_item(self, item: Dict):
        item_id, item_name, item_type = item.get("Id"), item.get("Name"), item.get("Type")
        if item_id in self.processed_items or item_type not in ["Movie", "Series", "Season", "Episode"]:
            return
        self.processed_items.add(item_id)
        self.update_media_date_added(item_id, item_name, item_type)

    def update_media_date_added(self, item_id: str, item_name: str, item_type: str):
        item_info = self.get_item_info(item_id)
        if not item_info:
            print(f"Failed to fetch details for {item_name}.")
            return

        premiere_date, date_created = item_info.get("PremiereDate"), item_info.get("DateCreated")
        if not premiere_date or not date_created:
            print(f"Skipping {item_name}, missing necessary date fields.")
            return
        
        if self.are_dates_equal(date_created, premiere_date):
            print(f"{item_name}: 'Date Added' already matches release date.")
            with lock:
                self.correct_count += 1
                if self.correct_count >= 10:
                    self.stop_processing = True
            return
        
        release_date = self.parse_date(premiere_date)
        if not release_date:
            print(f"Invalid release date format for {item_name}: {premiere_date}")
            return
        
        item_info["DateCreated"] = release_date.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
        if self.update_item_info(item_id, item_info):
            print(f"Updated {item_type} '{item_name}' 'Date Added' to {release_date}")
        else:
            print(f"Failed to update {item_type} '{item_name}' 'Date Added'")

    def get_library_items(self, library_id: str) -> List[Dict]:
        url = f"{self.emby_host}emby/Users/{self.user_id}/Items?ParentId={library_id}&Recursive=true&SortBy=DateCreated&SortOrder=Descending&IncludeItemTypes=Movie,Series,Season,Episode&api_key={self.api_key}"
        return requests.get(url, headers=DEFAULT_HEADERS).json().get("Items", [])

    def are_dates_equal(self, date_created: str, premiere_date: str) -> bool:
        try:
            return self.parse_date(date_created) == self.parse_date(premiere_date)
        except ValueError:
            return False

    def parse_date(self, date_str: str) -> Optional[datetime]:
        for fmt in ["%Y-%m-%dT%H:%M:%S.%f0Z", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]:
            try:
                return datetime.strptime(date_str, fmt)
            except ValueError:
                continue
        return None

    def get_item_info(self, item_id: str) -> Optional[Dict]:
        url = f"{self.emby_host}emby/Users/{self.user_id}/Items/{item_id}?api_key={self.api_key}"
        response = requests.get(url, headers=DEFAULT_HEADERS)
        return response.json() if response.status_code == 200 else None

    def update_item_info(self, item_id: str, data: Dict) -> bool:
        url = f"{self.emby_host}emby/Items/{item_id}?api_key={self.api_key}"
        response = requests.post(url, headers={"Content-Type": "application/json", **DEFAULT_HEADERS}, data=json.dumps(data))
        return response.status_code == 204

if __name__ == "__main__":
    emby_updater = EmbyDateUpdater(os.getenv("EMBY_HOST"), os.getenv("EMBY_API_KEY"), os.getenv("EMBY_USER_ID"))
    emby_updater.update_date_added_for_libraries(["1325", "2648", "5455", "13586", "2178", "2780", "17332", "17707", "19741", "17709", "20932", "20934", "20930", "20936"])
