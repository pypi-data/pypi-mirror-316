from typing import Dict, List
from uuid import uuid4
from .function_call import FunctionCall
from pathlib import Path


class ListDirFunctionCall(FunctionCall):
    def __init__(self):
        super().__init__(name="list_dir", parameters={
            "path": "relative/path/to/directory"}, description="List the contents of a directory, leaving the parameter value empty will return the contents of the current directory")

    def invoke(self, path: str = ""):
        try:
            directory = Path(path)
            if not directory.exists():
                return f"Directory {path} does not exist"
            return [str(p) for p in directory.iterdir()]
        except Exception as e:
            return f"{str(e)}\nFailed to list directory {path}"


class ReadFileFunctionCall(FunctionCall):
    def __init__(self):
        super().__init__(name="read_file", parameters={
            "file_path": "relative/path/to/file"}, description="Read the contents of a file")

    def invoke(self, file_path: str):
        try:
            file = Path(file_path)
            if not file.exists():
                return f"File {file_path} does not exist"
            return file.read_text(encoding='utf-8')
        except Exception as e:
            return f"{str(e)}\nFailed to read file {file_path}"


class WriteFileFunctionCall(FunctionCall):
    def __init__(self):
        super().__init__(name="write_file", parameters={
            "path": "relative/path/to/file",
            "content": "content to write to the file"}, description="Write content to a file")

    def invoke(self, path: str, content: str):
        try:
            # Ensure path is relative by resolving against current directory
            current_dir = Path.cwd()
            file = current_dir / Path(path)

            # Check that final path is still under current directory
            if not str(file).startswith(str(current_dir)):
                return f"Path {path} must be relative to current directory"

            # Create parent directories if they don't exist
            file.parent.mkdir(parents=True, exist_ok=True)

            file.write_text(content, encoding='utf-8')
            return f"File {path} has been written"
        except Exception as e:
            return f"{str(e)}\nFailed to write to file {path}"


class CopyFileOrFolderFunctionCall(FunctionCall):
    def __init__(self):
        super().__init__(name="copy", parameters={
            "src": "relative/path/to/source",
            "dst": "relative/path/to/destination"
        }, description="Copy a file or folder from source to destination path")

    def invoke(self, src: str, dst: str):
        try:
            src_path = Path(src)
            if not src_path.exists():
                return f"Source path {src} does not exist"

            # Ensure paths are relative by resolving against current directory
            current_dir = Path.cwd()
            dst_path = current_dir / Path(dst)

            # Check that final path is still under current directory
            if not str(dst_path).startswith(str(current_dir)):
                return f"Destination path {dst} must be relative to current directory"

            # Create parent directories if they don't exist
            dst_path.parent.mkdir(parents=True, exist_ok=True)

            if src_path.is_file():
                content = src_path.read_text()
                dst_path.write_text(content)
                return f"File {src} has been copied to {dst}"
            else:
                from shutil import copytree
                copytree(src_path, dst_path, dirs_exist_ok=True)
                return f"Directory {src} has been copied to {dst}"
        except Exception as e:
            return f"Failed to copy {src} to {dst}: {str(e)}"


# Global memory storage
MEMORIES: Dict[str, str] = {}


class AddMemoryFunctionCall(FunctionCall):
    def __init__(self):
        super().__init__(
            name="add_memory",
            parameters={
                "text": "The text content of the memory to store. Include descriptive context about what this memory represents (e.g., instead of just '4581234', use 'Important phone number for customer support: 4581234')"
            },
            description="Store a new memory with automatically assigned UUID. The memory text should include descriptive context to make it searchable - ask the user for additional context if the information is too vague (like a standalone number or word)"
        )

    def invoke(self, text: str):
        try:
            if not text or text.isspace():
                return "Error: Memory text cannot be empty"

            memory_id = str(uuid4())
            MEMORIES[memory_id] = text
            return f"Memory stored with UUID: {memory_id}"
        except Exception as e:
            return f"Error occurred while adding memory: {str(e)}"


class RemoveMemoryFunctionCall(FunctionCall):
    def __init__(self):
        super().__init__(
            name="remove_memory",
            parameters={
                "uuid": "The UUID of the memory to remove"
            },
            description="Remove a memory by its UUID"
        )

    def invoke(self, uuid: str):
        try:
            if not uuid or uuid.isspace():
                return "Error: UUID cannot be empty"

            if uuid in MEMORIES:
                del MEMORIES[uuid]
                return f"Memory {uuid} has been removed"
            return f"No memory found with UUID {uuid}"
        except Exception as e:
            return f"Error occurred while removing memory: {str(e)}"


class SearchMemoriesFunctionCall(FunctionCall):
    def __init__(self):
        super().__init__(
            name="search_memories",
            parameters={
                "terms": "List of search terms to match against memories' descriptive content",
                "limit": "Maximum number of results to return (default: 3)"
            },
            description="Search memories for given terms and return the top matching results. Memories should contain descriptive context, so searching for terms like 'phone' or 'customer' should find relevant memories even if they don't contain the exact number or data you're looking for"
        )

    def invoke(self, terms: str, limit: str = "3"):
        try:
            # Parse the terms string into a list
            try:
                # Handle both string representations: "['term1', 'term2']" or "term1, term2"
                if terms.startswith('['):
                    # Remove brackets and split by commas, then clean up quotes and whitespace
                    terms_list = [t.strip().strip("'\"")
                                  for t in terms[1:-1].split(',')]
                else:
                    terms_list = [t.strip() for t in terms.split(',')]
            except:
                return "Error: Invalid search terms format. Please provide terms as a comma-separated list"

            # Parse limit to integer
            try:
                limit_int = int(limit)
                if limit_int < 1:
                    return "Error: Limit must be a positive number"
            except ValueError:
                return "Error: Limit must be a valid number"

            if not MEMORIES:
                return "No memories stored"

            # Score each memory
            scored_memories = []
            for uuid, text in MEMORIES.items():
                score = 0
                text_lower = text.lower()
                for term in terms_list:
                    score += text_lower.count(term.lower())
                if score > 0:
                    scored_memories.append((score, uuid, text))

            # Sort by score and take top results
            scored_memories.sort(reverse=True)
            top_memories = scored_memories[:limit_int]

            if not top_memories:
                return "No memories found matching the search terms"

            # Format results
            result = []
            for _, uuid, text in top_memories:
                result.extend([
                    f"uuid:{uuid}",
                    text,
                    ""
                ])

            return "\n".join(result).rstrip()

        except Exception as e:
            return f"Error occurred while searching memories: {str(e)}"


def get_builtin_function_calls():
    return [ListDirFunctionCall(), ReadFileFunctionCall(), WriteFileFunctionCall(), CopyFileOrFolderFunctionCall(), AddMemoryFunctionCall(), RemoveMemoryFunctionCall(), SearchMemoriesFunctionCall()]
