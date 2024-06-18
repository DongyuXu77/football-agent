import json
import multiprocessing
import os
import signal
from threading import Thread
import pdb
import time
import redis

from colorama import Fore
from agent.plan import planner
from agent.control import controller
from agent.comment import commentator
from agent.env import announcer

"""
TO DO LIST:
    1. GIL issue. make log listener acquire GIL and log the message
"""

def set_env_variable():
    # OPENAI ENVIRONMENT
    os.environ["OPENAI_API_KEY"] = "sk-QJxd5dfa630db8c817a8eb06347957f2c6ad5cb1500YN9Gq"
    os.environ["OPENAI_LOG"] = "debug"

def workflow_process(planner, controller, commentator, state_queue, user_input: str, log_queue):
        r"""
        """
        while state_queue.empty():
            time.sleep(1)
        announcer_response = state_queue.get()
        log_queue.put(('announcer', announcer_response))
        planner.wrap_input_content(user_content=user_input, status=announcer_response)
        _, planner_response, _ = planner.get_response()
        # for sub_task in planner_response.split('\n'):
        # ...
        log_queue.put(('planner', planner_response))
        controller.wrap_input_content(content=planner_response, status=announcer_response)
        _, controller_response, _ = controller.get_response()
        log_queue.put(('controller', controller_response))
        commentator.wrap_input_content(result="", expect=planner_response)
        _, commentator_respoense, _ = commentator.get_response()
        log_queue.put('commentatir', commentator_respoense)

def announce_process(announcer, state_queue):
    r"""
    """
    _, announcer_response, _ = announcer.get_response()
    if not state_queue.empty():
        state_queue.get()
    state_queue.put(announcer_response)

def log_listener(log_queue):
    while True:
        time.sleep(2)
        if not log_queue.empty():
            tag, text = log_queue.get()
            if tag == 'announcer':
                print(Fore.RED + text)
            elif tag == 'planner':
                print(Fore.GREEN + text)
            elif tag == 'controller':
                print(Fore.YELLOW + text)
            elif tag == 'commentator':
                print(Fore.BLUE + text)

def input_listener(input_queue):
    while True:
        input_text = input("Please enter your strategy")
        input_queue.put(input_text)
        time.sleep(100) # free GIL

class google_football(object):
    r"""
    """

    def __init__(self) -> None:
        r"""
        """
        set_env_variable()
        self.play()
    
    def play(self):
        r"""
        """

        log_queue = multiprocessing.Queue()
        input_queue = multiprocessing.Queue()
        state_queue = multiprocessing.Queue()
        planner_instance = planner()
        planner_instance.set_few_shot_prompt(json_file_path="agent/argument/few_shot_prompt/few_shot_prompt.json")
        controller_instance = controller()
        announcer_instance = announcer()
        commentator_instance = commentator()
        #pdb.set_trace()
        redis_client = redis.StrictRedis(host='localhost', port=30386, db=0)
        
        env_info = redis_client.brpop('gfootball_env', timeout=0)
        announcer_instance.wrap_input_content(content=env_info, document_path='agent/argument/info_rule.md')

        input_thread = Thread(target=input_listener, args=(input_queue, ))
        input_thread.start()
        log_thread = Thread(target=log_listener, args=(log_queue, ))
        log_thread.start()
        announce_proc = multiprocessing.Process(target=announce_process, args=(announcer_instance, state_queue, ))
        announce_proc.start()

        workflow_proc = multiprocessing.Process()
        while True:
            while input_queue.empty():
                time.sleep(3)
            input_text = input_queue.get()
            if workflow_proc.is_alive():
                workflow_proc.terminate()
            workflow_proc = multiprocessing.Process(target=workflow_process, args=(planner_instance, controller_instance, commentator_instance, state_queue, input_text, log_queue, ))
            workflow_proc.start()
        
if __name__=="__main__":
    instance = google_football()
