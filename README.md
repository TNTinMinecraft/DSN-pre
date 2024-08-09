## Interactive Neural Network Workflow Framework - DSN

**English** | [简体中文](https://github.com/ccjjfdyqlhy/DSN-pre/blob/main/README_zh-CN.md)  

**DSN** is a powerful and innovative interactive prompt framework that combines the power of large language models with deep learning capabilities, creating truly intelligent and engaging conversational experiences.

**DSN can:**

* **Understand and respond to your natural language requests** - Ask it anything, and it will do its best to fulfill your requests.
* **Execute commands and scripts** - The framework will automatically execute code or commands on your computer, using actions to directly handle your requests.
* **Search files and information** - Effortlessly find files on your computer or search for information online.
* **Learn from your interactions** - DSN continuously learns from your interactions, improving its responses over time.
* **Integrate with external plugins** - Easily extend DSN's functionality using custom plugins.
* **Support local model deployment** - Run DSN offline using your custom models.
* **Generate experience-accelerated models** - Leverage your previous conversation history to build faster and more efficient models.
* **More features are waiting to be explored!**

**Features:**  
* **Voice control:** Speak to DSN and let it hear your commands!
* **Local model support:** Use your own custom models for privacy and offline access.
* **Advanced search capabilities:** Search files by name, type, or keyword.
* **Customizable settings:** Adjust DSN to your needs by modifying settings in `config.py`.
* **Error handling:** DSN handles errors gracefully and offers fully autonomous troubleshooting.
* **Experience acceleration:** Train DSN with your chat history for increased efficiency and speed.

**Getting started:**  

**1. Prerequisites:**  
* **Python 3.11+:** Install Python from the [official website](https://www.python.org/) (version 3.11.2 is recommended).
* **Google Cloud Platform API Key (for online model access):** You can get a free trial API key [here](https://aistudio.google.com/app/apikey).
* **Everything Search Engine (for file searching):** Download the full version from its [website](https://www.voidtools.com/downloads) and install it in the "binaries" folder of this cloned repository.
* **Moondream model:** Download from [Huggingface](https://huggingface.co/vikhyatk/moondream2) and place it in the `instances\\moondream` folder of this cloned repository.
* **ChatTTS model:** Obtain the modified integrated ChatTTS model from [here](https://www.123pan.com/s/oZO9jv-g46N.html), then unzip it into the `instances\\chatTTS` folder of this cloned repository. **Extraction code: 1145**
* **Paraformer model:** Obtain it from [Magic Model Zone](https://www.modelscope.cn/models/iic/speech_paraformer-large-vad-punc_asr_nat-zh-cn-16k-common-vocab8404-pytorch/summary), then unzip it into the `instances\\paraformer-zh` folder of this cloned repository.
* Note: When unzipping the above models, simply unzip the contained files into the specified folder, do not unzip the folder within the compressed file.

**2. Installation:**

1. **Clone the repository:** 
   ```bash
   git clone https://github.com/ccjjfdyqlhy/DSN.git
   ```
2. **Install necessary packages from `install_before_requirements.txt`.**
3. **Download the DSN-local.NT model:**
   * This model is not currently available publicly. Please contact the author to obtain it personally.
4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

**3. Configuration:**

* **Open `config.py` and adjust the following settings:**
    * **GENAI_APIKEY:** Your Google Cloud Platform API key.
    * **USERNAME:** Your desired username.
    * **CITY:** Your city.
    * **TIMEZONE:** Your preferred timezone.
    * **USER_PYTHON:** The path to your preferred Python interpreter.
    * **AI_NAME:** The name you want to give your AI.
    * **Set `MODEL_PATH` to the absolute path of the `DSN-local.NT` file.**
* **Optional:** 
    *  You can enable voice control by setting `SPEECH_CONTROL` to `True` in `config.py`.
    *  For offline use, set `USE_LOCAL` to `True`.

* **For more information, please refer to `config.py`.**

**4. Launching DSN:**

* **Open a command prompt or terminal and navigate to the project directory:** 
   ```bash
   cd DSN
   ```
* **Run the main program:**
   ```bash
   python DSN.Launch.py
   ```

**5. Enjoy the conversation!**

DSN is now ready to answer your questions, execute your commands, and help you with your tasks.

**How to build an experience-accelerated model:**

1. Start a conversation with DSN.
2. Type "BUILD_TRAIN_DATA".
3. DSN will guide you to read the conversation history files in the `generated\\chat_history` folder.
4. After reading each file, summarize the key points and provide your feedback.
5. Once satisfied, DSN will build an experience-accelerated model based on your input.

**Other Notes:**

* **Please Note: You must read and agree to all terms of use in the `LICENCE` file before starting to use.**  
* You will be presented with other features upon activating the interactive terminal.

This is a translated version of a repository's readme file.  I hope this helps! Let me know if you have any other questions. 
