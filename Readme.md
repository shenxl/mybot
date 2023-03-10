## ✅规则描述

- 指令集，所有指令以%%包裹，所有指令都与用户`creator`相关

```
 chatid: 111
 creator: 222
 creator_corpid: 3333
 content: "@自定义机器人 %help%"
 robot_key: "1111"
 reply: {…}
 reply_content: ""
 reply_creator: 0
 url: "https://f1bc8b53-fb53-4370-83d1-85dfaf6c8e00.mock.pstmn.io/mock"
 ctime: 1677849373
```



| 指令               | 作用                                                         | **对应权限**                |
| ------------------ | ------------------------------------------------------------ | --------------------------- |
| %help%             | 显示所有指令                                                 | /                           |
| %init%             | 初始化机器人。必须在回调中附加send key ,初始完成后可去除回调中的 send key信息 | rots 表，查找是否有该机器人 |
| %chats%            | 显示聊天队列信息                                             | user&assistant              |
| %chat cls n%       | 清理聊天队列(n 代表清理队列长度 ，默认全部清理)              | user&assistant              |
| %instrs%           | 显示所有的指令信息                                           | system                      |
| %instrs set xxx % | 修改某个指令的描述语                                         | system                      |
| %instrs cls xxx% | 清理指令(#xxx 代表某个指令 ，默认全部清理)                   |                             |
| %rekey%            | 手动更换秘钥                                                 | sks 表（优先级低）          |
| %channel% set  #频道 | 频道类，待定                                                 |                             |

指令可能的形式如下，内置指令

 \**info 当用户在对话开始处输入该指令，请返回固定文字：‘我现在状态一切正常’

 \**ts 当用户在对话开始处输入该指令，请将指令后面的中文翻译成英文

 \**emoji 当用户在对话开始处输入该指令，请将指令后面的文字转换成最匹配的 emoji"

 \**e2c 当用户在对话开始处输入该指令，请将指令后面的文字转换成中文"

 \**name-指令 当用户在对话开始处输入该指令，请提炼/{指令/}效果并为其命名。名字小于8个字.注意：仅输出名字，不要输出名字以外的任何内容！"

## ✅表设计（增、查）

可能的表有

- ~~bots: 记录 woa 机器人的robot_key 与 回调的关系（后期再看有没有注册的必要）~~

| ***\*字段\**** | ***\*备注\**** |
| -------------- | -------------- |
| robot_key      | 机器人ID       |
| chat_id        | 聊天ID         |
| hook           | 回调地址       |
| creatd         | 创建时间       |

- users: 记录 所有的用户信息

| ***\*字段\**** | ***\*备注\**** |
| -------------- | -------------- |
| user_id      | 用户ID       |
| usage        | 聊天使用的Token额度         |
| current_channel           | 当前频道(默认为group)       |
| creatd         | 创建时间       |

- sks: 记录 所有可用的 SK（TODO: 可基于消息做轮训使用）

| ***\*字段\**** | ***\*备注\**** |
| -------------- | -------------- |
| sk             | sk信息         |
| used           | 是否在使用     |

- chats： 主要表，每次聊天时均要做记录，包括

| ***\*字段\**** | ***\*备注\****                                               |
| -------------- | ------------------------------------------------------------ |
| user_id        | 用户的唯一标识                                               |
| role           | 消息的角色（assistant，system，user）所有system的消息均为指令 |
| created        | 消息创建时间（排序依据）                                     |
| content        | 消息内容                                                    |
| robot_key      | 机器人                                                      |
| usage          | 此条对话消耗的TOKEN                                                 |
| channel         | 频道(默认为group)                                         |

## 主要功能

### ~~HOOK BOT 注册~~

~~1. WOA 中添加 hook bot，所有的回调地址都是默认/chat 返回~~

```
{"result":"ok"}
```

1. ~~@bot时，后台先通过 bot_key 在 bots 库中查找是否已注册，若注册进入指令系统，否则，进入注册流程。~~
2. ~~hook bot 的注册方法是在回调中附件 hook url 的send key 如：`?key=d57a91bf7c8cdb2213ed49`~~

~~并显示的发送指令%init%~~

1. ~~接到指令后，判断是否可以注册，并给出相应提示。注册成功后，可以在回调中去掉 send key 的相关参数~~



### 指令系统（%xxx%）

1. 内置若干指令（待定），指令的标示均为system.在构造 chat messages 时，放置在最前部，内置指令由一个特殊的userid标识控制。如-1
2. 自定义指令，由用户通过%instrs set xxx%发起，自定义指令属于高阶玩法，与用户绑定。构造 chat messages 时，查找所有 该用户下的 system 即可。
3. 指令列出只涉及自定义指令，内置指令不允许修改。会通过内部函数调用，在自定义指令时，通过内置 #name 指令为自定义指令命名。
4. 自定义指令的修改命令为 %instrs set #指令代码 指令效果描述%



### 对话系统

1. @hook bot 后接对话 即可进入对话系统
2. 一个群是一个对话单元，以robot_key为标识。
3. 用户触发对话时，先获取用户的基本信息，并判断当前 channel，默认为群聊。
4. 默认获取上下文时，筛选条件为robot_key,以群里的所有信息进行答复，若用户使用 %channel 指令%,则会以 robot_key 与channel 两个维度进行上下文查找。查找的范围为 user & assistant。
5. 处理 system 信息；
   - 最初的起始指令，默认值。
   - 是否有内置的指令集合，程序初始化给出，所有者为 system。
   - 是否有群指令,由%instrs%指令设置，对话的所有者为robot_key
   - 是否有对话压缩指令,对话所有者为 robot_key,
6. 对话会以一问一答的形式，进行存储，最大程度保证上下文。
7. 每次对话会对 usage 属性做检查，若prompt_tokens大于2048则会对上下文进行清理。
8. 清理规则待定，目前针对当前主题的所有对话全部清理。
9.  用户可以通过 %chat cls%指令，主动清理。

```
{
    "id": "chatcmpl-6q0Uinq2J7BPzGe1WjGO9WOEZPGYG",
    "object": "chat.completion",
    "created": 1677852976,
    "model": "gpt-3.5-turbo-0301",
    "usage": {
        "prompt_tokens": 244,
        "completion_tokens": 18,
        "total_tokens": 262
    },
    "choices": [
        {
            "message": {
                "role": "assistant",
                "content": "xxxxx"
            },
            "finish_reason": "stop",
            "index": 0
        }
    ]
}
```

### SK 轮换（待规划）

为增加服务承载量，可以默认生成5个SK,每次请求附加的SK值不一样。每个用户第一次请求时 ,随机附加一个SK ,当前SK有效期为1d ,SK生效时判断一下有效期 ,若超期再按轮换池规则附加一个即可。若不超期则直接使用currentSK即可。



### 回复系统

针对质量较高的回复，配套内置指令，如主题等。





## 具体实现

### ~~✅hookbot 类~~

~~woa 机器人相关能力~~

### ✅instrs 类

指令处理的方法，核心能力以完成

### ✅firebase 类

持久化数据操作

### ✅chat 类

复杂与openai交互（stream 等）

### ✅test类

尽可能全面的单元测试