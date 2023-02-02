import jdatetime
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from . import jalali
from datetime import timedelta
from django.contrib import messages
from django.utils.translation import get_language
import os, re
from random import randint, choice


DAYS = (
    ('saturday', _('شنبه')),
    ('sunday', _('یک شنبه')),
    ('monday', _('دو شنبه')),
    ('tuesday', _('سه شنبه')),
    ('wednesday', _('چهار شنبه')),
    ('thursday', _('پنج شنبه')),
    ('friday', _('جمعه')),
)
TIMES = (
    ('6:00', '6:00'), ('6:30', '6:30'),
    ('7:00', '7:00'), ('7:30', '7:30'),
    ('8:00', '8:00'), ('8:30', '8:30'),
    ('9:00', '9:00'), ('9:30', '9:30'),
    ('10:00', '10:00'), ('10:30', '10:30'),
    ('11:00', '11:00'), ('11:30', '11:30'),
    ('12:00', '12:00'), ('12:30', '12:30'),
    ('13:00', '13:00'), ('13:30', '13:30'),
    ('14:00', '14:00'), ('14:30', '14:30'),
    ('15:00', '15:00'), ('15:30', '15:30'),
    ('16:00', '16:00'), ('16:30', '16:30'),
    ('17:00', '17:00'), ('17:30', '17:30'),
    ('18:00', '18:00'), ('18:30', '18:30'),
    ('19:00', '19:00'), ('19:30', '19:30'),
    ('20:00', '20:00'), ('20:30', '20:30'),
    ('21:00', '21:00'), ('21:30', '21:30'),
    ('22:00', '22:00'), ('22:30', '22:30'),
    ('23:00', '23:00'), ('23:30', '23:30'), ('24:00', '24:00'),
)

def is_email(email):
    return bool(re.compile(r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)').match(str(email)))

def is_phone(phone):
    return bool(re.compile(r'(^0?9([0-1][0-9]|3[1-9]|2[1-9])-?[0-9]{3}-?[0-9]{4}$)').match(str(phone)))

def is_national_code(value):
    return bool(re.compile(r'(^[0-9]{10}$)').match(str(value)))

def is_shaba(value):
    return bool(re.compile(r'(^(?:IR)(?=.{24}$)[0-9]*$)').match(str(value)))

def write_action(action, usertype):
    """ 
        this function write user actions in actions.log file in root directory 
        usertype must be 'USER' or 'ANONYMOUS'
    """
    if usertype == 'USER':
        with open('user_actions.log', 'a') as file:
            file.write('DATE: ' + str(jdatetime.datetime.now()) + ' .:. ACTION: ' + action)
            file.write('\n')
    elif usertype == 'ANONYMOUS':
        with open('anonymous_actions.log', 'a') as file:
            file.write('DATE: ' + str(jdatetime.datetime.now()) + ' .:. ACTION: ' + action)
            file.write('\n')

def date_range_list(start_date, end_date):
    date_list = []
    curr_date = start_date
    while curr_date <= end_date:
        date_list.append(curr_date)
        curr_date += timedelta(days=1)
    return date_list

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def safe_string(request, text):
    signs = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '=', '+', '-', '/', "'", '"', ',', '|', ".", '<', '>', '{', '}', '[', ']', '\\']
    if not text or len(str(text)) == 0:
        messages.info(request, _('مقدار فیلد را وارد کنید.'))
        return False
    for ch in text:
        if ch in signs:
            messages.info(request, _('محتوای متن نباید شامل علامت باشد.'))
            return False
    return text

def jalali_convertor(time, output='date_time', number=False):
    if get_language() == 'fa':
        jmonth = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
        intmonth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        time = timezone.localtime(time)

        time_to_str = f'{time.year} {time.month} {time.day}'
        time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
        time_to_list = list(time_to_tuple)
        for index, month in enumerate(jmonth):
            if time_to_list[1] == index + 1:
                time_to_list[1] = month
                break
        if number == True:
            time_to_list_num = list(time_to_tuple)
            for index, month in enumerate(intmonth):
                if time_to_list_num[1] == index + 1:
                    time_to_list_num[1] = month
                    break

        if output == 'date_time':        # ۲۱ دی ۱۴۰۰, ساعت ۲۱:۲۸
            output = f'{time_to_list[2]} {time_to_list[1]} {time_to_list[0]}, ساعت {time.hour}:{time.minute}'
            return persian_numbers(output)
        elif output == 'j_date':         # ۲۱ دی ۱۴۰۰
            output = f'{time_to_list[2]} {time_to_list[1]} {time_to_list[0]}'
            return persian_numbers(output)
        elif output == 'date' and number == True:           # ۲۱ - ۱۰ - ۱۴۰۰
            output = f'{time_to_list_num[2]} - {time_to_list_num[1]} - {time_to_list_num[0]}'
            return persian_numbers(output)
        elif output == 'j_month':        # دی 
            return persian_numbers(time_to_list[1])
        elif output == 'time':        # ۲۱:۲۸ 
            return persian_numbers(f'{time.hour}:{time.minute}')
        else:
            return 'No OutPut!'
    else:
        return time

def jnum_to_month_name(num):
        jmonth = ['فروردین', 'اردیبهشت', 'خرداد', 'تیر', 'مرداد', 'شهریور', 'مهر', 'آبان', 'آذر', 'دی', 'بهمن', 'اسفند']
        return jmonth[num - 1]

def persian_numbers(myStr):
    numbers = {'0': '۰', '1': '۱', '2': '۲', '3': '۳', '4': '۴', '5': '۵', '6': '۶', '7': '۷', '8': '۸', '9': '۹'}
    for e, p in numbers.items():
        myStr = myStr.replace(e,p)
    return myStr


def is_text(filename):
    extesion = os.path.splitext(str(filename))[1].lower()
    extesion_allowed = ['.pdf']
    if extesion in extesion_allowed:
        return True
    return False


def is_image(filename):
    extesion = os.path.splitext(str(filename))[1].lower()
    extesion_allowed = ['.png', '.jpg', 'jpeg']
    if extesion in extesion_allowed:
        return True
    return False


def is_video(filename):
    extesion = os.path.splitext(str(filename))[1].lower()
    extesion_allowed = ['.mp4', '.webm', '.mkv']
    if extesion in extesion_allowed:
        return True
    return False


def is_audio(filename):
    extesion = os.path.splitext(str(filename))[1].lower()
    extesion_allowed = ['.mp3']
    if extesion in extesion_allowed:
        return True
    return False


# =============== start static path

# before function File storage
def get_filename_ext_rand(filepath):
    time = timezone.now()
    intmonth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    time_to_str = f'{time.year} {time.month} {time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)
    for index, month in enumerate(intmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    random = randint(100, 999)
    output = f'{time_to_list[2]}{time_to_list[1]}{time_to_list[0]}{random}'
    return ext.lower(), output


# ######### for users profiles ######### #
def profile_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"users-profiles/{final_name}"

# ######### for users famous profiles ######### #
def famous_profile_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"users-famous-profiles/{final_name}"

# ######### for hospital costs ######### #
def costs_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"hospital-costs/{final_name}"

# ######### for hospital facilities ######### #
def facility_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"hospital-facilities/{final_name}"

# ######### for item in gallery ######### #
def gallery_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"galleries-items/{final_name}"

# ######### for item in home gallery ######### #
def home_gallery_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"home-gallery/{final_name}"

# ######### for certificate images ######### #
def certificate_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"certificates/{final_name}"

# ######### for blog image ######### #
def blog_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"blogs/{final_name}"

# ######### for blog pdf image ######### #
def blog_pdf_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"blog-pdf/{final_name}"

# ######### for blog qr code image ######### #
def blog_qrcode_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"blog-qr/{final_name}"

# ######### for blog image gallery ######### #
def blog_gallery_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"blogs-gallery/{final_name}"

# ######### for pamphelet ######### #
def pamphelet_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"pamphelets/{final_name}"

# ######### for blog image ######### #
def news_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"news/{final_name}"

# ######### for news image gallery ######### #
def news_gallery_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"news-gallery/{final_name}"

# ######### for hospital units images ######### #
def units_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"units/{final_name}"

# ######### for hospital units ICON ######### #
def units_icon_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"units-icon/{final_name}"

# ######### for insurance images ######### #
def insurance_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"insurances/{final_name}"

# ######### for reports ######### #
def report_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"reports/{final_name}"

# ######### for experiment results ######### #
def experiment_result_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"experiments/{final_name}"

# ######### for resumes ######### #
def resume_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"resumes/{final_name}"

# ######### for workshop ######### #
def workshop_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"workshops/{final_name}"

# ######### for career ######### #
def career_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"careers/{final_name}"

# ######### for unit member ######### #
def unit_member_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"unit-member/{final_name}"

# ######### for credit_edu ######### #
def credit_edu_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"credit-edu/{final_name}"

# ######### for IPD document ######### #
def ipd_doc_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"ipd-document/{final_name}"

# ######### for ancient ######### #
def ancient_image_path(instance, filename):
    ext, output = get_filename_ext_rand(filename)
    final_name = f"{output}{ext}"
    return f"ancient/{final_name}"


# =============== end static path


def daily_code_generator():
    time = timezone.now()
    intmonth = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

    time_to_str = f'{time.year} {time.month} {time.day}'
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()
    time_to_list = list(time_to_tuple)

    for index, month in enumerate(intmonth):
        if time_to_list[1] == index + 1:
            time_to_list[1] = month
            break

    random = randint(1000, 9999)
    year = time_to_list[0]
    month = time_to_list[1]
    day = time_to_list[2]

    if month < 10:
        month = f'0{month}'
    if day < 10:
        day = f'0{day}'
        
    return f'{str(year)[-2:]}{month}{day}{random}'


def get_blog_code():
    output = '2' + daily_code_generator()
    # 20012010000 => 2 => blog  // 00 => 1400 // 12 => month // 01 => day // 0000 => random
    return output


def get_news_code():
    output = '3' + daily_code_generator()
    # 30012010000 => 3 => news  // 00 => 1400 // 12 => month // 01 => day // 0000 => random
    return output


def get_patient_tracking_code():
    output = '4' + daily_code_generator()
    # 40012010000 => 4 => tracking_code  // 00 => 1400 // 12 => month // 01 => day // 0000 => random
    return output


def get_experiment_code():
    output = '5' + daily_code_generator()
    # 50012010000 => 5 => expriment_code  // 00 => 1400 // 12 => month // 01 => day // 0000 => random
    return output


def code_patient_turn():
    output = '6' + daily_code_generator()
    # 60012010000 => 6 => code_patient_turn  // 00 => 1400 // 12 => month // 01 => day // 0000 => random
    return output


def career_code():
    output = '7' + daily_code_generator()
    # 70012010000 => 7 => career  // 00 => 1400 // 12 => month // 01 => day // 0000 => random
    return output


def criticic_suggestion_code():
    output = '8' + daily_code_generator()
    # 80012010000 => 8 => career  // 00 => 1400 // 12 => month // 01 => day // 0000 => random    
    return output


def get_credit_edu_code():
    output = '9' + daily_code_generator()
    # 90012010000 => 9 => credit_edu  // 00 => 1400 // 12 => month // 01 => day // 0000 => random
    return output


def get_links_code():
    char_list = [
        'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
        'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 
        'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0'
    ]
    code = ''
    for _ in range(1, 20):
        code += choice(char_list)
    return code


def get_random_code():
    return randint(10000, 99999)

