# -*- coding: utf-8 -*-

import json
import logging
import urllib
import urllib2
import random
import fnmatch

import time
import datetime

from google.appengine.api import urlfetch
from google.appengine.ext import ndb
import webapp2

TOKEN = ''

BASE_URL = 'https://api.telegram.org/bot' + TOKEN + '/'


# ================================

class EnableStatus(ndb.Model):
    # key name: str(chat_id)
    enabled = ndb.BooleanProperty(indexed=False, default=False)

class WinStatus(ndb.Model):
    wins = ndb.IntegerProperty(default=0)

'''
w1 = WinStatus()
winz = w1.put()
'''

class LossStatus(ndb.Model):
    losses = ndb.IntegerProperty(default=0)

'''
l1 = LossStatus()
lossez = l1.put()
'''

# ================================

def setEnabled(chat_id, yes):
    es = EnableStatus.get_or_insert(str(chat_id))
    es.enabled = yes
    es.put()

def getEnabled(chat_id):
    es = EnableStatus.get_by_id(str(chat_id))
    if es:
        return es.enabled
    return False

def addWin():
    winz = WinStatus.get_or_insert(str(7))
    winz.wins = winz.wins + 1
    winz.put()

def checkWins():
    winz = WinStatus.get_by_id(str(7))
    return winz.wins

def addLoss():
    lossez = LossStatus.get_or_insert(str(7))
    lossez.losses = lossez.losses + 1
    lossez.put()

def checkLosses():
    lossez = LossStatus.get_by_id(str(7))
    return lossez.losses

'''
def addWin(new):
    w2 = winz.get()
    if new:
        w2.wins = w2.wins + 1
        w2.put()
    return w2.wins

def addLoss(new):
    l2 = lossez.get()
    if new:
        l2.losses = l2.losses + 1
        l2.put()
    return l2.losses
'''

# ================================

class MeHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getMe'))))


class GetUpdatesHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'getUpdates'))))


class SetWebhookHandler(webapp2.RequestHandler):
    def get(self):
        urlfetch.set_default_fetch_deadline(60)
        url = self.request.get('url')
        if url:
            self.response.write(json.dumps(json.load(urllib2.urlopen(BASE_URL + 'setWebhook', urllib.urlencode({'url': url})))))


class WebhookHandler(webapp2.RequestHandler):
    def post(self):
        urlfetch.set_default_fetch_deadline(60)
        body = json.loads(self.request.body)
        logging.info('request body:')
        logging.info(body)
        self.response.write(json.dumps(body))

        update_id = body['update_id']
        try:
            message = body['message']
            text = message.get('text')
        except:
            if 'channel_post' in body: return
            if 'edited_channel_post' in body: return
            message = body['edited_message']
            text = ""
        message_id = message.get('message_id')
        date = message.get('date')
        text = message.get('text')
        fr = message.get('from')
        firstname = fr.get('first_name')
        lastname = fr.get('last_name')
        fullname = firstname + " " + lastname
        chat = message['chat']
        chat_id = chat['id']

        if not text:
            logging.info('no text')
            return

        def reply(msg):
            resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                'chat_id': str(chat_id),
                'text': msg,
                'disable_web_page_preview': 'true',
            })).read()
            logging.info('send response:')
            logging.info(resp)

        def quoteReply(msg):
            resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                'chat_id': str(chat_id),
                'text': msg,
                'disable_web_page_preview': 'true',
                'reply_to_message_id': str(message_id),
            })).read()
            logging.info('send response:')
            logging.info(resp)

        def chatReply(s_chat_id, msg):
            resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                'chat_id': str(s_chat_id),
                'text': msg,
            })).read()
            logging.info('send response:')
            logging.info(resp)

        def stickerReply(sticker):
            resp = urllib2.urlopen(BASE_URL + 'sendSticker', urllib.urlencode({
                'chat_id': str(chat_id),
                'sticker': sticker,
            })).read()
            logging.info('send response:')
            logging.info(resp)

        def delMessage():
            resp = urllib2.urlopen(BASE_URL + 'deleteMessage', urllib.urlencode({
                'chat_id': str(chat_id),
                'message_id': str(message_id),
            })).read()
            logging.info('send response:')
            logging.info(resp)

        """
        def gutReply(msg):
            resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                'chat_id': '-18399216',
                'text': msg,
                'disable_web_page_preview': 'true',
            })).read()

        def nerdReply():
            resp = urllib2.urlopen(BASE_URL + 'sendMessage', urllib.urlencode({
                'chat_id': str(chat_id),
                'text': 'NEEERD',
                'disable_web_page_preview': 'true',
                'reply_to_message_id': str(message_id),
            })).read()
            logging.info('send response:')
            logging.info(resp)
        """

        wordList = text.split()
        for wordz in wordList:
            if wordz.startswith('/r/'):
                if "/r/fightsub" in wordList:
                    reply("We don't talk about that.")
                else: reply('http://www.reddit.com' + wordz)

        #times = fnmatch.filter(wordList, '??:??')
        #if times != []:
            #for timez in times:
                #if lastname == 'Latta':


        if text.startswith('/'):
            """
            if text == '/start' or text == '/start@LonkBot':
                reply('Sentience mode enabled')
                setEnabled(chat_id, True)
            elif text == '/stop' or text == '/stop@LonkBot':
                reply('Sentience mode disabled')
                setEnabled(chat_id, False)
            """
            if text == '/lonk' or text == '/lonk@LonkBot':
                reply('Lonk Live The Queen!')
            elif text == '/test':
            	reply('no thank you')
            elif text.startswith('/r/'):
                pass
            else:
                reply('Unknown command: ' + text)

        # CUSTOMIZE FROM HERE

        if 'lonk' in text.lower() and ('w' in wordList or 'won' in text.lower()):
            if 'stomp' in text.lower() or 'stomped' in text.lower() or 's' in wordList:
                stuff = {'value1': 'Win', 'value2': 'Yes', 'value3': fullname}
                responses = ['ggez','Good job bois','choo choo','holy whiskers you go sisters']
                resp_bit = 'Recorded a win (stomp)'
            else:
                stuff = {'value1': 'Win', 'value2': 'No', 'value3': fullname}
                responses = ['Good job bois','noise','Can I play too?','Oh fuck yeah bud']
                resp_bit = 'Recorded a win'
            addWin()
            winzz = checkWins()
            lossezz = checkLosses()
            record = 'W: ' + str(winzz) + ', L: ' + str(lossezz)
            quoteReply(resp_bit + ' (' + record + ')\n' + random.choice(responses))
            req = urllib2.Request("https://maker.ifttt.com/trigger/lonk_wl/with/key/hCqnD1OnmJZyTZL8c1x0V1FVpeiJZ-efWrYZxW93_QG")
            req.add_header('Content-Type', 'application/json')
            urllib2.urlopen(req, json.dumps(stuff)).read()

        if 'lonk' in text.lower() and ('l' in wordList or 'lost' in text.lower()):
            if 'stomp' in text.lower() or 'stomped' in text.lower() or 's' in wordList:
                stuff = {'value1': 'Loss', 'value2': 'Yes', 'value3': fullname}
                responses = ['ROUGH ROLL','get rekt','gg close','Was that a PRO Genji?']
                resp_bit = 'Recorded a loss (stomped)'
            else:
                stuff = {'value1': 'Loss', 'value2': 'No', 'value3': fullname}
                responses = ['git gud','neeerds','Better luck next time']
                resp_bit = 'Recorded a loss'
            addLoss()
            winzz = checkWins()
            lossezz = checkLosses()
            record = 'W: ' + str(winzz) + ', L: ' + str(lossezz)
            quoteReply(resp_bit + ' (' + record + ')\n' + random.choice(responses))
            req = urllib2.Request("https://maker.ifttt.com/trigger/lonk_wl/with/key/hCqnD1OnmJZyTZL8c1x0V1FVpeiJZ-efWrYZxW93_QG")
            req.add_header('Content-Type', 'application/json')
            urllib2.urlopen(req, json.dumps(stuff)).read()

        if 'lonk' in text.lower() and 'overwatch' in text.lower() and 'record' in text.lower():
            winzz = checkWins()
            lossezz = checkLosses()
            record = 'W: ' + str(winzz) + ', L: ' + str(lossezz)
            reply(record)

        if 'star wars' in text.lower() and 'lonk' in text.lower():
            currentDate = datetime.date.today()
            star_date = datetime.date(2019, 12, 20)
            daysLeft = (star_date - currentDate).days
            quoteReply("%s days until STAR WARS Episode IX" % (daysLeft))
            
        #if 'lonk' in text.lower():
        #    stickerReply('BQADAQADYQADyVB8ASPbHzvQy__JAg')
        if 'link' in text.lower():
            quoteReply('Did you mean "Lonk"?')
        if 'john cena' in text.lower():
            quoteReply("I sexually Identify as John Cena. Ever since I was a boy I dreamed of defending my WWE championship at WWE SUPERSLAM. People say to me that a person being John Cena is Impossible and I'm fucking retarded but I don't care, You Can't See Me. I'm having Vince McMahon inject me with Hustle, Loyalty, and Respect. From now on I want you guys to call me 'Champ' and respect my right to Five Knuckle Shuffle and Never Give Up. If you can't accept me you're a cenaphobe and need to check your championship privilege. Thank you for being so understanding.")
        if 'cyka blyat' in text.lower():
            quoteReply('Что ебать ты просто чертовски говорила обо мне, маленькая сука? Я тебе зкажу, я закончил вершину моего класса в ВДВ, и я принимал участие в многочисленных секретных рейдов на Аль-Каидой, и у меня есть более 300 подтвержденных убийств. Я тренировался в парижском войны, и я сверху снайпер в целых российских вооруженных сил.  Я могу быть где угодно, в любое время, и я могу убить тебя в более семисот способами, и это только голыми руками. Если бы только ты мог знать, что нечестивый возмездие ваш маленький "умный" комментарий был готов обрушить тебе, может быть, ты бы провели свой гребаный язык.')
            time.sleep(3)
            quoteReply('Вы ничто для меня, но только другая цель. Я протрите тебе нахрен с точностью, подобных которым никогда не видели раньше на этой Земле, запомните мои чертовы слова. Вы думаете, что вы можете уйти с того, что дерьмо для меня через Интернет? Подумайте еще раз, ублюдок. Как мы говорим Я контактирую мой секретный сеть шпионов по всей России, и ваш IP-трассируется прямо сейчас, так что вам лучше подготовиться к шторму, козу. Шторм, который стирает жалкий небольшое вещь ты называеш твоя жизнь. Ты находишься чертовски мертвых, малыш.')
            time.sleep(2)
            quoteReply('Я не только обучен приемам рукопашного боя, но у меня есть доступ ко всей арсенале Воздушно-десантные войска, и я буду использовать его в полной мере, чтобы вытереть задницу жалкий с лица континента, небольшое дерьма!!!!!!!!!!!11!!!')
            time.sleep(5)
            quoteReply('Но ты не мог, ты не сделал, и теперь ты платишь цену, ты идиот проклятый!!!!!!! Я дерьмо ярость все над тобойи ты тонуть в нем!!!!!!!!1!!!!!!!!!!11!1!!!!! Ты находишься чертовски мертв, детка!!!!')
        if 'its dat boi' in text.lower() or "it's dat boi" in text.lower():
            quoteReply('oh shit whaddup!')
        if 'shrek' in text.lower():
            quoteReply('SOME')
            stickerReply('BQADBAAD4AIAAq_rcwABA18HGch75tcC')
            quoteReply('BODY')
            stickerReply('BQADBAAD4gIAAq_rcwABTP4iwIgjjnIC')
            quoteReply('ONCE')
            stickerReply('BQADBAAD2gIAAq_rcwAB75hubEl6wb8C')
            quoteReply('TOLD ME')
        if 'name' in text.lower() and 'song' in text.lower():
            quoteReply('song name is Sandstorm by Darude\nhttps://www.youtube.com/watch?v=dQw4w9WgXcQ')
        if 'do it' in text.lower() and len(text) < 15:
            stickerReply('BQADAQADXgUAAiBWmALK7Xfe8O0gKAI')

        if text.startswith("Roll "):
            multiplier = 1
            sides = 1
            addon = 0
            x = 5
            now_d = False
            now_a = False
            fucked_up = False
            while x < (len(text)):
                c = text[x]
                if c.isdigit() and not now_d: multiplier = int(c)
                elif c.isdigit() and now_d and not now_a:
                    try: n = text[x+1]
                    except: n = ''
                    if n.isdigit():
                        sides = int(c + n)
                        x += 1
                    else: sides = int(c)
                elif c.isdigit() and now_a:
                    try: n = text[x+1]
                    except: n = ''
                    if n.isdigit():
                        addon = int(c + n)
                        x += 1
                    else: addon = int(c)
                elif c == "+" and now_d:
                    now_a = True
                elif c == 'd': now_d = True
                else:
                    quoteReply("I don't understand. Try again.")
                    fucked_up = True
                    break
                x += 1

            if sides == 0: fucked_up = True

            if not fucked_up:
                total = 0
                each_roll = []
                y = 0
                while y < multiplier:
                    roll = random.randint(1,sides)
                    each_roll.append(roll)
                    total += roll
                    y += 1
                    
                if multiplier == 1: multiplier = ''

                if addon > 0: s = 'Rolling %sd%s+%s...\nYou rolled %s!' % (multiplier,sides,addon,total+int(addon))
                else: s = 'Rolling %sd%s...\nYou rolled %s!' % (multiplier,sides,total)

                if multiplier != '':
                    s += '\nEach individual roll:\n'
                    z = 0
                    while z < multiplier:
                        s += '%s, ' % each_roll[z]
                        z += 1

                quoteReply(s)

        if 'btc' in text.lower() and 'lonk' in text.lower():
            url = "https://api.coindesk.com/v1/bpi/currentprice.json"
            try:
                data = urllib2.urlopen(url)
                data = json.loads(data.read())
                data = data['bpi']
                data = data['USD']
                price = data['rate']
                price = price[:-2]
                quoteReply('BTC price, courtesy of coindesk API:\n1 BTC = $%s' % price)
            except urllib2.HTTPError:
                quoteReply('coindesk API is currently unavailable.')
        
        #if (text == '10-4' or text == '10 4') and (str(chat_id) == '-1001127804428' or str(chat_id) == '-1001143780569'):
        if ('10-4' in text or '10 4' in text) and (str(chat_id) == '-1001127804428' or str(chat_id) == '-1001143780569'):
            delMessage()
            chatReply(24924361, "%s said %s" % (firstname, text))

        if "dennis" in text.lower():
            quoteReply('The MENACE of TENNIS?')
        if firstname == 'Kevin' and lastname == 'Meuller':
            kev_responses = ["What the fuck is wrong with you?","That's fucking disgusting.","ONE DEM COON HOUNDS GOT LET LOOSE","something something EUROTRASH","CYKA BLYAT"]
            if text.endswith("?") and bool(random.getrandbits(1)):
                    quoteReply("Where the fuck did you get that idea?")
            elif bool(random.getrandbits(1)) and bool(random.getrandbits(1)): quoteReply(random.choice(kev_responses))

        if text == '1test23':
            reply(str(chat_id))

        """
        else:
            if getEnabled(chat_id):
                resp1 = json.load(urllib2.urlopen('http://www.simsimi.com/requestChat?lc=en&ft=1.0&req=' + urllib.quote_plus(text.encode('utf-8'))))
                back = resp1.get('res')
                if not back:
                    reply('okay...')
                elif 'I HAVE NO RESPONSE' in back:
                    reply('RAISE YOUR LONKERS')
                else:
                    reply(back)
            else:
                logging.info('not enabled for chat_id {}'.format(chat_id))
        
        nagging = ["GUTMAAAAANNNNN","LET'S ALL GO TO THE MOVIES\n\nLET'S ALL GO TO THE MOVIES","Paging Mr. Gutmann. Please report to your driveway at 7, sharp.", "Joooiiiin ussss!", "JUST DO IT! DON'T LET YOUR DREAMS BE DREAMS."]
        x = 0
        while True:
            #gutReply("Mr. Gutmann! You have been invited to a screening party of the return of Doctor Who!\n\nWhen: This Saturday, 5 PM CST\nWhere: Matt's house\n\nPlease RSVP ASAP KK THX")
            #x = x + 1
        """

app = webapp2.WSGIApplication([
    ('/me', MeHandler),
    ('/updates', GetUpdatesHandler),
    ('/set_webhook', SetWebhookHandler),
    ('/webhook', WebhookHandler),
], debug=True)
