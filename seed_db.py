"""
Скрипт для заповнення бази даних тестовими даними
Запуск: python seed_db.py
"""

import os
import django
import random
import datetime
from decimal import Decimal

# Налаштування Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CFapp.settings')
django.setup()

from django.utils import timezone
from django.db import models
from django.contrib.auth import get_user_model
from app.models import Project, ProjectMedia, Donation, ChatMessage

# ОЧИЩЕННЯ БАЗИ ДАНИХ (будьте обережні з цим у реальному середовищі!)
print("Очищення бази даних...")
CustomUser = get_user_model()
# Зберігаємо суперкористувача
superusers = CustomUser.objects.filter(is_superuser=True)
superuser_data = [(user.username, user.email, user.password) for user in superusers]

# Видаляємо всі дані
ChatMessage.objects.all().delete()
Donation.objects.all().delete()
ProjectMedia.objects.all().delete()
Project.objects.all().delete()
CustomUser.objects.all().delete()

# Відновлюємо суперкористувача(ів)
for username, email, password in superuser_data:
    CustomUser.objects.create_superuser(
        username=username,
        email=email,
        password="admin"  # Встановлюємо пароль "admin"
    )

# Налаштування
INVESTORS_COUNT = 10
AUTHORS_COUNT = 5
ADMINS_COUNT = 2
PROJECTS_COUNT = 10
MEDIA_PER_PROJECT = 3
DONATIONS_PER_PROJECT = 10
MESSAGES_PER_PROJECT = 8

# Дані для автоматичного заповнення
UKRAINIAN_FIRST_NAMES = [
    "Олександр", "Андрій", "Іван", "Максим", "Дмитро", "Михайло", "Назар", "Олег", "Роман", "Віталій",
    "Ольга", "Марія", "Анна", "Юлія", "Наталія", "Ірина", "Катерина", "Вікторія", "Тетяна", "Світлана"
]

UKRAINIAN_LAST_NAMES = [
    "Шевченко", "Коваленко", "Бондаренко", "Ткаченко", "Мельник", "Кравченко", "Поліщук", "Петренко", "Іваненко", "Пономаренко",
    "Василенко", "Павленко", "Савченко", "Левченко", "Романенко", "Гордієнко", "Даниленко", "Захарченко", "Кириченко", "Марченко"
]

PROJECT_CATEGORIES = [
    "Технології", "Мистецтво", "Музика", "Їжа", "Ігри", "Спорт", "Освіта", "Медицина", "Екологія", "Культурна спадщина"
]

PROJECT_STATUSES = ['active', 'completed', 'active', 'active']  # Більше активних проектів

PROJECT_TITLES = [
    "Розумний будильник \"Світанок\"",
    "Еко-рюкзак з сонячними панелями",
    "Українська настільна гра \"Козаки\"",
    "Мобільний додаток для вивчення української мови",
    "Соціальна мережа для музикантів",
    "Екологічна ферма вертикального типу",
    "Пристрій для очищення води у походах",
    "Інтерактивна книга з доповненою реальністю",
    "Смарт-годинник для людей з вадами зору",
    "Платформа для онлайн-курсів з програмування",
    "Фільм про українських митців",
    "Серія коміксів про українську міфологію",
    "Електричний самокат \"Швидкий\"",
    "Розробка дитячих екологічних іграшок",
    "Документальний фільм про Карпати",
    "Інноваційна система переробки відходів",
    "Ресторан української кухні \"Смаколики\"",
    "Мобільний додаток для туристів",
    "3D-принтер для шкіл",
    "Реставрація історичного парку"
]

PROJECT_DESCRIPTIONS = [
    """Цей проект спрямований на створення інноваційного розумного будильника "Світанок", який допоможе користувачам прокидатись природним шляхом.

Особливості будильника:
- Імітація природного світанку за 30 хвилин до часу пробудження
- Плавне збільшення гучності звуку
- Відстеження фаз сну для оптимального пробудження
- Інтеграція з мобільним додатком
- Можливість налаштування різних сценаріїв пробудження
- Енергоефективний дизайн

Ваша підтримка допоможе нам закупити необхідні матеріали, оптимізувати програмне забезпечення та почати масове виробництво. Разом ми зробимо ранкове пробудження приємним!""",

    """Еко-рюкзак із вбудованими сонячними панелями – це інноваційний продукт для сучасних міських користувачів та любителів активного відпочинку.

Наш рюкзак дозволяє:
- Заряджати гаджети від сонячної енергії
- Економити електроенергію
- Бути незалежним від електричних розеток
- Підтримувати екологічний спосіб життя

Рюкзак виготовлений з переробленого поліестеру, має водонепроникне покриття та вбудовані гнучкі сонячні панелі. Внутрішній акумулятор накопичує енергію для зарядки пристроїв навіть у хмарну погоду.

З вашою підтримкою ми запустимо виробництво цього унікального продукту, який поєднує стиль, функціональність та екологічність.""",

    """Настільна гра "Козаки" – це захоплива стратегічна гра, присвячена історії українського козацтва XVII століття.

Особливості гри:
- 2-6 гравців
- Тривалість партії: 45-90 хвилин
- Стратегічний геймплей з елементами економіки та дипломатії
- Детально опрацьовані фігурки козаків, гетьманів та історичних персонажів
- Якісні ігрові компоненти та автентичні ілюстрації
- Підтримка різних сценаріїв гри, заснованих на реальних історичних подіях

Наша мета – створити не лише цікаву гру, але й освітній інструмент, який познайомить гравців з багатою історією та культурою України. Ваша підтримка допоможе нам завершити розробку, протестувати та випустити гру на український та міжнародний ринки.""",

    """Мобільний додаток для вивчення української мови – це інтерактивний інструмент, який допоможе всім бажаючим вивчити українську легко та цікаво.

Особливості додатку:
- Інтерактивні уроки з граматики, лексики та вимови
- Адаптивна система навчання, яка пристосовується до рівня користувача
- Gamification елементи для підвищення мотивації
- Щоденні 5-хвилинні вправи для регулярної практики
- Аудіоматеріали від носіїв мови
- Офлайн-режим для навчання без інтернету

Наша команда складається з досвідчених розробників та викладачів української мови. Зібрані кошти будуть використані для доопрацювання додатку, створення якісного контенту та запуску на iOS та Android платформах.""",

    """Соціальна мережа для музикантів – це платформа, яка допоможе талановитим виконавцям знаходити однодумців, створювати спільні проекти та розвивати свою творчу кар'єру.

Функціональність платформи:
- Профілі з можливістю завантаження аудіо- та відеоматеріалів
- Пошук музикантів за жанрами, інструментами та географічним розташуванням
- Система організації концертів та джем-сейшнів
- Відеочати для віддалених репетицій
- Інструменти для колаборативного створення музики
- Можливість продажу власної музики без посередників

Ми вже розробили прототип платформи та сформували команду розробників. Ваша підтримка допоможе нам реалізувати проект у повному обсязі та створити справжню екосистему для розвитку музичного таланту.""",
    
    """Екологічна ферма вертикального типу – це інноваційний проект, який дозволить вирощувати органічні продукти цілий рік, використовуючи мінімальну площу та ресурси.

Особливості проекту:
- Багаторівнева система вирощування на гідропоніці
- Використання LED-освітлення зі спеціальним спектром
- Автоматизована система поливу та моніторингу
- Відсутність пестицидів та хімічних добрив
- На 95% менше води порівняно з традиційним землеробством
- У 15 разів більша врожайність на одиницю площі

Наш проект має на меті не лише створення прибуткового бізнесу, але й вирішення проблеми доступності свіжих органічних продуктів у міських районах. Зібрані кошти будуть використані для облаштування приміщення, закупівлі обладнання та запуску першої експериментальної ферми."""
]

CHAT_MESSAGES = [
    "Дуже цікавий проект! Розкажіть, будь ласка, докладніше про технологію, яку ви використовуєте?",
    "Коли планується запуск проекту?",
    "Дякую за підтримку нашого проекту! Ми дуже цінуємо ваш внесок.",
    "Чи є у вас система знижок для тих, хто робить великі донати?",
    "Як ви плануєте використовувати зібрані кошти?",
    "Вітаю з успішним стартом! Проект справді заслуговує на увагу.",
    "Чи можна буде отримати детальний звіт про витрачені кошти?",
    "Мене зацікавив ваш проект. Розкажіть, будь ласка, про команду розробників.",
    "Чи є у вас соціальні мережі, де можна слідкувати за новинами проекту?",
    "Який мінімальний внесок потрібен для підтримки проекту?",
    "Чи будуть якісь бонуси для донатерів?",
    "Як довго триватиме збір коштів?",
    "Цей проект схожий на той, що я бачив минулого року. Чим ви відрізняєтесь?",
    "Ви плануєте розширювати проект після завершення кампанії?",
    "А чи можна відвідати вашу компанію/студію/офіс та побачити процес розробки?",
    "Чудова ідея! Давно мріяв про щось подібне.",
    "Чи можна стати частиною вашої команди, якщо я спеціаліст у цій сфері?",
    "Наскільки складно було розробити прототип?",
    "Це дійсно вирішує важливу проблему. Підтримую!",
    "Скільки часу займе виготовлення і доставка винагород для донатерів?",
    "Відповідаю на ваше запитання щодо технології. Ми використовуємо інноваційний підхід, заснований на найновіших дослідженнях.",
    "Запуск проекту запланований на наступний квартал, орієнтовно у вересні цього року.",
    "Так, для великих донатів ми передбачили спеціальну програму винагород. Деталі можна знайти в описі проекту.",
    "Зібрані кошти будуть спрямовані на закупівлю обладнання (60%), зарплату команді (25%) та маркетинг (15%).",
    "Дякуємо за інтерес! Нашу команду складають професіонали з багаторічним досвідом у цій галузі.",
    "Так, ви можете слідкувати за нами у Facebook, Instagram та Twitter. Посилання є на нашій сторінці проекту.",
    "Мінімальний внесок становить 100 грн, але будь-яка підтримка для нас цінна!",
    "Збір коштів триватиме 60 днів, після чого ми почнемо активну фазу реалізації проекту.",
    "Відмінність нашого проекту полягає у використанні новітніх технологій та унікальному дизайні продукту.",
    "Так, ми плануємо не лише реалізувати заявлені цілі, але й розширити функціонал у майбутньому."
]

DONATION_COMMENTS = [
    "Дуже цікавий проект! Бажаю успіху!",
    "Чудова ідея, радий підтримати!",
    "Вірю у вашу команду! Чекаю на результати!",
    "Вперше роблю донат, але ваш проект справді заслуговує на увагу!",
    "Хочу бути частиною цього інноваційного проекту!",
    "Таких проектів в Україні дуже не вистачає!",
    "Сподіваюсь, ви досягнете цілі! Буду слідкувати за прогресом.",
    "Чудовий проект, з нетерпінням чекаю на його реалізацію!",
    "Із задоволенням підтримую українських розробників!",
    "Донат зроблено! Удачі вам!",
    "Дякую за те, що робите щось таке потрібне!",
    "Внесок невеликий, але з великим бажанням підтримати!",
    "Сподіваюсь, мій внесок допоможе втілити ваші ідеї!",
    "Потрапив на вашу сторінку випадково, але проект дуже сподобався!",
    "Давно слідкую за вашою командою, радий підтримати новий проект!"
]

def generate_date_between(start, end):
    """Генерує випадкову дату між start та end з обробкою крайніх випадків"""
    # Якщо кінцева дата раніше за початкову, міняємо їх місцями
    if end < start:
        start, end = end, start
    
    # Якщо дати співпадають, повертаємо цю дату
    if start == end:
        return start
    
    # Різниця в днях + 1 (щоб включити кінцевий день)
    delta_days = (end - start).days + 1
    
    # Випадкова кількість днів від 0 до delta_days-1
    random_days = random.randint(0, max(0, delta_days - 1))
    
    # Нова дата
    return start + datetime.timedelta(days=random_days)

# Створення користувачів
print("Створення користувачів...")

investors = []
for i in range(INVESTORS_COUNT):
    first_name = random.choice(UKRAINIAN_FIRST_NAMES)
    last_name = random.choice(UKRAINIAN_LAST_NAMES)
    username = f"{first_name.lower()}{random.randint(100, 999)}"
    email = f"{username}@example.com"
    
    investor = CustomUser.objects.create_user(
        username=username,
        email=email,
        password="password123",
        first_name=first_name,
        last_name=last_name,
        user_type="investor"
    )
    investors.append(investor)
    print(f"Створено інвестора: {username}")

authors = []
for i in range(AUTHORS_COUNT):
    first_name = random.choice(UKRAINIAN_FIRST_NAMES)
    last_name = random.choice(UKRAINIAN_LAST_NAMES)
    username = f"author_{first_name.lower()}{random.randint(100, 999)}"
    email = f"{username}@example.com"
    
    author = CustomUser.objects.create_user(
        username=username,
        email=email,
        password="password123",
        first_name=first_name,
        last_name=last_name,
        user_type="author"
    )
    authors.append(author)
    print(f"Створено автора: {username}")

admins = []
for i in range(ADMINS_COUNT):
    first_name = random.choice(UKRAINIAN_FIRST_NAMES)
    last_name = random.choice(UKRAINIAN_LAST_NAMES)
    username = f"admin_{first_name.lower()}{random.randint(100, 999)}"
    email = f"{username}@example.com"
    
    admin = CustomUser.objects.create_user(
        username=username,
        email=email,
        password="password123",
        first_name=first_name,
        last_name=last_name,
        user_type="admin",
        is_staff=True
    )
    admins.append(admin)
    print(f"Створено адміністратора: {username}")

# Створення проектів
print("\nСтворення проектів...")

projects = []
now = timezone.now()
# Період до 6 місяців тому для дат створення проектів
past_date = now - datetime.timedelta(days=180)
# Період до 1 року вперед для дедлайнів
future_date = now + datetime.timedelta(days=365)

# Використовуємо копію списку назв, щоб не змінювати оригінал
available_titles = PROJECT_TITLES.copy()

for i in range(min(PROJECTS_COUNT, len(available_titles))):
    title = random.choice(available_titles)
    available_titles.remove(title)  # Видаляємо використану назву
    
    # Вибираємо опис або генеруємо стандартний
    description = PROJECT_DESCRIPTIONS[i] if i < len(PROJECT_DESCRIPTIONS) else f"Опис проекту {title}"
    
    author = random.choice(authors + admins)  # Автори та адміни можуть створювати проекти
    goal_amount = Decimal(random.randint(5000, 100000))
    
    # Дата створення - випадкова дата в минулому (до 6 місяців тому)
    created_at = generate_date_between(past_date, now)
    
    # Дедлайн - випадкова дата від 1 до 6 місяців після створення
    min_deadline = created_at + datetime.timedelta(days=30)  # мінімум 30 днів
    max_deadline = created_at + datetime.timedelta(days=180)  # максимум +6 місяців
    deadline = generate_date_between(min_deadline, max_deadline)
    
    # Початковий статус - завжди активний
    status = 'active'
    
    # Початкова сума - 0
    current_amount = Decimal('0.00')
    
    category = random.choice(PROJECT_CATEGORIES)
    
    project = Project.objects.create(
        title=title,
        description=description,
        author=author,
        goal_amount=goal_amount,
        current_amount=current_amount,
        status=status,
        created_at=created_at,
        deadline=deadline,
        category=category
    )
    projects.append(project)
    print(f"Створено проект: {title}")
    
    # Додаємо медіа-файли
    for j in range(random.randint(1, MEDIA_PER_PROJECT)):
        media_type = random.choice(['image', 'video', 'document'])
        
        if media_type == 'image':
            # Використовуємо Picsum для зображень
            image_id = random.randint(1, 1000)
            url = f"https://picsum.photos/id/{image_id}/800/600"
        elif media_type == 'video':
            # Використовуємо YouTube для відео
            video_ids = ['dQw4w9WgXcQ', 'J9go2nj6b3M', 'jNQXAC9IVRw', 'YE7VzlLtp-4', 'kXYiU_JCYtU']
            url = f"https://www.youtube.com/watch?v={random.choice(video_ids)}"
        else:
            # Для документів URL не потрібен
            url = None
        
        ProjectMedia.objects.create(
            project=project,
            media_type=media_type,
            url=url
        )

# Створення донатів
print("\nСтворення донатів...")

# Список всіх можливих донорів
all_donors = investors + authors + admins

for project in projects:
    # Кількість донатів для проекту
    num_donations = random.randint(5, DONATIONS_PER_PROJECT)
    
    # Період для донатів - від дати створення проекту до сьогодні або дедлайну, якщо він раніше
    donate_end_date = min(now, project.deadline)
    
    # Створюємо донати тільки якщо є період для них
    if donate_end_date > project.created_at:
        total_donated = Decimal('0.00')
        
        for _ in range(num_donations):
            # Випадковий донор
            donor = random.choice(all_donors)
            
            # Випадкова сума донату
            amount = Decimal(random.randint(100, 5000))
            total_donated += amount
            
            # Випадковий коментар (70% шанс)
            comment = random.choice(DONATION_COMMENTS) if random.random() > 0.3 else None
            
            # Дата донату - між створенням проекту та кінцевою датою для донатів
            created_at = generate_date_between(project.created_at, donate_end_date)
            
            # Створюємо донат
            donation = Donation.objects.create(
                investor=donor,
                project=project,
                amount=amount,
                comment=comment,
                created_at=created_at
            )
        
        # Оновлюємо проект з загальною сумою донатів
        project.current_amount = total_donated
        
        # Якщо сума досягла або перевищила ціль, позначаємо проект як завершений
        if total_donated >= project.goal_amount:
            project.status = 'completed'
        
        project.save()
        print(f"Додано {num_donations} донатів на загальну суму {total_donated} грн до проекту '{project.title}'")

# Створення чат-повідомлень
print("\nСтворення чат-повідомлень...")

for project in projects:
    # Спочатку вітальне повідомлення від автора
    welcome_msg = "Вітаю всіх, хто підтримав проект! На цій сторінці я буду публікувати всі важливі оновлення та відповідати на ваші запитання."
    
    welcome_date = project.created_at + datetime.timedelta(hours=random.randint(1, 24))
    
    ChatMessage.objects.create(
        project=project,
        sender=project.author,
        message=welcome_msg,
        created_at=welcome_date
    )
    
    # Донатори цього проекту
    project_donations = Donation.objects.filter(project=project)
    unique_donors = set([donation.investor for donation in project_donations])
    
    # Якщо є донатори, додаємо повідомлення від них та відповіді автора
    if unique_donors:
        # Випадкова кількість повідомлень
        num_messages = min(MESSAGES_PER_PROJECT, len(CHAT_MESSAGES))
        
        # Період для повідомлень - від першого донату до сьогодні
        first_donation = project_donations.order_by('created_at').first()
        if first_donation:
            chat_start_date = first_donation.created_at
            
            for i in range(num_messages):
                # Випадковий відправник (донатор або автор)
                is_author_message = (i % 2 == 0)  # Чергуємо повідомлення
                
                if is_author_message:
                    sender = project.author
                else:
                    sender = random.choice(list(unique_donors))
                
                # Випадкове повідомлення
                message = CHAT_MESSAGES[i % len(CHAT_MESSAGES)]
                
                # Дата повідомлення - після першого донату і до сьогодні
                created_at = generate_date_between(chat_start_date, now)
                
                # Створюємо повідомлення
                ChatMessage.objects.create(
                    project=project,
                    sender=sender,
                    message=message,
                    created_at=created_at
                )
        
        print(f"Додано {num_messages + 1} повідомлень до чату проекту '{project.title}'")

# Створюємо тестових користувачів
test_investor = CustomUser.objects.create_user(
    username="investor",
    email="investor@example.com",
    password="investor",
    first_name="Тестовий",
    last_name="Інвестор",
    user_type="investor"
)

test_author = CustomUser.objects.create_user(
    username="author",
    email="author@example.com",
    password="author",
    first_name="Тестовий",
    last_name="Автор",
    user_type="author"
)

print("\nПідсумок:")
print(f"Створено {INVESTORS_COUNT} інвесторів, {AUTHORS_COUNT} авторів та {ADMINS_COUNT} адміністраторів")
print(f"Створено {len(projects)} проектів")
print(f"Загальна кількість донатів: {Donation.objects.count()}")
print(f"Загальна кількість повідомлень у чатах: {ChatMessage.objects.count()}")
print("\nСтворено тестових користувачів:")
print("Інвестор: username=investor, password=investor")
print("Автор: username=author, password=author")
print("\nЗаповнення бази даних завершено успішно!")