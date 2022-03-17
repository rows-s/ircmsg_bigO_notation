from copy import copy
from typing import Optional, Dict, List

from src.utils import escape_tag_value

__all__ = ('IRCMsgOn',)


class IRCMsgOn:
    def __init__(
            self,
            raw_irc_msg: str
    ) -> None:
        self.command: str = ''
        # raw_tags
        self.tags: Dict[str, Optional[str]] = {}
        # prefix
        self.nickname: Optional[str] = None
        self.user: Optional[str] = None
        self.host: Optional[str] = None
        # raw_params
        self.params: List[str] = []
        self.trailing: Optional[str] = None

        self._parse_raw_irc_msg(raw_irc_msg)

    @property
    def text(self):
        return self.trailing

    @text.setter
    def text(self, value):
        self.trailing = value

    @classmethod
    def create_empty(cls):
        return cls('EMPTY')

    def copy(self):
        new = copy(self)
        new.tags = self.tags.copy()
        new.params = self.params.copy()
        return new

    def _parse_raw_irc_msg(
            self,
            raw_irc_msg: str
    ):
        """O(n) parsing algorithm"""
        i = 0
        if raw_irc_msg[0] == '@':
            i = self._parse_raw_tags(raw_irc_msg, i) + 1  # `i` now points at ' '

        if raw_irc_msg[i] == ':':
            i = self._parse_prefix(raw_irc_msg, i) + 1

        while i != len(raw_irc_msg) and (sym := raw_irc_msg[i]) != ' ':
            self.command += sym
            i += 1

        if i != len(raw_irc_msg):
            self._parse_raw_params(raw_irc_msg, i+1)

    def _parse_raw_tags(
            self,
            raw_irc_msg: str,
            start: int,
    ) -> int:
        """
        Sets `self.tags` with unescaped values

        Args:
            raw_irc_msg: not sliced raw irc msg
            start: start's index of tags (points at '@')

        Return:
            end's index of raw tags
        """
        i = start + 1
        tag, value = '', None
        unescape_map = {'s': ' ', ':': ';', '\\': '\\'}
        # loop
        while (sym := raw_irc_msg[i]) != ' ':
            # saving and reset
            if sym == ';':
                self.tags[tag] = value
                tag, value = '', None
            # tag filling
            elif value is None:
                if sym == '=':
                    value = ''
                else:
                    tag += sym
            # value filling
            else:
                if sym == '\\':
                    i += 1  # skip next sym. Or current in case of exception
                    try:
                        sym = unescape_map[raw_irc_msg[i]]  # `i` has increased
                    except KeyError:  # if wrong escaping, set next value as raw
                        continue
                value += sym
            i += 1
        # saving last
        self.tags[tag] = value
        return i

    def _parse_prefix(
            self,
            raw_irc_msg: str,
            start,
    ) -> int:
        """
        Sets `self.servername`, `self.nickname`, `self.user`, `self.host`

        Args:
            raw_irc_msg: not sliced raw irc msg
            start: start's index of prefix (points at ':')

        Return:
            end's index of prefix
        """
        i = start + 1
        is_servername = False
        raw_first_part = ''
        # loop
        while (sym := raw_irc_msg[i]) != ' ':
            # choosing what to fill
            if sym == '!':
                self.user = ''  # we're filling user now
            elif sym == '@':
                self.host = ''  # we're filling host now
            # filling
            elif self.host is not None:
                self.host += sym  # being filled third
            elif self.user is not None:
                self.user += sym  # being filled second
            else:
                raw_first_part += sym  # being filled first
            # is_servername checking
            if sym == '.' and self.host is None and self.user is None:  # don't take dots from user and host
                is_servername = True
            i += 1
        # set servername or nickname
        if is_servername:
            self.host = raw_first_part
        else:
            self.nickname = raw_first_part
        return i

    def _parse_raw_params(
            self,
            raw_irc_msg: str,
            start: int
    ) -> int:
        """
        Sets `self.params`, `self.trailing`

        Args:
            raw_irc_msg: not sliced raw irc msg
            start: start's index of raw params

        Return:
            end's index of raw params
        """
        i = start
        param = ''
        # loop
        while i != len(raw_irc_msg):
            sym = raw_irc_msg[i]
            if sym == ' ':
                self.params.append(param)
                param = ''
            elif sym == ':' and not param:  # param may contain ':' but must not start with
                self.trailing = raw_irc_msg[i+1:]
                break
            else:
                param += sym
            i += 1
        # add last
        self.params.append(param) if param else None
        return i

    def _str_tags(self) -> Optional[str]:
        if not self.tags:
            return ''
        else:
            raw_tags = '@'
            for key, value in self.tags.items():
                if raw_tags != '@':  # won't do it after last one and before first
                    raw_tags += ';'
                raw_tags += key
                if value is not None:
                    raw_tags += '=' + escape_tag_value(value)  # O(n) where n is len of value
        return raw_tags + ' '

    def _str_prefix(self) -> Optional[str]:
        if not any((self.nickname, self.user, self.host)):
            return ''
        if self.host and not any((self.nickname, self.user)):
            return f':{self.host}'
        prefix = ':'
        prefix += self.nickname if self.nickname is not None else ''
        prefix += f'!{self.user}' if self.user is not None else ''
        prefix += f'@{self.host}' if self.host is not None else ''
        return f'{prefix} '

    def _str_params(self) -> Optional[str]:
        raw_params = ''
        if self.params:
            raw_params = ' ' + ' '.join(self.params)
        if self.trailing:
            raw_params += f' :{self.trailing}'
        return raw_params

    def __eq__(self, other) -> bool:
        try:
            assert isinstance(other, IRCMsgOn)
            assert self.command == other.command
            assert self.nickname == other.nickname
            assert self.host == other.host
            assert self.user == other.user
            assert self.tags == other.tags
            assert set(self.params) == set(other.params)
            assert self.trailing == other.trailing
        except AssertionError:
            return False
        else:
            return True

    def __str__(self):
        return f'{self._str_tags()}{self._str_prefix()}{self.command}{self._str_params()}'

    def __repr__(self):
        return f'{self.__class__.__name__}({str(self)})'
