import json
import multiprocessing
import os
import signal
from threading import Thread
import time

from agent.plan import planner
from agent.control import controller
from agent.env import announcer

"""
TO DO LIST:
    1. GIL issue. make log listener acquire GIL and log the message
"""

def set_env_variable():
    # OPENAI ENVIRONMENT
    os.environ["OPENAI_API_KEY"] = ""
    os.environ["OPENAI_LOG"] = "debug"

def workflow_process(planner, controller, announcer, user_input: str, log_queue):
        r"""
        """
        _, announcer_response, _ = announcer.get_response()
        log_queue.put(announcer_response)
        planner.wrap_input_content(content=user_input, status=announcer_response)
        _, planner_response, _ = planner.get_response()
        log_queue.put(planner_response)
        controller.wrap_input_content(content=planner_response, status=announcer_response)

def log_listener(log_queue):
    while True:
        time.sleep(2)
        if not log_queue.empty():
            print(log_queue.get())

def input_listener(input_queue):
    while True:
        input_text = input("Please enter your strategy")
        input_queue.put(input_text)
        time.sleep(50) # free GIL

class google_football(object):
    r"""
    """

    def __init__(self) -> None:
        r"""
        """
        set_env_variable()
        self.planner = planner()
        self.controller = controller()
        self.play()
    
    def play(self):
        r"""
        """

        log_queue = multiprocessing.Queue()
        input_queue = multiprocessing.Queue()
        planner_instance = planner()
        planner_instance.set_few_shot_prompt(json_file_path="agent/argument/few_shot_prompt/few_shot_prompt.json")
        controller_instance = controller()
        announcer_instance = announcer()
        
        f = open('agent/argument/env.json', 'r')
        data = f.read()
        announcer_instance.wrap_input_content(content=data, document_path='agent/argument/info_rule.md')

        input_thread = Thread(target=input_listener, args=(input_queue, ))
        input_thread.start()
        log_thread = Thread(target=log_listener, args=(log_queue, ))
        log_thread.start()

        workflow_proc = multiprocessing.Process()
        while True:
            while input_queue.empty():
                time.sleep(3)
            input_text = input_queue.get()
            if workflow_proc.is_alive():
                workflow_proc.terminate()
            workflow_proc = multiprocessing.Process(target=workflow_process, args=(planner_instance, controller_instance, announcer_instance, input_text, log_queue, ))
            workflow_proc.start()
        
if __name__=="__main__":
    instance = google_football()
