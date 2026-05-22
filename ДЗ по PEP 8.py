# из модуля functools мы импортируем только объект total_ordering.
# (functools — это встроенный модуль Python. 
#  в нём лежат разные полезные инструменты для работы с функциями и классами.)
# (total_ordering — это специальный декоратор для классов.
#  он помогает не писать вручную все методы сравнения, если есть только __lt__ и __eq__
from functools import total_ordering

# функция подсчета среднего 
def calculate_avg(grades_dict):
    total = 0
    count = 0

    for grade_list in grades_dict.values():
        for grade in grade_list:
            total += grade
            count += 1

    if count:
        return total / count
    return 0

# декоратор @total_ordering Эта штука сама "дорисует" остальные знаки сравнения
@total_ordering
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

    # метод выставления оценок лекторам студентами
    def rate_lecture(self, lecturer, course, grade):
        if not (0 <= grade <= 10):
            return 'Ошибка: оценка должна быть от 0 до 10'
        if (isinstance(lecturer, Lecturer) and
                course in self.courses_in_progress and
                course in lecturer.courses_attached):
            if course in lecturer.grades:
                lecturer.grades[course] += [grade]
            else:
                lecturer.grades[course] = [grade]
        else:
            return 'Ошибка'

    # вызываем метод подсчета средней оценки студента за ДЗ 
    def _get_avg_grade(self):
        return calculate_avg(self.grades)

    # метод переопределения __str__ у студентов
    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за домашние задания: {self._get_avg_grade()}\n'
            f'Курсы в процессе изучения: {self.courses_in_progress}\n'
            f'Завершенные курсы: {self.finished_courses}'
        )

    # Магический метод сравнения (lt - меньше)
    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._get_avg_grade() < other._get_avg_grade()

    # Магический метод сравнения (eq - равенство)
    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._get_avg_grade() == other._get_avg_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []

    # метод выставления оценок лекторам студентами
    def rate_lecture(self, lecturer, course, grade):
        # Если метод вызывается у любого Ментора (в т.ч. Ревьюера), 
        # он просто возвращает None, так как оценивать может только Студент
        return None

    def rate_hw(self, student, course, grade):
        # Если метод вызывается у любого Ментора (в т.ч. Лектора), 
        # он просто возвращает None, так как оценивать может только ревьюир 
        return None

@total_ordering
class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    # вызываем метод подсчета средней оценки лектора 
    def _get_avg_grade(self):
        return calculate_avg(self.grades)

    # метод переопределения __str__ у леторов
    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за лекции: {self._get_avg_grade()}'
        )

    # Магический метод сравнения (lt - меньше)
    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._get_avg_grade() < other._get_avg_grade()

    # Магический метод сравнения (eq - равенство)
    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._get_avg_grade() == other._get_avg_grade()


class Reviewer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)

    # Метод выставления оценок студентам ревьюирами    
    def rate_hw(self, student, course, grade):
        if not (0 <= grade <= 10):
            return 'Ошибка: оценка должна быть от 0 до 10'
        if (isinstance(student, Student) and
                course in self.courses_attached and
                course in student.courses_in_progress):
            if course in student.grades:
                student.grades[course] += [grade]
            else:
                student.grades[course] = [grade]
        else:
            return 'Ошибка'

    # метод переопределения __str__ у ревьюиров
    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


# Создаем экземпляры студентов
student = Student('Алёхина', 'Ольга', 'Ж')
student2 = Student('Петрова', 'Марина', 'Ж')

# добавляем студентам курсы в процессе прохождения и пройденные
student.courses_in_progress += ['Python', 'Java']
student.finished_courses += ['Введение в программирование']

student2.courses_in_progress += ['Python', 'Java']
student2.finished_courses += ['Введение в программирование']

# Создаем экземпляры лекторов
lecturer = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Семен', 'Семенов')

# Добавляем лекторам прикрепленные за ними курсы
lecturer.courses_attached += ['Python', 'C++']
lecturer2.courses_attached += ['Python', 'C++']

# Создаем экземпляр ревьюера
reviewer = Reviewer('Пётр', 'Петров')
reviewer2 = Reviewer('Евгений', 'Васинов')

# Добавляем приклепленные к ревьюиру курсы 
reviewer.courses_attached += ['Python', 'C++']
reviewer2.courses_attached += ['Java', 'C++', 'Python']

# Выставляем оценки студентам (сценари когда можем выставить оценки)
print(reviewer.rate_hw(student, 'Python', 7))
print(reviewer.rate_hw(student, 'Python', 8))
print(reviewer2.rate_hw(student2, 'Java', 7))
print(reviewer2.rate_hw(student2, 'Python', 9))

# Выставляем оценки студентам (сценари когда не можем выставить оценки)
print(reviewer.rate_hw(student, 'GIT', 7)) # reviewer не ведет 'GIT'
print(reviewer.rate_hw(student, 'Java', 8)) # reviewer не ведет 'Java'
print(reviewer2.rate_hw(student2, 'C++', 7)) # student2 не проходит C++
print(reviewer2.rate_hw(student2, 'GO', 9)) # student2 не проходит 'GO'

# Выставляем оценки лекторам (сценари когда можем выставить оценки)
print(student.rate_lecture(lecturer, 'Python', 10))
print(student.rate_lecture(lecturer, 'Python', 3))
print(student.rate_lecture(lecturer2, 'Python', 7))
print(student.rate_lecture(lecturer2, 'Python', 8))

# Выставляем оценки лекторам (сценари когда не можем выставить оценки)
print(student.rate_lecture(lecturer, 'Java', 10)) # lecture не ведет 'Java'
print(student.rate_lecture(lecturer, 'C++', 3)) # student не изучает 'C++'
print(student2.rate_lecture(lecturer2, 'Введение в программирование', 7)) # (student2 закончил
#'Введение в программирование'и его не ведет lecturer2)
print(student2.rate_lecture(lecturer2, 'C++', 8)) # student2 не изучает 'C++'

# Сценарий когда ревьюир пытается оценить лектора 
result = reviewer.rate_lecture(lecturer2, 'C++', 8)
if result is None:
    print('Лектора оценивать может только студент')
else:
    print(result)

# Сценарий когда лектор пытается оценить студента 
result = lecturer2.rate_hw(student, 'C++', 8)
if result is None:
    print('Студента может оценивать только ревьюир')
else:
    print(result)

# Вывод информации по студентам, лекторам, ревьюирам
print(student)
print(lecturer)
print(reviewer)

# Сравнение
print(f"Лектор 1 < Лектор 2: {lecturer < lecturer2}")
print(f"Студент 1 > Студент 2: {student > student2}")


# Функции для подсчета средних оценок
def avg_homework_grade(students_list, course):
    all_grades = []
    for student in students_list:
        if course in student.grades:
            all_grades.extend(student.grades[course])
    if all_grades:
        return sum(all_grades) / len(all_grades)
    return 0


def avg_lecture_grade(lecturer_list, course):
    all_grades = []
    for lect in lecturer_list:
        if course in lect.grades:
            all_grades.extend(lect.grades[course])
    if all_grades:
        return sum(all_grades) / len(all_grades)
    return 0


all_students = [student, student2]
all_lecturers = [lecturer, lecturer2]

print(f"Средняя за ДЗ по Python: {avg_homework_grade(all_students, 'Python')}")
print(f"Средняя за лекции по Python: {avg_lecture_grade(all_lecturers, 'Python')}")

