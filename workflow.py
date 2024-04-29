import multiprocessing
import os
import threading
import time

from agent.plan import planner
from agent.control import controller

def set_env_variable():
    # OPENAI ENVIRONMENT
    os.environ["OPENAI_LOG"] = "debug"

def get_user_input():
    r"""
    """
    return input("请输入战术文本:")

def workflow(user_input: str=""):
    r"""
    """
    for l in range(10000):
        print(l)
        time.sleep(l)

class google_footbal(object):
    r"""
    """

    def __init__(self) -> None:
        r"""
        """
        set_env_variable()
        self.planner = planner()
        self.controller = controller()
        self.process_event = multiprocessing.Event()
        self.play_process = multiprocessing.Process(target=workflow)
        self.play_process.start()
        self.get_user_input()
    
    def get_user_input(self):
        r"""
        """
        self.user_input = input("请输入战术文本:")
        self.play_process.terminate()

if __name__=="__main__":
    instance = google_footbal()
