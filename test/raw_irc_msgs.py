from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class RawIRC:
    """Represents expected parts of a raw_irc_msg"""
    raw_irc_msg: str
    command: str
    tags: dict
    params: list
    text: Optional[str]
    nickname: Optional[str]
    user: Optional[str]
    host: Optional[str]

    def __str__(self):
        return self.raw_irc_msg


raw_tags = r'@tag=value;no-value-tag;escaped_tag=\\\s\:;wrong_escaping=\val\\\ue\s\;no-value-tag-at-the-end '
tags = {
    'tag': 'value',
    'no-value-tag': None,
    'escaped_tag': r'\ ;',
    'wrong_escaping': r'val\ue ',
    'no-value-tag-at-the-end': None,
}

nick = 'nickname'
user = 'user'
host = 'host.com'
prefix_nuh = f':{nick}!{user}@{host} '

command = r'COMMAND'

raw_params = r' param1 param2 param:with:colon'
params = ['param1', 'param2', 'param:with:colon']

trailing = r' :trailing with colon and others:\;!@.'
text = r'trailing with colon and others:\;!@.'

raw_irc_msgs: Dict[str, RawIRC] = dict()

raw_irc_msgs['min'] = RawIRC(
    command,
    command, {}, [], None, None, None, None
    )

raw_irc_msgs['prefix'] = RawIRC(
    prefix_nuh + command,
    command, {}, [], None, nick, user, host
)

raw_irc_msgs['tags'] = RawIRC(
    raw_tags + command,
    command, tags, [], None, None, None, None
)

raw_irc_msgs['tags+prefix'] = RawIRC(
    raw_tags + str(raw_irc_msgs['prefix']),
    command, tags, [], None, nick, user, host
)

raw_irc_msgs['params'] = RawIRC(
    command + raw_params,
    command, {}, params, None, None, None, None
)

raw_irc_msgs['trailing'] = RawIRC(
    command + trailing,
    command, {}, [], text, None, None, None
)

raw_irc_msgs['params+trailing'] = RawIRC(
    command + raw_params + trailing,
    command, {}, params, text, None, None, None
)

raw_irc_msgs['params+trailing'] = RawIRC(
    str(raw_irc_msgs['params']) + trailing,
    command, {}, params, text, None, None, None
)

raw_irc_msgs['real'] = RawIRC(
    '@badge-info=subscriber/1;badges=subscriber/0;client-nonce=3f58e4f3107d580b8a29626738823a5c;color=#FF69B4;'
    'display-name=fernandx_z;emotes=;flags=;id=aa3b5987-1929-414c-bc55-10f9e6c1723e;mod=0;'
    'reply-parent-display-name=MaYidRaMaS;reply-parent-msg-body=axozerTem\\sato\\saxozerPium\\saxozerPium_HF;'
    'reply-parent-msg-id=2f06b2b8-d33d-4e65-a0c4-82d1894c7b63;reply-parent-user-id=612074199;'
    'reply-parent-user-login=mayidramas;room-id=133528221;subscriber=1;tmi-sent-ts=1622471612333;turbo=0;'
    'user-id=602696060;user-type= '
    ':fernandx_z!fernandx_z@fernandx_z.tmi.twitch.tv '
    'PRIVMSG #axozer '
    ':@MaYidRaMaS PERO JAJSJAJSJASJASJA',
    command='PRIVMSG',
    tags={
        'badge-info': 'subscriber/1',
        'badges': 'subscriber/0',
        'client-nonce': '3f58e4f3107d580b8a29626738823a5c',
        'color': '#FF69B4',
        'display-name': 'fernandx_z',
        'emotes': '',
        'flags': '',
        'id': 'aa3b5987-1929-414c-bc55-10f9e6c1723e',
        'mod': '0',
        'reply-parent-display-name': 'MaYidRaMaS',
        'reply-parent-msg-body': 'axozerTem ato axozerPium axozerPium_HF',
        'reply-parent-msg-id': '2f06b2b8-d33d-4e65-a0c4-82d1894c7b63',
        'reply-parent-user-id': '612074199',
        'reply-parent-user-login': 'mayidramas',
        'room-id': '133528221',
        'subscriber': '1',
        'tmi-sent-ts': '1622471612333',
        'turbo': '0',
        'user-id': '602696060',
        'user-type': ''
    },
    text='@MaYidRaMaS PERO JAJSJAJSJASJASJA',
    params=['#axozer'],
    nickname='fernandx_z',
    user='fernandx_z',
    host='fernandx_z.tmi.twitch.tv'
)

