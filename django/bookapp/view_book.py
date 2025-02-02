from django.shortcuts import render, redirect
from .models import *
from .run import *


# Проверка данных формы бронирования
def check_booking_data(date, tbeg, tend, room_id, book_id):
    if not check_data(date):
        return 'Неверная дата'
    if not check_time(tbeg):
        return 'Неверное время начала бронирования'
    if not check_time(tend):
        return 'Неверное время завершения бронирования'
    # Проверка доступности помещения по времени
    if not check_book_time(tbeg, tend, Booking.objects.filter(date=make_date(date), room_id=room_id), book_id):
        return 'На данное время помещение уже забронировано'
    return ''


# Новое бронирование
def booking(request):
    room_id = '0'
    if request.method == 'POST':
        room_id = request.POST.get('room')
        date = request.POST.get('date')
        timebeg = request.POST.get('timebeg')
        timeend = request.POST.get('timeend')
        confirm = confirm_to_bool(request.POST.get('confirm'))
        err_mess = check_booking_data(date, timebeg, timeend, room_id, -1)
        if len(err_mess) == 0:
            # Добавление записи в БД
            user_id = request.user.id
            Booking.objects.create(user_id=user_id, room_id=room_id, date=make_date(date),
                                   beg_hour=make_time_h(timebeg), beg_min=make_time_m(timebeg),
                                   end_hour=make_time_h(timeend), end_min=make_time_m(timeend),
                                   confirm=confirm)
            # Данные для формы
            room_id = '0'
            fdata = {
                'caption': 'Бронирование выполнено!', 'date': '', 'timebeg': '', 'timeend': '', 'confirm': ''
            }
        else:
            fdata = {
                'caption': err_mess,
                'date': date, 'timebeg': timebeg, 'timeend': timeend, 'confirm': 'checked' if confirm else ''
            }
    else:
        fdata = {'caption': 'укажите данные для бронирования', 'date': '', 'timebeg': '', 'timeend': '', 'confirm': ''}
    rooms = []
    for el in Room.objects.all().order_by('name'):
        rooms.append({
            'room': el,
            'select': 'selected' if str(el.id) == str(room_id) else ''
        })
    fdata['rooms'] = rooms
    fdata['key_title'] = 'Бронировать'
    return render(request, 'bookapp/booking.html', {'fdata': fdata})


# Изменение бронирования
def book_edit(request):
    book_id = request.GET.get('id')
    # print('book_id:', book_id)
    # room_id = '0'
    if request.method == 'POST':
        room_id = request.POST.get('room')
        date = request.POST.get('date')
        timebeg = request.POST.get('timebeg')
        timeend = request.POST.get('timeend')
        confirm = confirm_to_bool(request.POST.get('confirm'))
        err_mess = check_booking_data(date, timebeg, timeend, room_id, book_id)
        if len(err_mess) == 0:
            # Изменение записи в БД
            Booking.objects.filter(id=book_id).update(room_id=room_id, date=make_date(date),
                                                      beg_hour=make_time_h(timebeg), beg_min=make_time_m(timebeg),
                                                      end_hour=make_time_h(timeend), end_min=make_time_m(timeend),
                                                      confirm=confirm)
            return redirect('/booklist')
        else:
            fdata = {
                'caption': err_mess,
                'date': date, 'timebeg': timebeg, 'timeend': timeend, 'confirm': 'checked' if confirm else ''
            }
    else:
        Book_dt = Booking.objects.get(id=book_id)
        room_id = Book_dt.room_id
        fdata = {
            'caption': 'изменение данных',
            'date': load_date(Book_dt.date),
            'timebeg': load_time(Book_dt.beg_hour, Book_dt.beg_min),
            'timeend': load_time(Book_dt.end_hour, Book_dt.end_min),
            'confirm': 'checked' if Book_dt.confirm else ''
        }
    rooms = []
    for el in Room.objects.all().order_by('name'):
        rooms.append({
            'room': el,
            'select': 'selected' if str(el.id) == str(room_id) else ''
        })
    fdata['rooms'] = rooms
    fdata['key_title'] = 'Изменить бронирование'
    return render(request, 'bookapp/booking.html', {'fdata': fdata})


def book_delete(request):
    # Удаление записи в БД
    book_id = request.GET.get('id')
    Booking.objects.get(id=book_id).delete()
    return redirect('/booklist')


def booklist(request):
    user_id = request.user.id
    book_lists = Booking.objects.filter(user_id=user_id)
    context = []
    for el in book_lists:
        stat = 'Не подтверждено'
        if el.confirm:
            stat = 'Подтверждено'
        context.append({
            'booking': el,
            'time_beg': "{:02d}".format(el.beg_hour) + ':' + "{:02d}".format(el.beg_min),
            'time_end': "{:02d}".format(el.end_hour) + ':' + "{:02d}".format(el.end_min),
            'roomname': str(Room.objects.filter(id=el.room_id)[0]),
            'status': stat,
        })
    return render(request, 'bookapp/book_list.html', {'book_lists': context})
