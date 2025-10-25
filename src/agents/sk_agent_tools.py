from typing import Optional 
from semantic_kernel.functions import kernel_function, KernelArguments
from ..services import TaskService

class SKAgentPlugins:
    """Task Management Plugin"""

    def __init__(self, task_service: TaskService):
        self.task_service = task_service

    @kernel_function(name="CreateTask", description="Create a new task.")
    async def create_task(self, title: str, isComplete: bool = False) -> str:
        """
        Create a new task.
        Parameters:
        - title: the title of the new task.
        - isComplete: the status of the task. When this value is true, it means that the task is completed.
        Return: 
        - task information as a string.
        """ 
        task = await self.task_service.add_task(title, isComplete)
        return f'Task created successfully: "{task.title}" (ID: {task.id})'
    
    @kernel_function(name="GetTasks", description="Get all tasks.")
    async def get_tasks(self) -> str:
        """
        Get all tasks.

        Return: 
        - list of tasks as a string.
        """ 
        tasks = await self.task_service.get_all_tasks()
        if not tasks:
            return 'No tasks found.'
        
        task_list = '\n'.join([
            f'- {t.id}: {t.title} ({"Complete" if t.isComplete else "Incomplete"})'
            for t in tasks
        ])
        return f'Found {len(tasks)} tasks:\n{task_list}'
    
    @kernel_function(name="GetTask", description="Get one specific task with id.")
    async def get_task(self, id: int) -> str:
        """
        Get one specific task with id.

        Parameters:
        - id: the id of the target task.

        Return: 
        - task information as a string.
        """ 
        task = await self.task_service.get_task_by_id(id)
        if not task:
            return f'Task with ID {id} not found.'
        
        status = "Complete" if task.isComplete else "Incomplete"
        return f'Task {task.id}: "{task.title}" - Status: {status}'
    
    @kernel_function(name="UpdateTask", description="Update a specific task with its id, its new title and its new complete status.")
    async def update_task(self, id: int, title: Optional[str] = None, isComplete: Optional[bool] = None) -> str:
        """
        Update a specific task with its id, its new title and its new complete status.

        Parameters:
        - id: the id of the target task.
        - title: the new title of the task.
        - isComplete: the new status of the task. When this value is true, it means that the task is completed.

        Return: 
        - updated task information as a string.
        """ 
        updated = await self.task_service.update_task(id, title, isComplete)
        if not updated:
            return f'Task with ID {id} not found.'
        return f'Task {id} updated successfully.'
    
    @kernel_function(name="DeleteTask", description="Delete a specific task with its id.")
    async def delete_task(self, id: int) -> str:
        """
        Delete a specific task with its id.

        Parameters:
        - id: the id of the target task.

        Return: 
        - deletion result as a string.
        """ 
        deleted = await self.task_service.delete_task(id)
        if not deleted:
            return f'Task with ID {id} not found.'
        return f'Task {id} deleted successfully.'