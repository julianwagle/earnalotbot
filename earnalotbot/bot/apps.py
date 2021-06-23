from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BotConfig(AppConfig):
    name = "earnalotbot.bot"
    verbose_name = _("Bot")
