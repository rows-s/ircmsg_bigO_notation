from copy import copy
from typing import Optional, Dict, List

from src_On.utils import escape_tag_value, unescape_tag_value

__all__ = ('IRCMsg',)


class IRCMsg:
    def __init__(
            self,
            raw_irc_msg: str
    ) -> None:
        self.command: str
        # raw_tags
        self.tags: Dict[str, Optional[str]] = {}
        # prefix
        self.nickname: Optional[str] = None
        self.user: Optional[str] = None
        self.host: Optional[str] = None
        # raw_params
        self.params: List[str] = []
        self.trailing: Optional[str] = None

        # whole logic within it
        self._parse_raw_irc_msg(raw_irc_msg)

    @property
    def text(self):
        return self.trailing

    @text.setter
    def text(self, value):
        self.trailing = value

    def copy(self):
        new = copy(self)
        new.tags = self.tags.copy()
        new.params = self.params.copy()
        return new

    def _parse_raw_irc_msg(
            self,
            raw_irc_msg: str
    ):
        if raw_irc_msg.startswith('@'):
            raw_tags, raw_irc_msg = raw_irc_msg[1:].split(' ', 1)  # at least one tag. Ends with ' '
            self._parse_raw_tags(raw_tags)
        if raw_irc_msg.startswith(':'):
            prefix, raw_irc_msg = raw_irc_msg[1:].split(' ', 1)  # ends with ' '
            self._parse_prefix(prefix)

        try:
            self.command, raw_irc_msg = raw_irc_msg.split(' ', 1)
        except ValueError:
            self.command = raw_irc_msg
        else:
            self._parse_raw_params(raw_irc_msg)

    def _parse_raw_tags(
            self,
            raw_tags: str
    ):
        for raw_tag in raw_tags.split(';'):
            try:
                key, value = raw_tag.split('=', 1)
            except ValueError:  # if has not value
                key, value = raw_tag, None
            else:  # if has value
                value = unescape_tag_value(value)
            finally:
                self.tags[key] = value

    def _parse_prefix(
            self,
            prefix: str
    ):
        try:
            prefix, self.host = prefix.split('@', 1)
        except ValueError:
            pass

        try:
            prefix, self.user = prefix.split('!', 1)
        except ValueError:
            pass

        if '.' not in prefix:  # host and user are cut out
            self.nickname = prefix
        else:
            self.host = prefix

    def _parse_raw_params(
            self,
            raw_params: str
    ):
        if raw_params.startswith(':'):
            self.trailing = raw_params.removeprefix(':')
            return

        try:
            raw_params, self.trailing = raw_params.split(' :', 1)
        except ValueError:
            pass
        finally:
            self.params = raw_params.split(' ') if raw_params else []

    def _str_tags(self) -> str:
        if not self.tags:
            return ''
        raw_tags = ';'.join(
            [key + (f'={escape_tag_value(value)}' if value is not None else '')
             for key, value in self.tags.items()]
        )
        return f"@{raw_tags} "

    def _str_prefix(self) -> str:
        if not any((self.nickname, self.user, self.host)):
            return ''
        if self.host and not any((self.nickname, self.user)):
            return f':{self.host}'
        prefix = ':'
        prefix += self.nickname if self.nickname is not None else ''
        prefix += f'!{self.user}' if self.user is not None else ''
        prefix += f'@{self.host}' if self.host is not None else ''
        return f'{prefix} '

    def _str_params(self) -> str:
        raw_params = ''
        if self.params:
            raw_params += ' ' + ' '.join(self.params)
        if self.trailing:
            raw_params += f" :{self.trailing}"
        return raw_params

    def __eq__(self, other) -> bool:
        try:
            assert isinstance(other, IRCMsg)
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
