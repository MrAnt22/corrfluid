import requests
from .models import Game

def game_info():
    api_key = '9cd0cf3eff464ad1abf557ba6c3d7726'
    url = f"https://api.rawg.io/api/games?key={api_key}&page_size=40"
    response = requests.get(url)

    if response.status_code != 200:
        print("Main API request failed:", response.status_code)
        return

    data = response.json()

    for game_item in data.get("results", []):
        game_id = game_item["id"]
        game_name = game_item.get("name", "Unknown")

        detail_url = f"https://api.rawg.io/api/games/{game_id}?key={api_key}"
        screenshots_url = f"https://api.rawg.io/api/games/{game_id}/screenshots?key={api_key}"
        trailer_url = f"https://api.rawg.io/api/games/{game_id}/movies?key={api_key}"

        detail_response = requests.get(detail_url)
        screenshots_response = requests.get(screenshots_url)
        trailer_response = requests.get(trailer_url)

        if detail_response.status_code != 200 or trailer_response.status_code != 200:
            continue

        detail_data = detail_response.json()
        screenshots_data = screenshots_response.json()
        trailer_data = trailer_response.json()

        description = detail_data.get("description_raw", "")
        screenshots_list = screenshots_data.get("results", [])
        screenshot_image = screenshots_list[0].get("image", "") if screenshots_list else ""

        trailer_mp4_url = ""
        trailer_list = trailer_data.get("results", [])

        if trailer_list:
            first_trailer = trailer_list[0]
            trailer_mp4_url = first_trailer.get("data", {}).get("max", "")

        genres = [genre["name"] for genre in detail_data.get("genres", [])]
        developers = [dev["name"] for dev in detail_data.get("developers", [])]
        publishers = [pub["name"] for pub in detail_data.get("publishers", [])]

        Game.objects.create(
            name=game_name,
            image=game_item.get("background_image", ""),
            description=description,
            screenshots=screenshot_image,
            genres=", ".join(genres),
            developers=", ".join(developers),
            publishers=", ".join(publishers),
            trailer_url=trailer_mp4_url,
        )
        print("Trailer data:", trailer_list)