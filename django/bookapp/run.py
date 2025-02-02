
# Проверка даты из формы
def check_data(date):
    dt = date.split('/')
    if len(dt) != 3:
        return False
    for el in dt:
        if not el.isdigit():
            return False
    if int(dt[0]) < 1 or int(dt[0]) > 31:
        return False
    if int(dt[1]) < 1 or int(dt[1]) > 12:
        return False
    return True


# Преобразование строки даты для выполнения запроса к БД
def make_date(date):
    dt = date.split('/')
    return str(dt[2]) + '-' + str(dt[1]) + '-' + str(dt[0])


# Преобразование из БД
def load_date(date):
    dt = str(date).split('-')
    return str(dt[2]) + '/' + str(dt[1]) + '/' + str(dt[0])



# Проверка времени из формы
def check_time(time):
    tm = time.split(':')
    if len(tm) != 2:
        return False
    for el in tm:
        if not el.isdigit():
            return False
    if int(tm[0]) < 0 or int(tm[0]) > 23:
        return False
    if int(tm[1]) < 0 or int(tm[1]) > 59:
        return False
    return True


# Преобразование строки времени для выполнения запроса к БД
def make_time_h(time):
    tm = time.split(':')
    return tm[0]


def make_time_m(time):
    tm = time.split(':')
    return tm[1]


def confirm_to_bool(confirm):
    if str(confirm) == 'None':
        return False
    return True


def load_time(h, m):
    return "{:02d}".format(h) + ':' + "{:02d}".format(m)


# Проверка пересечения времен
def check_book_time_cross(bh, bm, eh, em, bk_bh, bk_bm, bk_eh, bk_em):
    #print(bh, bm, eh, em, bk_bh, bk_bm, bk_eh, bk_em)
    if bk_bh > eh:
        return False
    if bk_eh < bh:
        return False
    if eh == bk_bh and em < bk_bm:
        print('1')
        return False
    if bh == bk_eh and bk_em < bm:
        print('2')
        return False
    return True

# Проверка доступности помещения по времени
def check_book_time(tbeg, tend, book_lst, book_id):
    bh = int(make_time_h(tbeg))
    bm = int(make_time_m(tbeg))
    eh = int(make_time_h(tend))
    em = int(make_time_m(tend))
    for bk in book_lst:
        if str(book_id) != str(bk.id):
            #print(book_id, bk.id)
            if check_book_time_cross(bh, bm, eh, em, bk.beg_hour, bk.beg_min, bk.end_hour, bk.end_min):
                return False
    return True

