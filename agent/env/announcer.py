import os

from agent.base.meta import agent

class announcer(agent):
    r"""
    """

    def __init__(self,
                 system_prompt: str="您是一名场上广播员，您需要根据用户提供的文档将场上结构化的实时状态数据转换为对应的实时状态文本"
                 ) -> None:
        r"""
        """
        super().__init__(system_prompt)
    
    def wrap_input_content(self, content: str, document_path: str) -> None:
        r"""
        """
        if not os.path.exists(document_path):
            raise FileNotFoundError(f" the announcer document file in path :{document_path} doesn't exist")
        f = open(document_path, 'r')
        data = f.read()
        self.wrap_content = "用户提供的文档为:"+data+"当前的实时状态数据为:"+content