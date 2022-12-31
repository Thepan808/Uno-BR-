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

from telegram import ParseMode, Update
from telegram.ext import CommandHandler, CallbackContext

from user_setting import UserSetting
from utils import send_async
from shared_vars import dispatcher
from internationalization import _, user_locale

@user_locale
def help_handler(update: Update, context: CallbackContext):
    """Handler for the /help command"""
    help_text = _("Siga estes passos:\n\n"
      "1. Adicionar este bot a um grupo\n"
      "2. No grupo, comece um novo jogo com /new ou junte-se a um já"
      " jogo em execução com /join\n"
      "3. Depois que pelo menos dois jogadores se juntarem, comece o jogo com"
      " /start\n"
      "4. Tipo <code>@Makoto_xyz_bot</code> na sua caixa de bate-papo e clique em "
      "<b>espaço</b>, ou clique no botão <code>via @Makoto_xyz_bot</code> texto "
      "ao lado de mensagens. Você verá seus cartões (alguns acinzentados), "
      "quaisquer opções extras, como desenho, e um <b>?</b> para ver o "
      "estado atual do jogo. O <b>cartões acinzentados</b> são aqueles que você "
      "<b>não pode jogar</b> no momento. Toque em uma opção para executar "
      "a ação selecionada.\n"
      "Os jogadores podem participar do jogo a qualquer momento. Para sair de um jogo, "
      "use /leave. Se um jogador demorar mais de 90 segundos a jogar, "
      "você pode usar /skip para pular esse jogador. Use /notify_me para "
      "receber uma mensagem privada quando um novo jogo é iniciado.\n\n"
      "<b>Idioma</b> e outras configurações: /settings\n"
      "Outros comandos (somente criador de jogos):\n"
      "/close - Fechar lobby\n"
      "/open - Abrir lobby\n"
      "/kill - Encerrar o jogo\n"
      "/kick - Selecione um jogador para vazar do jogo "
      "respondendo-lhe\n"
      "/enable_translations - Traduzir textos relevantes em todos "
      "idiomas falados em um jogo\n"
      "/disable_translations - Use Inglês ou Português para esses textos\n\n"
      "<b>Experimental:</b> Jogue em vários grupos ao mesmo tempo. "
      "Pressione o botão <code>Jogo atual: ...</code> e selecione o botão "
      "grupo no qual você deseja jogar uma carta.\n"
      "Se você gosta deste bot, "
      "<a href=\"https://telegram.me/the_panda_official\">"
      "avalie-me</a>, junte-se ao "
      "<a href=\"https://telegram.me/botssaved\">Canal</a>"
      " e se divertir em um jogo de cartas UNO.")

    send_async(context.bot, update.message.chat_id, text=help_text,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)

@user_locale
def modes(update: Update, context: CallbackContext):
    """Handler for the /help command"""
    modes_explanation = _("Este bot UNO tem quatro modos de jogo: Classic, Sanic, Wild e Text.\n\n"
      " 🎻 O modo Classic usa o deck UNO convencional e não há salto automático.\n"
      " 🚀 O modo Sanic usa o baralho UNO convencional e o bot ignora automaticamente um jogador se ele demorar muito para jogar sua vez.\n"
      " 🐉 O modo Wild usa um baralho com mais cartas especiais, menos variedade de números e nenhum salto automático.\n"
      " ✍️ O modo Texto usa o deck UNO convencional, mas em vez de adesivos ele usa o texto.\n\n"
      "To change the game mode, the GAME CREATOR has to type the bot nickname and a space, "
      "just like when playing a card, and all gamemode options should appear.")
    send_async(context.bot, update.message.chat_id, text=modes_explanation,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)

@user_locale
def source(update: Update, context: CallbackContext):
    """Handler for the /help command"""
    source_text = _("This bot is Free Software and licensed under the AGPL. "
      "The code is available here: \n"
      "https://github.com/jh0ker/mau_mau_bot")
    attributions = _("Attributions:\n"
      'Draw icon by '
      '<a href="http://www.faithtoken.com/">Faithtoken</a>\n'
      'Pass icon by '
      '<a href="http://delapouite.com/">Delapouite</a>\n'
      "Originals available on http://game-icons.net\n"
      "Icons edited by ɳick")

    send_async(context.bot, update.message.chat_id, text=source_text + '\n' +
                                                 attributions,
               parse_mode=ParseMode.HTML, disable_web_page_preview=True)


@user_locale
def news(update: Update, context: CallbackContext):
    """Handler for the /news command"""
    send_async(context.bot, update.message.chat_id,
               text=_("All news here: https://telegram.me/unobotupdates"),
               disable_web_page_preview=True)


@user_locale
def stats(update: Update, context: CallbackContext):
    user = update.message.from_user
    us = UserSetting.get(id=user.id)
    if not us or not us.stats:
        send_async(context.bot, update.message.chat_id,
                   text=_("You did not enable statistics. Use /settings in "
                          "a private chat with the bot to enable them."))
    else:
        stats_text = list()

        n = us.games_played
        stats_text.append(
            _("{number} game played",
              "{number} games played",
              n).format(number=n)
        )

        n = us.first_places
        m = round((us.first_places / us.games_played) * 100) if us.games_played else 0
        stats_text.append(
            _("{number} first place ({percent}%)",
              "{number} first places ({percent}%)",
              n).format(number=n, percent=m)
        )

        n = us.cards_played
        stats_text.append(
            _("{number} card played",
              "{number} cards played",
              n).format(number=n)
        )

        send_async(context.bot, update.message.chat_id,
                   text='\n'.join(stats_text))


def register():
    dispatcher.add_handler(CommandHandler('help', help_handler))
    dispatcher.add_handler(CommandHandler('source', source))
    dispatcher.add_handler(CommandHandler('news', news))
    dispatcher.add_handler(CommandHandler('stats', stats))
    dispatcher.add_handler(CommandHandler('modes', modes))
