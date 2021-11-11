import logging


from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    CallbackContext,
    MessageHandler,
    Filters,
    ConversationHandler,)


# this will help with debugging by letting me know of the errors
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)
ORDER, BUY, SERVER, ID, CONFIRM, END, ORDERED = range(7)

admin_id = ""


order_keyboard = []


def start (update:Update, context:CallbackContext)->None:
    context.bot.send_message(chat_id= update.effective_user.id,
    text =("hello"))

    context.bot.send_message(chat_id=update.effective_user.id, text = "Use /order to begin ordering!")

    return ORDER

def order (update:Update, context:CallbackContext)->None:

    context.bot.send_message(chat_id= update.effective_user.id, text = "What would you like to buy?", reply_markup=ReplyKeyboardMarkup(order_keyboard))
    return ID

def id (update:Update, context:CallbackContext)->None:
    global diamond
    diamond = update.message.text

    context.bot.send_message (chat_id = update.effective_user.id, text = "What is your ID number?",reply_markup=ReplyKeyboardRemove())
    return SERVER

def server (update:Update, context:CallbackContext)->None:
    global id

    id = update.message.text
    context.bot.send_message (chat_id = update.effective_user.id, text = "What is your server number?")
    return CONFIRM

def confirm (update:Update, context:CallbackContext)->None:
    global server
    server = update.message.text
    context.bot.send_message (chat_id = update.effective_user.id,
    text = "Please review your order!\n\n"
    f"Item Wanted: {diamond}\n"
    f"ID: {id}\n"
    f"Server: {server}\n\n"
    "Use /confirm to confirm your order!")
    return END

def end (update:Update, context:CallbackContext)->None:
    context.bot.send_message (chat_id = update.effective_user.id, text= "Before we place your order, we require you to make payment first!")
    context.bot.send_message(chat_id=update.effective_user.id,
                             text=""
                             "")
    context.bot.send_message (chat_id = update.effective_user.id, text="")


    return ORDERED

def admin (update:Update, context:CallbackContext)->None:
    file_id = update.message['photo'][-1]['file_id']
    context.bot.sendPhoto(chat_id=admin_id,
                          caption=(
                              f"{update.effective_user.first_name}'s order\n"
                              f"ID: {id}  Server: {server}\n"
                              f"Order wanted: {diamond}"),
                          photo=file_id)
    context.bot.send_message (chat_id = update.effective_user.id, text= ""
                              "n")
    context.bot.send_message (chat_id = update.effective_user.id, text = "")

    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
   
    user = update.message.from_user
    logger.info("User %s canceled the booking.", user.first_name)
    update.message.reply_text(
        'Order has been cancelled! Do /start to try again!', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END

def help (update:Update, context:CallbackContext)->None:

    update.message.reply_text ("Do /start to view the prices!\n"
                               "Do /cancel at any point to restart the bot!"
                               "Do /order to begin ordering!\n\n"
                               "If you have other questions, please send your question to @badawg.")

def main() -> None:
    updater = Updater(token='', use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ORDER: [MessageHandler((Filters.command), order)],
            ID: [MessageHandler(Filters.regex (''), id)],
            SERVER: [MessageHandler((Filters.regex ('')), server)],
            CONFIRM: [MessageHandler((Filters.regex ('')), confirm)],
            END: [MessageHandler((Filters.command), end)],
            ORDERED: [MessageHandler((Filters.photo | Filters.document), admin)],

        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)

    start_handler = CommandHandler('start',start)
    order_handler = CommandHandler('order',order)
    help_handler = CommandHandler('help', help)
    confirm_handler = CommandHandler('confirm', confirm)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(order_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(confirm_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
