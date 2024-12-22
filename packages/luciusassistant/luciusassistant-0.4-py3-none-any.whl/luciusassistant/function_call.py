import inspect
import re


class FunctionCall:
    def __init__(self, name: str, parameters: dict, description: str):
        self.name = name
        self.parameters = parameters
        self.description = description

    def invoke(self, **kwargs):
        return f"Function {self.name} is not implemented"

    def trigger(self, **kwargs):
        # Get the signature of the invoke method
        sig = inspect.signature(self.invoke)

        # Filter kwargs to only include parameters that exist in invoke
        filtered_kwargs = {
            k: v for k, v in kwargs.items()
            if k in sig.parameters
        }

        # Call invoke with filtered kwargs
        return self.invoke(**filtered_kwargs)

    def __str__(self):
        return f"<lucius:invoke name=\"{self.name}\">\n" + "\n".join([f"<lucius:parameter name=\"{k}\">{v}</lucius:parameter>" for k, v in self.parameters.items()]) + f"\n</lucius:invoke>\n\n{self.description}"

    def call_text(self):
        return f"<lucius:invoke name=\"{self.name}\">\n" + "\n".join([f"<lucius:parameter name=\"{k}\">{v}</lucius:parameter>" for k, v in self.parameters.items()]) + f"\n</lucius:invoke>"

    @staticmethod
    def parse_call(call: str):
        try:
            # Find the function calls section
            function_calls_pattern = re.compile(r"<lucius:function_calls>(.*?)</lucius:function_calls>", re.DOTALL)
            function_calls_match = function_calls_pattern.search(call)
            
            # Check for missing tags
            if not function_calls_match:
                if "<lucius:function_calls>" not in call:
                    return {"error": "missing_start_tag"}
                elif "</lucius:function_calls>" not in call:
                    return {"error": "missing_end_tag"}
                return {"error": "missing_both_tags"}
            
            # Extract function calls content
            function_calls = function_calls_match.group(1).strip() 
            
            # Find all invoke blocks
            invoke_pattern = re.compile(r"<lucius:invoke\s+name=\"(.*?)\">(.*?)</lucius:invoke>", re.DOTALL)
            invoke_matches = invoke_pattern.finditer(function_calls)
            
            results = []
            for invoke in invoke_matches:
                function_name = invoke.group(1)
                params_text = invoke.group(2)
                
                # Extract parameters
                param_pattern = re.compile(r"<lucius:parameter\s+name=\"(.*?)\">(.*?)</lucius:parameter>", re.DOTALL)
                param_matches = param_pattern.finditer(params_text)
                
                params = {}
                for param in param_matches:
                    param_name = param.group(1)
                    param_value = param.group(2).strip()
                    params[param_name] = param_value
                
                results.append({
                    "name": function_name,
                    "parameters": params
                })
            
            return results if results else {"error": "incorrect_syntax"}
            
        except Exception as e:
            return {"error": "incorrect_syntax"}
