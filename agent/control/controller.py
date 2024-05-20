from agent.base.meta import agent

class controller(agent):
    r"""
    """

    def __init__(self, 
                 system_prompt: str="请深吸一口气并仔细思考如何根据需要达成的目标及当前场上的局势提供完成该战术所需要调用的子模型，回答过程请严格保持风格统一",
                 ) -> None:
        r"""
        """
        super().__init__(system_prompt)

    def wrap_input_content(self, content: str, status: str, output_format: str='') -> None:
        r"""
        """
        self.wrap_content = "当前的实时状态为:"+status+"\n需要达成的目标是:"+content+"\n能够调用子模型所具有的特征是:"+self.model_info+f"\n请问达成该战术目标所需要调用的子模型是({output_format})?"
    
    def get_model_info(self):
        self.model_info="模型1:进攻能力强,用于射门,消耗体力大\n模型2:集中包围持球者,体力消耗大;模型3:球员回到禁区,体力消耗小"