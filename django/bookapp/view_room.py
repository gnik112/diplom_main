from django.shortcuts import render, redirect
from .models import *
from .run import *



def check_room_data(people_count, cost):
    if not people_count.isdigit():
        return 'Количество людей должно быть целым числом'
    dt = cost.split('.')
    if len(dt) != 2:
        return 'Ошибка в стоимости'
    for el in dt:
        if not el.isdigit():
            return 'Ошибка в стоимости'
    return ''

def rooms(request):
    rooms = Room.objects.all().order_by('name')
    return render(request, 'bookapp/rooms.html', {'rooms': rooms})


def room_edit(request):
    room_id = request.GET.get('id')
    #print('room_id:', room_id)
    if room_id is None:
        if request.method == 'POST':
            roomname = request.POST.get('roomname')
            people_count = request.POST.get('people_count')
            cost = request.POST.get('cost').replace(',', '.')
            err_mess = check_room_data(people_count, cost)
            if len(err_mess) == 0:
                # Создание записи в БД
                Room.objects.create(name=roomname, people_count=people_count, cost=cost)
                return redirect('/rooms')
            else:
                content = {
                    'caption': err_mess,
                    'roomname': roomname,
                    'people_count': people_count,
                    'cost': cost.replace('.', ','),
                    'key_title': 'Создать'
                }
        else:
            content = {'caption': 'создание нового помещения', 'key_title': 'Создать'}
    else:
        if request.method == 'POST':
            roomname = request.POST.get('roomname')
            people_count = request.POST.get('people_count')
            cost = request.POST.get('cost').replace(',', '.')
            err_mess = check_room_data(people_count, cost)
            if len(err_mess) == 0:
                # Изменение записи в БД
                Room.objects.filter(id=room_id).update(name=roomname, people_count=people_count, cost=cost)
                return redirect('/rooms')
            else:
                content = {
                    'caption': err_mess,
                    'roomname': roomname,
                    'people_count': people_count,
                    'cost': cost.replace('.', ','),
                    'key_title': 'Изменить'
                }
        else:
            room = Room.objects.filter(id=room_id)[0]
            #print(room)
            content = {
                'caption': 'изменение данных',
                'roomname': room.name,
                'people_count': room.people_count,
                'cost': room.cost,
                'key_title': 'Изменить'
            }
    return render(request, 'bookapp/room_edit.html', {'fdata': content})


def room_busy(request):
    date = request.GET.get('date')
    #print('date:', date)
    if date is None:
        content = {'caption': 'Укажите дату:', 'key_title': 'Показать'}
        return render(request, 'bookapp/room_busy.html', {'fdata': content})
    busy_list = []
    for rm in Room.objects.all().order_by('name'):
        titl = True
        bk_el = {}
        bk_lst = []
        for bk in Booking.objects.filter(date=make_date(date), room_id=rm.id):
            if titl:
                bk_el['title'] = rm.name
                titl = False
            stat = 'Не подтверждено'
            if bk.confirm:
                stat = 'Подтверждено'
            bk_lst.append({
                'beg': load_time(bk.beg_hour, bk.beg_min),
                'end': load_time(bk.end_hour, bk.end_min),
                'id': bk.id,
                'roomname': rm.name,
                'edit_enable': True if request.user.id == bk.user_id else False,
                'date': date,
                'status': stat,
            })
        if not titl:
            bk_el['data'] = bk_lst
            busy_list.append(bk_el)
    content = {'caption': 'Укажите дату:', 'date': date, 'key_title': 'Показать', 'busy_list': busy_list}
    return render(request, 'bookapp/room_busy.html', {'fdata': content})


def room_delete(request):
    # Удаление помещения
    room_id = request.GET.get('id')
    Room.objects.get(id=room_id).delete()
    # Удаление бронирований по помещению
    Booking.objects.filter(room_id=room_id).delete()
    return redirect('/rooms')
