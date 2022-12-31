#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Telegram bot to play UNO in group chats
# Copyright (c) 2016 Jannes Höke <uno@jhoeke.de>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


"""Defines helper functions to build the inline result list"""

from uuid import uuid4

from telegram import InlineQueryResultArticle, InputTextMessageContent, \
    InlineQueryResultCachedSticker as Sticker

import card as c
from utils import display_color, display_color_group, display_name
from internationalization import _, __


def add_choose_color(results, game):
    """Adicionar opções de cores escolhidas"""
    for color in c.COLORS:
        results.append(
            InlineQueryResultArticle(
                id=color,
                title=_("Escolher a cor"),
                description=display_color(color),
                input_message_content=
                InputTextMessageContent(display_color_group(color, game))
            )
        )


def add_other_cards(player, results, game):
    """Adicionar cartões de mão ao escolher cores"""

    results.append(
        InlineQueryResultArticle(
            "hand",
            title=_("Cartão (toque para o estado do jogo):",
                    "Cartas (toque para o estado do jogo):",
                    len(player.cards)),
            description=', '.join([repr(card) for card in player.cards]),
            input_message_content=game_info(game)
        )
    )


def player_list(game):
    """Generate list of player strings"""
    return [_("{name} ({number} cartão)",
              "{name} ({number} cartas)",
              len(player.cards))
            .format(name=player.user.first_name, number=len(player.cards))
            for player in game.players]


def add_no_game(results):
    """Add text result if user is not playing"""
    results.append(
        InlineQueryResultArticle(
            "nogame",
            title=_("Você não está jogando"),
            input_message_content=
            InputTextMessageContent(_('Não está jogando agora. Use /new para '
                                      'iniciar um jogo ou /join para entrar ao '
                                      'jogo atual neste grupo'))
        )
    )


def add_not_started(results):
    """Add text result if the game has not yet started"""
    results.append(
        InlineQueryResultArticle(
            "nogame",
            title=_("O jogo ainda não tinha começado"),
            input_message_content=
            InputTextMessageContent(_('Comece o jogo com /start'))
        )
    )


def add_mode_classic(results):
    """Alterar o modo para clássico"""
    results.append(
        InlineQueryResultArticle(
            "mode_classic",
            title=_("🎻 Classic mode"),
            input_message_content=
            InputTextMessageContent(_('Classic 🎻'))
        )
    )


def add_mode_fast(results):
    """Change mode to classic"""
    results.append(
        InlineQueryResultArticle(
            "mode_fast",
            title=_("🚀 Sanic mode"),
            input_message_content=
            InputTextMessageContent(_('Tem que ir rápido! 🚀'))
        )
    )


def add_mode_wild(results):
    """Alterar o modo para clássico"""
    results.append(
        InlineQueryResultArticle(
            "mode_wild",
            title=_("🐉 Wild mode"),
            input_message_content=
            InputTextMessageContent(_('Na Natureza~ 🐉'))
        )
    )


def add_mode_text(results):
    """Alterar o modo para texto"""
    results.append(
        InlineQueryResultArticle(
            "mode_text",
            title=_("✍️ Text mode"),
            input_message_content=
            InputTextMessageContent(_('Text ✍️'))
        )
    )
    
    
def add_draw(player, results):
    """Adicionar opção para desenhar"""
    n = player.game.draw_counter or 1

    results.append(
        Sticker(
            "draw", sticker_file_id=c.STICKERS['option_draw'],
            input_message_content=
            InputTextMessageContent(__('Pegou {number} carta',
                                       'Pegou {number} cartas', n,
                                       multi=player.game.translate)
                                    .format(number=n))
        )
    )


def add_gameinfo(game, results):
    """Add option to show game info"""

    results.append(
        Sticker(
            "gameinfo",
            sticker_file_id=c.STICKERS['option_info'],
            input_message_content=game_info(game)
        )
    )


def add_pass(results, game):
    """Add option to pass"""
    results.append(
        Sticker(
            "pass", sticker_file_id=c.STICKERS['option_pass'],
            input_message_content=InputTextMessageContent(
                __('Passo', multi=game.translate)
            )
        )
    )


def add_call_bluff(results, game):
    """Add option to call a bluff"""
    results.append(
        Sticker(
            "call_bluff",
            sticker_file_id=c.STICKERS['option_bluff'],
            input_message_content=
            InputTextMessageContent(__("Estou chamando seu blefe!",
                                       multi=game.translate))
        )
    )


def add_card(game, card, results, can_play):
    """Add an option that represents a card"""

    if can_play:
        if game.mode != "text":
            results.append(
                Sticker(str(card), sticker_file_id=c.STICKERS[str(card)])
        )
        if game.mode == "text":
            results.append(
                Sticker(str(card), sticker_file_id=c.STICKERS[str(card)], input_message_content=InputTextMessageContent("Card Played: {card}".format(card=repr(card).replace('Draw Four', '+4').replace('Draw', '+2').replace('Colorchooser', 'Color Chooser')))
        ))
    else:
        results.append(
            Sticker(str(uuid4()), sticker_file_id=c.STICKERS_GREY[str(card)],
                    input_message_content=game_info(game))
        )


def game_info(game):
    players = player_list(game)
    return InputTextMessageContent(
        _("Jogador atual: {name}")
        .format(name=display_name(game.current_player.user)) +
        "\n" +
        _("Última carta: {card}").format(card=repr(game.last_card)) +
        "\n" +
        _("Jogador: {player_list}",
          "Jogadores: {player_list}",
          len(players))
        .format(player_list=" -> ".join(players))
    )
