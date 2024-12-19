from __future__ import annotations
from chatollama import Engine, Conversation
from pathlib import Path


class LuciusAssistant:
    def __init__(self, model: str = "llama3.1:8b"):
        self.engine = Engine(model=model)
        self.engine.stream = True
        self.engine.stream_event.on(self.handle_stream)
        self.function_calls = []
        self.engine.system(self.get_system_prompt())

        self.chat_text = ""
        self.function_calls_text = ""

    def add_function_call(self, function_call: FunctionCall):
        self.function_calls.append(function_call)

    def remove_function_call(self, function_call: FunctionCall):
        self.function_calls.remove(function_call)

    def get_system_prompt(self):
        prompt_path = Path(__file__, "..", "lucius_prompt.md").resolve()
        prompt = open(prompt_path, "r", encoding="utf-8").read()

        if len(self.function_calls) > 0:
            for function_call in self.function_calls:
                prompt += "\n\n```\n" + str(function_call) + "\n```"
        else:
            prompt += "\n\nNo function calls are available as of now"

        return prompt

    def submit_function_calls(self):
        self.engine.conversation = Conversation()
        self.engine.conversation.system(self.get_system_prompt())

    def set_function_calls(self, function_calls: list[FunctionCall]):
        self.function_calls = list(function_calls)
        self.submit_function_calls()

    def handle_stream(self, mode: int, delta: str, text: str):
        if mode == 0:
            print("[Lucius]:\n")
        elif mode == 1:
            print(delta, end="", flush=True)
        elif mode == 2:
            print("")

    def chat(self, message: str):
        self.chat_text = ""
        self.function_calls_text = ""

        self.engine.conversation.user(message)
        self.engine.chat()
        return self.engine.response


class FunctionCall:
    def __init__(self, name: str, parameters: dict, description: str):
        self.name = name
        self.parameters = parameters
        self.description = description

    def __str__(self):
        return f"<lucius:invoke name=\"{self.name}\">\n" + "\n".join([f"<lucius:parameter name=\"{k}\">{v}</lucius:parameter>" for k, v in self.parameters.items()]) + f"\n</lucius:invoke>\n\n{self.description}"

    def parse_call(self, call: str):
        try:
            # Find the function calls section
            start = call.find("<lucius:function_calls>")
            end = call.find("</lucius:function_calls>")

            # Check for missing tags
            if start == -1 and end == -1:
                return {"error": "missing_both_tags"}
            if start == -1:
                return {"error": "missing_start_tag"}
            if end == -1:
                return {"error": "missing_end_tag"}

            # Extract just the function calls content
            function_calls = call[start +
                                  len("<lucius:function_calls>"):end].strip()

            results = []

            # Find each invoke section
            while "<lucius:invoke" in function_calls:
                invoke_start = function_calls.find("<lucius:invoke")
                invoke_end = function_calls.find("</lucius:invoke>")
                if invoke_start == -1 or invoke_end == -1:
                    return {"error": "incorrect_syntax"}

                invoke_content = function_calls[invoke_start:invoke_end + len(
                    "</lucius:invoke>")]

                # Extract function name
                name_start = invoke_content.find('name="')
                name_end = invoke_content.find('"', name_start + 6)
                if name_start == -1 or name_end == -1:
                    return {"error": "incorrect_syntax"}
                function_name = invoke_content[name_start + 6:name_end]

                # Extract parameters
                params = {}
                param_content = invoke_content
                while "<lucius:parameter" in param_content:
                    param_start = param_content.find("<lucius:parameter")
                    param_end = param_content.find("</lucius:parameter>")
                    if param_start == -1 or param_end == -1:
                        return {"error": "incorrect_syntax"}

                    param_section = param_content[param_start:param_end +
                                                  len("</lucius:parameter>")]

                    # Get parameter name
                    pname_start = param_section.find('name="')
                    pname_end = param_section.find('"', pname_start + 6)
                    if pname_start == -1 or pname_end == -1:
                        return {"error": "incorrect_syntax"}
                    param_name = param_section[pname_start + 6:pname_end]

                    # Get parameter value
                    value_start = param_section.find(">") + 1
                    value_end = param_section.find("</lucius:parameter>")
                    param_value = param_section[value_start:value_end]

                    params[param_name] = param_value

                    # Move to next parameter
                    param_content = param_content[param_end +
                                                  len("</lucius:parameter>"):]

                results.append({
                    "name": function_name,
                    "parameters": params
                })

                # Move to next invoke
                function_calls = function_calls[invoke_end +
                                                len("</lucius:invoke>"):]

            return results[0] if results else {"error": "incorrect_syntax"}

        except:
            return {"error": "incorrect_syntax"}

    def invoke(self, **kwargs):
        return f"Function {self.name} is not implemented"


class ListDirFunctionCall(FunctionCall):
    def __init__(self):
        super().__init__(name="list_dir", parameters={
            "path": "relative/path/to/directory"}, description="List the contents of a directory, leaving the parameter value empty will return the contents of the current directory")

    def invoke(self, path: str = ""):
        directory = Path(path)
        if not directory.exists():
            return f"Directory {path} does not exist"
        return directory.listdir()


class ReadFileFunctionCall(FunctionCall):
    def __init__(self):
        super().__init__(name="read_file", parameters={
            "path": "relative/path/to/file"}, description="Read the contents of a file")

    def invoke(self, path: str):
        file = Path(path)
        if not file.exists():
            return f"File {path} does not exist"
        return file.read_text()


class WriteFileFunctionCall(FunctionCall):
    def __init__(self):
        super().__init__(name="write_file", parameters={
            "path": "relative/path/to/file",
            "content": "content to write to the file"}, description="Write content to a file")

    def invoke(self, path: str, content: str):
        file = Path(path)
        file.write_text(content)
        return f"File {path} has been written"


list_dir_function_call = ListDirFunctionCall()
read_file_function_call = ReadFileFunctionCall()
write_file_function_call = WriteFileFunctionCall()


lucius = LuciusAssistant()
lucius.set_function_calls(
    [list_dir_function_call, read_file_function_call, write_file_function_call])

lucius.chat("What are the current files in the directory")
