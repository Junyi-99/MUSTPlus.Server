from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from Services.Basic.models import Faculty, Program, Major, Department


def get_department(name: str, auto_create: bool = True) -> Optional[Department]:
    try:
        return Department.objects.get(name_zh=name)
    except ObjectDoesNotExist:
        if auto_create:
            d = Department(name_zh=name)
            d.save()
            print("Create a new Department [%s]" % (d.name_zh,))
            return d
        else:
            return None
    except Exception as e:
        print("Exception in get_department(%s,%d):" % (name, auto_create), e)
        return None


def get_faculty(name: str, auto_create: bool = True) -> Optional[Faculty]:
    try:
        return Faculty.objects.get(name_zh=name)
    except ObjectDoesNotExist:
        if auto_create:
            f = Faculty(name_zh=name)
            f.save()
            print("Create a new Faculty [%s]" % (f.name_zh,))
            return f
        else:
            return None
    except Exception as e:
        print("Exception in get_faculty(%s,%d):" % (name, auto_create), e)
        return None


# 因为有从属关系，所以默认不自动创建
def get_major(name: str, auto_create: bool = False, belongs: Program = None) -> Optional[Major]:
    try:
        return Major.objects.get(name_zh=name)
    except ObjectDoesNotExist:
        if auto_create:
            m = Major(name_zh=name, program=belongs)
            m.save()
            print("Create a new Major [%s] belongs to Program [%s]" % (m.name_zh, m.program.name_zh))
            return m
        else:
            return None
    except Exception as e:
        print("Exception in get_major(%s,%d):" % (name, auto_create), e)
        return None


# 因为有从属关系，所以默认不自动创建
def get_program(name: str, auto_create: bool = False, belongs: Faculty = None) -> Optional[Program]:
    try:
        return Program.objects.get(name_zh=name)
    except ObjectDoesNotExist:
        if auto_create:
            p = Program(name_zh=name, faculty=belongs)
            p.save()
            print("Create a new Program [%s] belongs to Faculty [%s]" % (p.name_zh, p.faculty.name_zh))
            return p
        else:
            return None
    except Exception as e:
        print("Exception in get_program(%s,%d):" % (name, auto_create), e)
        return None
