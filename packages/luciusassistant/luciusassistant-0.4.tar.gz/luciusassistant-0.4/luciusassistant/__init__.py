from __future__ import annotations
from chatollama import Engine, Conversation, Event
from pathlib import Path
from .function_call import FunctionCall
from .builtin_function_calls import get_builtin_function_calls
import ollama

__all__ = [
    "LuciusAssistant",
    "FunctionCall",
    "Engine",
    "Conversation",
    "Event",
    "get_builtin_function_calls"
]


class LuciusAssistant:
    def __init__(self, model: str = "lucius1.0:8b"):
        model = self._find_suitable_model(model)
        self.engine = Engine(model=model)
        self.engine.stream = True
        self.engine.stream_event.on(self.handle_stream)
        self.engine.stream_stopped_event.on(self.handle_stream_stopped_event)
        self.function_calls = []
        self.update_system_prompt()

        self.chat_text = ""
        self.function_calls_text = ""
        self.accumulated_text = ""
        self.generation_mode = "chat"

        self.debug = False

        self.chat_text_event = Event()
        self.function_calls_text_event = Event()
        self.automated_response_event = Event()
        self.chat_text_event.on(self.handle_chat_text_event)

    def clear(self):
        self._reset_state()
        self.engine.conversation = Conversation()
        self.update_system_prompt()

    def _find_suitable_model(self, requested_model: str) -> str:
        # Get list of available models
        models = ollama.list().models
        model_names = [m.model for m in models]

        # Check if requested model exists
        if requested_model not in model_names:
            def find_preferred_size(models_list):
                # Try to find 8b variant first
                eight_b_models = [m for m in models_list if "8b" in m.lower()]
                if eight_b_models:
                    return eight_b_models[0]

                # If no 8b, get the smallest model by finding the number before 'b'
                # and sorting by that number
                def extract_size(model_name):
                    import re
                    match = re.search(r'(\d+)b', model_name.lower())
                    return int(match.group(1)) if match else float('inf')

                return min(models_list, key=extract_size, default=None)

            # Try to find llama3.1 models first
            llama31_models = [
                m for m in model_names if "llama3.1" in m.lower()]
            if llama31_models:
                if result := find_preferred_size(llama31_models):
                    return result

            # Then try llama3.2 models
            llama32_models = [
                m for m in model_names if "llama3.2" in m.lower()]
            if llama32_models:
                if result := find_preferred_size(llama32_models):
                    return result

            # Then try any other llama models
            llama_models = [m for m in model_names if "llama" in m.lower()]
            if llama_models:
                if result := find_preferred_size(llama_models):
                    return result

            # Finally, try lucius models as last resort
            lucius_models = [m for m in model_names if "lucius" in m.lower()]
            if lucius_models:
                if result := find_preferred_size(lucius_models):
                    return result

            raise ValueError(f"Could not find suitable model. Requested model '{
                             requested_model}' not found and no llama or lucius models available. Available models: {', '.join(model_names)}")

        return requested_model

    def add_function_call(self, function_call: FunctionCall):
        self.function_calls.append(function_call)

    def remove_function_call(self, function_call: FunctionCall):
        self.function_calls.remove(function_call)

    def update_system_prompt(self):
        prompt_path = Path(__file__, "..", "lucius_prompt.md").resolve()
        prompt = open(prompt_path, "r", encoding="utf-8").read()

        self.base_system_prompt = prompt
        self.function_calls_prompt = ""

        if len(self.function_calls) > 0:
            for function_call in self.function_calls:
                function_call_part = f"\n\n```\n<lucius:function_calls>\n{
                    function_call.call_text()}\n</lucius:function_calls>\n\n{function_call.description}\n```"
                prompt += function_call_part
                self.function_calls_prompt += function_call_part
        else:
            function_call_part = "\n\nNo function calls are available as of now"
            prompt += function_call_part
            self.function_calls_prompt += function_call_part

        self.engine.conversation = Conversation()
        self.engine.conversation.system(prompt)

    def set_function_calls(self, function_calls: list[FunctionCall]):
        self.function_calls = list(function_calls)
        self.update_system_prompt()

    def find_function_call(self, name: str):
        for function_call in self.function_calls:
            if function_call.name == name:
                return function_call
        return None

    def handle_chat_text_event(self, mode: int, delta: str, text: str, switch: bool):
        if switch:
            self.engine.stream_stop = True
            self.needs_result_handling = True

    def handle_stream_stopped_event(self):
        if self.needs_result_handling:
            result = FunctionCall.parse_call(self.function_calls_text)
            self.function_calls_results = []
            if isinstance(result, list):
                for call in result:
                    call_name = call.get("name", None)
                    function_call = self.find_function_call(call_name)
                    if function_call:
                        value = function_call.trigger(
                            **call.get("parameters", {}))
                        self.function_calls_results.append({
                            "name": call_name,
                            "value": value
                        })
                    else:
                        self.function_calls_results.append({
                            "name": call_name,
                            "value": f"ERROR: Function '{call_name}' does not exist and is not available"
                        })
            else:
                print(result.get("error"))

            self.function_calls_text = ""

            self.engine.conversation.assistant(self.engine.response)
            function_calls_prompt = "This is an automated system message. The user does not see this message and is only here to return to you the results of the function calls. The results are as follows:\n"
            for result in self.function_calls_results:
                function_calls_prompt += f"\n---\nFunction {
                    result['name']} returned: \n{result['value']}\n---\n"

            function_calls_prompt += "\nNow please continue with your response, do not state that you recieved the results but instead just respond how you would after getting the results"

            self.automated_response_event.trigger(function_calls_prompt)
            self.chat(function_calls_prompt)

    def handle_stream(self, mode: int, delta: str, text: str):
        # Initialize state on first call
        if mode == 0:
            if self.debug:
                print("[Lucius]:\n")
            self._reset_state()
            self._trigger_both_events(mode, delta, text, False)
            return

        # Handle final call
        if mode == 2:
            if self.debug:
                print("")
            self._trigger_both_events(mode, delta, text, False)
            self.engine.conversation.assistant(self.engine.response)
            return

        # Handle streaming tokens (mode == 1)
        if self.debug:
            print(delta, end="", flush=True)

        self.accumulated_text += delta

        if self.generation_mode == "chat":
            self._handle_chat_mode()
        else:  # function_calls mode
            self._handle_function_calls_mode()

    def _reset_state(self):
        """Reset all state variables at the start of generation"""
        self.generation_mode = "chat"
        self.accumulated_text = ""
        self.chat_text = ""
        self.function_calls_text = ""

    def _trigger_both_events(self, mode: int, delta: str, text: str, switch: bool):
        """Trigger both chat and function calls events"""
        self.chat_text_event.trigger(mode, delta, text, switch)
        self.function_calls_text_event.trigger(mode, delta, text, switch)

    def _handle_chat_mode(self):
        """Handle token processing while in chat mode"""
        start_tag = "<lucius:function_calls>"

        if start_tag in self.accumulated_text:
            # Switch to function_calls mode
            parts = self.accumulated_text.split(start_tag)
            if parts[0]:  # Handle any chat content before the tag
                self.chat_text += parts[0]
                self.chat_text_event.trigger(1, parts[0], "", False)

            # Initialize function_calls content with the tag and preserve any following content
            self.function_calls_text = start_tag + "\n"  # Add explicit newline after tag
            self.function_calls_text_event.trigger(
                1, start_tag + "\n", "", True)
            self.generation_mode = "function_calls"
            self.accumulated_text = ""

        elif not start_tag.startswith(self.accumulated_text):
            # Confirmed chat content
            self.chat_text += self.accumulated_text
            self.chat_text_event.trigger(1, self.accumulated_text, "", False)
            self.accumulated_text = ""

    def _handle_function_calls_mode(self):
        """Handle token processing while in function_calls mode"""
        end_tag = "</lucius:function_calls>"

        if end_tag in self.accumulated_text:
            # Switch back to chat mode
            parts = self.accumulated_text.split(end_tag)

            # Handle function calls content including end tag
            function_content = parts[0] + end_tag
            self.function_calls_text += function_content
            self.function_calls_text_event.trigger(
                1, function_content, "", False)

            # Handle any chat content after the tag
            if len(parts) > 1 and parts[1].strip():
                self.chat_text += parts[1]
                self.chat_text_event.trigger(1, parts[1], "", True)
            else:
                self.chat_text_event.trigger(1, "", "", True)

            self.generation_mode = "chat"
            self.accumulated_text = ""

        elif not end_tag.startswith(self.accumulated_text):
            # Confirmed function calls content
            self.function_calls_text += self.accumulated_text
            self.function_calls_text_event.trigger(
                1, self.accumulated_text, "", False)
            self.accumulated_text = ""

    def chat(self, message: str):
        self.needs_result_handling = False
        self.chat_text = ""
        self.function_calls_text = ""
        self.accumulated_text = ""

        self.engine.conversation.user(message)
        self.engine.chat()
        return self.engine.response
