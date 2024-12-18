import asyncio
import logging
import ray
from pycityagent.agent import Agent
from pycityagent.economy.econ_client import EconomyClient
from pycityagent.environment.simulator import Simulator
from pycityagent.llm.llm import LLM
from pycityagent.llm.llmconfig import LLMConfig
from pycityagent.message import Messager

@ray.remote
class AgentGroup:
    def __init__(self, agents: list[Agent], config: dict):
        self.agents = agents
        self.config = config
        self.messager = Messager(config["simulator_request"]["mqtt"]["server"], config["simulator_request"]["mqtt"]["port"])
        self.initialized = False

        # Step:1 prepare LLM client
        llmConfig = LLMConfig(config["llm_request"])
        logging.info("-----Creating LLM client in remote...")
        self.llm = LLM(llmConfig)

        # Step:2 prepare Simulator
        logging.info("-----Creating Simulator in remote...")
        self.simulator = Simulator(config["simulator_request"])

        # Step:3 prepare Economy client
        logging.info("-----Creating Economy client in remote...")
        self.economy_client = EconomyClient(config["simulator_request"]["economy"]['server'])

        for agent in self.agents:
            agent.set_llm_client(self.llm)
            agent.set_simulator(self.simulator)
            agent.set_economy_client(self.economy_client)
            agent.set_messager(self.messager)

    async def init_agents(self):
        for agent in self.agents:
            await agent.bind_to_simulator()
        self.id2agent = {agent._agent_id: agent for agent in self.agents}
        await self.messager.connect()
        if self.messager.is_connected():
            await self.messager.start_listening()
            for agent in self.agents:
                agent.set_messager(self.messager)
                topic = f"/agents/{agent._agent_id}/chat"
                await self.messager.subscribe(topic, agent)
        self.initialized = True

    async def step(self):
        if not self.initialized:
            await self.init_agents()

        # Step 1: 如果 Messager 无法连接，则跳过消息接收
        if not self.messager.is_connected():
            logging.warning("Messager is not connected. Skipping message processing.")
            # 跳过接收和分发消息
            tasks = [agent.run() for agent in self.agents]
            await asyncio.gather(*tasks)
            return

        # Step 2: 从 Messager 获取消息
        messages = await self.messager.fetch_messages()

        # Step 3: 分发消息到对应的 Agent
        for message in messages:
            topic = message.topic.value
            payload = message.payload

            # 添加解码步骤，将bytes转换为str
            if isinstance(payload, bytes):
                payload = payload.decode('utf-8')

            # 提取 agent_id（主题格式为 "/agents/{agent_id}/chat"）
            _, agent_id, _ = topic.strip("/").split("/")
            agent_id = int(agent_id)

            if agent_id in self.id2agent:
                agent = self.id2agent[agent_id]
                await agent.handle_message(payload)

        # Step 4: 调用每个 Agent 的运行逻辑
        tasks = [agent.run() for agent in self.agents]
        await asyncio.gather(*tasks)

    async def run(self, day: int = 1):
        """运行模拟器

        Args:
            day: 运行天数,默认为1天
        """
        try:
            # 获取开始时间
            start_time = await self.simulator.get_time()
            # 计算结束时间（秒）
            end_time = start_time + day * 24 * 3600  # 将天数转换为秒
            
            while True:
                current_time = await self.simulator.get_time()
                if current_time >= end_time:
                    break
                
                await self.step()

        except Exception as e:
            logging.error(f"模拟器运行错误: {str(e)}")
            raise

