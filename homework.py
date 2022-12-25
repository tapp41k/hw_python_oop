"""Программа представляет собой модуль фитнес трекера,
    отвечающий за обработку и вывод данных для разных видов тренеровок:
    Бега, Спортивной ходьбы и Плаванья"""
from dataclasses import dataclass, asdict
from typing import Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    INF_MESSAGE = ('Тип тренировки: {training_type}; '
                   'Длительность: {duration:.3f} ч.; '
                   'Дистанция: {distance:.3f} км; '
                   'Ср. скорость: {speed:.3f} км/ч; '
                   'Потрачено ккал: {calories:.3f}.')

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        '''Вывести информационное сообщение о результате тренировки.'''
        return self.INF_MESSAGE.format(**asdict(self))


class Training:
    """ Базовый класс тренировки.
      Параметры:
        action, int - кол-во совершенных действие (число шагов или гребков);
        duration, float - длительность тренировки в часах;
        weight, float - вес пользователя;
        LEN_STEP, float - длинна шага пользователя;
        M_IN_KM, int - константа для перевода значений из метров в километры;
        DURATION_MIN, float - константа для перевода значений из час. в мин."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    MIN_IN_H: float = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        super().__init__()

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            'Метод определения кол-во затраченных калорий'
            '(get_spent_calories) не определен'
        )

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег.
       Все свойства и методы класса наследуются от родительского класса
       За исключением метода расчета калорий, который переопределен ниже."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба.
        Конструктор этого класса принимает доп. параметр:
        height, float - рост пользователя.
        Так же переопределяется метод расчета калорий."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + ((self.get_mean_speed() * self.KMH_IN_MSEC)**2
                    / (self.height / self.CM_IN_M))
                 * self.CALORIES_SPEED_HEIGHT_MULTIPLIER * self.weight)
                * (self.duration * self.MIN_IN_H))


class Swimming(Training):
    """Тренировка: плавание.
        Конструктор этого класса принимает два доп. параметра:
        lenght_pool, float - длина бассейна в метрах;
        count_pool, float - сколько раз пользователь проплыл бассейн.
        Переопределяются методы получения ср. скорости и кол-во калорий."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: float
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    CALORIES_COEF1 = 1.1
    CALORIES_COEF2 = 2
    LEN_STEP = 1.38

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения в воде."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество калорий."""
        return ((self.get_mean_speed() + self.CALORIES_COEF1)
                * self.CALORIES_COEF2 * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков.
        Проверить наличие вида активности в словаре."""
    training_types: dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in training_types:
        return training_types[workout_type](*data)
    else:
        raise TypeError('Вид активности не определен')


def main(training: Training) -> None:
    """Главная функция.
        Вернуть строку сообщения с данными о тренировке."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    """Запуск трекера."""
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
