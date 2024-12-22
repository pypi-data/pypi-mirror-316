import os
from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from azure.ai.inference.models import SystemMessage
from azure.ai.inference.models import UserMessage

api_key = "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"

client = ChatCompletionsClient(
    endpoint="https://models.inference.ai.azure.com",
    credential=AzureKeyCredential(api_key),
)

def is_13(number) -> str:
    response = client.complete(
        messages=[
            SystemMessage(content="""You are a bot that answers True or False ONLY whether an input is number 13 or not. Don't include any special characters like a period or comma."""),
            UserMessage(content=number),
        ],
        model="Phi-3.5-MoE-instruct",
        temperature=0.8,
        max_tokens=2048,
        top_p=0.1
    )

    return response.choices[0].message.content
