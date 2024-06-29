from agent.base.meta import agent

class commentator(agent):
    r"""
    """

    def __init__(self, 
                 system_prompt: str="请深吸一口气并仔细分析当前实际执行结果与期望执行结果是否一致，回答过程请严格保持风格统一",
                 ) -> None:
        r"""
        """
        super().__init__(system_prompt)

    def wrap_input_content(self, result: str, expect: str, output_format: str='') -> None:
        r"""
        """
        self.wrap_content = "当前实际执行结果为:"+result+"\n预期执行的结果为:"+expect+"\n请问是否完成了预期阶段执行结果，如果没有，请给出对应的建议({output_format})?"
    