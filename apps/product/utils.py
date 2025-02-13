import csv
import random

categories = [
    "Одежда",
    "Обувь",
    "Электроника",
    "Товары для дома",
    "Книги",
    "Спортивные товары",
    "Мебель",
    "Товары для детей",
    "Автотовары",
    "Продукты питания",
    "Одежда и обувь",
    "Электроника",
    "Товары для дома",
    "Книги",
    "Спорт и отдых",
    "Красота и здоровье",
    "Детские товары",
    "Продукты питания",
    "Автотовары",
    "Мебель",
    "Инструменты",
    "Сад и огород",
    "Товары для животных",
    "Ювелирные изделия",
    "Часы",
    "Сумки и аксессуары",
    "Канцелярские товары",
    "Музыкальные инструменты",
    "Хобби и творчество",
    "Туризм и путешествия",
    "Праздники и подарки",
    "Цветы",
    "Искусство",
    "Антиквариат",
    "Коллекционирование",
    "Handmade",
    "Винтаж",
    "Семена",
    "Растения",
    "Удобрения",
    "Пестициды",
    "Садовый инвентарь",
    "Строительные материалы",
    "Сантехника",
    "Отделочные материалы",
    "Окна",
    "Двери",
    "Кровля",
    "Фасады",
    "Фундамент",
    "Инженерные системы",
    "Электрика",
    "Вентиляция",
    "Кондиционеры",
    "Отопление",
    "Водоснабжение",
    "Канализация",
    "Безопасность",
    "Пожарная безопасность",
    "Охранные системы",
    "Видеонаблюдение",
    "Домофоны",
    "Автоматизация",
    "Умный дом",
    "Бытовая техника",
    "Кухонная техника",
    "Аудио- и видеотехника",
    "Компьютеры и комплектующие",
    "Мобильные телефоны",
    "Фото- и видеокамеры",
    "Игры и приставки",
    "Программное обеспечение",
    "Офисная техника",
    "Расходные материалы",
    "Мебель для офиса",
    "Оборудование для бизнеса",
    "Торговое оборудование",
    "Производственное оборудование",
    "Сельскохозяйственная техника",
    "Промышленное оборудование",
    "Медицинское оборудование",
    "Лабораторное оборудование",
    "Спортивное оборудование",
    "Туристическое снаряжение",
    "Охота и рыбалка",
    "Велосипеды",
    "Самокаты",
    "Ролики",
    "Скейтборды",
    "Тренажеры",
    "Бассейны",
    "Сауны",
    "Детские площадки",
    "Аттракционы",
    "Парки и скверы",
    "Животные",
    "Собаки",
    "Кошки",
    "Птицы",
    "Рыбы",
    "Грызуны",
    "Рептилии",
    "Насекомые",
    "Корма для животных",
    "Ветеринарные препараты",
    "Услуги",
    "Ремонт",
    "Строительство",
    "Уборка",
    "Перевозки",
    "Образование",
    "Туризм",
    "Красота",
    "Здоровье",
    "Развлечения",
    "Питание",
    "Финансы",
    "Юридические услуги",
    "Недвижимость",
    "Автомобили",
    "Мотоциклы",
    "Велосипеды",
    "Водный транспорт",
    "Авиатранспорт",
    "Железнодорожный транспорт",
    "Общественный транспорт",
    "Такси",
    "Аренда автомобилей",
    "Каршеринг",
    "Автосервис",
    "Запчасти для автомобилей",
    "Шины",
    "Диски",
    "Аккумуляторы",
    "Автохимия",
    "Автокосметика",
    "Автоаксессуары",
    "Страхование",
    "Кредитование",
    "Инвестирование",
    "Банковские услуги",
    "Финансовые консультации",
    "Бухгалтерские услуги",
    "Юридические услуги",
    "Нотариат",
    "Переводческие услуги",
    "Курьерские услуги",
    "Почтовые услуги",
    "Телекоммуникации",
    "Интернет",
    "Мобильная связь",
    "Телевидение",
    "Радио",
    "Печатные издания",
    "Электронные издания",
    "Онлайн-сервисы",
    "Социальные сети",
    "Мессенджеры",
    "Видеохостинги",
    "Музыкальные сервисы",
    "Облачные хранилища",
    "Онлайн-игры",
    "Виртуальная реальность",
    "Искусственный интеллект",
    "Большие данные",
    "Интернет вещей",
    "Блокчейн",
    "Криптовалюты",
    "Кибербезопасность",
    "Программирование",
    "Разработка",
    "Тестирование",
    "Дизайн",
    "Маркетинг",
    "Продажи",
    "Логистика",
    "Управление",
    "Персонал",
    "Бухгалтерия",
    "Финансы",
    "Юриспруденция",
    "Медицина",
    "Образование",
    "Культура",
    "Спорт",
    "Туризм",
    "Религия",
    "Философия",
    "Психология",
    "Социология",
    "История",
    "География",
    "Экономика",
    "Политика",
    "Право",
    "Экология",
    "Космос",
    "Наука",
    "Техника",
    "Искусство",
    "Литература",
    "Музыка",
    "Кино",
    "Театр",
    "Архитектура",
    "Живопись",
    "Скульптура",
    "Фотография",
    "Дизайн",
    "Мода",
    "Кулинария",
    "Садоводство",
    "Животноводство",
    "Охота",
    "Рыбалка",
    "Пчеловодство",
    "Виноделие",
    "Пивоварение",
    "Коньячное производство",
    "Ликероводочное производство",
    "Безалкогольные напитки",
    "Минеральная вода",
    "Соки",
    "Газированные напитки",
    "Чай",
    "Кофе",
    "Какао",
    "Молоко",
    "Кисломолочные продукты",
    "Сыры",
    "Масло",
    "Яйца",
    "Мясо",
    "Птица",
    "Рыба",
    "Морепродукты",
    "Овощи",
    "Фрукты",
    "Ягоды",
    "Грибы",
    "Орехи",
    "Семена",
    "Крупы",
    "Макароны",
    "Хлеб",
    "Кондитерские изделия",
    "Шоколад",
    "Мороженое",
    "Детское питание",
    "Диетическое питание",
    "Спортивное питание",
    "Вегетарианское питание",
    "Веганское питание",
    "Халяль",
    "Кошерное питание",
    "Безглютеновое питание",
    "Безлактозное питание",
    "Органическое питание",
    "Натуральные продукты",
    "Фермерские продукты",
    "Экопродукты",
    "Биопродукты",
    "Суперфуды",
    "Продукты для похудения",
    "Продукты для набора массы",
    "Продукты для здоровья",
    "Продукты для красоты",
    "Продукты для дома",
    "Продукты для животных",
]
units = ["шт", "кг", "л", "м", "м2", "м3", "упаковка", "банка", "бутылка", "коробка"]

header = [
    "name",
    "category",
    "price",
    "sale_price",
    "discount",
    "quantity",
    "min_quantity",
    "bar_code",
    "unit",
]
rows = []
row_quantity = 500
for i in range(row_quantity):
    name = f"Товар {i+1}"
    category = random.choice(categories)
    price = random.randint(100, 10000)
    sale_price = random.randint(100, price)
    discount = random.randint(1, 100)
    quantity = random.randint(0, 100)
    min_quantity = random.randint(1, 10)
    bar_code = f"{random.randint(100000, 9999999)}"
    unit = random.choice(units)

    rows.append(
        [
            name,
            category,
            price,
            sale_price,
            discount,
            quantity,
            min_quantity,
            bar_code,
            unit,
        ]
    )


csv_filename = f"products_{row_quantity}.csv"
with open(csv_filename, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(rows)

csv_filename
