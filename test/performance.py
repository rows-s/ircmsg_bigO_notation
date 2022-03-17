from time import time
from random import choices
from src_On.ircmsgOn import IRCMsgOn
from src.ircmsg import IRCMsg


raw_irc_msg = '@badge-info=subscriber/1;badges=subscriber/0;client-nonce=3f58e4f3107d580b8a29626738823a5c;color=#FF69B4;display-name=fernandx_z;emotes=;flags=;id=aa3b5987-1929-414c-bc55-10f9e6c1723e;mod=0;reply-parent-display-name=MaYidRaMaS;reply-parent-msg-body=axozerTem\\sato\\saxozerPium\\saxozerPium_HF;reply-parent-msg-id=2f06b2b8-d33d-4e65-a0c4-82d1894c7b63;reply-parent-user-id=612074199;reply-parent-user-login=mayidramas;room-id=133528221;subscriber=1;tmi-sent-ts=1622471612333;turbo=0;user-id=602696060;user-type= :fernandx_z!fernandx_z@fernandx_z.tmi.twitch.tv PRIVMSG #axozer :@MaYidRaMaS PERO JAJSJAJSJASJASJA'
empty = 'PING'

tags_leng = 1000
params_leng = 1000

tag_population = 'abcdefghijklmnopqrstuvwxyz'
tag_population += tag_population.upper()
tag_population += '-'

value_population = tag_population + r'\:!@#$%^&*(){}[]'
params_population = value_population.replace(':', '')
trailing_population = value_population + ' '

tags = {
    ''.join(choices(tag_population, k=25)): ''.join(choices(value_population, k=150))
    for _ in range(tags_leng)
}
nick = 'someusersnickname'
user = 'someuserslogin'
host = 'and.some.host.com'
params = [''.join(choices(params_population, k=25)) for _ in range(params_leng)]
trailing = ''.join(choices(trailing_population, k=1000))

mim = massive_irc_msg = IRCMsg('MASSIVE')
mim.tags, mim.params, mim.trailing = tags, params, trailing
mim.nickname, mim.user, mim.host = nick, user, host
raw_massive_irc_msg = str(massive_irc_msg)

avarage_irc_msg = massive_irc_msg._str_tags()[:4500] + ' '
avarage_irc_msg += massive_irc_msg._str_prefix() + massive_irc_msg.command
avarage_irc_msg += massive_irc_msg._str_params()[:4500] + ' :' + massive_irc_msg.trailing
raw_avarage_irc_msg = str(avarage_irc_msg)


def main(
        classes=(IRCMsg, IRCMsgOn),
        msgs=(raw_massive_irc_msg, avarage_irc_msg, raw_irc_msg, empty),
        times=100,
        print_stat=True,
):
    stat = {_class: [] for _class in classes}
    first_class = classes[0]
    for _class in classes:
        for i, msg in enumerate(msgs):
            t0 = time()
            for _ in range(times):
                _ = _class(msg)
            stat[_class].append(time()-t0)

    if print_stat:
        for i in range(len(msgs)):
            print(len(msgs[i]), ':', msgs[i][:200])
            for _class in classes:
                print(f'    {classes.index(_class)+1}: {str(stat[_class][i])[:6]}', end=' ')
                if _class is not first_class:
                    over_1st = stat[_class][i]/stat[first_class][i]*100
                    print(' (+', round(over_1st), '% over the 1st)', sep='')
                else:
                    print()
            print()


if __name__ == '__main__':
    _print = lambda x: print('='*100, x, '='*100)
    _print('statistic')
    main()
    _print('profiling')
    import cProfile
    cProfile.run('main(print_stat=False)', sort='cumtime')
