# 常用技术词汇与术语正误表（Word List）

融合 Google 开发者文档词汇表与中文技术文档高频词汇规范，用于在撰写和审校时快速核对中英文用词、交互动词、禁用词替换及英文专有名词拼写。

## 一、UI 交互动词快速选词表

| 界面操作场景 | 推荐中文用词（对应英文） | 禁用/不推荐写法 |
|---|---|---|
| 桌面端鼠标左键操作 | **点击**（click） | 单击、点选、点击在……上（click on）、敲击（hit） |
| 桌面端鼠标右键 / 双击 | **右键点击**、**双击** | 右击、双点 |
| 移动端触摸屏操作 | **点按**（tap）、**按住**（touch & hold） | 点击、长按（long press，Android 规范优先用“按住”） |
| 复选框（Checkbox）操作 | **选中**（select）/ **清除**（clear） | 勾选、打勾、取消勾选（check / uncheck） |
| 下拉菜单、单选按钮或列表项 | **选择**（select / choose） | 挑选、点选 |
| 在文本框中填写内容 | **输入**（enter，优先）/ **键入**（type） | 填入、打字、敲入 |
| 物理键盘按键或机械按钮 | **按**（press，如“按 `Enter` 键”） | 敲击（hit）、点击 `Enter` 键 |
| 鼠标悬停等待反应 | **将指针悬停在……上**（hold the pointer over） | 悬停（hover，口语中若用“悬停”需指明对象：“将鼠标悬停在**设置**上”） |
| 拖拽操作 | **拖动**（drag）；作定语用**拖放式**（drag-and-drop） | 点击并拖动 |
| 填写表单 vs. 填写单个字段 | **填写**表单（fill out）；在字段中**输入**（enter） | — |
| 开关（Toggle）控件 | **开启 / 关闭**（turn on / turn off）或点击 **XX** **开关** | 不要把“切换（toggle）”当及物动词直接接功能名 |

## 二、常见禁用词与规范替换总表

| 避免写法（违例 / 翻译腔 / 旧术语） | 推荐写法（规范中文技术表达） |
|---|---|
| `用户`（指代正在读文档的开发者） | **你**（或**您**，全文统一）；`用户`仅指最终使用者（End User） |
| `让我们（Let's）……` | 直接用祈使句，或写**建议…… / 你可以……** |
| `使得你能够 / 允许你（enables / allows you to）` | **支持…… / 借助……，你可以……** |
| `将会（will，用于描述常规确定行为）` | **会**，或直接陈述（如“服务器返回响应”） |
| `进行配置 / 进行安装 / 进行初始化` | 直接用动词：**配置 / 安装 / 初始化** |
| `简单地 / 只需 / 轻松 / 显然 / 毫无疑问` | **直接删除**（客观陈述步骤，不评价难易） |
| `仔细地 / 正确地 / 妥善地（carefully / properly）` | **直接删除**，改为可验证的具体指标（如“确保端口 `443` 已开放”） |
| `目前 / 现在 / 最新 / 即将 / 截至本文撰写时` | **直接删除**，或锚定到具体版本号/日期（如“自 v2.0 起”） |
| `e.g.` / `i.e.` / `etc.` / `vs.` / `aka` | **例如** / **即（也就是说）** / **等** / **对比（与……相比）** / **又称** |
| `和/或（and/or）` | **A、B 或两者兼具**（通常直接写“A 或 B”即可涵盖） |
| `由于 / 鉴于（当翻译英文 as / since / while 时）` | 明确区分因果与时间：表原因用**因为 / 由于**，表时间用**在……之后**，表转折用**虽然 / 尽管** |
| `通过……的方式（via / by using）` | **使用…… / 通过……** |
| `白名单 / 黑名单 / 灰名单` | **允许列表 / 拒绝列表（或阻止列表）/ 观察列表**（代码字面量用 `` `whitelist` ``） |
| `主从（master / slave）` | **主节点 / 副本节点（primary / replica）**、**控制节点 / 工作节点** |
| `中间人攻击（man-in-the-middle）` | **在途攻击 / 路径劫持攻击（on-path attacker）** |
| `健全性检查（sanity check）` | **快速检查 / 完整性检查 / 置信度检查** |
| `哑变量 / 傻瓜值（dummy variable / value）` | **占位符 / 示例值 / 测试值**（统计学中称“虚拟变量/指示变量”） |
| `卡死 / 挂起（hang / hung）` | **停止响应 / 未响应** |
| `杀死进程（kill）` | **终止 / 停止 / 结束进程**（专门讲解 Linux `kill` 命令或 `SIGKILL` 信号除外） |
| `汉堡菜单 / 三道杠图标 / 三个点图标` | 直接写元素的无障碍标签名：**菜单**、**更多操作** |
| `弹窗（pop-up / popup）` | **对话框**（dialog）或**菜单**（menu） |
| `下拉（drop-down，单独作名词）` | **下拉列表 / 下拉菜单**（操作步骤中通常直接写“在**区域**列表中选择……”） |
| `勾上 / 取消勾选` | **选中 / 清除**（复选框） |
| `解压（写成 unzip / untar 动词混排）` | **解压** ZIP 文件 / **提取** tar 归档文件 |
| `2.2+` / `2.2 及更高版本` | **2.2 及更高版本**或 **2.2 及之后的版本**（避免在正文中写 `2.2+` 符号） |
| `10x`（在散文句子中） | **10 倍**（如“吞吐量提升 10 倍”） |
| `foo` / `bar` / `baz` | 使用有实际业务意义的占位符名称（如 `EXAMPLE_BUCKET`、` item_count`） |
| `点击这里 / 此文档 / 这篇博客`（作链接文本） | 使用**目标页面的具体标题**作为链接文本 |
| `如上图 / 下图 / 左边 / 右侧所示` | **如前文所示 / 如下图所示（仅限紧邻下方时）/ 如图 1 所示** |

## 三、中文技术文档中的高频英文词汇拼写与混排准则

在中文技术文档中保留英文专业词汇或代码术语时，必须严格遵守其官方拼写、大小写与连字符规范：

### 1. 官方大小写易错词（切勿写错大小写）
- **云与基础设施**：`Google Cloud`（不要写 `GCP`）、`Kubernetes`（正文中尽量拼写全称，少用 `k8s`）、`Docker`、`Terraform`、`Linux`、`macOS`、`Windows`、`iOS`、`Android`。
- **语言与框架**：`JavaScript`、`TypeScript`、`Node.js`、`Python`、`Go`（或 `Golang`）、`GraphQL`、`gRPC`、`REST`、`WebAssembly`（缩写为 `Wasm`，非 `WASM`）。
- **数据库与中间件**：`PostgreSQL`、`MySQL`、`MongoDB`、`Redis`、`BigQuery`、`Cloud Spanner`。
- **网络与安全**：`HTTP`、`HTTPS`、`HTTP/2`、`TCP/IP`、`IPv4`、`IPv6`、`IPsec`（小写 `sec`）、`OAuth 2.0`（带空格和 `.0`，不写 `OAuth2`）、`OpenID Connect`、`TLS`、`SSH`、`JSON`、`YAML`、`TOML`、`UTF-8`、`Base64`、`SHA-1`、`SHA-256`。
- **通用缩写与标识**：`ID`（全大写，不写 `Id` 或 `id`，代码标识符除外）、`API`、`SDK`、`CLI`、`GUI`、`UI`、`URL`、`URI`、`I/O`、`IoT`（中间 `o` 小写）、`AI`、`ML`、`Wi-Fi`（带连字符，F 大写）。

### 2. 英文合成词写法（一词 vs. 两词 vs. 连字符）
当文档中包含英文术语（如在双语术语对照、英文架构图图注或代码块注释中）时：
- **合并为一个词（不加连字符或空格）**：`allowlist`、`denylist`、`autoscaling`、`backend`、`frontend`、`codebase`、`codelab`、`colocate`、`datastream`、`email`（绝不写 `e-mail`）、`endpoint`、`filename`、`hardcode`、`hostname`、`inline`、`lifecycle`、`livestream`、`login`（作名词/形容词时）、`namespace`、`prebuilt`、`runbook`、`startup`（作名词时）、`timestamp`、`toolkit`、`touchscreen`、`walkthrough`、`whitespace`、`wildcard`。
- **分开写为两个词**：`data center`、`data source`、`data type`、`file system`、`key ring`、`name server`、`web server`。
- **加连字符（Hyphenated）**：`on-premises`（绝不写 `on-premise`）、`read-only`、`long-running`、`error-prone`、`key-value`、`big-endian`、`little-endian`、`non-negative`、`non-integer`、`multi-cluster`、`multi-region`、`third-party`（作定语时；作名词时为 `third party`，绝不写 `3rd party`）。
- **动词短语（两词）vs. 名词/形容词（一词或连字符）**：
  - 登录：动词用 `sign in` / `log in`（中文写“登录”，注意是“登录”不是“登陆”！）；名词/形容词用 `sign-in` / `login`。
  - 配置/安装：动词用 `set up`，名词/形容词用 `setup`。
  - 启动：动词用 `start up`，名词用 `startup`。
  - 故障转移：动词用 `fail over`，名词用 `failover`。
  - 超时：动词用 `time out`，名词用 `timeout`。
  - 插件：动词用 `plug in`，名词用 `plugin`（或 `plug-in`）。
  - 运行时：指运行环境用 `runtime`（一词），指运行阶段耗时（相对于编译期 `compile time`）用 `run time`（两词）。

### 3. 中文近义技术词辨析（彻底杜绝错别字）
- **登录 vs. 登陆**：进入系统、账号验证一律写**“登录”**（登名入册），绝不写“登陆”（渡海抢滩上岸才叫登陆）。
- **启用 / 停用 vs. 开启 / 关闭**：功能、API、插件、服务用**“启用 / 停用（Enable / Disable）”**；开关按钮、端口、连接用**“开启 / 关闭（Turn on / Turn off / Open / Close）”**。注意：“已停用（disabled）”不等于“发生故障不可用（unavailable）”。
- **废弃（Deprecated）vs. 移除（Removed）**：**“已废弃”**表示该功能或接口仍可使用但不再推荐、未来可能删除；**“已移除”**表示在当前版本中已彻底删除、调用会报错。切勿将两者混为一谈。
- **元数据（Metadata）**、**幂等性（Idempotency）**、**句柄（Handle）**、**套接字（Socket）**、**负载（Payload / Load）**、**阈值（Threshold）**：注意“阈值”读音与写法为“阈（yù）值”，**绝不写成错别字“阀（fá）值”**。
- **目录（Directory）vs. 文件夹（Folder）**：命令行与代码路径语境下优先称为**“目录”**；图形界面（GUI）语境下可称为**“文件夹”**。
- **实参（Argument）vs. 形参/参数（Parameter）**：在命令行中，`--flag` 称为**“标志（Flag）”**或**“选项（Option）”**，传入的具体值称为**“参数（Argument）”**；在 HTTP 请求中称为**“查询参数（Query parameter）”**或**“路径参数（Path parameter）”**。
- **镜像（Image）**：提及时请明确指明是哪种镜像——**“容器镜像（Container image）”**还是**“磁盘镜像 / 系统镜像（Disk / OS image）”**，以免与普通的“图片（Image）”混淆。
- **密钥（Key）**：提及时请明确指明是哪种密钥——**“API 密钥（API key）”“SSH 密钥（SSH key）”“加密密钥（Encryption key）”**还是键值对中的**“键（Key）”**。
