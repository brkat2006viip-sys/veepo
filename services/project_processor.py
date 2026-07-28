import os
import shutil
import zipfile
import tempfile
from typing import Dict, Any
from app.schemas import ProjectAnalysis
from utils.file_safe import safe_extract_zip
from utils.security import generate_random_name
from ai.agentrouter import AgentRouterClient
from app.config import settings
import logging

logger = logging.getLogger(__name__)

class SimpleProject:
    def __init__(self, name: str, path: str, zip_path: str = None):
        self.name = name
        self.path = path
        self.zip_path = zip_path

class ProjectProcessor:
    def __init__(self, db=None, user=None):
        self.db = db
        self.user = user
        self.upload_dir = os.path.abspath("uploads")
        os.makedirs(self.upload_dir, exist_ok=True)
        self.temp_dir = os.path.abspath("temp")
        os.makedirs(self.temp_dir, exist_ok=True)

    async def create_from_zip(self, zip_path: str) -> SimpleProject:
        # Generate project name
        name = generate_random_name(prefix="proj_")
        dest = os.path.join(self.upload_dir, name)
        os.makedirs(dest, exist_ok=True)
        safe_extract_zip(zip_path, dest)
        zip_copy = os.path.join(self.upload_dir, f"{name}.zip")
        shutil.copy2(zip_path, zip_copy)
        return SimpleProject(name=name, path=dest, zip_path=zip_copy)

    async def analyze_project(self, project_path: str) -> ProjectAnalysis:
        file_count = 0
        loc = 0
        languages = {}
        files = {}
        for root, dirs, filenames in os.walk(project_path):
            for fn in filenames:
                file_count += 1
                p = os.path.join(root, fn)
                try:
                    size = os.path.getsize(p)
                    files[os.path.relpath(p, project_path)] = size
                    # estimate lines for text files
                    if size < 10 * 1024 * 1024:  # skip huge files
                        try:
                            with open(p, "r", encoding="utf-8", errors="ignore") as fh:
                                lines = fh.readlines()
                            loc += len(lines)
                            ext = os.path.splitext(fn)[1].lower().lstrip(".")
                            languages[ext or "unknown"] = languages.get(ext or "unknown", 0) + len(lines)
                        except Exception:
                            continue
                except Exception:
                    continue
        return ProjectAnalysis(file_count=file_count, loc=loc, languages=languages, files=files)

    async def prepare_files_for_agent(self, project_path: str) -> Dict[str, bytes]:
        files = {}
        for root, dirs, filenames in os.walk(project_path):
            for fn in filenames:
                p = os.path.join(root, fn)
                rel = os.path.relpath(p, project_path)
                try:
                    with open(p, "rb") as fh:
                        files[rel] = fh.read()
                except Exception:
                    continue
        return files

    async def send_to_agentrouter(self, project_path: str, instructions: str, api_key: str, provider: str = "default", model: str = "default"):
        client = AgentRouterClient(api_key=api_key, base_url=settings.AGENTROUTER_API_URL)
        files = await self.prepare_files_for_agent(project_path)
        return await client.send_files_for_processing(files, instructions, provider, model)

    async def package_project(self, project_path: str, out_zip: str):
        base = out_zip if out_zip.endswith(".zip") else out_zip + ".zip"
        shutil.make_archive(base_name=base.replace(".zip",""), format="zip", root_dir=project_path)
        return base
