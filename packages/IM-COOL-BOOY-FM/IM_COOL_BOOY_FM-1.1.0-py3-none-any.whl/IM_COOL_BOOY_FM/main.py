import sys
import argparse
import requests
import vlc
import os
import time
from colorama import Fore, Style, init

init(autoreset=True)

def format_decimal(value):
    try:
        return f"{float(value):.2f}"
    except ValueError:
        return value

def print_radio_interface(station_name=None, company_name=None, country=None, bitrate=None, genre=None, is_playing=False, station_number=None):
    os.system('clear')
    radio_art = f"""
{Fore.GREEN}+--------------------------------------------------+
{Fore.YELLOW}|               {Fore.RED}🔰SL Android Official ™            {Fore.YELLOW}|
{Fore.YELLOW}|           👨‍💻TOOL DEVELOPED BY IM COOL BOOY     {Fore.YELLOW}|
{Fore.CYAN}|                 📻 IM-COOL-BOOY-FM               {Fore.CYAN}|
{Fore.GREEN}+--------------------------------------------------+
{Fore.CYAN}
{Fore.CYAN}   Station: {Fore.LIGHTYELLOW_EX}{station_name if station_name else "None"}{Fore.CYAN}
{Fore.CYAN}   Company: {Fore.LIGHTYELLOW_EX}{company_name if company_name else "Unknown"}{Fore.CYAN}
{Fore.CYAN}   Country: {Fore.LIGHTYELLOW_EX}{country if country else "Unknown"}{Fore.CYAN}
{Fore.CYAN}   Bitrate: {Fore.LIGHTYELLOW_EX}{format_decimal(bitrate) if bitrate else "Unknown"} kbps{Fore.CYAN}
{Fore.CYAN}   Genre:   {Fore.LIGHTYELLOW_EX}{genre if genre else "Unknown"}{Fore.CYAN}
{Fore.CYAN}   Status:  {Fore.LIGHTGREEN_EX}{"Playing" if is_playing else "Stopped"}{Fore.CYAN}
{Fore.CYAN}   Station No: {Fore.LIGHTYELLOW_EX}{station_number if station_number else "None"}{Fore.CYAN}
{Fore.CYAN}
{Fore.GREEN}+--------------------------------------------------+
{Fore.LIGHTMAGENTA_EX}|    Options:                                      |
{Fore.LIGHTMAGENTA_EX}|    1️⃣ Search for a Radio Station                 |
{Fore.LIGHTMAGENTA_EX}|    2️⃣ Switch Channel                             |
{Fore.LIGHTMAGENTA_EX}|    3️⃣ Stop Playing                               |
{Fore.LIGHTMAGENTA_EX}|    4️⃣ View Station Details                       |
{Fore.LIGHTMAGENTA_EX}|    5️⃣ Exit                                       |
{Fore.GREEN}+--------------------------------------------------+
    """
    print(radio_art)

def search_radio_stations(query):
    url = f"https://de1.api.radio-browser.info/json/stations/search?name={query}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        stations = response.json()
        if not stations:
            print(f"{Fore.RED}No stations found for '{query}'. Please try again.")
            return []
        for station in stations:
            station['country'] = station.get('country', 'Unknown')
            station['company'] = station.get('name', 'Unknown')
            station['bitrate'] = station.get('bitrate', 'Unknown')

            station['genre'] = station.get('tags', ['Unknown'])[0] if station.get('tags') else 'Unknown'
        return stations
    except requests.exceptions.RequestException as e:
        print(f"{Fore.RED}Error fetching station list: {e}")
        return []

def display_and_play_stations(stations):
    os.system('clear')
    print(f"\n{Fore.CYAN}Available Stations:")
    for i, station in enumerate(stations):
        print(f"{Fore.YELLOW}[{i + 1}] {Fore.LIGHTYELLOW_EX}{station['name']} - {Fore.YELLOW}{station['url']} "
              f"({Fore.LIGHTGREEN_EX}{station['country']}, {Fore.LIGHTYELLOW_EX}{station['company']}, {format_decimal(station['bitrate'])} kbps, Genre: {station['genre']})")
    print(f"\n{Fore.MAGENTA}Enter the station number to play (or 0 to go back):")

    choice = input(f"{Fore.LIGHTCYAN_EX}> ")
    if choice == "0":
        return None
    try:
        choice = int(choice)
        if 1 <= choice <= len(stations):
            return stations[choice - 1]
        else:
            print(f"{Fore.RED}Invalid choice. Please try again.")
            time.sleep(2)
            return display_and_play_stations(stations)
    except ValueError:
        print(f"{Fore.RED}Invalid input. Please enter a number.")
        time.sleep(2)
        return display_and_play_stations(stations)

def show_station_details(station):
    print(f"\n{Fore.CYAN}Station Details:")
    print(f"Name: {Fore.LIGHTYELLOW_EX}{station['name']}")
    print(f"Company: {Fore.LIGHTYELLOW_EX}{station['company']}")
    print(f"Country: {Fore.LIGHTYELLOW_EX}{station['country']}")
    print(f"Bitrate: {Fore.LIGHTYELLOW_EX}{format_decimal(station['bitrate'])} kbps")
    print(f"Genre: {Fore.LIGHTYELLOW_EX}{station['genre']}")
    print(f"URL: {Fore.LIGHTYELLOW_EX}{station['url']}")
    print("\nPress any key to go back...")
    input(f"{Fore.LIGHTCYAN_EX}> ")

def show_help():
    help_message = f"""
{Fore.GREEN}+--------------------------------------------------+
{Fore.YELLOW}|              {Fore.RED}🔰SL Android Official ™             {Fore.YELLOW}|
{Fore.YELLOW}|           👨‍💻TOOL DEVELOPED BY IM COOL BOOY     {Fore.YELLOW}|
{Fore.CYAN}|                 📻 IM-COOL-BOOY-FM               {Fore.CYAN}|
{Fore.GREEN}+--------------------------------------------------+
{Fore.BLUE}   Usage:
{Fore.LIGHTCYAN_EX}     IM-COOL-BOOY-FM -h [options]

{Fore.BLUE}   Options:
{Fore.LIGHTCYAN_EX}     -h, --help    ➡️         Show this help message and exit
{Fore.LIGHTCYAN_EX}     1️⃣            ➡️         Search for a Radio Station
{Fore.LIGHTCYAN_EX}     2️⃣            ➡️         Switch Channel
{Fore.LIGHTCYAN_EX}     3️⃣            ➡️         Stop Playing
{Fore.LIGHTCYAN_EX}     4️⃣            ➡️         View Station Details
{Fore.LIGHTCYAN_EX}     5️⃣            ➡️         Exit
{Fore.GREEN}+--------------------------------------------------+
    """
    print(help_message)

def main():

    if len(sys.argv) > 1 and sys.argv[1] in ('-h', '--help'):
        show_help()
        return

    player = None
    current_station = None
    station_number = None

    while True:
        print_radio_interface(
            station_name=current_station['name'] if current_station else None,
            company_name=current_station['company'] if current_station else None,
            country=current_station['country'] if current_station else None,
            bitrate=current_station['bitrate'] if current_station else None,
            genre=current_station['genre'] if current_station else None,
            is_playing=player is not None and player.is_playing(),
            station_number=station_number
        )

        print(f"{Fore.MAGENTA}Enter your choice:")
        choice = input(f"{Fore.LIGHTCYAN_EX}> ")
        if choice == "1":
            query = input(f"{Fore.MAGENTA}Enter the radio station name to search: ")
            stations = search_radio_stations(query)

            if not stations:
                time.sleep(2)
                continue

            selected_station = display_and_play_stations(stations)
            if selected_station:
                if player:
                    player.stop()
                current_station = selected_station
                station_number = stations.index(selected_station) + 1
                print(f"\n{Fore.GREEN}Playing: {current_station['name']} - {current_station['url']}")
                player = vlc.MediaPlayer(current_station['url'])
                player.play()

                time.sleep(1)

        elif choice == "2":
            if current_station:
                print(f"{Fore.GREEN}Switching Channel: {current_station['name']} - {current_station['url']}")
                player.stop()
                time.sleep(2)

        elif choice == "3":
            if current_station:
                print(f"{Fore.RED}Stopping: {current_station['name']}")
                player.stop()
                current_station = None
                time.sleep(2)

        elif choice == "4":
            if current_station:
                show_station_details(current_station)
            else:
                print(f"{Fore.RED}No station is currently playing.")
                time.sleep(2)

        elif choice == "5":
            if player:
                player.stop()
            print(f"{Fore.GREEN}📻IM-COOL-BOOY-FM")
            print(f"{Fore.YELLOW}👨‍💻TOOL DEVELOPED BY IM COOL BOOY")
            print(f"{Fore.CYAN}🔰SL Android Official ™")
            break
        else:
            print(f"{Fore.RED}Invalid option. Please try again.")
            time.sleep(2)

if __name__ == "__main__":
    main()
