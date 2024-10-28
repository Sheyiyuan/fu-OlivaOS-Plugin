import OlivOS
import fu
import random
import string
import re

help_msg = {
'fu': '''最终物语的检定辅助指令。
拥有两种模式：
0，默认模式
    难度留空时仅显示结果。
    指令为.fu 属性1 属性2 补正 难度
1，便捷模式
    难度可以留空，默认为10。补正可以留空，默认为0。使用补正必须输入难度
    指令为.fu 属性1 属性2 难度 补正
ps：属性不用不用加d作为前缀，直接用数字即可。
。''',
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
0，关闭.     1，开启.'''
}

fmod_list = ['0，默认模式', '1，便捷模式']

fcmod_list = ['0，关闭', '1，开启']

cmd_list = ['fu', 'fst', 'fmod','fc']

keyList ={
    "力量": "mig",
    "灵巧": "dex",
    "洞察": "ins",
    "意志": "wis",
    "m":"mig",
    "d":"dex",
    "i":"ins",
    "w":"wis",
}



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
    cmd = cmd_fmt(plugin_event.data.message, plugin_event, Proc)
    cmd_args =cmd.split(" ")
    cmd_args =[x for x in cmd_args if x!='']
    reply = ''
    delta_clock = 0
    # fu命令
    if cmd_args[0] =='fu':
        if len(cmd_args) == 1 or cmd_args[1] == 'help':
            plugin_event.reply(help_msg['fu'])
        elif len(cmd_args) >=3:
            # 首先获取检定模式
            try:
                mode = Proc.database.get_group_config_from_event('fu', 'fmod', plugin_event, default_value=0, pkl=False)
                fc = Proc.database.get_group_config_from_event('fu', 'fc', plugin_event, default_value=0, pkl=False)
            except Exception as e:
                mode = Proc.database.get_user_config_from_event('fu', 'fmod', plugin_event, default_value=0, pkl=False)
                fc = Proc.database.get_user_config_from_event('fu', 'fc', plugin_event, default_value=0, pkl=False)
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
                    if result >= difficulty:
                        if result1 >=6 and result1==result2:
                            reply += '大成功！'
                            rank =3
                        else:
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
                try:
                    Proc.database.set_group_config_from_event('fu', 'fmod', fmod, plugin_event, pkl=False)
                except Exception as e:
                    Proc.database.set_user_config_from_event('fu', 'fmod', fmod, plugin_event, pkl=False)
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
                try:
                    Proc.database.set_group_config_from_event('fu', 'fc', fcmod, plugin_event, pkl=False)
                except Exception as e:
                    Proc.database.set_user_config_from_event('fu', 'fc', fcmod, plugin_event, pkl=False)
                plugin_event.reply('命刻显示：'+ fcmod_list[fcmod] )
            else:
                plugin_event.reply('模式代码只能为 0 或 1。')



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

def cmd_fmt(cmd, plugin_event, Proc):
    """
    函数功能：格式化命令，如果不是命令则返回原参数
    :param cmd: 传入的命令
    :param plugin_event: 用于获取自身信息
    :param Proc: 无实际作用，仅用于保持函数签名一致
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
    return cmd