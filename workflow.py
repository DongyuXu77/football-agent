import json
import multiprocessing
import os
import signal
import threading
from threading import Thread
import pdb
import time
import redis

from colorama import Fore
from agent.plan import planner
from agent.control import controller
from agent.comment import commentator
from agent.env.announcer import announcer

"""
TO DO LIST:
    1. GIL(Global Interpret Lock) issue. make log listener acquire GIL and log the message
"""

def set_env_variable():
    # OPENAI ENVIRONMENT
    os.environ["OPENAI_API_KEY"] = "sk-QJxd5dfa630db8c817a8eb06347957f2c6ad5cb1500YN9Gq"
    os.environ["OPENAI_LOG"] = "debug"

def workflow_process(planner, controller, commentator, state_queue, reward_queue, user_input: str, log_queue):
        r"""
        """
        while True:
            #print("workflow restart")
            while state_queue.empty():
                time.sleep(1)
            announcer_response = state_queue.get()
            log_queue.put(('announcer', announcer_response))

            try:
                commentator_respoense
            except NameError:
                commentator_respoense = ''
            planner.wrap_input_content(user_content=user_input, status=announcer_response, commentator_content=commentator_respoense)
            _, planner_response, _ = planner.get_response()
            # for sub_task in planner_response.split('\n'):
            # ...
            log_queue.put(('planner', planner_response))
            controller.wrap_input_content(content=planner_response, status=announcer_response)
            _, controller_response, _ = controller.get_response()
            log_queue.put(('controller', controller_response))

            # use to judge whether executer is end
            while reward_queue.empty():
                time.sleep(1)
            # update the environment state
            while state_queue.empty():
                time.sleep(1)
            announcer_response = state_queue.get()
            commentator.wrap_input_content(result=announcer_response, expect=planner_response)
            _, commentator_respoense, _ = commentator.get_response()
            log_queue.put(('commentator', commentator_respoense))

def announce_process(announcer, state_queue, redis_client):
    r"""
    """
    while True:
        observation = redis_client.brpop('observations', timeout=0)
        announcer.wrap_input_content(content=observation, document_path='agent/argument/info_rule.md')
        _, announcer_response, _ = announcer.get_response()
        # make state_queue always store the new observation
        while not state_queue.empty():
            state_queue.get()
        state_queue.put(announcer_response)

def log_listener(log_queue, redis_client):
    while True:
        if not log_queue.empty():
            tag, text = log_queue.get()
            if tag == 'announcer':
                print(Fore.RED + text)
            elif tag == 'planner':
                print(Fore.GREEN + text)
            elif tag == 'controller':
                redis_client.lpush('control', text)
                redis_client.ltrim('control', 0, 0) # keep length to 1
                print(Fore.YELLOW + text)
            elif tag == 'interactor':
                print(Fore.WHITE + text)
            elif tag == 'commentator':
                print(Fore.BLUE + text)
        time.sleep(2)

def input_listener(input_queue, input_lock, input_event):
    while True:
        input_text = input("Please enter your strategy")
        with input_lock:
            input_queue.put(input_text)
            input_event.set()
        #time.sleep(200) # free GIL

def reward_listener(reward_queue, redis_client):
    while True:
        rewards = redis_client.brpop('rewards', timeout=0)
        reward_queue.put(rewards)

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
        reward_queue = multiprocessing.Queue()
        planner_instance = planner()
        controller_instance = controller()
        announcer_instance = announcer()
        commentator_instance = commentator()
        planner_instance.set_few_shot_prompt(json_file_path="agent/argument/few_shot_prompt/planner/few_shot_prompt.json")
        controller_instance.set_few_shot_prompt(json_file_path="agent/argument/few_shot_prompt/controller/few_shot_prompt.json")
        #pdb.set_trace()
        redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

        input_lock = threading.Lock()
        input_event = threading.Event()
        announce_thread = Thread(target=announce_process, args=(announcer_instance, state_queue, redis_client, ))
        input_thread = Thread(target=input_listener, args=(input_queue, input_lock, input_event, ))
        log_thread = Thread(target=log_listener, args=(log_queue, redis_client, ))
        reward_thread = Thread(target=reward_listener, args=(reward_queue, redis_client, ))
        log_thread.start()
        input_thread.start()
        announce_thread.start()
        reward_thread.start()

        workflow_proc = multiprocessing.Process()
        while True:
            event_occur = input_event.wait(timeout=20)
            if event_occur:
                input_text = input_queue.get()
                if workflow_proc.is_alive():
                    workflow_proc.terminate()
                with input_lock:
                    workflow_proc = multiprocessing.Process(target=workflow_process, args=(planner_instance, controller_instance, commentator_instance, state_queue, reward_queue, input_text, log_queue))
                    workflow_proc.start()
        
if __name__=="__main__":
    instance = google_football()
