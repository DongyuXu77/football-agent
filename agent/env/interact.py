from agent.base.meta import agent

class interactor(agent):
    r"""
    """

    def __init__(self, 
                 system_prompt: str="您需要将场上结构化的结果数据转换为文本化表达",
                 ) -> None:
        r"""
        """
        super().__init__(system_prompt)
    
    def wrap_input_content(self, result: str="", output_format: str="") -> None:
        r"""
        """
        self.wrap_content = "当前结构化的结果数据为:"+result+"\n请问结果数据的文本化表达为({output_format})?"
    