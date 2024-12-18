from typing import List


class Primitive:
    def __init__(self):
        pass

    def execute(self):
        raise NotImplementedError


class Directive:
    def get_primitives(self) -> List[Primitive]:
        raise NotImplementedError

    def get_prompt(self) -> str:
        raise NotImplementedError


class Agent:
    def __init__(self):
        self.directive = None

    def set_directive(self, directive: Directive):
        self.directive = directive

    def run(self):
        if not self.directive:
            raise RuntimeError("No directive set")
        print("Running agent with directive...")
        # Add agent execution logic here
