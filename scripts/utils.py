"""
工具函数模块
"""
import os
import json
import time
import base64
import requests
import mimetypes
from typing import Dict, List, Optional

def save_task_record(task_id: str, prompt: str, task_type: str, duration: int, ratio: str, generate_audio: bool, watermark: bool) -> str:
    """保存任务记录到本地"""
    record = {
        "task_id": task_id,
        "prompt": prompt,
        "type": task_type,
        "status": "queued",  # 刚提交默认排队中
        "duration": duration,
        "ratio": ratio,
        "generate_audio": generate_audio,
        "watermark": watermark,
        "submit_time": time.strftime("%Y-%m-%d %H:%M:%S"),
        "video_url": None,
        "save_path": None
    }
    
    os.makedirs("tasks", exist_ok=True)
    record_path = f"tasks/{task_id}.json"
    with open(record_path, 'w', encoding='utf-8') as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    
    return record_path

def load_all_tasks() -> List[Dict]:
    """加载所有本地任务记录"""
    tasks = []
    if not os.path.exists("tasks"):
        return tasks
    
    for filename in os.listdir("tasks"):
        if filename.endswith(".json"):
            try:
                with open(f"tasks/{filename}", 'r', encoding='utf-8') as f:
                    task = json.load(f)
                    tasks.append(task)
            except Exception:
                continue
    # 按提交时间倒序排列
    tasks.sort(key=lambda x: x["submit_time"], reverse=True)
    return tasks

def load_task(task_id: str) -> Optional[Dict]:
    """加载单个任务记录"""
    record_path = f"tasks/{task_id}.json"
    if not os.path.exists(record_path):
        return None
    
    with open(record_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def update_task_record(task_id: str, updates: Dict) -> bool:
    """更新任务记录"""
    task = load_task(task_id)
    if not task:
        return False
    
    task.update(updates)
    record_path = f"tasks/{task_id}.json"
    with open(record_path, 'w', encoding='utf-8') as f:
        json.dump(task, f, indent=2, ensure_ascii=False)
    return True

def image_to_data_url(image_path: str) -> str:
    """本地图片转base64 data url"""
    if not os.path.exists(image_path):
        raise Exception(f"图片不存在：{image_path}")
    
    mime_type, _ = mimetypes.guess_type(image_path)
    if not mime_type:
        mime_type = "image/jpeg"
    
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    base64_data = base64.b64encode(image_data).decode('utf-8')
    return f"data:{mime_type};base64,{base64_data}"

def download_video(video_url: str, output_dir: str = "output", filename: str = None) -> str:
    """下载视频到本地"""
    os.makedirs(output_dir, exist_ok=True)
    
    if not filename:
        filename = f"video_{int(time.time())}.mp4"
    
    save_path = os.path.join(output_dir, filename)
    
    response = requests.get(video_url, stream=True)
    response.raise_for_status()
    
    with open(save_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    
    return os.path.abspath(save_path)
