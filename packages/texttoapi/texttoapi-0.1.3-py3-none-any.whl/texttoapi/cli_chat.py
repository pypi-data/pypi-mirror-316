
print("Starting chat...")
import os
import logging
from . import env
# Configure the logger
logging.getLogger(os.path.basename(__file__)).setLevel(logging.DEBUG if env.log_level == "debug" else logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)

import time
import re
# Below import is used
import readline
import inspect
import io
import contextlib
import datetime
import requests
from rich.markdown import Markdown
from rich.console import Console

from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.agent import AgentRunner
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import Settings
from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.core import VectorStoreIndex
from llama_index.core.objects import ObjectIndex

# Set up tracing and logging
from openinference.instrumentation.llama_index import LlamaIndexInstrumentor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk import trace as trace_sdk
from opentelemetry.sdk.trace.export import SimpleSpanProcessor


try:
    if requests.get(env.trace_url, timeout=3).status_code == 200:
        tracer_provider = trace_sdk.TracerProvider()
        tracer_provider.add_span_processor(SimpleSpanProcessor(OTLPSpanExporter(env.trace_url)))

        LlamaIndexInstrumentor().instrument(tracer_provider=tracer_provider)
        logging.getLogger(os.path.basename(__file__)).debug("Tracing enabled")
except Exception:
    logging.getLogger(os.path.basename(__file__)).debug("Tracing not enabled")

import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.simplefilter('ignore', InsecureRequestWarning)

logging.getLogger(os.path.basename(__file__)).debug("Configuring llm...")
# Set up the OpenAI Embedding and LLM models
embed_model = AzureOpenAIEmbedding(
    model="text-embedding-ada-002",
    deployment_name="ada-002",
    api_key=env.api_key,
    azure_endpoint=env.azure_endpoint,
    api_version=env.api_version,
)

llm = AzureOpenAI(
    model=env.model,
    api_key=env.api_key,
    deployment_name=env.model,
    azure_endpoint=env.azure_endpoint,
    api_version=env.api_version,
)

Settings.llm = llm
Settings.embed_model = embed_model


def init_agent(tool):
    obj_index = ObjectIndex.from_objects(
    tool,
    index_cls=VectorStoreIndex,
)
    agent_worker = FunctionCallingAgentWorker.from_tools(
        tool_retriever=obj_index.as_retriever(similarity_top_k=6),
        llm=llm,
        verbose=True,
        allow_parallel_tool_calls=False
        # system_prompt=env.llm_system_prompt
        )
    agent = AgentRunner(agent_worker)
    return agent

def print_json_aligned(data, indent=0, is_top_level=True):
    """
    Recursively print JSON data in a structured format without braces, brackets, or extra symbols.
    Args:
    - data (dict or list): The JSON object to print.
    - indent (int): The current level of indentation for nested structures.
    - is_top_level (bool): Indicates if the function is at the top level to manage blank lines.
    """
    if isinstance(data, list):
        for item in data:
            print_json_aligned(item, indent, is_top_level=True)
    elif isinstance(data, dict):
        # Calculate the max key length at this level for alignment
        max_key_length = max(len(key) for key in data.keys())
        for key, value in data.items():
            if isinstance(value, dict):
                print(" " * indent + f"{key.ljust(max_key_length)} :")
                print_json_aligned(value, indent + 4, is_top_level=False)
            elif isinstance(value, list):
                print(" " * indent + f"{key.ljust(max_key_length)} :")
                print_json_aligned(value, indent + 4, is_top_level=False)
            else:
                print(" " * indent + f"{key.ljust(max_key_length)} : {value}")
        # Add a blank line after each top-level item for readability
        if is_top_level:
            print()

def display_gpt_response_pretty(gpt_response: str):
    """
    Display a GPT response in Markdown format for better readability in the terminal.

    Args:
        gpt_response (str): The response from the OpenAI API in Markdown format.
    """
    console = Console()
    markdown_response = Markdown(gpt_response)
    console.print(markdown_response)


def chat_with_agent_final(chat_history, user_input, agent):
    results_final = []

    start_time = time.time()
    output_capture = io.StringIO()
    with contextlib.redirect_stdout(output_capture):
        response = agent.chat(user_input)
    # Get the captured output
    captured_output = output_capture.getvalue()

    # TODO: need to check how to print nested functions
    func, output= extract_function_details(captured_output)
    logging.getLogger(os.path.basename(__file__)).info(f"gpt: Initial {func}")

    tool_outputs = response.sources
    results = [(output.tool_name, output.raw_input) for output in tool_outputs if not output.is_error]
    results_final.append(results)

    # Calculate duration
    end_time = time.time()
    duration = end_time - start_time

    # Return structured data
    return {
        "question": user_input,
        "gpt_response": response,
        "time_taken": duration,
        "tool_calls": results_final,
        "verbose_response": captured_output,
        "json_response": [output.raw_output for output in tool_outputs if not output.is_error]
    }

def chat_output(result):
    logging.getLogger(os.path.basename(__file__)).debug(f'Question: {result["question"]}')
    logging.getLogger(os.path.basename(__file__)).debug(f'Time taken: {datetime.datetime.fromtimestamp(result["time_taken"]).strftime("%S")} seconds')
    logging.getLogger(os.path.basename(__file__)).debug("===json response===")
    logging.getLogger(os.path.basename(__file__)).debug(result['json_response'])
    logging.getLogger(os.path.basename(__file__)).debug("===gpt response===")
    logging.getLogger(os.path.basename(__file__)).debug(result['gpt_response'])

    print("Agent:")
    if env.log_level != "error":
        try:
            print("===pretty print===")
            print_json_aligned(result['json_response'])
            print("======")
        except Exception:
            pass
        print("===gpt response===")
    display_gpt_response_pretty(result['gpt_response'].response)

def start_chat(tool):
    chat_history = []
    agent = init_agent(tool)
    logging.getLogger(os.path.basename(__file__)).info("type 'quit' or 'exit' to end the chat")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit"]:
            logging.getLogger(os.path.basename(__file__)).info("Ending chat. Goodbye!")
            break
        user_input = user_input.strip()
        if not user_input:
            continue
        logging.getLogger(os.path.basename(__file__)).info("Please wait processing...")
        try: 
            result = chat_with_agent_final(chat_history, user_input, agent)
            chat_output(result)
        except Exception as e:
            try: 
                logging.getLogger(os.path.basename(__file__)).error(f"First error processing user input: {user_input}. Restarted agent and tried again.")
                logging.getLogger(os.path.basename(__file__)).error(f"Error processing user input: {user_input}")
                logging.getLogger(os.path.basename(__file__)).error(f"Error details: {str(e)}")
                agent = init_agent(tool)
                result = chat_with_agent_final(chat_history, user_input, agent)
                chat_output(result)
            except Exception as e:
                logging.getLogger(os.path.basename(__file__)).error(f"Agent: Sorry, I couldn't process your request. Please try again. Check logs for more info")
                logging.getLogger(os.path.basename(__file__)).error(f"Error processing user input: {user_input}")
                logging.getLogger(os.path.basename(__file__)).error(f"Error details: {str(e)}")
                agent = init_agent(tool)


def extract_function_details(text):
    # Regular expressions to match the function call and function output sections
    function_call_pattern = r'=== Calling Function ===\nCalling function: (.*?) with args: (.*?)\n'
    function_output_pattern = r'=== Function Output ===\n(.*?)\n=== LLM Response ==='

    # Extract the function call with args
    function_call_match = re.search(function_call_pattern, text)
    if function_call_match:
        function_call = f"Calling function: {function_call_match.group(1)} with args: {function_call_match.group(2)}"
    else:
        function_call = "Function call not found"

    # Extract the function output
    function_output_match = re.search(function_output_pattern, text, re.DOTALL)
    if function_output_match:
        function_output = f"Function Output: {function_output_match.group(1).strip()}"
    else:
        function_output = "Function output not found"

    return function_call, function_output


if __name__ == "__main__":
    start_chat()