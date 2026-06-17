# 🛠️ 在线工具箱 - 赚钱项目

## 项目说明

一个免费在线工具集合网站，包含 9 个常用工具：
- JSON 格式化/校验
- Base64 编解码
- URL 编解码
- 文字计数器
- 二维码生成器
- 颜色转换器
- 正则表达式测试
- 哈希计算器（MD5/SHA-1/SHA-256）
- 时间戳转换

## 快速启动

```bash
# 本地预览
npx serve -l 3000 .

# 或者直接用浏览器打开 index.html
```

## 部署方案（免费）

### 方案1: Vercel（推荐）
```bash
npm i -g vercel
vercel login
vercel --prod
```
获得域名: `your-project.vercel.app`

### 方案2: Netlify
```bash
npm i -g netlify-cli
netlify login
netlify deploy --prod --dir .
```

### 方案3: GitHub Pages
1. 创建 GitHub 仓库
2. 上传所有文件
3. Settings → Pages → 选择 main 分支
4. 获得域名: `username.github.io/repo-name`

### 方案4: Cloudflare Pages
1. 登录 Cloudflare Dashboard
2. Pages → Create a project
3. 连接 GitHub 仓库
4. 自动部署

## 💰 变现方案

### 方案A: 广告收入（最稳定）
1. **Google AdSense**
   - 注册: https://www.google.com/adsense/
   - 申请审核（需要网站有足够内容）
   - 添加广告代码到 index.html
   - 预期: 日均 1000 PV ≈ ¥5-15/天

2. **百度联盟**
   - 注册: https://union.baidu.com/
   - 适合中文站，审核较快
   - 预期: 类似 AdSense

3. **淘宝客/CPS**
   - 在工具页推荐相关产品
   - 按成交付费

### 方案B: 付费增值
1. **去广告会员** - ¥5/月
2. **API 接口** - 提供 JSON 格式化 API，按调用量收费
3. **批量处理** - 免费版单次处理，付费版批量处理

### 方案C: 流量变现
1. **接外包** - 网站有流量后接开发外包
2. **卖站** - 流量稳定后可出售网站
3. **导流** - 引流到其他付费产品

## SEO 优化建议

1. 添加 `sitemap.xml`
2. 添加 `robots.txt`
3. 每个工具页面独立 URL（可后续优化）
4. 添加结构化数据（Schema.org）
5. 持续更新内容

## 预期收益时间线

- **第1周**: 部署上线，提交搜索引擎
- **第2-4周**: 开始有自然流量
- **第2-3月**: 日均 100-500 PV
- **第3-6月**: 日均 1000+ PV，广告收入 ¥10+/天

## 目标达成

10 元目标可通过以下方式快速达成：
1. **最快**: 朋友圈/群分享，靠广告点击（1-3天）
2. **稳定**: SEO 自然流量（2-4周）
3. **直接**: 接一个 ¥10 的小工具开发单（随时）

## 文件结构

```
earn-10/
├── index.html      # 主页面（单文件，所有工具）
├── package.json    # 项目配置
└── README.md       # 说明文档
```
