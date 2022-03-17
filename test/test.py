import sys
sys.path.append('..')
from src.ircmsg import IRCMsg
# from src_On.ircmsgOn import IRCMsgOn as IRCMsg
from raw_irc_msgs import raw_irc_msgs


def test_irc_msg():
    for name, raw_irc_msg in raw_irc_msgs.items():
        irc_msg = IRCMsg(str(raw_irc_msg))
        assert irc_msg.command == raw_irc_msg.command
        try:
            assert irc_msg.tags == raw_irc_msg.tags
        except AssertionError as e:
            if not irc_msg.tags['wrong_escaping'] == '\\val\\\\ue \\':
                raise AssertionError(irc_msg.tags['wrong_escaping']) from e
        assert irc_msg.params == raw_irc_msg.params
        assert irc_msg.text == irc_msg.trailing == raw_irc_msg.text
        assert irc_msg.nickname == raw_irc_msg.nickname
        assert irc_msg.user == raw_irc_msg.user
        assert irc_msg.host == raw_irc_msg.host
        print(name, 'passed')


def test_parse_raw_tags():
    irc_msg = IRCMsg(r'@no-value-tag;key=value;key2=escaped\svalue\\\: COMMAND')
    assert irc_msg.tags == {'no-value-tag': None, 'key': 'value', 'key2': r'escaped value\;'}
    irc_msg = IRCMsg('COMMAND')
    assert irc_msg.tags == {}


def test_parse_prefix():
    # servername
    irc_msg = IRCMsg(r':server.name.tv COMMAND')
    assert irc_msg.nickname is None
    assert irc_msg.user is None
    assert irc_msg.host == 'server.name.tv'
    # full
    irc_msg = IRCMsg(r':nickname!user@host COMMAND')
    assert irc_msg.nickname == 'nickname'
    assert irc_msg.user == 'user'
    assert irc_msg.host == 'host'
    # no user
    irc_msg = IRCMsg(r':nickname@host COMMAND')
    assert irc_msg.nickname == 'nickname'
    assert irc_msg.user is None
    assert irc_msg.host == 'host'
    # no user, no host
    irc_msg = IRCMsg(r':nickname COMMAND')
    assert irc_msg.nickname == 'nickname'
    assert irc_msg.user is None
    assert irc_msg.host is None
    # None
    irc_msg = IRCMsg('COMMAND')
    assert irc_msg.nickname is None
    assert irc_msg.user is None
    assert irc_msg.host is None


def test_parse_raw_params():
    # middle
    irc_msg = IRCMsg('COMMAND middle')
    assert irc_msg.params == ['middle']
    assert irc_msg.trailing is None
    # middle, trailing (':')
    irc_msg = IRCMsg('COMMAND middle :trailing')
    assert irc_msg.params == ['middle']
    assert irc_msg.trailing == 'trailing'
    # same and trailing contains separators
    irc_msg = IRCMsg('COMMAND middle :trai :ling')
    assert irc_msg.params == ['middle']
    assert irc_msg.trailing == 'trai :ling'
    # trailing
    irc_msg = IRCMsg('COMMAND :trailing')
    assert irc_msg.params == []
    assert irc_msg.trailing == 'trailing'
    # None
    irc_msg = IRCMsg('COMMAND')
    assert irc_msg.params == []
    assert irc_msg.trailing is None


def test_join_tags():
    irc_msg = IRCMsg('EMPTY')
    irc_msg.tags = {'one-tag': 'one-value'}
    assert irc_msg._str_tags() == '@one-tag=one-value '
    irc_msg.tags = {'one-no-tag-value': None}
    assert irc_msg._str_tags() == '@one-no-tag-value '
    irc_msg.tags = {'key': 'value', 'no-value-tag': None, 'key2': 'value2'}
    assert irc_msg._str_tags() == '@key=value;no-value-tag;key2=value2 '


def test_eq():
    # same positions tags
    irc_msg = IRCMsg('@key=value;no-value-tag :username COMMAND')
    new_msg = IRCMsg('@key=value;no-value-tag :username COMMAND')
    assert irc_msg == new_msg
    # different positions tags
    irc_msg = IRCMsg('@key=value;no-value-tag :username COMMAND')
    new_msg = IRCMsg('@no-value-tag;key=value :username COMMAND')
    assert irc_msg == new_msg
    # same positions middles
    irc_msg = IRCMsg('@key=value;no-value-tag :username COMMAND param #target')
    new_msg = IRCMsg('@no-value-tag;key=value :username COMMAND param #target')
    assert irc_msg == new_msg
    # different positions middles
    irc_msg = IRCMsg('@key=value;no-value-tag :username COMMAND param #target :trai :ling')
    new_msg = IRCMsg('@no-value-tag;key=value :username COMMAND #target param :trai :ling')
    assert irc_msg == new_msg
    # others
    assert IRCMsg('COMMAND') == IRCMsg('COMMAND')
    assert IRCMsg('COMMAND') != IRCMsg('ERROR')


def test_str_repr():
    assert str(IRCMsg('COMMAND')) == 'COMMAND'
    assert repr(IRCMsg('COMMAND')) == f'{IRCMsg.__name__}(COMMAND)'

    for raw_irc_msg in raw_irc_msgs.values():
        irc_msg = IRCMsg(str(raw_irc_msg))
        if 'wrong_escaping' not in irc_msg.tags:
            assert str(irc_msg) == str(raw_irc_msg)
