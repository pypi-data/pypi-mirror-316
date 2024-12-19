#!/usr/bin/env python3

import click

import src.defaults.download
from src.defaults import defaults


def __help__(
    name: str | None,
    maximum: bool,
    elements: str | None,
    no_min_max: bool,
    no_score: bool,
):
    name = "" if not name else name
    return f"""
        {("Maximum" if maximum else "Minimum") if not no_min_max else ""}
        {name if no_score else "score threshold"}
        for including {
            ("" if no_score else name)
            + (" " if elements and not no_score else "")
            + (elements if elements else "")
        }.
        """


def __number__(
    name: str | None,
    default_value: int | float | None = None,
    integer: bool = True,
    letter: str | None = None,
    option: str | None = None,
    show_min_max: bool = True,
    show_name: bool = False,
    show_score: bool = True,
    maximum: bool = False,
    help_message: str | None = None,
    elements: str | None = "albums",
):
    s = []
    if show_min_max:
        s.append("max" if maximum else "min")
    if show_name:
        s.append((option if option else name[:4]).lower())
    if show_score:
        s.append("score")
    option = "-".join(s)
    help_message = (
        help_message
        if help_message
        else __help__(
            name=name,
            maximum=maximum,
            elements=elements,
            no_min_max=not show_min_max,
            no_score=not show_score,
        )
    )
    if letter:
        return click.option(
            f"-{letter}",
            f"--{option}",
            type=click.INT if integer else click.FLOAT,
            default=default_value,
            show_default=True,
            help=help_message,
        )
    else:
        return click.option(
            f"--{option}",
            type=click.INT if integer else click.FLOAT,
            default=default_value,
            show_default=True,
            help=help_message,
        )


def aoty_score(
    name: str | None = "AOTY",
    default_value: int | None = None,
    letter: str | None = None,
    option: str | None = None,
    show_min_max: bool = True,
    show_name: bool = False,
    show_score: bool = True,
    maximum: bool = False,
    help_message: str | None = None,
):
    if not default_value:
        default_value = (
            src.defaults.download.AOTY_MAX_SCORE
            if maximum
            else src.defaults.download.AOTY_MIN_SCORE
        )
    return __number__(
        name=name,
        integer=True,
        default_value=default_value,
        letter=letter,
        option=option,
        show_min_max=show_min_max,
        show_name=show_name,
        show_score=show_score,
        maximum=maximum,
        help_message=help_message,
    )


def prog_score(
    name: str | None = "ProgArchives",
    default_value: int | None = None,
    letter: str | None = None,
    option: str | None = None,
    show_min_max: bool = True,
    show_name: bool = False,
    show_score: bool = True,
    maximum: bool = False,
    help_message: str | None = None,
):
    if not default_value:
        default_value = (
            src.defaults.download.PROG_MAX_SCORE
            if maximum
            else src.defaults.download.PROG_MIN_SCORE
        )
    return __number__(
        name=name,
        integer=True,
        default_value=default_value,
        letter=letter,
        option=option,
        show_min_max=show_min_max,
        show_name=show_name,
        show_score=show_score,
        maximum=maximum,
        help_message=help_message,
    )


def albums_score(
    name: str | None = "albums",
    integer: bool = False,
    default: int | None = None,
    letter: str | None = None,
    option: str | None = "album",
    show_min_max: bool = True,
    show_name: bool = False,
    maximum: bool = False,
    help_message: str | None = None,
):
    if not default:
        default = (
            defaults.ALBUM_MAX_SCORE if maximum else defaults.ALBUM_MIN_SCORE
        )
    return __number__(
        name=name,
        integer=integer,
        default_value=default,
        letter=letter,
        option=option,
        show_min_max=show_min_max,
        show_name=show_name,
        show_score=True,
        maximum=maximum,
        help_message=help_message,
        elements="",
    )


def tracks_score(
    name: str | None = "tracks",
    integer: bool = True,
    default: int | None = None,
    letter: str | None = None,
    option: str | None = "tracks",
    show_min_max: bool = True,
    show_name: bool = False,
    maximum: bool = False,
    help_message: str | None = None,
):
    if not default:
        default = (
            defaults.TRACK_MAX_SCORE if maximum else defaults.TRACK_MIN_SCORE
        )
    return __number__(
        name=name,
        integer=integer,
        default_value=default,
        letter=letter,
        option=option,
        show_min_max=show_min_max,
        show_name=show_name,
        show_score=True,
        maximum=maximum,
        help_message=help_message,
        elements=None,
    )


def ratings(
    name: str = "ratings",
    default: int | None = None,
    letter: str | None = None,
    option: str | None = "ratings",
    show_min_max: bool = True,
    maximum: bool = False,
    help_message: str | None = None,
):
    if not default:
        default = (
            defaults.ALBUM_MAX_RATINGS
            if maximum
            else defaults.ALBUM_MIN_RATINGS
        )
    return __number__(
        name=name,
        integer=True,
        default_value=default,
        letter=letter,
        option=option,
        show_min_max=show_min_max,
        show_name=True,
        show_score=False,
        maximum=maximum,
        help_message=help_message,
        elements="tracks",
    )


def similarity(
    name: str = "rate of similarity",
    default_value: int | None = 0.6,
    letter: str | None = "s",
    option: str | None = None,
    show_min_max: bool = True,
    maximum: bool = False,
    help_message: str | None = None,
):
    return __number__(
        name=name,
        integer=False,
        default_value=default_value,
        letter=letter,
        option=option,
        show_min_max=show_min_max,
        show_name=True,
        show_score=False,
        maximum=maximum,
        help_message=help_message,
        elements="matches",
    )


def num_results(
    name: str = "results",
    default_value: int | None = 15,
    letter: str | None = "r",
    option: str | None = "results",
    help_message: str = "Limit of results to return.",
):
    return __number__(
        name=name,
        integer=True,
        default_value=default_value,
        letter=letter,
        option=option,
        show_min_max=True,
        show_name=True,
        show_score=False,
        maximum=True,
        help_message=help_message,
        elements="matches",
    )


def limit_per_column(
    name: str,
    entries: str = "albums",
    default_value: int | None = None,
    letter: str | None = None,
    option: str | None = None,
    help_message: str | None = None,
):
    if not help_message:
        help_message = f"Limit of {entries} returned per {name} column."
    if not option:
        option = f"limit-{name.lower()}"
    return __number__(
        name=name,
        integer=True,
        default_value=default_value,
        letter=letter,
        option=option,
        show_min_max=False,
        show_name=True,
        show_score=False,
        maximum=True,
        help_message=help_message,
        elements=entries,
    )
