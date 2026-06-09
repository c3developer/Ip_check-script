import requests
import session_store

BASE_URL = "http://127.0.0.1:8000"


class ApiClient:

    def get_headers(self):

        return {
            "Authorization":
            f"Bearer {session_store.TOKEN}"
        }

    def login(
            self,
            username,
            password
    ):

        response = requests.post(
            f"{BASE_URL}/login",
            json={
                "username": username,
                "password": password
            }
        )

        return response.json()

    def register(
            self,
            username,
            email,
            password
    ):

        response = requests.post(
            f"{BASE_URL}/register",
            json={
                "username": username,
                "email": email,
                "password": password
            }
        )

        return response.json()

    def create_chat(
            self,
            title
    ):

        response = requests.post(
            f"{BASE_URL}/chat/create",
            json={
                "title": title
            },
            headers=self.get_headers()
        )

        return response.json()

    def send_message(
            self,
            session_id,
            message
    ):

        response = requests.post(
            f"{BASE_URL}/chat/send",
            json={
                "session_id": session_id,
                "message": message
            },
            headers=self.get_headers()
        )

        return response.json()

    def get_chats(self):

        response = requests.get(
            f"{BASE_URL}/chat/list",
            headers=self.get_headers()
        )

        return response.json()

    def get_history(
            self,
            session_id
    ):

        response = requests.get(
            f"{BASE_URL}/chat/history/{session_id}",
            headers=self.get_headers()
        )

        return response.json()
    
    def get_settings(self):

        response = requests.get(
        f"{BASE_URL}/settings",
        headers=self.get_headers()
    )

        return response.json()


    def save_settings(
         self,
            data
            ):

     response = requests.post(
        f"{BASE_URL}/settings",
        json=data,
        headers=self.get_headers()
    )

     return response.json()
    
    def delete_chat(
            self,
            session_id
    ):
        response = requests.delete(

        f"{BASE_URL}/chat/delete/{session_id}",

        headers=self.get_headers()
    
    )
        return response.json
    
    def rename_chat(
        self,
        session_id,
        title
):

        response = requests.put(

        f"{BASE_URL}/chat/rename/{session_id}",

        params={
            "title": title
        },

        headers=self.get_headers()
    )

        return response.json()
    

        