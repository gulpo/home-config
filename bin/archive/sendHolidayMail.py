#!/bin/python3
import smtplib, ssl, csv, sys, os.path, time

from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

DEBUG = True
TRACE = True
PROCESS_INSTRUCTION = False
DRY_RUN = False

# configured by Arek Mroczkowski for christmas 2022
# Send as: event@hycom.pl
#   server = smtplib.SMTP('smtp.office365.com:587')
#   server.login('smtpout@hycom.pl', 'Yaha9485’)
SMTP_CONFIG = {
    'sender_email' : "event@hycom.pl",
    'sender_username' : 'smtpout@hycom.pl',
    'sender_passwd' : 'Yaha9485',
    'smtp_host' : 'smtp.office365.com',
    'smtp_port' : '587',
    'smtp_tls' : True,
    # 'smtp_host' : 'mail.hycom.dev',
    # 'smtp_port' : '587'
}

DICT_VOUCHER_NAME = 0
DICT_VOUCHER_ID = 1

DICT_STORE_IMAGE = 0
DICT_STORE_URL = 1
DICT_STORE_INSTR_PATH = 2
DICT_STORE_NAME = 3
STORE_DICT = {
    "de_adult_amazon" :      ("christmas2022/store_logos/de_adult_amazon.png"       , "https://de_adult_amazon.com"     , "de_amazon_path_to_file"      , "Amazon"      ,"2023-12-01"),
    "de_child_amazon" :      ("christmas2022/store_logos/de_child_amazon.png"       , "https://de_child_amazon.com"     , "de_amazon_path_to_file"      , "Amazon"      ,"2023-12-01"),
    "pl_adult_ikea" :        ("christmas2022/store_logos/pl_adult_ikea.png"         , "https://pl_adult_ikea.com"       , "pl_ikea_path_to_file"        , "Ikea"        ,"2023-12-01"),
    "pl_child_smyk" :        ("christmas2022/store_logos/pl_child_smyk.png"         , "https://pl_child_smyk.com"       , "pl_smyk_path_to_file"        , "Smyk"        ,"2023-12-14"),
    "pl_child_mandoria" :    ("christmas2022/store_logos/pl_child_mandoria.png"     , "https://pl_child_mandoria.com"   , "pl_mandoria_path_to_file"    , "Mandoria"    ,"2023-06-09"),
    "pl_child_airo" :        ("christmas2022/store_logos/pl_child_airo.png"         , "https://pl_child_airo.com"       , "pl_airo_path_to_file"        , "Airo"        ,"2023-12-01"),
    "de_adult_ikea" :        ("christmas2022/store_logos/de_adult_ikea.png"         , "https://de_adult_ikea.com"       , "de_ikea_path_to_file"        , "Ikea"        ,"forever and ever"),
    "pl_child_saltos" :      ("christmas2022/store_logos/pl_child_saltos.png"       , "https://pl_child_saltos.com"     , "pl_saltos_path_to_file"      , "Saltos"      ,"2023-12-01"),
    "de_adult_muller" :      ("christmas2022/store_logos/de_adult_muller.png"       , "https://de_adult_muller.com"     , "de_muller_path_to_file"      , "Müller"      ,"2023-12-01"),
    "pl_adult_empik" :       ("christmas2022/store_logos/pl_adult_empik.png"        , "https://pl_adult_empik.com"      , "pl_empik_path_to_file"       , "Empik"       ,"2023-12-12"),
    "pl_adult_allegro" :     ("christmas2022/store_logos/pl_adult_allegro.png"      , "https://pl_adult_allegro.com"    , "pl_allegro_path_to_file"     , "Allegro"     ,"2023-12-14"),
    "de_child_galeria" :     ("christmas2022/store_logos/de_child_galeria.png"      , "https://de_child_galeria.com"    , "de_galeria_path_to_file"     , "Galeria"     ,"2023-12-01"),
    "de_adult_hugendubel" :  ("christmas2022/store_logos/de_adult_hugendubel.png"   , "https://de_adult_hugendubel.com" , "de_hugendubel_path_to_file"  , "Hugendubel"  ,"2023-12-01"),
    "pl_child_empik" :       ("christmas2022/store_logos/pl_child_empik.png"        , "https://pl_child_empik.com"      , "pl_empik_path_to_file"       , "Empik"       ,"2023-12-12"),
    "de_child_sportschek" :  ("christmas2022/store_logos/de_child_sportschek.png"   , "https://de_child_sportschek.com" , "de_sportschek_path_to_file"  , "Sportschek"  ,"2023-12-01"),
    "de_child_hugendubel" :  ("christmas2022/store_logos/de_child_hugendubel.png"   , "https://de_child_hugendubel.com" , "de_hugendubel_path_to_file"  , "Hugendubel"  ,"2023-12-01"),
    "pl_adult_pyszne.pl" :   ("christmas2022/store_logos/pl_adult_pyszne.png"       , "https://pl_adult_pyszne.com"     , "pl_pyszne_path_to_file"      , "Pyszne.pl"   ,"2023-12-01"),
    "de_adult_zalando" :     ("christmas2022/store_logos/de_adult_zalando.png"      , "https://de_adult_zalando.com"    , "de_zalando_path_to_file"     , "Zalando"     ,"2023-12-01"),
    "pl_adult_morele" :      ("christmas2022/store_logos/pl_adult_morele.png"       , "https://pl_adult_morele.com"     , "pl_morele_path_to_file"      , "Morele"      ,"2023-12-12"),
    "pl_child_allegro" :     ("christmas2022/store_logos/pl_child_allegro.png"      , "https://pl_child_allegro.com"    , "pl_allegro_path_to_file"     , "Allegro"     ,"2023-12-14"),
}

def log_debug(comment):
    if DEBUG:
        print("[DEBUG] " + comment)

def log_trace(comment):
    if TRACE:
        print("[TRACE] " + comment)

def create_message(sender_email:str, receiver_email:str):
    message = MIMEMultipart("mixed")
    message["Subject"] = "[hy!Christmas] Your gift is waiting!"
    message["From"] = sender_email
    message["To"] = receiver_email
    return message

# defines email msg body without pin
# format_dict [who, image_block]
# who transfers to ["you", "your kid", "you and your kid", "your kids", "you and your kids"]
def get_msg_body_html(format_dict:dict):
    return """\
<html>
    <head><style type="text/css">
        a, a:link, a:visited, a:hover {{ color:#fff; }}
        div .hy_separator {{ background-color: "#ddd"; width:100%; height:2px;}}
        span .hy_bold {{ font-size:20px; font-weight:bold; }}
        span .hy_ps {{ font-size:16px; }}
    </style></head>
    <body style='font-size:14px;background-color:#6335cc; color:#fff; padding:30px;'>
        <center>
            <p>
                <span style="font-size:20px; font-weight:bold;">Hi!</span><br/>
                <span style="font-size:20px; font-weight:bold;">Here you can find a gift for {0[who]}!</span><br/>
            </p>
            {0[image_block]}
            <p>
                <span style="font-size:16px;">Hope the gift will be</span><br/>
                <span style="font-size:16px;">another reason to smile</span><br/>
                <span style="font-size:16px;">for {0[who]} ❤️!</span><br/>
            </p>
        </center>
    </body>
</html>
""".format(format_dict)

#Create image html part
#format: [image_id, voucher_store, voucher_id, voucher_date]
def get_image_html(format: dict):
    return """
    <div>
        <p><img style="width:256px;height:110px;" src="cid:{0[image_id]}" alt="{0[voucher_store]}"/></p>
        <p><span style="font-size:20px; font-weight:bold;">{0[voucher_id]}</span><br/></p>
        <p><span style="font-size:16px;margin-top:15px;">Use it until<br/>{0[voucher_date]}</span></p>
        <div style="background-color:rgba(200,200,200, 0.8); width:100%; height:1px; margin: 10px auto 30px auto;">&nbsp;</div>
    </div>
    """.format(format)

def create_mime_image(file_name:str, img_id:int):
    fp = open(file_name, 'rb')
    mime_image = MIMEImage(fp.read())
    mime_image.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(file_name)))
    fp.close()
    # Add 'Content-ID' header value to the above MIMEImage object to make it refer to the image source (src="cid:image1") in the Html content.
    mime_image.add_header('Content-ID', 'img' + str(img_id))
    return mime_image

def create_mime_attachment(file_name:str):
    fp = open(file_name, 'rb')
    mime_file = MIMEApplication(fp.read())
    mime_file.add_header('Content-Disposition', 'attachment; filename="{}"'.format(os.path.basename(file_name)))
    fp.close()
    return mime_file

def process_voucher(voucher:list[str], store:tuple, mime_image_list:list[str], image_html_list:list[str]):
    image_id = len(mime_image_list) + 1
    mime_image_list.append(create_mime_image(store[DICT_STORE_IMAGE], image_id))
    
    #format: [image_id, voucher_store, voucher_id, voucher_date]
    image_html_dict = {
        "image_id" : 'img' + str(image_id),
        "voucher_store" : store[DICT_STORE_NAME],
        "voucher_id" : voucher[DICT_VOUCHER_ID],
        "voucher_date" : '2023-12-01' # TODO: Change hardcoded date
    }
    image_html_list.append(get_image_html(image_html_dict))

def get_who_text(adult_count:int, kids_count:int):
    who = ''
    if adult_count == 1:
        who = 'You'
        if kids_count == 1:
            who += ' and your kid'
        elif kids_count > 1:
            who += ' and your kids'
    else:
        if kids_count == 1:
            who += 'your kid'
        elif kids_count > 1:
            who += 'your kids'
    return who

if __name__ == '__main__':
    if len(sys.argv) == 1 or not os.path.exists(sys.argv[1]) :
        print('No argument was given. Expected user data [csv] file path as arg[1]')
        sys.exit(1)

    msg_mime_list = []
    log_debug('Opening file:{}'.format(sys.argv[1]))
    with open(sys.argv[1]) as file:
        reader = csv.reader(file, delimiter=',')
        next(reader)  # Skip header row
        #row: <email>,<adult_store>,<kids_store>,<country>
        # email: username@domain
        # adult_store: <store_name:voucher_id>
        # kids_store: [<store_name:voucher_id>;<store_name:voucher_id>;...]
        # country: pl|de
        # example: dominika.ozog@hycom.pl,decathlon:V0004,amazon:V0003;hugendubel:V002;amazon:V001,pl
        for receiver_email, adult_voucher, kids_voucher_list, country in reader:
            log_debug('Processing row [email:{}, adult_voucher: {}, kids_voucher_list: {}, country: {}]'
                .format(receiver_email, adult_voucher, kids_voucher_list, country))
            distinct_store_instr_set = set()
            image_html_list = []
            mime_image_list = []

            # 0:name, 1:id
            voucher = adult_voucher.split("|")
            adult_count = 0
            if voucher and voucher[DICT_VOUCHER_NAME]:
                adult_count += 1
                store_id = country.lower() + "_adult_" + voucher[DICT_VOUCHER_NAME].lower() # ex: de_adult_amazon
                log_trace('store code: {}'.format(store_id))
                # [0:image_path, 1:url, 2:instr_path, 3:name]
                store = STORE_DICT[store_id] 
                log_trace("Adult store - {} - img_exists:{}".format(store, os.path.exists(store[DICT_STORE_IMAGE])))
                distinct_store_instr_set.add(store[DICT_STORE_INSTR_PATH])
                process_voucher(voucher, store, mime_image_list, image_html_list)
            else:
                log_debug('Empty adult voucher')
            kids_voucher_list = kids_voucher_list.split(';')
            kids_count = 0
            for kid_voucher in kids_voucher_list:
                voucher = kid_voucher.split("|")
                if voucher and voucher[DICT_VOUCHER_NAME]:
                    kids_count += 1
                    store_id = country.lower() + "_child_"+voucher[DICT_VOUCHER_NAME].lower()
                    store = store = STORE_DICT[store_id] 
                    log_trace("Kid store - {} - img_exists:{}".format(store, os.path.exists(store[DICT_STORE_IMAGE])))
                    process_voucher(voucher, store, mime_image_list, image_html_list)
                else:
                    log_trace('Empty kid voucher')

            mime_instruction_list = []
            if PROCESS_INSTRUCTION:
                for instruction in distinct_store_instr_set:
                    mime_instruction_list.append(create_mime_attachment(instruction))

            who = get_who_text(adult_count, kids_count)
            if not who:
                log_debug('No vouchers found, omitting row')
                continue
            image_block = ''
            for html_part in image_html_list:
                image_block += "\n" + html_part
            msg_dict = {
                'who' : who,
                'image_block' : image_block
            }
            # Turn these into plain/html MIMEText objects
            msg_mime_html = MIMEText(get_msg_body_html(msg_dict), 'html')

            # Add HTML/plain-text parts to MIMEMultipart message
            # The email client will try to render the last part first
            msg_mime = create_message(SMTP_CONFIG['sender_email'], receiver_email)
            msg_mime.attach(msg_mime_html)
            for mime_image in mime_image_list:
                msg_mime.attach(mime_image)
            if PROCESS_INSTRUCTION:
                for mime_instr in mime_instruction_list:
                    msg_mime.attach(mime_instr)

            log_debug('Appending  to [receiver:{}, adult_count:{}. kids_count:{},] to toSend list'
                    .format(msg_mime['To'], adult_count, kids_count))
            msg_mime_list.append(msg_mime)
    
    if len(msg_mime_list) > 0:
        log_debug('Connecting to SMTP server. Got {} messages to send'.format(len(msg_mime_list)))
        #Create secure connection with server and send email
        context = ssl.create_default_context()
        # with smtplib.SMTP_SSL(SMTP_CONFIG['smtp_host'], SMTP_CONFIG['smtp_port'], context=context) as server:
        with smtplib.SMTP(SMTP_CONFIG['smtp_host'], SMTP_CONFIG['smtp_port']) as server:
            server.connect(SMTP_CONFIG['smtp_host'], SMTP_CONFIG['smtp_port'])
            if 'smtp_tls' in SMTP_CONFIG:
                server.ehlo()
                server.starttls()
                server.ehlo()
            
            if 'sender_username' in SMTP_CONFIG and 'sender_passwd' in SMTP_CONFIG:
                server.login(SMTP_CONFIG['sender_username'], SMTP_CONFIG['sender_passwd'])
            for msg_mime in msg_mime_list:
                log_debug('Sending msg to ' + msg_mime['To'])
                # if TRACE:
                #     log_trace('Msg:\n{}'.format(msg_mime)) # binary files in output are bad bad bad
                if not DRY_RUN:
                    server.sendmail(
                        SMTP_CONFIG['sender_email'], msg_mime['To'] , msg_mime.as_string()
                    )
            server.quit()
    else:
        log_debug('Got nothing to send')
