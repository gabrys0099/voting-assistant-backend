import json
import csv
from collections import Counter
from datetime import datetime


class DialogueManager:
    def __init__(self):
        self.state = "INITIAL"
        self.user_choice = None
        self.start_conversation = False
        try:
            with open('candidates.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.candidates = data.get("candidates", [])
                self.election_title = data.get("electionTitle", "Wybory")
        except FileNotFoundError:
            print("ERROR: candidates.json file not found. Using default candidates.")
            self.candidates = ["Default Candidate A", "Default Candidate B"]
            self.election_title = "Default Election"

        print(f"DialogueManager initialized/reset for '{self.election_title}', state: INITIAL")

    def get_election_results(self):
        try:
            with open('results.csv', 'r', newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                votes = [row[0] for row in reader]
                vote_counts = Counter(votes)

                if not vote_counts:
                    return {"text": "Nie oddano jeszcze żadnych głosów.", "payload": None}

                results_text = "Oto aktualne wyniki głosowania: "
                results_parts = [f"{candidate} - {count} głosów" for candidate, count in vote_counts.items()]
                results_text += ", ".join(results_parts) + "."

                return {"text": results_text, "payload": None}
        except FileNotFoundError:
            return {"text": "Nie oddano jeszcze żadnych głosów, plik z wynikami nie istnieje.", "payload": None}
        except Exception as e:
            print(f"Błąd odczytu wyników: {e}")
            return {"text": "Wystąpił błąd podczas odczytywania wyników.", "payload": None}

    def process_message(self, user_text):
        if user_text == '__START_CONVERSATION__':
            self.__init__()
            user_text = "Dzień dobry"

        user_text = user_text.lower()
        response = {"text": "Nie rozumiem. Czy możesz powtórzyć?", "data": None}

        if self.state == "INITIAL":
            if "start" in user_text or "głos" in user_text or "tak" in user_text:
                self.state = "AWAITING_VOTE"
                candidates_str = "\n".join(f"- {name}" for name in self.candidates)
                response_text = f"Przechodzimy do wyboru kandydatów. Dostępni kandydaci to:\n {candidates_str}\nNa kogo chcesz oddać swój głos?"
                response = {"text": response_text, "data": self.candidates}
                print(f"State transition: INITIAL -> AWAITING_VOTE")
            elif "wyniki" in user_text:
                response = self.get_election_results()
            else:
                if self.start_conversation:
                    response['text'] = "Nie zrozumiałem Twojego wyboru. Chcesz oddać głos, czy sprawdzić wyniki?"
                else:
                    self.start_conversation = True
                    response["text"] = "Cześć! Jestem asystentem do głosowania. Proces weryfikacji został zakończony pomyślnie. Chcesz oddać głos, czy sprawdzić wyniki?"

        elif self.state == "AWAITING_VOTE":
            found_candidate = False
            for candidate in self.candidates:
                if candidate.lower() in user_text:
                    self.user_choice = candidate
                    self.state = "AWAITING_VOTE_CONFIRMATION"
                    response[
                        "text"] = f"Wybrano opcję: {self.user_choice}. Czy potwierdzasz swój wybór? Powiedz 'potwierdzam' lub 'anuluj'."
                    print(f"State transition: AWAITING_VOTE -> AWAITING_VOTE_CONFIRMATION")
                    found_candidate = True
                    break

            if not found_candidate:
                response["text"] = "Nie rozpoznałem podanego kandydata. Proszę, podaj imię i nazwisko tego z listy, który znajduje się po prawej stronie."

        elif self.state == "AWAITING_VOTE_CONFIRMATION":
            if "tak" in user_text or "potwierdzam" in user_text:
                vote_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                vote_data = [self.user_choice, vote_timestamp]

                with open('results.csv', 'a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(vote_data)

                print(f"VOTE SAVED for: {self.user_choice}")
                self.state = "FINISHED"
                response["text"] = f"Dziękuję. Twój głos na kandydata '{self.user_choice}' został bezpiecznie zapisany. Do widzenia!"
                response["data"] = {"status": "finished"}
                print(f"State transition: AWAITING_VOTE_CONFIRMATION -> FINISHED")
            elif "nie" in user_text or "anuluj" in user_text:
                self.state = "AWAITING_VOTE"
                self.user_choice = None
                response["text"] = "Anulowano wybór. Powiedz mi jeszcze raz, na kogo chcesz zagłosować."
                response["data"] = self.candidates
                print(f"State transition: AWAITING_VOTE_CONFIRMATION -> AWAITING_VOTE")
            else:
                response["text"] = "Proszę, odpowiedz 'tak' lub 'nie', aby potwierdzić lub anulować swój wybór."


        return response


dialogue_manager_instance = DialogueManager()
