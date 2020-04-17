from gatherdumps.scripts.captchaSolver import txt
import datetime
import os

def bypass_captcha(captcha_image):
    
        try:
            x = txt.solve_captcha_dbc(captcha_image)
        except Exception as e:
            print('Exception at captcha processing')
            if captcha_image:
                os.remove(captcha_image)
        else:
            if captcha_image:
                os.remove(captcha_image)
            print('decoded captcha ')
            captcha = x
            return captcha
        return None
    