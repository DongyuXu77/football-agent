from agent.base.meta import agent

class planner(agent):
    r"""
    """

    def __init__(self, 
                 system_prompt: str="您是一名专业的足球教练,请深吸一口气并仔细思考如何根据人类教练提供的战术内容及当前场上的局势提供完成该战术所需要实现的子目标，回答过程请严格保持风格的统一",
                 ) -> None:
        r"""
        """
        super().__init__(system_prompt)
    
    def wrap_input_content(self, content: str, status: str="", output_format: str="") -> None:
        r"""
        """
        self.wrap_content = "当前的实时状态为:"+status+"\n教练组提供的战术内容是:"+content+f"\n请问达成该战术目标所需要完成的子目标是({output_format})?"
    