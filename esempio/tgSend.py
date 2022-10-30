import os, telegram, re

cwd = os.getcwd()

bot = telegram.Bot(token='2137946322:AAFTASN-baZ6iN_dN3e-l22r_WptXKLigNM')
chat_id = ["-1001580210471"]


images = []
final_list = lambda start_list: [start_list[i:i+10] for i in range(0, len(start_list), 10)]

for root, dirs, files in os.walk(os.path.join(cwd, "results")):
    for f in files:
        if re.search("\.txt$", f):
            txt = os.path.join(root, f)
            continue
        images.append(telegram.InputMediaPhoto(open(os.path.join(root,f), 'rb')))
    images_final = final_list(images)
    
for id in chat_id:
    bot.send_document(id, open(txt))
    for chunk in images_final:
        bot.send_media_group(id, chunk)

    