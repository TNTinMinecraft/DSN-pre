## 交互式神经网络工作流框架 - DSN 

[English](https://github.com/ccjjfdyqlhy/DSN-pre/) | **简体中文**  

**DSN** 是一种强大且创新的交互式提示框架，它结合了大型语言模型的强大功能和深度学习能力，创造出真正智能且引人入胜的对话体验。

**DSN 可以:**

* **理解和响应你的自然语言请求** - 向它询问任何问题，它将尽力满足你的要求。
* **执行命令和脚本** - 框架将自动在你的计算机上执行代码或命令，使用 action 直接处理你的请求。
* **搜索文件和信息** - 轻松地找到你计算机上的文件或在网络上查找信息。
* **从你的交互中学习** - DSN 不断从你的交互中学习，随着时间的推移改进其响应。
* **与外部插件集成** - 使用自定义插件轻松扩展 DSN 的功能。
* **支持本地模型部署** - 使用你的自定义模型离线运行 DSN。
* **生成经验加速模型** - 利用之前的对话历史来构建更快、更高效的模型。
* **更多功能等待探索！**

**特点:**  
* **语音控制:** 对 DSN 说话，让它听到你的命令！
* **本地模型支持:** 使用你自己的自定义模型，以确保隐私和离线访问。
* **高级搜索功能:** 按名称、类型或关键字搜索文件。
* **可自定义设置:** 通过调整 `config.py` 中的设置，将 DSN 调整到你的需求。
* **错误处理:** DSN 会优雅地处理错误并进行全自主故障排除。
* **经验加速:** 用你的聊天历史训练 DSN，使其更加高效和快速。

**入门:**  

**1. 先决条件:**  
* **Python 3.11+:** 从 [官方网站](https://www.python.org/) 安装 Python（建议使用 3.11.2）。
* **Google Cloud Platform API 密钥（用于在线模型访问）：** 你可以在 [此处](https://aistudio.google.com/app/apikey) 获取免费试用 API 密钥。
* **Everything 搜索引擎（用于文件搜索）：** 从其 [网站](https://www.voidtools.com/downloads) 下载完整版，然后安装到此克隆仓库的 "binaries" 文件夹中。
* **Moondream 模型：** 从 [Huggingface](https://huggingface.co/vikhyatk/moondream2) 下载到此克隆仓库的 `instances\\moondream` 文件夹中。
* **ChatTTS 模型：** 从 [此处](https://www.123pan.com/s/oZO9jv-g46N.html) 获取修改版的整合ChatTTS模型，然后将其解压到此克隆仓库的 `instances\\chatTTS` 文件夹中。**提取码:1145**
* **Paraformer 模型：** 从 [魔搭设区](https://www.modelscope.cn/models/iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch/summary) 获取，然后将其解压到此克隆仓库的 `instances\\paraformer-zh` 文件夹中。
* 注：以上模型解压时均直接将内含文件解压到指定文件夹即可，不要连带压缩包内文件夹一起解压。

**2. 安装:**

1. **克隆仓库:** 
   ```bash
   git clone https://github.com/ccjjfdyqlhy/DSN.git
   ```
2. **安装 `install_before_requirements.txt` 中的必要包。**
3. **下载 DSN-local.NT 模型:**
   * 该模型暂时不对外开放。请联系作者来以个人名义获取。
4. **安装依赖项:**
   ```bash
   pip install -r requirements.txt
   ```

**3. 配置:**

* **打开 `config.py` 并调整以下设置:**
    * **GENAI_APIKEY:** 你的 Google Cloud Platform API 密钥。
    * **USERNAME:** 你想要的用户名。
    * **CITY:** 你所在的城市。
    * **TIMEZONE:** 你首选的时区。
    * **USER_PYTHON:** 你首选的 Python 解释器的路径。
    * **AI_NAME:** 你想给你的 AI 起的名字。
    * **将 `MODEL_PATH`设定为 `DSN-local.NT` 文件的绝对路径。**
* **可选:** 
    *  你可以在 `config.py` 中将 `SPEECH_CONTROL` 设置为 `True` 以启用语音控制。
    *  对于离线使用，将 `USE_LOCAL` 设置为 `True`。

* **更多信息，请查看 `config.py`。**

**4. 启动 DSN:**

* **打开命令提示符或终端并导航到项目目录:** 
   ```bash
   cd DSN
   ```
* **运行主程序:**
   ```bash
   python DSN.Launch.py
   ```

**5. 尽情享受对话吧！**

DSN 现在已准备好回答你的问题、执行你的命令并帮助你完成任务。

**如何构建经验加速模型:**

1. 与 DSN 开始对话。
2. 键入 "BUILD_TRAIN_DATA"。
3. DSN 将指导你读取 `generated\\chat_history` 文件夹中的对话历史文件。
4. 读取每个文件后，总结要点并提供你的反馈。
5. 满意后，DSN 将根据你的输入构建经验加速模型。

**其他注意事项:**

* **注意: 在开始使用之前，你必须阅读并同意 `LICENCE` 文件中的所有使用条款。**  
* 你激活交互式终端后，将向你展示其他功能。
