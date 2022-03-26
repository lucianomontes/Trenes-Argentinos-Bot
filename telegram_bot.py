import schedule
import requests


class TelegramBot:
      def __init__(self, bot_token, bot_chat_id) -> None:
            self.token =  bot_token
            self.bot_chat_id = bot_chat_id
      pass

      def send_message(self, mensaje, chat_id = None):

      # Si no pasamos un chat especifico (grupo de telegram), se le asignará el chat del bot
            if chat_id == None:
                  chat_id = self.bot_chat_id

            telegram_text = 'https://api.telegram.org/bot' + self.token + '/sendMessage?chat_id=' + chat_id + '&parse_mode=Markdown&text=' + mensaje

            response = requests.get(telegram_text)

            return response
