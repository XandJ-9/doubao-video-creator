# 豆包视频生成API参考
## 模型名称
doubao-seedance-2-0-260128
## 支持参数
### 通用参数
- prompt: 视频内容描述，支持中文，描述越详细效果越好
- duration: 视频时长，单位秒，支持5-15秒
- ratio: 视频比例，支持16:9, 9:16, 1:1, adaptive（自适应图片比例）
- watermark: 是否添加水印，默认true
- generate_audio: 是否生成带环境音效的视频，默认false
### 图生视频参数
- image_url: 图片的base64 URL，或者网络图片URL
## 任务状态
- queued: 排队中
- running: 生成中
- succeeded: 生成成功
- failed: 生成失败
## 错误码
- InvalidCredential: API密钥无效
- InvalidParameter: 参数错误
- PermissionDenied: 没有模型调用权限
- QuotaExceeded: 额度不足
