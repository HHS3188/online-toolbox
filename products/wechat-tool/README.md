# 微信聊天记录分析工具

## 功能
- 加载微信聊天记录（支持 TXT、CSV、JSON 格式）
- 关键词搜索和正则表达式搜索
- 统计分析（消息数、发言排行、时间分布）
- 查找链接、图片、红包消息
- 词频统计
- 导出为多种格式
- 生成完整分析报告

## 使用方法

```bash
# 分析聊天记录
python wechat_tool.py analyze -i chat.txt

# 搜索关键词
python wechat_tool.py search -i chat.txt -k "关键词"

# 正则搜索
python wechat_tool.py search -i chat.txt -r "\d{11}"

# 导出为CSV
python wechat_tool.py export -i chat.txt -f csv -o output.csv

# 生成报告
python wechat_tool.py report -i chat.txt -o report.txt
```

## 适用人群
- 想要分析聊天记录的人
- 需要查找历史消息的人
- 想要统计聊天数据的人

## 售价建议
¥15-30
