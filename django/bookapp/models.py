from django.db import models

class Room(models.Model):
    name = models.CharField(max_length=100)
    people_count = models.IntegerField()
    cost = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name


class Booking(models.Model):
    user_id = models.IntegerField()
    #room_id = models.IntegerField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='booking')
    date = models.DateField()
    beg_hour = models.IntegerField()
    beg_min = models.IntegerField()
    end_hour = models.IntegerField()
    end_min = models.IntegerField()
    confirm = models.BooleanField()

    def __str__(self):
        return 'Юзер:' + str(self.user_id) + ', Комната:' + str(self.room) + ', Дата:' + str(self.date)

