from random import choice

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from datacenter.models import Commendation, Lesson, Schoolkid


COMMENDATIONS =['Молодец!', 'Отлично!', 'Хорошо!', 'Гораздо лучше, чем я ожидал!', 'Ты меня приятно удивил!',
                'Великолепно!', 'Прекрасно!', 'Ты меня очень обрадовал!', 'Именно этого я давно ждал от тебя!',
                'Сказано здорово – просто и ясно!']


def fix_marks(schoolkid):
    marks = schoolkid.mark_set.all()
    bad_marks = marks.filter(points__lt=4)
    for bad_mark in bad_marks:
        bad_mark.points = 5
        bad_mark.save()


def remove_chastisements(schoolkid):
    chastisements = schoolkid.chastisement_set.all()
    chastisements.delete()


def create_commendation(name, name_subject):
    try: 
        child = Schoolkid.objects.get(full_name__contains=name)
    except MultipleObjectsReturned:
        print('Найдено несколько учеников! Уточните запрос!')
        return
    except ObjectDoesNotExist:
        print('Не найдено ни одного ученика!')
        return
    last_lesson = Lesson.objects.filter(group_letter=child.group_letter, year_of_study=child.year_of_study, subject__title=name_subject).order_by('-date').first()
    if not last_lesson:
        print('Такой предмет не найден!')
        return
    child_commendation = Commendation.objects.filter(created=last_lesson.date,
                                                     schoolkid=child,
                                                     subject=last_lesson.subject)
    if not child_commendation:
        Commendation.objects.create(text=choice(COMMENDATIONS),
                                    created=last_lesson.date,
                                    schoolkid=child,
                                    subject=last_lesson.subject,
                                    teacher=last_lesson.teacher)
    else:
        print('Похвала уже существует!')
