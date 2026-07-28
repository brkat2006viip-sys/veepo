import aiohttp
import asyncio
import logging
from typing import Optional, Dict, Any
from app.config import settings

logger = logging.getLogger(__name__)

class AgentRouterClient:
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None):
        self.base_url = base_url or settings.AGENTROUTER_API_URL
        self.api_key = api_key

    async def test_connection(self) -> bool:
        if not self.api_key:
            return False
        url = f"{self.base_url}/v1/ping"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers=headers, timeout=10) as resp:
                    logger.debug("AgentRouter test connection status: %s", resp.status)
                    return resp.status == 200
            except Exception as e:
                logger.exception("AgentRouter test failed: %s", e)
                return False

    async def send_files_for_processing(self, files: Dict[str, bytes], instructions: str, provider: str, model: str) -> Dict[str, Any]:
        """
        files: mapping filename->bytes
        instructions: user instructions
        provider/model: provider selection
        Returns a dict with results, e.g., changed files, logs, artifacts
        """
        url = f"{self.base_url}/v1/process"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        data = aiohttp.FormData()
        data.add_field("provider", provider)
        data.add_field("model", model)
        data.add_field("instructions", instructions)
        for name, content in files.items():
            data.add_field("files", content, filename=name, content_type="application/octet-stream")
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, data=data, headers=headers, timeout=120) as resp:
                    text = await resp.text()
                    if resp.status != 200:
                        logger.error("AgentRouter returned %s: %s", resp.status, text)
                        return {"ok": False, "status": resp.status, "text": text}
                    j = await resp.json()
                    return {"ok": True, "data": j}
            except Exception as e:
                logger.exception("Failed to call AgentRouter: %s", e)
                return {"ok": False, "error": str(e)}
