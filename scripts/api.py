"""
API调用封装模块
"""
from volcenginesdkarkruntime import Ark
from typing import Dict, List, Optional

def init_client(api_key: str, base_url: str = "https://ark.cn-beijing.volces.com/api/v3") -> Ark:
    """初始化API客户端"""
    return Ark(base_url=base_url, api_key=api_key)

def submit_text_task(client: Ark, prompt: str, duration: int = 5, ratio: str = "16:9", 
                    watermark: bool = True, generate_audio: bool = False) -> Dict:
    """提交文生视频任务"""
    result = client.content_generation.tasks.create(
        model="doubao-seedance-2-0-260128",
        content=[
            {
                "type": "text",
                "text": prompt
            }
        ],
        ratio=ratio,
        duration=duration,
        watermark=watermark,
        generate_audio=generate_audio,
    )
    return result.model_dump()

def submit_image_task(client: Ark, prompt: str, image_url: str, duration: int = 5, 
                     ratio: str = "adaptive", watermark: bool = True, 
                     generate_audio: bool = False) -> Dict:
    """提交单图生视频任务"""
    result = client.content_generation.tasks.create(
        model="doubao-seedance-2-0-260128",
        content=[
            {
                "type": "text",
                "text": prompt
            },
            {
                "type": "image_url",
                "image_url": {"url": image_url}
            }
        ],
        ratio=ratio,
        duration=duration,
        watermark=watermark,
        generate_audio=generate_audio,
    )
    return result.model_dump()

def get_task_status(client: Ark, task_id: str) -> Dict:
    """查询任务状态"""
    result = client.content_generation.tasks.get(task_id=task_id)
    return result.model_dump()

def delete_task(client: Ark, task_id: str) -> bool:
    """取消/删除任务"""
    try:
        client.content_generation.tasks.delete(task_id=task_id)
        return True
    except Exception:
        return False
