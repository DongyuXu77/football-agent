from agent.base.meta import agent

class planner(agent):
    r"""
    """

    def __init__(self, 
                 system_prompt: str="您是一名专业的足球教练,请深吸一口气并仔细思考如何根据评估模块所给反馈建议与人类教练提供的战术内容及当前场上的局势提供完成该战术所需要实现的子目标，教练组有时不会战术内容，需要您自行思考如何基于现有状态设计目标从而帮助球队获胜，回答过程请严格保持风格的统一",
                 ) -> None:
        r"""
        """
        super().__init__(system_prompt)
    
    def wrap_input_content(self, user_content: str, commentator_content: str, status: str="", output_format: str="") -> None:
        r"""
        """
        self.wrap_content = "当前的实时状态为:"+status+"\n评估模块给出的反馈建议为:"+commentator_content+"\n教练组提供的战术内容为:"+user_content+f"\n请问达成该战术目标所需要完成的子目标是({output_format})?"
    