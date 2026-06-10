"""
查询任务状态入口
用法：
python query.py                    # 查询所有未完成的任务
python query.py <task_id>          # 查询单个任务状态
python query.py --all              # 查询所有任务（包括已完成/失败的）
"""
import sys
import argparse
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import load_config
from scripts.api import init_client, get_task_status
from scripts.utils import load_all_tasks, load_task, update_task_record, download_video

def query_single_task(client, task_id):
    """查询单个任务"""
    task = load_task(task_id)
    if not task:
        print(f"未找到任务ID：{task_id} 的本地记录")
        return
    
    print(f"查询任务 {task_id} 状态...")
    status_data = get_task_status(client, task_id)
    new_status = status_data["status"]
    
    if new_status != task["status"]:
        update_task_record(task_id, {"status": new_status})
        print(f"状态更新：{task['status']} -> {new_status}")
    else:
        print(f"当前状态：{new_status}")
    
    if new_status == "succeeded":
        # 提取视频地址
        video_url = status_data.get("content", {}).get("video_url")
        if video_url and not task.get("save_path"):
            print("视频生成完成，正在自动下载...")
            try:
                filename = f"{task_id}_{task['prompt'][:20].replace(' ', '_')}.mp4"
                save_path = download_video(video_url, filename=filename)
                update_task_record(task_id, {
                    "video_url": video_url,
                    "save_path": save_path
                })
                print(f"视频已保存到：{save_path}")
            except Exception as e:
                print(f"视频下载失败：{str(e)}")
                print(f"视频地址：{video_url}")
    
    elif new_status == "failed":
        error_msg = status_data.get("error", {}).get("message", "未知错误")
        print(f"生成失败：{error_msg}")
        update_task_record(task_id, {"error_msg": error_msg})

def query_all_tasks(client, only_running: bool = True):
    """批量查询所有任务"""
    tasks = load_all_tasks()
    if not tasks:
        print("没有找到任何任务记录")
        return
    
    print(f"共找到 {len(tasks)} 个任务记录")
    print("-" * 80)
    
    for task in tasks:
        task_id = task["task_id"]
        status = task["status"]
        
        if only_running and status not in ["running", "queued"]:
            continue
        
        print(f"任务ID：{task_id}")
        print(f"描述：{task['prompt'][:50]}{'...' if len(task['prompt'])>50 else ''}")
        print(f"状态：{status}")
        print(f"提交时间：{task['submit_time']}")
        
        if status in ["running", "queued"]:
            # 查询最新状态
            try:
                status_data = get_task_status(client, task_id)
                new_status = status_data["status"]
                if new_status != status:
                    update_task_record(task_id, {"status": new_status})
                    print(f"最新状态：{new_status}")
                
                if new_status == "succeeded":
                    video_url = status_data.get("content", {}).get("video_url")
                    if video_url and not task.get("save_path"):
                        print("视频生成完成，正在自动下载...")
                        try:
                            filename = f"{task_id}_{task['prompt'][:20].replace(' ', '_')}.mp4"
                            save_path = download_video(video_url, filename=filename)
                            update_task_record(task_id, {
                                "video_url": video_url,
                                "save_path": save_path
                            })
                            print(f"视频已保存到：{save_path}")
                        except Exception as e:
                            print(f"视频下载失败：{str(e)}")
                elif new_status == "failed":
                    error_msg = status_data.get("error", {}).get("message", "未知错误")
                    print(f"生成失败：{error_msg}")
                    update_task_record(task_id, {"error_msg": error_msg})
            except Exception as e:
                print(f"查询失败：{str(e)}")
        
        if task.get("save_path"):
            print(f"已保存到：{task['save_path']}")
        
        print("-" * 80)

def main():
    parser = argparse.ArgumentParser(description="查询视频生成任务状态")
    parser.add_argument("task_id", nargs="?", help="要查询的任务ID，不填则查询所有进行中的任务")
    parser.add_argument("--all", action="store_true", help="查询所有任务（包括已完成/失败的）")
    parser.add_argument("--config", type=str, default="config/config.yaml", help="配置文件路径")
    
    args = parser.parse_args()
    
    # 加载配置和初始化客户端
    config = load_config(args.config)
    client = init_client(config["api_key"])
    
    if args.task_id:
        # 查询单个任务
        query_single_task(client, args.task_id)
    else:
        # 查询多个任务
        query_all_tasks(client, only_running=not args.all)

if __name__ == "__main__":
    main()
