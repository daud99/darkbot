from gatherdumps.scripts.captchaSolver import deathbycaptcha
#import deathbycaptcha
from os import getcwd
from PIL import Image
def solve_captcha_dbc(img):

    client = deathbycaptcha.SocketClient("omergr85", "Mm5730613")
    try:
        balance = client.get_balance()
        print('your balance is:', balance)
        captcha = client.decode(img, 60)

        if captcha:

            #print("Text is",captcha["text"], "and Captcha code is",captcha["captcha"])
            print(captcha)
            return captcha['text']
        if ...:
            client.report(captcha["captcha"])
            return None
    except deathbycaptcha.AccessDeniedException:
        print("Nothing")
        return None
    except Exception as e:
        print("Exception in captcha module")
        return None