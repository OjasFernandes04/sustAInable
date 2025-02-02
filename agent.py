from uagents import Agent, Context, Model

class ContextPrompt(Model):
    context: str
    text: str

class Response(Model):
    text: str

agent = Agent(
    name="user",
    endpoint="http://localhost:8000/submit",
)

# Replace with the remote address of the GPT-4-mini agent
AI_AGENT_ADDRESS = "agent1qvkse4g5y3k8yn2kcnlcs6ydxtuht8d6zpk2lplgs5z4a7l633jckp2m3ux"

# Example code snippet with a bug
code = """
    def do_something():
        for i in range(10)
            pass
    """

# Create the context prompt
prompt = ContextPrompt(
    context="Find and fix the bug in the provided code snippet",
    text=code,
)

# Send the prompt to the GPT-4-mini agent on startup
@agent.on_event("startup")
async def send_message(ctx: Context):
    await ctx.send(AI_AGENT_ADDRESS, prompt)

# Handle the response from the GPT-4-mini agent
@agent.on_message(Response)
async def handle_response(ctx: Context, sender: str, msg: Response):
    ctx.logger.info(f"Received response from {sender}: {msg.text}")

# Run the agent
if __name__ == "__main__":
    agent.run()
