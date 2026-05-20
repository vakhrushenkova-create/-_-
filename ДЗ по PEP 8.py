from functools import total_ordering


@total_ordering
class Student:
    def __init__(self, name, surname, gender):
        self.name = name
        self.surname = surname
        self.gender = gender
        self.finished_courses = []
        self.courses_in_progress = []
        self.grades = {}

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

    def _get_avg_grade(self):
        total = 0
        count = 0
        for grade_list in self.grades.values():
            for grade in grade_list:
                total += grade
                count += 1
        if count:
            return total / count
        return 0

    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за домашние задания: {self._get_avg_grade()}\n'
            f'Курсы в процессе изучения: {self.courses_in_progress}\n'
            f'Завершенные курсы: {self.finished_courses}'
        )

    def __lt__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._get_avg_grade() < other._get_avg_grade()

    def __eq__(self, other):
        if not isinstance(other, Student):
            return NotImplemented
        return self._get_avg_grade() == other._get_avg_grade()


class Mentor:
    def __init__(self, name, surname):
        self.name = name
        self.surname = surname
        self.courses_attached = []


@total_ordering
class Lecturer(Mentor):
    def __init__(self, name, surname):
        super().__init__(name, surname)
        self.grades = {}

    def _get_avg_grade(self):
        total = 0
        count = 0
        for grade_list in self.grades.values():
            for grade in grade_list:
                total += grade
                count += 1
        if count:
            return total / count
        return 0

    def __str__(self):
        return (
            f'Имя: {self.name}\n'
            f'Фамилия: {self.surname}\n'
            f'Средняя оценка за лекции: {self._get_avg_grade()}'
        )

    def __lt__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._get_avg_grade() < other._get_avg_grade()

    def __eq__(self, other):
        if not isinstance(other, Lecturer):
            return NotImplemented
        return self._get_avg_grade() == other._get_avg_grade()


class Reviewer(Mentor):
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

    def __str__(self):
        return f'Имя: {self.name}\nФамилия: {self.surname}'


# Создаем экземпляры студентов
student = Student('Алёхина', 'Ольга', 'Ж')
student2 = Student('Петрова', 'Марина', 'Ж')

student.courses_in_progress += ['Python', 'Java']
student.finished_courses += ['Введение в программирование']

student2.courses_in_progress += ['Python', 'Java']
student2.finished_courses += ['Введение в программирование']

# Создаем экземпляры лекторов
lecturer = Lecturer('Иван', 'Иванов')
lecturer2 = Lecturer('Семен', 'Семенов')

lecturer.courses_attached += ['Python', 'C++']
lecturer2.courses_attached += ['Python', 'C++']

# Создаем экземпляр ревьюера
reviewer = Reviewer('Пётр', 'Петров')
reviewer.courses_attached += ['Python', 'C++']

# Выставляем оценки
print(reviewer.rate_hw(student, 'Python', 7))
print(reviewer.rate_hw(student, 'Python', 8))
reviewer.rate_hw(student2, 'Python', 7)
reviewer.rate_hw(student2, 'Python', 9)

student.rate_lecture(lecturer, 'Python', 10)
student.rate_lecture(lecturer, 'Python', 3)
student.rate_lecture(lecturer2, 'Python', 7)
student.rate_lecture(lecturer2, 'Python', 8)

# Вывод информации
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

