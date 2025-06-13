import json
import os
import csv
from datetime import datetime


class DialogueManager:
    def __init__(self):
        self.state = "INITIAL"
        self.user_choice = None
        try:
            with open('candidates.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.candidates = data.get("candidates", [])
                self.election_title = data.get("electionTitle", "Wybory")
        except FileNotFoundError:
            print("ERROR: candidates.json file not found. Using default candidates.")
            self.candidates = ["Default Candidate A", "Default Candidate B"]
            self.election_title = "Default Election"

        print(f"DialogueManager initialized for '{self.election_title}', state: INITIAL")

    def process_message(self, user_text):
        user_text = user_text.lower()
        response = {"text": "Nie rozumiem. Czy możesz powtórzyć?", "data": None}

        if self.state == "INITIAL":
            if "start" in user_text or "głos" in user_text or "tak" in user_text:
                self.state = "AWAITING_VOTE"
                candidates_str = ", ".join(self.candidates)
                response_text = f"Dobrze, zaczynamy głosowanie. Dostępni kandydaci to: {candidates_str}. Na kogo chcesz zagłosować?"
                response = {"text": response_text, "data": self.candidates}
                print(f"State transition: INITIAL -> AWAITING_VOTE")
            else:
                response["text"] = "Cześć! Jestem asystentem do głosowania. Powiedz 'start', aby rozpocząć."

        elif self.state == "AWAITING_VOTE":
            found_candidate = False
            for candidate in self.candidates:
                if candidate.lower() in user_text:
                    self.user_choice = candidate
                    self.state = "AWAITING_VOTE_CONFIRMATION"
                    response[
                        "text"] = f"Wybrano opcję: {self.user_choice}. Czy potwierdzasz swój wybór? Powiedz 'tak' lub 'nie'."
                    print(f"State transition: AWAITING_VOTE -> AWAITING_VOTE_CONFIRMATION")
                    found_candidate = True
                    break

            if not found_candidate:
                response["text"] = "Nie rozpoznałem tego kandydata. Proszę, wybierz jednego z listy."

        elif self.state == "AWAITING_VOTE_CONFIRMATION":
            if "tak" in user_text or "potwierdzam" in user_text:
                vote_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                vote_data = [self.user_choice, vote_timestamp]

                with open('results.csv', 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(vote_data)

                print(f"VOTE SAVED for: {self.user_choice}")
                self.state = "FINISHED"
                response[
                    "text"] = f"Dziękuję. Twój głos na kandydata '{self.user_choice}' został zapisany. Do widzenia!"
                print(f"State transition: AWAITING_VOTE_CONFIRMATION -> FINISHED")
            elif "nie" in user_text or "anuluj" in user_text:
                self.state = "AWAITING_VOTE"
                self.user_choice = None
                response["text"] = "Anulowano wybór. Powiedz mi jeszcze raz, na kogo chcesz zagłosować."
                response["data"] = self.candidates
                print(f"State transition: AWAITING_VOTE_CONFIRMATION -> AWAITING_VOTE")
            else:
                response["text"] = "Proszę, odpowiedz 'tak' lub 'nie', aby potwierdzić lub anulować swój wybór."

        elif self.state == "FINISHED":
            if "restart" in user_text or "jeszcze raz" in user_text:
                self.__init__()
                response["text"] = "Dobrze, zaczynamy od nowa. Powiedz 'start', aby rozpocząć."
            else:
                response[
                    "text"] = "Proces głosowania został już zakończony. Możesz powiedzieć 'restart', aby zacząć od nowa."

        return response


dialogue_manager_instance = DialogueManager()