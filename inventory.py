from agents import Agent, Runner, OpenAIChatCompletionsModel, RunContextWrapper, set_tracing_disabled, AsyncOpenAI, function_tool, ReasoningItem
import asyncio
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

set_tracing_disabled(disabled=True)

provider = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=provider
)

inventory = []

@function_tool
def addItem(product_id:int, itemName:str, itemQuantity:str, operation:str):
    if not product_id:
        return "Product id not recieved"
    inventory.append({"id":product_id, "itemName": itemName, "itemQuantity": itemQuantity, "operation": operation})
    return f"Product Id is: {inventory["product_id"]}, Product Name is: {inventory["itemName"]}, Product Quantity is: {inventory["itemQuantity"]}, Operation is: {inventory["operation"]}"

@function_tool
def deleteItem(product_id:int):
    if not product_id:
        return "Product Not Found!"
    for i,item in enumerate(inventory):
        if item["product_id"] == product_id:
            inventory.pop(i)
            return f"Product with id {product_id} removed successfully."
    return f"Product with id {product_id} not found in inventory."

@function_tool
def updateItem(product_id:int, itemName:str, itemQuantity:int, operation:str):
    for i, item in enumerate(inventory):
        if item["product_id"] == product_id:
            inventory.pop(i)
            inventory.append({"id":product_id, "itemName": itemName, "itemQuantity": itemQuantity, "operation": operation})
            return f"Product with id {product_id} update successfully."
    return f"Product with id {product_id} not found in inventory."


inventoryAgent = Agent(
    name="InventoryAgent",
    instructions="""
You can manage the inventory using these commands:

1. addItem(product_id, itemName, itemQuantity, operation)
   - Adds a new item to the inventory.
   - Example: addItem(101, "Laptop", 5, "add")

2. deleteItem(product_id)
   - Deletes an item from inventory by product_id.
   - Example: deleteItem(101)

3. updateItem(product_id, itemName, itemQuantity, operation)
   - Updates the details of an existing item by product_id.
   - Example: updateItem(101, "Laptop Pro", 3, "update")

Use these commands to add, delete, or update items in the inventory.
""",
    model=model,
    tools=[addItem, deleteItem, updateItem]
)

memory = []

while True:
    user_input = input("Ask: ")
    memory.append({"role": "user", "content": user_input})
    result = Runner.run_sync(inventoryAgent, memory)
    memory.append({"role": "assistant", "content": result.final_output})
    print(result.final_output)