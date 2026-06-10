#!/usr/bin/env python3
"""
豆包视频生成工具统一入口
用法：
doubao-video submit --prompt "视频描述"    提交任务
doubao-video query [task_id]              查询任务
doubao-video download <task_id>           下载视频
"""
import sys
import os

# 把根目录加入Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_help():
    print("豆包视频生成工具 v1.0")
    print("")
    print("用法:")
    print("  doubao-video submit [选项]    提交视频生成任务")
    print("  doubao-video query [任务ID]   查询任务状态，不填ID则查询所有进行中的任务")
    print("  doubao-video download <任务ID> 下载已生成的视频")
    print("  doubao-video help             显示帮助信息")
    print("")
    print("示例:")
    print("  doubao-video submit --prompt '蓝天下风吹草地' --duration 5")
    print("  doubao-video query cgt-xxx")
    print("  doubao-video download cgt-xxx")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print_help()
        sys.exit(0)
    
    cmd = sys.argv[1]
    
    if cmd == "submit":
        from cli.submit import main
        main()
    elif cmd == "query":
        from cli.query import main
        main()
    elif cmd == "download":
        from cli.download import main
        main()
    elif cmd == "help":
        print_help()
    else:
        print(f"未知命令: {cmd}")
        print_help()
        sys.exit(1)
