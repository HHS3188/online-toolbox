# 批量文件重命名工具

## 功能
- 添加前缀/后缀
- 添加序号（001_、002_...）
- 替换文件名中的文本
- 正则表达式替换
- 修改大小写
- 添加日期前缀
- 预览模式（先看效果再执行）

## 使用方法

```bash
# 添加前缀
python batch_rename.py /path/to/files -a prefix --prefix "备份_"

# 添加序号
python batch_rename.py /path/to/files -a number --start 1

# 替换文本
python batch_rename.py /path/to/files -a replace --old "旧文本" --new "新文本"

# 正则替换
python batch_rename.py /path/to/files -a regex --pattern-regex "\d+" --new "编号"

# 添加日期
python batch_rename.py /path/to/files -a date

# 预览模式（不实际执行）
python batch_rename.py /path/to/files -a number --preview
```

## 适用人群
- 需要整理大量文件的人
- 摄影师（整理照片）
- 设计师（整理素材）
- 办公人员（整理文档）

## 售价建议
¥10-20
