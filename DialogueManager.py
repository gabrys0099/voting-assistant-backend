class DialogueManager:
    """
    Manages the state and flow of the conversation for the voting process.
    """

    def __init__(self):
        self.state = "INITIAL"
        self.candidates = ["Kandydat A", "Kandydat B", "Kandydat C"]
        self.user_choice = None
        print("DialogueManager initialized, current state: INITIAL")

    def process_message(self, user_text):
        """
        Processes user input based on the current conversation state.
        """
        user_text = user_text.lower()
        response = "Nie rozumiem. Czy możesz powtórzyć?"

        if self.state == "INITIAL":
            if "start" in user_text or "głos" in user_text or "tak" in user_text:
                self.state = "AWAITING_VOTE"
                candidates_str = ", ".join(self.candidates)
                response = f"Dobrze, zaczynamy głosowanie. Dostępni kandydaci to: {candidates_str}. Na kogo chcesz zagłosować?"
                print(f"State transition: INITIAL -> AWAITING_VOTE")
            else:
                response = "Cześć! Jestem asystentem do głosowania. Powiedz 'start', aby rozpocząć."

        elif self.state == "AWAITING_VOTE":
            for candidate in self.candidates:
                if candidate.lower() in user_text:
                    self.user_choice = candidate
                    self.state = "AWAITING_VOTE_CONFIRMATION"
                    response = f"Wybrano opcję: {self.user_choice}. Czy potwierdzasz swój wybór? Powiedz 'tak' lub 'nie'."
                    print(f"State transition: AWAITING_VOTE -> AWAITING_VOTE_CONFIRMATION")
                    return response

            response = "Nie rozpoznałem tego kandydata. Proszę, wybierz jednego z listy."

        elif self.state == "AWAITING_VOTE_CONFIRMATION":
            if "tak" in user_text or "potwierdzam" in user_text:
                print(f"VOTE CAST for: {self.user_choice}")
                self.state = "FINISHED"
                response = f"Dziękuję. Twój głos na kandydata '{self.user_choice}' został zapisany. Do widzenia!"
                print(f"State transition: AWAITING_VOTE_CONFIRMATION -> FINISHED")
            elif "nie" in user_text or "anuluj" in user_text:
                self.state = "AWAITING_VOTE"
                self.user_choice = None
                response = "Anulowano wybór. Powiedz mi jeszcze raz, na kogo chcesz zagłosować."
                print(f"State transition: AWAITING_VOTE_CONFIRMATION -> AWAITING_VOTE")
            else:
                response = "Proszę, odpowiedz 'tak' lub 'nie', aby potwierdzić lub anulować swój wybór."

        elif self.state == "FINISHED":
            if "restart" in user_text or "jeszcze raz" in user_text:
                self.__init__()
                response = "Dobrze, zaczynamy od nowa. Powiedz 'start', aby rozpocząć."
            else:
                response = "Proces głosowania został już zakończony. Możesz powiedzieć 'restart', aby zacząć od nowa."

        return response


dialogue_manager_instance = DialogueManager()
