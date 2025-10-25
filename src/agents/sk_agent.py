import os
from semantic_kernel.agents import ChatCompletionAgent, ChatHistoryAgentThread
from semantic_kernel.connectors.ai.open_ai import OpenAIChatCompletion, AzureChatCompletion
from semantic_kernel.connectors.ai import FunctionChoiceBehavior, PromptExecutionSettings
from semantic_kernel.functions import kernel_function, KernelArguments
from semantic_kernel.kernel import Kernel
from .sk_agent_tools import SKAgentPlugins
from ..models import ChatMessage, Role 
from ..services import TaskService

class SKAgent:
    def __init__(self, task_service: TaskService):
        self.agent: ChatCompletionAgent = None
        self.thread: ChatHistoryAgentThread = None

        api_key = os.environ.get("API_KEY")
        deployment_name = os.environ.get("MODEL_DEPLOYMENT_NAME")
        endpoint = os.environ.get("PROJECT_ENDPOINT")

        service_id = "agent"

        ai_service = AzureChatCompletion(
            service_id=service_id, 
            api_key= api_key,
            deployment_name= deployment_name,
            endpoint=endpoint
        )

        # Configure the function choice behavior to auto invoke kernel functions
        settings =  PromptExecutionSettings()
        settings.function_choice_behavior = FunctionChoiceBehavior.Auto()      

        agent = ChatCompletionAgent(
            service=ai_service,
            name="task-management-agent",
            plugins=[SKAgentPlugins(task_service)],
            instructions="""You are a task management agent.
                            You help users manage their tasks effectively by calling the function available to you.
                            You should help users create, read, update, and delete tasks as needed.
                        """,
            arguments=KernelArguments(settings=settings),
        )  
        self.agent = agent

    async def process_message(self, message: str) -> ChatMessage:

        if not self.agent:
            return ChatMessage(
                role=Role.ASSISTANT,
                content="The agent is not properly configured. Please check your settings."
            )
        
        first_chunk = True
        content = ""
        async for response in self.agent.invoke_stream(
            messages=message, thread=self.thread,
        ):
            if first_chunk:
                content += f"# {response.name}: "
                first_chunk = False
            content+= str(response)
            self.thread = response.thread

        return ChatMessage(
            role=Role.ASSISTANT,
            content=content if content else "I received your message but couldn't generate a response."
        )