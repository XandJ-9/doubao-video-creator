"""
提交视频生成任务入口
用法：
python submit.py --prompt "视频描述" --duration 5 --ratio 16:9
python submit.py --prompt "视频描述" --image ./test.jpg --duration 3
"""
import argparse
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scripts.config import load_config
from scripts.api import init_client, submit_text_task, submit_image_task
from scripts.utils import save_task_record, image_to_data_url

def main():
    parser = argparse.ArgumentParser(description="提交豆包视频生成任务")
    parser.add_argument("--prompt", type=str, required=True, help="视频内容描述")
    parser.add_argument("--image", type=str, help="本地图片路径，提供则使用图生视频模式")
    parser.add_argument("--duration", type=int, default=5, choices=range(5, 16), help="视频时长，单位秒，默认5秒")
    parser.add_argument("--ratio", type=str, default="16:9", choices=["16:9", "9:16", "1:1", "adaptive"], help="视频比例，默认16:9")
    parser.add_argument("--audio", action="store_true", help="是否生成带音效的视频")
    parser.add_argument("--no-watermark", action="store_true", help="关闭水印")
    parser.add_argument("--config", type=str, default="config/config.yaml", help="配置文件路径")
    
    args = parser.parse_args()
    
    # 加载配置和初始化客户端
    config = load_config(args.config)
    client = init_client(config["api_key"])
    
    watermark = not args.no_watermark
    generate_audio = args.audio
    
    # 提交任务
    if args.image:
        # 图生视频模式
        image_url = image_to_data_url(args.image)
        task_data = submit_image_task(
            client=client,
            prompt=args.prompt,
            image_url=image_url,
            duration=args.duration,
            ratio=args.ratio if args.ratio != "adaptive" else "adaptive",
            watermark=watermark,
            generate_audio=generate_audio
        )
        task_type = "image2video"
    else:
        # 文生视频模式
        task_data = submit_text_task(
            client=client,
            prompt=args.prompt,
            duration=args.duration,
            ratio=args.ratio,
            watermark=watermark,
            generate_audio=generate_audio
        )
        task_type = "text2video"
    
    task_id = task_data["id"]
    
    # 保存任务记录（用我们自己已知的参数，不用从返回结果里读）
    save_task_record(
        task_id=task_id,
        prompt=args.prompt,
        task_type=task_type,
        duration=args.duration,
        ratio=args.ratio,
        generate_audio=generate_audio,
        watermark=watermark
    )
    
    # 输出结果
    print("任务提交成功！任务ID：" + task_id)
    print("您可以随时运行 `doubao-video query " + task_id + "` 查询任务状态")
    print("或直接运行 `doubao-video query` 查看所有进行中的任务")
    print("生成完成后会自动下载到 output/ 目录")

if __name__ == "__main__":
    main()
