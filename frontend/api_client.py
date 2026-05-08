import requests
from config import BACKEND_URL


def send_message_to_backend(message):
    try:
        response = requests.post(
            BACKEND_URL,
            json={"message": message},
            timeout=20
        )

        try:
            data = response.json()
        except ValueError:
            return "Backend returned invalid JSON."

        if response.status_code == 200:
            return data.get("reply", "No reply received from backend.")

        return data.get("reply", f"Backend error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        return "Cannot connect to backend. Please make sure the Flask server is running."

    except requests.exceptions.Timeout:
        return "The backend took too long to respond."

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Request failed: {e}")
        return "A network error occurred while contacting the backend."

    except Exception as e:
        print(f"[ERROR] Unexpected frontend API error: {e}")
        return "An unexpected error occurred."