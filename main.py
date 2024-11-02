import OlivOS
import random
import re

class Event(object):
    def init(plugin_event, Proc):
        pass

    def private_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)

    def group_message(plugin_event, Proc):
        unity_reply(plugin_event, Proc)

    def poke(plugin_event, Proc):
        poke_reply(plugin_event, Proc)

    def save(plugin_event, Proc):
        pass

    def menu(plugin_event, Proc):
        pass

def unity_reply(plugin_event, Proc):
    cmd = Fmt(plugin_event.data.message, plugin_event)
    if cmd is None:
        return
    cmd_args =cmd.split(" ")
    cmd_args =[x for x in cmd_args if x!='']
    if len(cmd_args) < 1:
        return
    reply = ''
    delta_clock = 0
    # fu命令
    if cmd_args[0] =='fu':
        if len(cmd_args) == 1 or cmd_args[1] == 'help':
            plugin_event.reply(help_msg['fu'])
        elif len(cmd_args) >=3:
            # 首先获取检定模式
            mode,_ = VarGetAuto(plugin_event,Proc,'fu','fmod',0)
            fc,_ = VarGetAuto(plugin_event,Proc,'fu','fc',0)
            val1 ='1'
            val2 ='1'
            if cmd_args[1].isdigit():
                val1 = int(cmd_args[1])
            else:
                if cmd_args[1] in keyList:
                    val1 = Proc.database.get_user_config_from_event(None, keyList[cmd_args[1]], plugin_event, 1, False)
                else:
                    val1 = val1.lower()
                    val1 =  Proc.database.get_user_config_from_event(None, val1, plugin_event, 1, False)
            if cmd_args[2].isdigit():
                val2 = int(cmd_args[2])
            else:
                if cmd_args[2] in keyList:
                    val2 = Proc.database.get_user_config_from_event(None, keyList[cmd_args[2]], plugin_event, 1, False)
                else:
                    val2 = val2.lower()
                    val2 =  Proc.database.get_user_config_from_event(None, val2, plugin_event, 1, False)
            result1 = D(1, val1)
            result2 = D(1, val2)
            if mode == 0:
                # 默认模式
                if len(cmd_args) >= 4:
                    bonus = int(cmd_args[3])
                else:
                    bonus = 0
                # 检查difficulty是否存在
                if len(cmd_args) >= 5:
                    # 存在则正常检定
                    difficulty = int(cmd_args[4])
                    result = result1 + result2 + bonus
                    delta = result - difficulty
                    reply = '['+str(plugin_event.data.sender['nickname']) + ']'+ '掷出了d' + str(val1) + '+d' + str(val2) + '+' + str(bonus) + '='+ str(result1) + '+' + str(result2) + '+' + str(bonus) + '='+ str(result) + '点。'
                    if result1 >=6 and result1==result2:
                        reply += '大成功！'
                        rank =3
                    if result >= difficulty:
                        reply += '成功。'
                        rank =2
                    else:
                        if result1 ==1 and result1==result2:
                            reply += '大失败！'
                            rank =0
                        else:
                            reply += '失败。'
                            rank =1
                    delta_clock = clock_get(delta,rank)
                else:
                    # 不存在则忽略难度直接给出结果
                    difficulty = 0
                    result = result1 + result2 + bonus
                    reply = '['+str(plugin_event.data.sender['nickname']) + ']'+ '掷出了d' + str(val1) + '+d' + str(val2) + '+' + str(bonus) + '='+ str(result1) + '+' + str(result2) + '+' + str(bonus) + '='+ str(result) + '点。'
                    plugin_event.reply(reply)
                    return
            else:
                # 便捷模式
                # 检查difficulty是否存在
                if len(cmd_args) >= 4:
                    difficulty = int(cmd_args[3])
                else:
                    difficulty = 10
                # 检查bonus是否存在
                if len(cmd_args) >= 5:
                    bonus = int(cmd_args[4])
                else:
                    bonus = 0
                result = result1 + result2 + bonus
                delta = result - difficulty
                reply = '['+str(plugin_event.data.sender['nickname']) + ']'+ '掷出了d' + str(val1) + '+d' + str(val2) + '+' + str(bonus) + '='+ str(result1) + '+' + str(result2) + '+' + str(bonus) + '='+ str(result) + '点。'
                if result >= difficulty:
                    if result1 >=6 and result1==result2:
                        reply += '大成功！'
                        rank =3
                    else:
                        reply += '>'+str(difficulty) + '成功。'
                        rank =2
                else:
                    if result1 ==1 and result1==result2:
                        reply += '大失败！'
                        rank =0
                    else:
                        reply += '<'+str(difficulty) + '失败。'
                        rank =1
                delta_clock = clock_get(delta,rank)
            if fc==1:
                reply += '命刻变动为' + str(delta_clock) + '。'
            plugin_event.reply(reply)
    # fst命令
    if cmd_args[0] =='fst':
        if len(cmd_args) == 1 or cmd_args[1] == 'help':
            plugin_event.reply(help_msg['fst'])
        elif cmd_args[1] =='show':
            # 展示对应属性，如果参数为空则展示所有属性
            pass
        else:
            count = 0
            for arg in cmd_args[1:]:
                key, value = split_string(arg)
                if key in keyList:
                    key = keyList[key]
                key = key.lower()
                Proc.database.set_user_config_from_event(None, key, value, plugin_event, False)
                count+=1
            plugin_event.reply('成功录入' + str(plugin_event.data.sender['nickname']) + '的' + str(count) + '条属性。')
    # fumod命令
    if cmd_args[0] =='fmod':
        if len(cmd_args) == 1 or cmd_args[1] == 'help':
            plugin_event.reply(help_msg['fmod'])
        else:
            fmod = int(cmd_args[1])
            if fmod == 0 or fmod == 1:
                VarSetAuto(plugin_event,Proc,'fu','fmod',fmod)
                plugin_event.reply('检定模式：'+ fmod_list[fmod] )
            else:
                plugin_event.reply('模式代码只能为 0 或 1 。')
    # fc命令
    if cmd_args[0] =='fc':
        if len(cmd_args) == 1 or cmd_args[1] == 'help':
            plugin_event.reply(help_msg['fc'])
        else:
            fcmod = int (cmd_args[1])
            if fcmod == 0 or fcmod == 1:
                VarSetAuto(plugin_event,Proc,'fu','fc',fcmod)
                plugin_event.reply('命刻显示：'+ fcmod_list[fcmod] )
            else:
                plugin_event.reply('模式代码只能为 0 或 1。')
    # cg命令
    if cmd_args[0] =='cg':
        plugin_event.reply(help_msg['cg'])
    if cmd_args[0] =='cgsave':
        if len(cmd_args) == 1 or cmd_args[1] == 'help':
            plugin_event.reply(help_msg['cgsave'])
        else:
            key = cmd_args[1]
            if key =='cgList':
                plugin_event.reply('你不能使用保留关键字cgList作为标识符')
                return
            key_for_show =key
            key = 'key_for_cg_loader_'+key
            value = " ".join(cmd_args[2:])
            value_formal =Proc.database.get_user_config_from_event(None, key, plugin_event, None, False)
            Proc.database.set_user_config_from_event(None, key, value, plugin_event, False)
            cg_list = Proc.database.get_user_config_from_event(None,'cgList', plugin_event, [], True)
            if key in cg_list:
                plugin_event.reply('cg:<'+key_for_show+'>已存在,将覆盖原有值:\n'+value_formal)
            else:
                cg_list.append(key_for_show)
                Proc.database.set_user_config_from_event(None,'cgList', cg_list, plugin_event, True)
                plugin_event.reply('cg:<'+key_for_show+'>成功录入')
    if cmd_args[0] =='cgload':
        if len(cmd_args) == 1 or cmd_args[1] == 'help':
            plugin_event.reply(help_msg['cgload'])
        else:
            key = cmd_args[1]
            key_for_show =key
            key = 'key_for_cg_loader_'+key
            value = Proc.database.get_user_config_from_event(None, key, plugin_event, None, False)
            cg_list = Proc.database.get_user_config_from_event(None,'cgList', plugin_event, [], True)
            if key_for_show in cg_list:
                plugin_event.reply('<'+key_for_show+'>:\n'+value)
            else:
                plugin_event.reply('cg:<'+key_for_show+'>不存在')
    if cmd_args[0] =='cgdel':
        if len(cmd_args) == 1 or cmd_args[1] == 'help':
            plugin_event.reply(help_msg['cgdel'])
        else:
            key = cmd_args[1]
            if key =='cgList':
                plugin_event.reply('你不能使用保留关键字cgList作为标识符')
                return
            key_for_show =key
            key = 'key_for_cg_loader_'+key
            value = Proc.database.get_user_config_from_event(None, key, plugin_event,None, False)
            cg_list = Proc.database.get_user_config_from_event(None,'cgList', plugin_event, [], True)
            if key in cg_list:
                cg_list.remove(key_for_show)
                Proc.database.set_user_config_from_event(None,'cgList', cg_list, plugin_event, True)
                Proc.database.set_user_config_from_event(None, key,None,plugin_event,False)
                plugin_event.reply('cg:<'+key_for_show+'>已成功删除')
            else:
                plugin_event.reply('cg:<'+key_for_show+'>不存在')
    if cmd_args[0] =='cglist':
        if len(cmd_args) > 1 and cmd_args[1] == 'help':
            plugin_event.reply(help_msg['cglist'])
        else:
            cg_list = Proc.database.get_user_config_from_event(None,'cgList', plugin_event, [], True)
            if len(cg_list) == 0:
                plugin_event.reply('cgList为空')
            else:
                reply = ",\n".join(cg_list)
                plugin_event.reply('cgList:\n'+reply)
    if cmd_args[0] =='cgclear':
        cg_list = Proc.database.get_user_config_from_event(None,'cgList', plugin_event, [], True)
        for key in cg_list:
            key = 'key_for_cg_loader_'+key
            Proc.database.set_user_config_from_event(None, key,None,plugin_event,False)
        Proc.database.set_user_config_from_event(None,'cgList', [], plugin_event, True)
        plugin_event.reply('cgList已清空')

def poke_reply(plugin_event, Proc):
    if plugin_event.data.target_id == plugin_event.base_info['self_id']:
        pass
    elif plugin_event.data.target_id == plugin_event.data.user_id:
        pass
    elif plugin_event.data.group_id == -1:
        pass

# 函数区
def D(n, x, k=1, p=0, c=0):
    """
    函数功能：计算n次骰子的结果
    :param n: 骰子个数
    :param x: 骰子面数
    :param k: 倍率
    :param p: 一级修正
    :param c: 二级修正
    :return: (ndx+p)*k+c
    """
    sum_val = 0
    if x<1:
        return k * p + c
    for _ in range(n):
        random_number = random.randint(1, x)
        sum_val += random_number
    sum_val += p
    sum_val *= k
    sum_val += c
    return sum_val

def split_string(s):
    match = re.match("([a-zA-Z\u4e00-\u9fff]+)(\d+)", s)
    if match:
        str_part = match.group(1)
        int_part = int(match.group(2))
        return str_part, int_part
    else:
        return None, None

def clock_get(delta,rank):
    if delta>=6 or rank==3:
        clock = 3
    elif delta>=3:
        clock = 2
    elif delta>=0:
        clock = 1
    elif delta> -3 and rank!=0:
        clock = -1
    elif delta> -6 and rank!=0:
        clock = -2
    else:
        clock = -3
    return clock

def VarSetAuto(plugin_event, Proc,NameSpace,Key,Value,pkl=False):
    """
    用于设置数据库配置项，具体配置项取决于对话情况，私聊中为个人变量，群聊中为群组变量
    :param plugin_event:
    :param Proc:
    :param NameSpace:
    :param Key:
    :param Value:
    :param pkl:
    :return:变量位置，0为个人变量，1为群组变量
    """
    try:
        Proc.database.set_group_config_from_event(NameSpace, Key, Value, plugin_event, pkl)
        return 1
    except Exception as e:
        Proc.database.set_user_config_from_event(NameSpace, Key, Value, plugin_event, pkl)
        return 0

def VarGetAuto(plugin_event, Proc,NameSpace,Key,default_value=None,pkl=False):
    """
    用于获取数据库配置项，具体配置项取决于对话情况，私聊中为个人变量，群聊中为群组变量
    :param default_value:
    :param plugin_event:
    :param Proc:
    :param NameSpace:
    :param Key:
    :param pkl:
    :return:value ,type 第一个返回值为配置项的值，第二个返回值为变量位置，0为个人变量，1为群组变量
    """
    try:
        value = Proc.database.get_group_config_from_event(NameSpace, Key, plugin_event, default_value, pkl)
        return value, 1
    except Exception as e:
        value = Proc.database.get_user_config_from_event(NameSpace, Key, plugin_event, default_value, pkl)
        return value, 0

def Fmt(cmd, plugin_event):
    """
    函数功能：格式化命令，如果不是命令则返回原参数
    :param cmd: 传入的命令
    :param plugin_event: 用于获取自身信息
    :return: 格式化后的命令
    """
    fmt_cmd = None
    if cmd.startswith('[CQ:at,qq=' + str(plugin_event.base_info['self_id']) + ']') :
        cmd = cmd.replace('[CQ:at,qq=' + str(plugin_event.base_info['self_id']) + ']', '')
    if cmd.startswith('/') or cmd.startswith('.') or cmd.startswith('。'):
        cmd = cmd[1:]
        for key in cmd_list:
            if cmd.startswith(key):
                cmd = cmd.replace(key, '')
                fmt_cmd = str(key)+' '+cmd
                break
        return fmt_cmd
    return ' '

# 文案资源区

cmd_list = ['fuh', 'fst', 'fmod','fc','fu','cgclear','cgsave','cgload','cglist','cgdel','cg']

help_msg = {
'fu': '''最终物语的检定辅助指令。
拥有两种模式：
0，默认模式
    难度留空时仅显示结果。
    指令为.fu 属性1 属性2 补正 难度
1，便捷模式
    难度可以留空，默认为10。补正可以留空，默认为0。使用补正必须输入难度
    指令为.fu 属性1 属性2 难度 补正
ps：属性不用不用加d作为前缀，直接用数字即可。''',
'fst': '''最终物语的角色录入指令。
属性录入: .fst 属性名&属性值（中间不加其他符号，属性值不加d前缀） ... 
示例: .fst 力量6 灵巧8 洞察10 意志12 等级5
可以使用中文名称或英文缩写，二者完全等价。''',
'fmod': '''最终物语的检定模式切换指令。
指令：.fmod 模式代码
模式：
0，默认模式
    难度留空时仅显示结果。
    检定指令为.fu 属性1 属性2 补正 难度
1，便捷模式
    难度可以留空，默认为10。补正可以留空，默认为0。使用补正必须输入难度
    检定指令为.fu 属性1 属性2 难度 补正''',
'fc': '''最终物语的检定命刻变动显示开关。
指令：.fc 开关代码
0，关闭.     1，开启.''',
'cg':"""用于存储和管理cg
指令：
.cgsave 名称 内容 
    保存当前cg
.cgload 名称 
    加载指定cg
.cglist 
    显示当前cg列表
.cgdel 名称 
    删除指定cg
""",
'cgsave':"""用于保存cg
.cgsave 名称 内容 
    保存当前cg
名称：cg名称，不能重复
内容：cg内容，可以是任何文字+图片""",
'cgload':"""用于加载cg
.cgload 名称 
    加载指定cg
名称：cg名称，必须存在""",
'cglist':"""用于显示当前cg列表
.cglist 
    显示当前cg列表""",
'cgdel':"""用于删除cg
.cgdel 名称 
    删除指定cg
名称：cg名称，必须存在"""
}

keyList ={
    "力量": "mig",
    "灵巧": "dex",
    "洞察": "ins",
    "意志": "wlp",
    "m":"mig",
    "d":"dex",
    "i":"ins",
    "w":"wlp",
}

fmod_list = ['0，默认模式', '1，便捷模式']

fcmod_list = ['0，关闭', '1，开启']

opportunity_list ={
    "优势":"你或盟友的下一个检定将获得+4加值。",
    "苦难":"目标生物会眩晕、动摇、缓慢或虚弱",
    "羁绊":"你对某人或某物建立了一种新羁绊，或者在你现有的羁绊中添加一种情感",
    "失言":"选择一个出现在场景之中的生物：做出一个由控制他们的人选择的妥协",
    "亲睐":"的行为为你赢得了某人的支持或赞赏",
    "线索":"你发现了有用的线索或细节。GM可能会告诉你这是什么，或者让你自己说明自己想要什么。",
    "丢失":"丢失一件物品被摧毁、丢失、被盗或留下。",
    "进展":"你可以在命刻上填充或删除两个部分",
    "情节转折！":"你选择的某个人或某物突然出现在现场。",
    "扫描":"你会发现目标的一个弱点或者一个特质",
    "揭秘":"你可以了解你所选择的生物的目标和动机"
}