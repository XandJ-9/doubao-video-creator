# 快速使用指南
## 1. 申请API Key
1. 访问火山引擎方舟平台：https://console.volcengine.com/ark/
2. 注册账号并开通服务
3. 获取你的API Key
## 2. 配置
复制`config/config.example.yaml`为`config/config.yaml`，填入你的API Key
## 3. 安装依赖
Windows用户运行`install.bat`，Mac/Linux用户运行`bash install.sh`
## 4. 生成第一个视频
```bash
doubao-video submit --prompt "动漫风格，蓝天下风吹草地，阳光明媚" --duration 5 --ratio 16:9
```
## 5. 查询生成状态
```bash
doubao-video query
```
生成成功会自动下载到`output/`目录
## 常见问题
### 生成失败提示版权限制
请不要使用知名IP名称（如"鬼灭之刃"、"迪士尼"等），改用风格描述，例如"日式热血动漫风格，少年穿黑橙相间羽织，手持武士刀"
### 生成速度慢
5秒视频通常需要2-3分钟，10秒视频需要3-5分钟，提交任务后可以关闭终端，后续随时查询状态即可
### 视频效果不好
请优化提示词，增加更多细节：风格、光线、运镜方式、动作、背景等，描述越具体效果越好
