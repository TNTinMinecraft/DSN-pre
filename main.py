
# DSN main
# update 240809

try:
    from prompt import *
    from config import *
except ImportError:
    print('关键文件缺失。')
    exit()

try:
    import google.generativeai as genai
    import numpy as np
    from google.generativeai.types import HarmCategory, HarmBlockThreshold
    from funasr import AutoModel
    from llama_cpp import Llama
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from PIL import Image
    import os,sys,requests,win32gui,win32api,psutil,cv2,pyaudio,google.api_core,wave,traceback,datetime,subprocess,re
except ModuleNotFoundError:
    print('缺少必要的模块，请确保安装完整。')
    exit()

_ver_ = '0.8.3'
BUILDNUM = 240809
cwd = os.getcwd()
platform = sys.platform
timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
use_device = 'camera'
turn = 0
building = False
global result

def send(msgcontent):
    if USE_LOCAL:
        output = llm.create_chat_completion(messages=msgcontent)
        history.append({"role": "assistant", "content": output})
        return extract_model_output(str(output))
    else:
        return chat.send_message(msgcontent,safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        }).text

def chattts(required_text):
    res = requests.post('http://127.0.0.1:9966/tts', data={
  "text": required_text,
  "prompt": "",
  "voice": "2222",
  "temperature": CHATTTS_TEMP,
  "top_p": 0.7,
  "top_k": 20,
  "refine_max_new_token": "384",
  "infer_max_new_token": "2048",
  "skip_refine": 0,
  "is_split": 1,
  "custom_voice": CHATTTS_SEED
})
    return res

def get_cursored_hwnd():
    cursor_point = win32api.GetCursorPos()  
    hwnd = win32gui.WindowFromPoint(cursor_point)
    return hwnd

def get_dailyinfo():
    rep = requests.get('http://v1.yiketianqi.com/api?unescape=1&version=v91&appid=99245552&appsecret=RL8NtmPx&ext=&city='+CITY)
    rep.encoding = 'utf-8'
    return rep.json()

def check_process(process_name):
    for process in psutil.process_iter(['name']):
        if process.info['name'] == process_name:
            return True
    return False

def start_everything():
    # 启动 Everything.exe
    try:
        subprocess.Popen(cwd+'\\binaries\\Everything.exe', shell=True)
    except FileNotFoundError:
        print('未安装 Everything，请前往安装')
        exit()

def start_chattts():
    # 启动 Chatts.exe
    try:
        subprocess.Popen(cwd+'\\instances\\chattts\\app.exe', shell=True)
    except FileNotFoundError:
        print('未安装 ChatTTS，请前往安装')
        exit()

def remove_extension(filename):
    if '.' in filename:
        return filename.split('.')[0]
    else:
        return filename
    
def search_file_by_name(file_name):
    search_result = str(os.popen(cwd+'\\binaries\\search_everything.exe wfn:'+file_name+' 2>&1').readlines())
    if len(search_result) > 0:
        return search_result
    else:
        return 'No result found'

def search_file_by_kind(file_kind, keyword):
    search_result = []
    file_kinds = ['audio','zip','doc','exe','pic','video']
    audio = ['mp3','wav','aac','flac','wma','ogg']
    zipname = ['zip','rar','7z','iso']
    doc = ['doc','docx','ppt','pptx','xls','xlsx','pdf']
    exe = ['exe','msi','bat','cmd']
    pic = ['jpg','jpeg','png','gif','bmp','tiff']
    video = ['mp4','avi','mov','wmv','flv','mkv']
    i = 0
    keyword = remove_extension(keyword)
    if file_kind == 'audio':
        for name in audio:
            search_result.append('extension: .'+name+', result: '+str(os.popen(cwd+'\\binaries\\search_everything.exe '+keyword+'.'+name+' 2>&1').readlines()))
    elif file_kind == 'zip':
        for name in zipname:
            search_result.append('extension: .'+name+', result: '+str(os.popen(cwd+'\\binaries\\search_everything.exe '+keyword+'.'+name+' 2>&1').readlines()))
    elif file_kind == 'doc':
        for name in doc:
            search_result.append('extension: .'+name+', result: '+str(os.popen(cwd+'\\binaries\\search_everything.exe '+keyword+'.'+name+' 2>&1').readlines()))
    elif file_kind == 'exe':
        for name in exe:
            search_result.append('extension: .'+name+', result: '+str(os.popen(cwd+'\\binaries\\search_everything.exe '+keyword+'.'+name+' 2>&1').readlines()))
    elif file_kind == 'pic':
        for name in pic:
            search_result.append('extension: .'+name+', result: '+str(os.popen(cwd+'\\binaries\\search_everything.exe '+keyword+'.'+name+' 2>&1').readlines()))
    elif file_kind == 'video':
        for name in video:
            search_result.append('extension: .'+name+', result: '+str(os.popen(cwd+'\\binaries\\search_everything.exe '+keyword+'.'+name+' 2>&1').readlines()))
    else:
        return 'Invalid file kind, please choose one: '+str(file_kinds)
    if len(search_result) > 0:
        return str(search_result)
    else:
        return 'No result found'
    
def search_file_by_keyword(keyword):
    search_result = str(os.popen(cwd+'\\binaries\\search_everything.exe '+keyword+' 2>&1').readlines())
    if len(search_result) > 0:
        return search_result
    else:
        return 'No result found'

def get_vision(use_file=False):
    if use_file:
        image_path = input('[ 键入图片路径 ] > ')
        print('使用本地图片：'+image_path)
    else:
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)
        ret, frame = cap.read()
        cv2.imwrite(cwd+'\\TEMP\\latest_photo.jpg', frame)
        print('[拍照成功]')
        cap.release()
        image_path = cwd+'\\TEMP\\latest_photo.jpg'
    try:
        image = Image.open(image_path)
        enc_image = picmodel.encode_image(image)
        vision_ans=(picmodel.answer_question(enc_image, "Describe this image.", tokenizer))
    except FileNotFoundError:
        print('[ 文件不存在 ]')
    return vision_ans

def extract_code(md_string):
    code_box = re.search(r'```python(.*?)```', md_string, re.DOTALL)
    if code_box:
        code = code_box.group(1)
        return code.strip()
    else:
        return None

def extract_model_output(response_json):
    match = re.search(r"'content': '(.*?)'", response_json)
    if match:
        return match.group(1).split(r'\n')
    else:
        return []

def save_history():
    folder = cwd+"\\generated\\chat_history"
    if not os.path.exists(folder):
        os.makedirs(folder)
    time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    history_file_path = os.path.join(folder, f"history{time_str}.txt")
    if len(chat.history) > 0:
        with open(history_file_path, "w", encoding="utf-8") as f:
            for message in chat.history:
                f.write(f'{message.role}: {message.parts[0].text}')
                f.write("\n")
            f.close()

def listen():
    temp = 20
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    mindb=2000
    delayTime=1.3
    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    #snowboydecoder.play_audio_file()
    print("[ 请说出指令 ]")
    frames = []
    flag = False
    stat = True
    stat2 = False
    tempnum = 0
    tempnum2 = 0
    while stat:
        data = stream.read(CHUNK,exception_on_overflow = False)
        frames.append(data)
        audio_data = np.frombuffer(data, dtype=np.short)
        temp = np.max(audio_data)
        if temp > mindb and flag==False:
            flag =True
            if DEBUG: print("开始录音")
            tempnum2=tempnum
        if flag:
            if(temp < mindb and stat2==False):
                stat2 = True
                tempnum2 = tempnum
                if DEBUG: print("关键点记录")
            if(temp > mindb):
                stat2 =False
                tempnum2 = tempnum
            if(tempnum > tempnum2 + delayTime*15 and stat2==True):
                if DEBUG: print("%.2lfs后开始检查关键点"%delayTime)
                if(stat2 and temp < mindb):
                    stat = False
                else:
                    stat2 = False
        #print(str(temp)  +  "      " +  str(tempnum))
        tempnum = tempnum + 1
        if tempnum > EXCEED_TIME:
            stat = False
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf = wave.open(cwd+'\\TEMP\\latest_record.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()
    return cwd+'\\TEMP\\latest_record.wav'

def merge_msg():
    pic_msh = ''
    return_vision = False
    if SPEECH_CONTROL:
        res = model.generate(input=listen(),batch_size_s=300)
        for dic in res:
            for key, value in dic.items():
                if key == 'text':
                    msgin = value.replace(' ', '')
        print('> '+msgin)
    else:
        msgin=input('> ')
    if AUTO_VISION:
        for keyword in VISION_KEYWORDS:
            if keyword in msgin:
                return_vision = True
                if USE_CAMERA == 'True':
                    use_device = 'camera'
                    pic_msg = VISION_START1+get_vision(False)
                elif USE_CAMERA == 'False':
                    use_device = 'image'
                    pic_msg = VISION_START2+get_vision(True)
                elif USE_CAMERA == 'Auto':
                    for keyword in CAMERA_KEYWORDS:
                        if keyword in msgin:
                            use_device = 'camera'
                            pic_msg = VISION_START1+get_vision(False)
                        break
                    for keyword in IMAGE_KEYWORDS:
                        if keyword in msgin:
                            use_device = 'image'
                            pic_msg = VISION_START2+get_vision(True)
                        break
                    TEMP = input('[早期未实现功能的替代品] 选择使用摄像头还是本地图片(cam/img)> ')
                    if TEMP == 'cam':
                        use_device = 'camera'
                        pic_msg = VISION_START1+get_vision(False)
                    elif TEMP == 'img':
                        use_device = 'image'
                        pic_msg = VISION_START2+get_vision(True)
                break
    else:
        if 'VISION' in msgin or '使用视觉' in msgin:
            return_vision = True
            if USE_CAMERA == 'True':
                use_device = 'camera'
                pic_msg = VISION_START1+get_vision(False)
            elif USE_CAMERA == 'False':
                use_device = 'image'
                pic_msg = VISION_START2+get_vision(True)
            else:
                print('配置文件冲突：USE_CAMERA在未开启AUTO_VISION时只能为True或False，跳过应用视觉。')
    if msgin == 'BUILD_TRAIN_DATA' or msgin == '构建加速模型':
        building = True
        return '请你阅读'+cwd+'\\generated\\chat_history\\文件夹下的全部内容。'
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if return_vision:
        msg = "系统UTC+8时间："+timestamp+" "+pic_msg+" 用户输入："+msgin
    else:
        msg = "系统UTC+8时间："+timestamp+" 用户输入："+msgin
    return msg

def process_output(output,execute_layer):
    if output.startswith('cmd /c'):
        result = str(os.popen(output+' 2>&1').readlines())
        if DEBUG: print(result)
        print('[系统指令已执行]')
        skipreturn = False
    elif output.startswith('```python'):
        folder = cwd+"\\generated\\program_history"
        if not os.path.exists(folder):
            os.makedirs(folder)
        time_str = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        history_file_path = os.path.join(folder, f"program{time_str}.py")
        code_content = extract_code(output)
        with open(history_file_path, "w", encoding="utf-8") as f:
            f.write(code_content)
            f.close()
        if not os.path.exists('TEMP'):
            os.makedirs('TEMP')
        with open(cwd+'\\TEMP\\historydest.txt','w',encoding='utf-8') as f:
            f.write(history_file_path)
            f.close()
        coderunner = subprocess.Popen([PYTHON, cwd+'\\coderunner.py'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        result = coderunner.communicate()[0].decode('gbk')
        if DEBUG:print(result)
        print('[Python代码已运行]')
        skipreturn = False
    elif '[GETDAILYINFO]' in output:
        result = str(get_dailyinfo())
        print('[获取今日信息]')
        skipreturn = False
    elif output.startswith('[SFBYNAME]'):
        process = output.split(' ')
        print('[以标准文件名为索引检索：'+process[1]+']')
        result = str(search_file_by_name(process[1]))
        if DEBUG:print(result)
        print('[检索完成]')
        skipreturn = False
    elif output.startswith('[SFBYKIND]'):
        process = output.split(' ')
        print('[以文件类型为索引检索：'+process[1]+', Keyword: '+process[2]+']')
        result = str(search_file_by_kind(process[1], process[2]))
        if DEBUG:print(result)
        print('[检索完成]')
        skipreturn = False
    elif output.startswith('[SFBYKEY]'):
        process = output.split(' ')
        print('[以关键词模糊检索：'+process[1]+']')
        result = str(search_file_by_keyword(process[1]))
        if DEBUG:print(result)
        print('[检索完成]')
        skipreturn = False
    elif '[VISION]' in output:
        if AUTO_VISION:
            if USE_CAMERA == 'True':
                print('[正在使用摄像头]')
                result = get_vision(False)
            elif USE_CAMERA == 'False':
                print('[正在使用图片]')
                result = get_vision(True)
            elif USE_CAMERA == 'Auto':
                if use_device == 'camera':
                    print('[正在使用摄像头]')
                    result = get_vision(False)
                elif use_device == 'image':
                    print('[正在使用图片]')
                    result = get_vision(True)
                else:
                    print('不可能！！绝对不可能！！')
        else:
            result = '用户禁止你使用视觉。'
        skipreturn = False
    elif '[SAVE_HISTORY]' in output:
        save_history()
        print('[聊天记录已存档]')
        result = ''
        skipreturn = False
    elif output.startswith('[END_CONVERSATION]'):
        print('['+AI_NAME+' 结束了对话。]')
        print("重新启动程序以继续。")
        return False
    else:
        print('< '+output)
        if TEXT_TO_SPEECH:
            if USE_CHATTTS:
                chattts(output)
        result=''
        skipreturn = True
    if skipreturn == False:
        if str(result) == '' or result == '[]':
            response = send('[Terminal Output] 操作成功完成。')
            print('[Layer '+str(execute_layer)+' Mission Complete]')
        else:
            if execute_layer >= 10 and execute_layer <= LAYERS_LIMIT:
                print('[Layer '+str(execute_layer)+' Mission Complete / Maximum layers limit: '+LAYERS_LIMIT+']')
                execute_layer = execute_layer + 1
                response = send('[Terminal Output] '+str(result))
                process_output(response, execute_layer)
            elif execute_layer > LAYERS_LIMIT:
                print('[Layer '+str(execute_layer)+' Mission Complete / Maximum layers limit reached]')
                response = send('停止尝试纠正，错误次数太多。请详细描述遇到的错误，以便我们一起解决它。')
                print('< '+response)
            else:
                print('[Layer '+str(execute_layer)+' Mission Complete]')
                execute_layer = execute_layer + 1
                response = send('[Terminal Output] '+str(result))
                process_output(response, execute_layer)

print('\nDeep Streaming Neural Network Interactive Prompt\n核心 Framework 版本 '+_ver_+' build '+str(BUILDNUM)+'\n')
if GENAI_APIKEY == '<Your-API-key-here>': print('[ API 密钥没有设置。请转到 config.py 以配置。 ]\n'); exit()
if USERNAME == '<Your-username-here>': print('[ 用户名没有设置。请转到 config.py 以配置。 ]\n'); exit()
if CITY == '<Your-city-here>': print('[ 用户城市没有设置。请转到 config.py 以配置。 ]\n'); exit()
if TIMEZONE == '<Your-timezone-here>': print('[ 用户时区没有设置。请转到 config.py 以配置。 ]\n'); exit()
if USER_PYTHON == '<Your-preferred-python-here>': print('[ 用户Python 解释器没有设置。请转到 config.py 以配置。 ]\n'); exit()
if AI_NAME == '<AI-name-here>': print('[ AI 名称没有设置。请转到 config.py 以配置。 ]\n'); exit()
try:
    print('实例节点编号: '+sys.argv[1])
    agent_id = int(sys.argv[1])
except:
    if USE_LOCAL:
        pass
    else:
        print('未采用分布式处理。智能体可能会出现不可预测的行为。')
    agent_id = 0
print()
if DEBUG: print('WARNING: Debug 模式已启用。这会显示智能体与终端互动的所有输入和响应，显示可能很长。')
if ENABLE_PLUGINS: print('加速器加载已启用。加载耗时会更长。\n')
if USE_LOCAL:
    print('正在初始化本地模型...')
    try:
        if LOCAL_SEED == 0:
            llm = Llama(
                model_path=MODEL_PATH,
                n_gpu_layers=GPU_LAYERS,
                n_ctx=CONTEXT_WINDOW
            )
        else:
            llm = Llama(
                model_path=MODEL_PATH,
                n_gpu_layers=GPU_LAYERS,
                n_ctx=CONTEXT_WINDOW,
                seed = LOCAL_SEED
            )
    except:
        print('本地模型初始化失败。请确保已经正确在'+cwd+'\\instances文件夹下安装了DSN-local.NT模型，python环境正常，以及配置文件无误。')
        exit()
    history = [{'role': 'user', 'content': PROMPT}]
    print('本地部署完成。模型已就绪。')
else:
    genai.configure(api_key=GENAI_APIKEY,transport=GENAI_TRANSPORT_TYPE)
    model = genai.GenerativeModel(model_name=SELECTED_MODEL)
    history = []
    chat = model.start_chat(history=history)
    print('API初始化完成。')
if TEXT_TO_SPEECH:
    print('语音生成已启动...')
    if USE_CHATTTS:
        start_chattts()
if ALLOW_VISION:
    print('正在初始化视觉模型...')
    try:
        picmodel = AutoModelForCausalLM.from_pretrained(MOONDREAM_PATH,trust_remote_code=True)
        tokenizer = AutoTokenizer.from_pretrained(MOONDREAM_PATH,trust_remote_code=True)
    except OSError:
        print('视觉模型未找到。请确保已经正确在'+cwd+'\\instances文件夹下安装了Moondream模型，python环境正常，以及配置文件无误。')
        exit()
    print('视觉模型已启用。已准备好处理图像。')
if SPEECH_CONTROL: 
    print('正在初始化语音控制模型...')
    try:
        model = AutoModel(model=PARAFORMER_PATH)
    except OSError:
        print('语音控制模型未找到。请确保已经正确在'+cwd+'\\instances文件夹下安装了Paraformer模型，python环境正常，以及配置文件无误。')
        exit()
    print('语音控制已启用。试着通过说话命令DSN执行操作！\n')
print('欲修改设置，请编辑 config.py。')
print('可供合成经验加速模型的迭代次数: '+str(len(os.listdir(cwd+'\\generated\\chat_history\\'))))
if ALLOW_VISION:
    if AUTO_VISION:
        print('自动视觉已启用。AI会学习你的上下文来决定是否需要通过摄像头获取视觉。')
        if USE_CAMERA == False:
            print('USE_CAMERA设置项已强制覆盖为自动。')
        USE_CAMERA = 'Auto'
    else:
        if SPEECH_CONTROL:
            print('自动视觉已禁用。在你的句子中提到“使用视觉”来让AI处理图像。')
        else:
            print('在你的输入中加入 VISION 来让AI处理图片。')
if USE_CUSTOM_PROMPT:
    if PROMPT != '':
        print('自定义提示词已启用。')
    else:
        print('自定义提示提示词为空。这将对AI没有自定义效果。')
if SPEECH_CONTROL:
    print('说出“构建加速模型”来立即采用本次聊天记录合成经验加速模型。')
else:
    print('使用指令 BUILD_TRAIN_DATA 来立即采用本次聊天记录合成经验加速模型。')
if SPEECH_CONTROL:
    print('说出“结束对话”来让AI保存聊天记录并结束对话。')
else:
    print('使用 Ctrl+C 组合键来保存聊天记录并退出。')
print()
if not check_process('Everything.exe'):
    print('搜索服务未运行，正在启动。\n')
    start_everything()
try:
    if not os.path.exists(cwd+'\\TEMP\\'):
        os.makedirs(cwd+'\\TEMP\\')
    with open(cwd+'\\TEMP\\last_login.txt', 'r') as f: last_login = f.read(); f.close()
except FileNotFoundError: last_login = 'Never'; f = open(cwd+'\\TEMP\\last_login.txt', 'w'); f.close()
if USE_LOCAL: print('WARNING: 你正在使用本地模型。动作执行能力可能会很差。')
print('登录为： '+USERNAME+'，上次登录：'+last_login+'\n')
with open(cwd+'\\TEMP\\last_login.txt', 'w') as f: f.write(timestamp); f.close()
while True:
    try:
        if turn == 0:
            # First turn
            if ENABLE_PLUGINS:
                print('[配置加速器](1/3) < '+send(PROMPT+'第一步：执行一条命令，获取可以加载的加速器：cmd /c dir '+cwd+'\\generated\\accelerators\\').text)
                print('[配置加速器](2/3) < '+send('第二步：书写Python代码，用utf-8-sig编码读取'+cwd+'\\generated\\accelerators\\read_files.py的全部内容并输出。获取终端的输出之后，你无需再复述一遍。学习这个代码的技能。之后当我要求阅读文档时适当修改并运用你的这项技能。').text)
                print('[配置加速器](3/3) < '+send('第三步：书写Python代码阅读文件夹'+cwd+'\\generated\\accelerators\\'+'下的全部程序内容并输出。获取终端的输出之后，学习这些代码中的技能。').text)
                response = send('第四步：学习完之后你可以在我提出指定要求之后直接利用代码中的技能帮助你写新代码或执行操作。记住以上技能。完成以上操作后，加速器配置完成。请回复“代码实现加速器已加载，欢迎回来。”这句话。')
            else:
                if USE_LOCAL:
                    response = send(history)
                else:
                    if agent_id == 0:
                        response = send(PROMPT)
                    elif agent_id == 1:
                        response = send(MAIN_PROMPT+p_PROTECT+p_ENDING)
                    elif agent_id == 2:
                        response = send(BEGINNING_PROMPT+SEARCH_LOCAL_PROMPT+ENDING_PROMPT)
                    elif agent_id == 3:
                        response = send(BEGINNING_PROMPT+SEARCH_ONLINE_PROMPT+ENDING_PROMPT)
                    elif agent_id == 4:
                        response = send(BEGINNING_PROMPT+READ_FILE_PROMPT+ENDING_PROMPT)
        else:
            if agent_id == 0:
                if USE_LOCAL:
                    history.append({"role": "user", "content": merge_msg()})
                    response = send(history)
                else:
                    response = send(merge_msg())
                if building == True:
                    if DEBUG: print('< '+response)
                    print('[文档阅读完成]')
                    response = send('现在，请根据你阅读的内容，总结每个历史记录中解决用户请求的要点。对于每个历史文件，需要提取的要点包括且仅包括如下类别的内容：1、用户让编写程序的请求和你编写的最后修改版本的程序；2、用户让打开具体应用的应对策略，如对应需要执行的指令。3、对话中进行的搜索操作结果。4、用户提出一个要求，你是的最终解决方案（一句话叙述即可）。处理每个历史文件时，一律先输出文件记录时间，再给出要点。')
                    accepted = False
                    while not accepted:
                        print('(BUILDING) < '+response)
                        ask_accept = input('[ 以上总结是否需要修改？(y/n/cancel) ] > ')
                        if ask_accept == 'n':
                            accepted = True
                            with open ('acclerator.dsn','wb') as f:
                                f.write(response.encode('utf-8'))
                                f.close()
                            print('[ 经验加速模型构建完成 ]')
                        elif ask_accept == 'y':
                            response = send(input('[ 键入修改意见 ] > '))
                        elif ask_accept == 'cancel':
                            print('[ 构建取消 ]')
                            accepted = True
        if not building:
            if USE_LOCAL:
                for line in response:
                    if line != '':
                        process_output(line,1)
            else:
                chat_status = process_output(response,1)
        else:
            chat_status = True
            building = False
        if chat_status == False:
            break
        turn = turn + 1
    except KeyboardInterrupt:
        break
    except ConnectionError:
        print('[ Connection Error 请确保你的网络连接稳定。 ]')
        exit()
    except requests.exceptions.ProxyError:
        print('[ Connection Unstable 请检查代理后重试。 ]')
    except google.api_core.exceptions.TooManyRequests:
        print('[ Too Many Requests 请求频率过高，请稍后再试。 ]')
    except Exception as e:
        print('[ Python程序抛出异常：'+str(traceback.format_exc())+' ]')

save_history()
