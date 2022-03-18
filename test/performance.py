import sys
sys.path.append('..')
from time import time
from random import choices
from src.ircmsg import IRCMsg
from src_On.ircmsgOn import IRCMsgOn


class Constructor:
    tag_population = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ-'
    params_population = tag_population + r'!@#$%^&*,.;"`~(){}[]<>\/'
    value_population = params_population + ':'
    trailing_population = value_population + ' '

    @staticmethod
    def create_flexible_irc():
        return IRCMsg(':someusernickname!someuserlogin@and.some.host.com FLEXIBLE')

    @staticmethod
    def add_mass(irc_msg: IRCMsg, tags_count=25, params_count=25, trailing_len=150):
        irc_msg.tags.update(C.gen_tags(tags_count))
        irc_msg.params += C.gen_params(params_count)
        if irc_msg.trailing is not None:
            irc_msg.trailing += C.gen_trailing(trailing_len)
        else:
            irc_msg.trailing = C.gen_trailing(trailing_len)
        return irc_msg

    @staticmethod
    def gen_tags(count, *, k_len=25, v_len=100):
        tags = {}
        for _ in range(count):
            tags.update(C.gen_tag(k_len=k_len, v_len=v_len))
        return tags

    @staticmethod
    def gen_params(count, *, length=50):
        params = []
        for _ in range(count):
            params.append(C.gen_param(length))
        return params

    @staticmethod
    def gen_tag(*, k_len=25, v_len=100):
        return {C.gen_key(k_len): C.gen_value(v_len)}

    @staticmethod
    def gen_param(length=50):
        return C.gen_str(C.params_population, length)

    @staticmethod
    def gen_trailing(length=150):
        return C.gen_str(C.trailing_population, length)

    @staticmethod
    def gen_key(length=25):
        return C.gen_str(C.tag_population, length)

    @staticmethod
    def gen_value(length=100):
        return C.gen_str(C.value_population, length)

    @staticmethod
    def gen_str(population, length):
        return ''.join(choices(population, k=length))


C = Constructor


real_irc = '@badge-info=subscriber/1;badges=subscriber/0;client-nonce=3f58e4f3107d580b8a29626738823a5c;color=#FF69B4;display-name=fernandx_z;emotes=;flags=;id=aa3b5987-1929-414c-bc55-10f9e6c1723e;mod=0;reply-parent-display-name=MaYidRaMaS;reply-parent-msg-body=axozerTem\\sato\\saxozerPium\\saxozerPium_HF;reply-parent-msg-id=2f06b2b8-d33d-4e65-a0c4-82d1894c7b63;reply-parent-user-id=612074199;reply-parent-user-login=mayidramas;room-id=133528221;subscriber=1;tmi-sent-ts=1622471612333;turbo=0;user-id=602696060;user-type= :fernandx_z!fernandx_z@fernandx_z.tmi.twitch.tv PRIVMSG #axozer :@MaYidRaMaS PERO JAJSJAJSJASJASJA'
empty = 'PING'


def create_msgs(count):
    msg = Constructor.create_flexible_irc()
    msgs = [str(msg)]
    for i in range(count):
        msgs.append(str(Constructor.add_mass(msg)))
    return msgs


def main(
        classes=(IRCMsg, IRCMsgOn),
        msgs=(empty, real_irc),
        count_to_generate=25,
        times=1000,
        should_print_stat=True,
):
    msgs = list(msgs) + create_msgs(count_to_generate)
    stat = {_class: [] for _class in classes}

    for _class in classes:
        for i, msg in enumerate(msgs):
            t0 = time()
            for _ in range(times):
                _ = _class(msg)
            stat[_class].append(time()-t0)
            print(f'{_class.__name__}: {i+1}/{len(msgs)} {time()-t0}')
            sys.stdout.write("\033[F")  # back to previous line
            sys.stdout.write("\033[K")  # clear line

    if should_print_stat:
        print_stat(stat, msgs, classes)
    return stat, msgs, classes


def print_stat(stat, msgs, classes):
    first_class = classes[0]
    for i in range(len(msgs)):
        print(first_class(msgs[i]).command, ':', len(msgs[i]))
        for _class in classes:
            print(f'    {classes.index(_class)+1}: {str(stat[_class][i])[:6]}', end=' ')
            if _class is not first_class:
                over_1st = round(stat[_class][i]/stat[first_class][i]*100 - 100)
                over_1st = str(over_1st) if over_1st < 0 else f'+{over_1st}'
                print(' (', over_1st, '% compared to the 1st)', sep='')
            else:
                print()
        print()


if __name__ == '__main__':
    _print = lambda x: print('='*100, x, '='*100)
    _print('statistic')
    main()
    # _print('profiling')
    # import cProfile
    # cProfile.run('main(should_print_stat=False)', sort='cumtime')
