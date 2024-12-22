from RFML.core.Conversation import Context
from RFML.core.Interaction import Interaction
from RFML.core.Results import PromptProcessResult
from RFML.core.SentenceFilters import SentenceFilters
from RFML.interface.IPromptValidator import IPromptValidator
from RFML.prompt.PromptCash import PromptCash
from RFML.prompt.PromptQuery import PromptQuery
import re


class Validator(IPromptValidator):
    def configure_sentence_filter(self, filters: SentenceFilters, context: Context,
                                  interaction: Interaction) -> str:
        pass

    # configure prompt_queries for validation check
    def configure_prompt_queries(self, model_name: str, prompt_query_list: list[PromptQuery]):
        if model_name == "rf-ce-on_desk_booking":
            self.rooom_booking(prompt_query_list)

    def rooom_booking(self, prompt_query_list: list[PromptQuery]):
        prompt_query_list.append(
            PromptQuery("Room_ID", {
                "Q1": "Which room is your priority?",
                "Q2": "Please specify the room name"
            })
        )

        prompt_query_list.append(
            PromptQuery("Pickup_time", {
                "Q1": "From when the room will be needed?",
                "Q2": "Please specify the start time for room reservation"
            })
        )
        prompt_query_list.append(
            PromptQuery("Drop_time", {
                "Q1": "Until when the room will be needed?",
                "Q2": "Please specify the end time for room reservation"
            })
        )
        prompt_query_list.append(
            PromptQuery("Pickup_date", {
                "Q1": "Could you specify the room booking date?",
                "Q2": "Please specify the room booking date"
            })
        )
        prompt_query_list.append(
            PromptQuery("Participant", {
                "Q1": "How many participants will be attending?",
                "Q2": "Please specify the number of participants"
            })
        )
        prompt_query_list.append(
            PromptQuery("Meeting_purpose", {
                "Q1": "The room will be needed for which reason?",
                "Q2": "Please specify the purpose of room booking"
            })
        )

    # process input and store in prompt_queries for validation check
    def process_prompt_queries(self, model_name: str, pc: PromptCash, user_input: str) -> PromptProcessResult:
        return PromptProcessResult(True, "")

    def format_prompt_queries(self, model_name: str, pc: PromptCash, valid_fields, user_input: str):
        msg = ""
        if valid_fields.get('Pickup_time'): msg += f"Please book a room from {valid_fields['Pickup_time']} to "
        if valid_fields.get('Drop_time'): msg += f"{valid_fields['Drop_time']} on "
        if valid_fields.get('Pickup_date'): msg += f"{valid_fields['Pickup_date']} at "
        if valid_fields.get('Room_ID'): msg += f"{valid_fields['Room_ID']} for "
        if valid_fields.get('Participant'): msg += f"{valid_fields['Participant']} participants for "
        if valid_fields.get('Meeting_purpose'): msg += f"{valid_fields['Meeting_purpose']}."
        result = re.sub(r"\b(at|on|to|for)\b$", "", msg.strip()).strip()
        return result
