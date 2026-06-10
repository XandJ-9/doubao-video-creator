"""
手动下载视频入口
用法：
python download.py <task_id>          # 下载指定任务的视频
python download.py <task_id> --output ./mydir  # 下载到指定目录
"""
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import load_config
from scripts.api import init_client, get_task_status
from scripts.utils import load_task, update_task_record, download_video

def main():
    parser = argparse.ArgumentParser(description="手动下载生成好的视频")
    parser.add_argument("task_id", help="要下载的任务ID")
    parser.add_argument("--output", type=str, default="output", help="下载到指定目录")
    parser.add_argument("--filename", type=str, help="自定义保存文件名")
    parser.add_argument("--config", type=str, default="config/config.yaml", help="配置文件路径")
    
    args = parser.parse_args()
    
    # 加载配置和初始化客户端
    config = load_config(args.config)
    client = init_client(config["api_key"])
    
    # 查询任务状态
    task = load_task(args.task_id)
    if not task:
        print(f"未找到任务ID：{args.task_id} 的本地记录")
        return
    
    status_data = get_task_status(client, args.task_id)
    if status_data["status"] != "succeeded":
        print(f"任务未完成，当前状态：{status_data['status']}")
        return
    
    # 获取视频地址
    video_url = status_data.get("content", {}).get("video_url")
    if not video_url:
        print("未找到视频地址")
        return
    
    # 下载视频
    try:
        save_path = download_video(video_url, output_dir=args.output, filename=args.filename)
        update_task_record(args.task_id, {
            "video_url": video_url,
            "save_path": save_path
        })
        print(f"视频已成功下载到：{save_path}")
    except Exception as e:
        print(f"下载失败：{str(e)}")
        print(f"视频地址：{video_url}")

if __name__ == "__main__":
    main()
