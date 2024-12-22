# Copyright 2024 John Sirois.
# Licensed under the Apache License, Version 2.0 (see LICENSE).

import os
from typing import Any, Dict, Iterator, List, Mapping, Optional, Tuple, cast

from dev_cmd.errors import InvalidModelError
from dev_cmd.model import Command, Dev
from dev_cmd.project import PyProjectToml


def assert_list_str(obj: Any) -> List[str]:
    if not isinstance(obj, list) or not all(isinstance(item, str) for item in obj):
        raise InvalidModelError("TODO: XXX: foo")
    return cast("List[str]", obj)


def assert_dict_str_keys(obj: Any) -> Dict[str, Any]:
    if not isinstance(obj, dict) or not all(isinstance(key, str) for key in obj):
        raise InvalidModelError("TODO: XXX 21")
    return cast("Dict[str, Any]", obj)


def parse_commands(commands: Optional[Dict[str, Any]]) -> Iterator[Command]:
    if not commands:
        raise InvalidModelError("TODO: XXX: -1")

    for name, data in commands.items():
        env = os.environ.copy()
        if isinstance(data, list):
            args = tuple(assert_list_str(data))
            accepts_extra_args = False
        else:
            command = assert_dict_str_keys(data)

            for key, val in assert_dict_str_keys(command.pop("env", {})).items():
                if not isinstance(val, str):
                    raise InvalidModelError("TODO: XXX: 0")
                env[key] = val

            try:
                args = tuple(assert_list_str(command.pop("args")))
            except KeyError:
                raise InvalidModelError("TODO: XXX 1")

            accepts_extra_args = command.pop("accepts-extra-args", False)
            if not isinstance(accepts_extra_args, bool):
                raise InvalidModelError("TODO: XXX 3")
            if data:
                raise InvalidModelError("TODO: XXX 4")
        yield Command(name, env, args, accepts_extra_args=accepts_extra_args)


def parse_aliases(aliases: Optional[Dict[str, Any]]) -> Iterator[Tuple[str, Tuple[str, ...]]]:
    if aliases:
        for alias, commands in aliases.items():
            yield alias, tuple(assert_list_str(commands))


def parse_default(
    default: Optional[Dict[str, Any]],
    commands: Mapping[str, Command],
    aliases: Mapping[str, Tuple[Command, ...]],
) -> Optional[Tuple[str, Tuple[Command, ...]]]:
    if not default:
        if len(commands) == 1:
            name, command = next(iter(commands.items()))
            return name, tuple([command])
        return None

    default_commands: Optional[Tuple[str, Tuple[Command, ...]]] = None
    alias = default.pop("alias", None)
    if alias:
        if not isinstance(alias, str):
            raise InvalidModelError(
                f"Expected default alias to be a string but given {alias} of type {type(alias)}."
            )
        try:
            default_commands = alias, aliases[alias]
        except KeyError:
            raise InvalidModelError(f"The default alias {alias!r} is not defined.")
    else:
        command = default.pop("command", None)
        if command:
            if not isinstance(command, str):
                raise InvalidModelError(
                    f"Expected default command to be a string but given {alias} of type "
                    f"{type(alias)}."
                )
            try:
                default_commands = command, tuple([commands[command]])
            except KeyError:
                raise InvalidModelError(f"The default command {command!r} is not defined.")
    if default:
        raise InvalidModelError(
            f"Unexpected configuration keys in the default table: {' '.join(default)}"
        )
    return default_commands


def parse_dev_config(pyproject_toml: PyProjectToml) -> Dev:
    pyproject_data = pyproject_toml.parse()
    try:
        run_dev_data = assert_dict_str_keys(pyproject_data["tool"]["dev-cmd"])  # type: ignore[index]
    except KeyError as e:
        raise InvalidModelError(
            f"The commands, aliases and defaults run-dev acts upon must be defined in the "
            f"[tool.dev-cmd] table in {pyproject_toml}: {e}"
        )

    def pop_dict(key: str) -> Optional[Dict[str, Any]]:
        data = run_dev_data.pop(key, None)
        return assert_dict_str_keys(data) if data else None

    commands = {command.name: command for command in parse_commands(pop_dict("commands"))}
    aliases: Dict[str, Tuple[Command, ...]] = {}
    for alias, cmds in parse_aliases(pop_dict("aliases")):
        if alias in commands:
            raise InvalidModelError("TODO: XXX: bar")
        alias_cmds: List[Command] = []
        for cmd in cmds:
            if cmd in commands:
                alias_cmds.append(commands[cmd])
            elif cmd in aliases:
                alias_cmds.extend(aliases[cmd])
            else:
                raise InvalidModelError("TODO: XXX: baz")
        aliases[alias] = tuple(alias_cmds)

    default = parse_default(pop_dict("default"), commands, aliases)

    if run_dev_data:
        raise InvalidModelError(
            f"Unexpected configuration keys in the [tool.dev-cmd] table: {' '.join(run_dev_data)}"
        )
    if not commands:
        raise InvalidModelError(
            "No commands are defined in the [tool.dev-cmd.commands] table. At least one must be "
            "configured to use the dev task runner."
        )

    return Dev(default=default, commands=commands, aliases=aliases, source=pyproject_toml.path)
