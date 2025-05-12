from app import create_app, mongo
import requests
import datetime
import time
from threading import Thread

app = create_app()

def reload_website():    
    url = "https://learn-easy-1avz.onrender.com"  # Replace with your Render URL
    interval = 60  # Interval in seconds
    while True:
        try:
            response = requests.get(url)
            print(f"Reloaded at {datetime.datetime.now().isoformat()}: Status Code {response.status_code}")
        except requests.RequestException as error:
            print(f"Error reloading at {datetime.datetime.now().isoformat()}: {error}")
        time.sleep(interval)

# Start the reloader in a separate thread
reloader_thread = Thread(target=reload_website)
reloader_thread.daemon = True 
reloader_thread.start()

if __name__ == "__main__":
    app.run(debug=True)
