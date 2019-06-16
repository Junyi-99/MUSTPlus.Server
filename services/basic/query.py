from typing import Optional

from django.core.exceptions import ObjectDoesNotExist

from services.basic.models import Faculty, Program, Major, Department


def get_department(name: str, auto_create: bool = True) -> Optional[Department]:
    try:
        return Department.objects.get(name_zh=name)
    except ObjectDoesNotExist:
        if auto_create:
            department = Department(name_zh=name)
            department.save()
            print("Create a new Department [%s]" % (department.name_zh,))
            return department
        return None
    except Exception as exception:
        print("Exception in get_department(%s,%d):" % (name, auto_create), exception)
        return None


def get_faculty(name_zh: str, auto_create: bool = True) -> Optional[Faculty]:
    try:
        print("Get Faculty", name_zh)
        return Faculty.objects.get(name_zh=name_zh)
    except ObjectDoesNotExist:
        if auto_create:
            faculty = Faculty(name_zh=name_zh)
            faculty.save()
            print("Create a new Faculty [%s]" % (faculty.name_zh,))
            return faculty
        return None
    except Exception as exception:
        print("Exception in get_faculty(%s,%d):" % (name_zh, auto_create), exception)
        return None


# 因为有从属关系，所以默认不自动创建
def get_major(name: str, auto_create: bool = False, belongs: Program = None) -> Optional[Major]:
    try:
        return Major.objects.get(name_zh=name)
    except ObjectDoesNotExist:
        if auto_create:
            major = Major(name_zh=name, program=belongs)
            major.save()
            print(
                "Create a new Major [%s] belongs to Program [%s]"
                %
                (major.name_zh, major.program.name_zh)
            )
            return major
        return None
    except Exception as exception:
        print("Exception in get_major(%s,%d):" % (name, auto_create), exception)
        return None


# 因为有从属关系，所以默认不自动创建
def get_program(name: str, auto_create: bool = False, belongs: Faculty = None) -> Optional[Program]:
    try:
        return Program.objects.get(name_zh=name)
    except ObjectDoesNotExist:
        if auto_create:
            program = Program(name_zh=name, faculty=belongs)
            program.save()
            print(
                "Create a new Program [%s] belongs to Faculty [%s]"
                %
                (program.name_zh, program.faculty.name_zh)
            )
            return program
        return None
    except Exception as exception:
        print("Exception in get_program(%s, %d):" % (name, auto_create), exception)
        return None
