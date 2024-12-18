# Innate SDK

The Innate SDK introduces a revolutionary paradigm where every physical robot becomes an AI agent. Build sophisticated AI applications combining state-of-the-art manipulation, navigation, and reasoning capabilities.

## Documentation

For full documentation, visit [docs.innate.bot](https://docs.innate.bot)

## Key Features

- 🤖 Full robotic control (navigation, manipulation, sensing)
- 🧠 Built-in AI agent capabilities
- 📱 Simple Python SDK and CLI tools
- 🛠 Extensible hardware support
- 🎓 Learning from demonstration
- 👀 Advanced visual understanding

## Quick Start

Visit our [Get Started Guide](https://docs.innate.bot/get-started) to:
- Set up your Innate-powered robot
- Create your first AI agent
- Learn core concepts like Primitives and Directives
- Build sophisticated robotic applications

## Community

Join our [developer community](https://docs.innate.bot/welcome) to share and learn from other builders.

## Example: Service Robot

Here's a simple example of creating a robot that serves drinks - provided that you trained a policy to pickup glasses as described in the [training guide](https://docs.innate.bot/docs.innate.bot/basics/manipulation).

```python
from innate import Agent, Primitive, Directive
from innate import manipulation
from typing import List

# Initialize your robot as an agent
robot = Agent()

# Create a primitive for grabbing glasses
class GrabGlass(Primitive):
    def init(self):
        super().init()
        manipulation.init()

    def execute(self):
        manipulation.run_policy("pickup_glass")
        return "Retrieved glass.", True


# Create a directive to guide the robot's behavior
class ServingDirective(Directive):
    def init(self):
        self.primitives = [GrabGlass()]
    def get_prompt(self) -> str:
        return """You are a helpful robot called Maurice that serves drinks to people.
Navigate between rooms to find people and serve them drinks."""


# Start your robot  
robot.set_directive(ServingDirective())
robot.run()
```

## Learn More

Explore our detailed documentation at [docs.innate.bot](https://docs.innate.bot)
