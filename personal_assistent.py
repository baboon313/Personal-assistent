import json
from datetime import datetime
import csv

class Note:
    def __init__(self, note_id, title, content, timestamp=None):
        self.id = note_id
        self.title = title
        self.content = content
        self.timestamp = timestamp or datetime.now().strftime('%d-%m-%Y %H:%M:%S')

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'timestamp': self.timestamp
        }

class Task:
    def __init__(self, task_id, title, description, done=False, priority='Средний', due_date=None):
        self.id = task_id
        self.title = title
        self.description = description
        self.done = done
        self.priority = priority
        self.due_date = due_date

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'done': self.done,
            'priority': self.priority,
            'due_date': self.due_date
        }

class Contact:
    def __init__(self, contact_id, name, phone, email):
        self.id = contact_id
        self.name = name
        self.phone = phone
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'phone': self.phone,
            'email': self.email
        }

class FinanceRecord:
    def __init__(self, record_id, amount, category, date, description):
        self.id = record_id
        self.amount = amount
        self.category = category
        self.date = date
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'category': self.category,
            'date': self.date,
            'description': self.description
        }

def load_notes():
    try:
        with open('notes.json', 'r') as file:
            notes = json.load(file)
        return [Note(**note) for note in notes]
    except FileNotFoundError:
        return []

def save_notes(notes):
    with open('notes.json', 'w') as file:
        json.dump([note.to_dict() for note in notes], file, indent=4)

def create_note(notes):
    title = input("Введите заголовок заметки: ")
    content = input("Введите содержимое заметки: ")
    note_id = len(notes) + 1
    note = Note(note_id, title, content)
    notes.append(note)
    print("Заметка создана успешно!")

def view_notes(notes):
    for note in notes:
        print(f"{note.id}. {note.title} ({note.timestamp})")

def view_note_details(notes):
    note_id = int(input("Введите ID заметки: "))
    note = next((n for n in notes if n.id == note_id), None)
    if note:
        print(f"Заголовок: {note.title}")
        print(f"Содержимое: {note.content}")
        print(f"Дата/время: {note.timestamp}")
    else:
        print("Заметка не найдена.")

def edit_note(notes):
    note_id = int(input("Введите ID заметки: "))
    note = next((n for n in notes if n.id == note_id), None)
    if note:
        title = input(f"Введите новый заголовок ({note.title}): ")
        content = input(f"Введите новое содержимое ({note.content}): ")
        note.title = title or note.title
        note.content = content or note.content
        note.timestamp = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
        print("Заметка отредактирована успешно!")
    else:
        print("Заметка не найдена.")

def delete_note(notes):
    note_id = int(input("Введите ID заметки: "))
    note = next((n for n in notes if n.id == note_id), None)
    if note:
        notes.remove(note)
        print("Заметка удалена успешно!")
    else:
        print("Заметка не найдена.")

def import_notes_from_csv(notes):
    filename = input("Введите имя CSV файла: ")
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                note_id = len(notes) + 1
                note = Note(note_id, row['title'], row['content'], row['timestamp'])
                notes.append(note)
        print("Заметки импортированы успешно!")
    except FileNotFoundError:
        print("Файл не найден.")

def export_notes_to_csv(notes):
    filename = input("Введите имя CSV файла: ")
    with open(filename, 'w', newline='') as file:
        fieldnames = ['id', 'title', 'content', 'timestamp']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for note in notes:
            writer.writerow(note.to_dict())
    print("Заметки экспортированы успешно!")

def manage_notes():
    notes = load_notes()
    while True:
        print("Управление заметками:")
        print("1. Создать новую заметку")
        print("2. Просмотреть список заметок")
        print("3. Просмотреть подробности заметки")
        print("4. Редактировать заметку")
        print("5. Удалить заметку")
        print("6. Импорт заметок из CSV")
        print("7. Экспорт заметок в CSV")
        print("8. Назад")
        choice = input("Введите номер действия: ")
        if choice == '1':
            create_note(notes)
        elif choice == '2':
            view_notes(notes)
        elif choice == '3':
            view_note_details(notes)
        elif choice == '4':
            edit_note(notes)
        elif choice == '5':
            delete_note(notes)
        elif choice == '6':
            import_notes_from_csv(notes)
        elif choice == '7':
            export_notes_to_csv(notes)
        elif choice == '8':
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
        save_notes(notes)

# Функции для управления задачами
def load_tasks():
    try:
        with open('tasks.json', 'r') as file:
            tasks = json.load(file)
        return [Task(**task) for task in tasks]
    except FileNotFoundError:
        return []

def save_tasks(tasks):
    with open('tasks.json', 'w') as file:
        json.dump([task.to_dict() for task in tasks], file, indent=4)

def add_task(tasks):
    title = input("Введите краткое описание задачи: ")
    description = input("Введите подробное описание задачи: ")
    priority = input("Введите приоритет задачи (Высокий, Средний, Низкий): ")
    due_date = input("Введите срок выполнения задачи (ДД-ММ-ГГГГ): ")
    task_id = len(tasks) + 1
    task = Task(task_id, title, description, priority=priority, due_date=due_date)
    tasks.append(task)
    print("Задача добавлена успешно!")

def view_tasks(tasks):
    for task in tasks:
        print(f"{task.id}. {task.title} ({task.priority}, {task.due_date}, {'Выполнено' if task.done else 'Не выполнено'})")

def mark_task_done(tasks):
    task_id = int(input("Введите ID задачи: "))
    task = next((t for t in tasks if t.id == task_id), None)
    if task:
        task.done = True
        print("Задача отмечена как выполненная!")
    else:
        print("Задача не найдена.")

def edit_task(tasks):
    task_id = int(input("Введите ID задачи: "))
    task = next((t for t in tasks if t.id == task_id), None)
    if task:
        title = input(f"Введите новое краткое описание ({task.title}): ")
        description = input(f"Введите новое подробное описание ({task.description}): ")
        priority = input(f"Введите новый приоритет ({task.priority}): ")
        due_date = input(f"Введите новый срок выполнения ({task.due_date}): ")
        task.title = title or task.title
        task.description = description or task.description
        task.priority = priority or task.priority
        task.due_date = due_date or task.due_date
        print("Задача отредактирована успешно!")
    else:
        print("Задача не найдена.")

def delete_task(tasks):
    task_id = int(input("Введите ID задачи: "))
    task = next((t for t in tasks if t.id == task_id), None)
    if task:
        tasks.remove(task)
        print("Задача удалена успешно!")
    else:
        print("Задача не найдена.")

def import_tasks_from_csv(tasks):
    filename = input("Введите имя CSV файла: ")
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                task_id = len(tasks) + 1
                task = Task(task_id, row['title'], row['description'], row['done'] == 'True', row['priority'], row['due_date'])
                tasks.append(task)
        print("Задачи импортированы успешно!")
    except FileNotFoundError:
        print("Файл не найден.")

def export_tasks_to_csv(tasks):
    filename = input("Введите имя CSV файла: ")
    with open(filename, 'w', newline='') as file:
        fieldnames = ['id', 'title', 'description', 'done', 'priority', 'due_date']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow(task.to_dict())
    print("Задачи экспортированы успешно!")

def manage_tasks():
    tasks = load_tasks()
    while True:
        print("Управление задачами:")
        print("1. Добавить новую задачу")
        print("2. Просмотреть список задач")
        print("3. Отметить задачу как выполненную")
        print("4. Редактировать задачу")
        print("5. Удалить задачу")
        print("6. Импорт задач из CSV")
        print("7. Экспорт задач в CSV")
        print("8. Назад")
        choice = input("Введите номер действия: ")
        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            mark_task_done(tasks)
        elif choice == '4':
            edit_task(tasks)
        elif choice == '5':
            delete_task(tasks)
        elif choice == '6':
            import_tasks_from_csv(tasks)
        elif choice == '7':
            export_tasks_to_csv(tasks)
        elif choice == '8':
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
        save_tasks(tasks)

# Функции для управления контактами
def load_contacts():
    try:
        with open('contacts.json', 'r') as file:
            contacts = json.load(file)
        return [Contact(**contact) for contact in contacts]
    except FileNotFoundError:
        return []

def save_contacts(contacts):
    with open('contacts.json', 'w') as file:
        json.dump([contact.to_dict() for contact in contacts], file, indent=4)

def add_contact(contacts):
    name = input("Введите имя контакта: ")
    phone = input("Введите номер телефона: ")
    email = input("Введите адрес электронной почты: ")
    contact_id = len(contacts) + 1
    contact = Contact(contact_id, name, phone, email)
    contacts.append(contact)
    print("Контакт добавлен успешно!")

def search_contact(contacts):
    query = input("Введите имя или номер телефона для поиска: ")
    results = [contact for contact in contacts if query in contact.name or query in contact.phone]
    for contact in results:
        print(f"{contact.id}. {contact.name} ({contact.phone}, {contact.email})")

def edit_contact(contacts):
    contact_id = int(input("Введите ID контакта: "))
    contact = next((c for c in contacts if c.id == contact_id), None)
    if contact:
        name = input(f"Введите новое имя ({contact.name}): ")
        phone = input(f"Введите новый номер телефона ({contact.phone}): ")
        email = input(f"Введите новый адрес электронной почты ({contact.email}): ")
        contact.name = name or contact.name
        contact.phone = phone or contact.phone
        contact.email = email or contact.email
        print("Контакт отредактирован успешно!")
    else:
        print("Контакт не найден.")

def delete_contact(contacts):
    contact_id = int(input("Введите ID контакта: "))
    contact = next((c for c in contacts if c.id == contact_id), None)
    if contact:
        contacts.remove(contact)
        print("Контакт удален успешно!")
    else:
        print("Контакт не найден.")

def import_contacts_from_csv(contacts):
    filename = input("Введите имя CSV файла: ")
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                contact_id = len(contacts) + 1
                contact = Contact(contact_id, row['name'], row['phone'], row['email'])
                contacts.append(contact)
        print("Контакты импортированы успешно!")
    except FileNotFoundError:
        print("Файл не найден.")

def export_contacts_to_csv(contacts):
    filename = input("Введите имя CSV файла: ")
    with open(filename, 'w', newline='') as file:
        fieldnames = ['id', 'name', 'phone', 'email']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for contact in contacts:
            writer.writerow(contact.to_dict())
    print("Контакты экспортированы успешно!")

def manage_contacts():
    contacts = load_contacts()
    while True:
        print("Управление контактами:")
        print("1. Добавить новый контакт")
        print("2. Поиск контакта")
        print("3. Редактировать контакт")
        print("4. Удалить контакт")
        print("5. Импорт контактов из CSV")
        print("6. Экспорт контактов в CSV")
        print("7. Назад")
        choice = input("Введите номер действия: ")
        if choice == '1':
            add_contact(contacts)
        elif choice == '2':
            search_contact(contacts)
        elif choice == '3':
            edit_contact(contacts)
        elif choice == '4':
            delete_contact(contacts)
        elif choice == '5':
            import_contacts_from_csv(contacts)
        elif choice == '6':
            export_contacts_to_csv(contacts)
        elif choice == '7':
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
        save_contacts(contacts)

# Функции для управления финансовыми записями
def load_finance_records():
    try:
        with open('finance.json', 'r') as file:
            records = json.load(file)
        return [FinanceRecord(**record) for record in records]
    except FileNotFoundError:
        return []

def save_finance_records(records):
    with open('finance.json', 'w') as file:
        json.dump([record.to_dict() for record in records], file, indent=4)

def add_finance_record(records):
    amount = float(input("Введите сумму операции (положительное число для доходов, отрицательное для расходов): "))
    category = input("Введите категорию операции: ")
    date = input("Введите дату операции (ДД-ММ-ГГГГ): ")
    description = input("Введите описание операции: ")
    record_id = len(records) + 1
    record = FinanceRecord(record_id, amount, category, date, description)
    records.append(record)
    print("Финансовая запись добавлена успешно!")

def view_finance_records(records):
    for record in records:
        print(f"{record.id}. {record.amount} ({record.category}, {record.date}, {record.description})")

def generate_finance_report(records):
    start_date = input("Введите начальную дату (ДД-ММ-ГГГГ): ")
    end_date = input("Введите конечную дату (ДД-ММ-ГГГГ): ")
    filtered_records = [record for record in records if start_date <= record.date <= end_date]
    total_income = sum(record.amount for record in filtered_records if record.amount > 0)
    total_expense = sum(record.amount for record in filtered_records if record.amount < 0)
    print(f"Общий доход: {total_income}")
    print(f"Общие расходы: {total_expense}")
    print(f"Общий баланс: {total_income + total_expense}")

def import_finance_records_from_csv(records):
    filename = input("Введите имя CSV файла: ")
    try:
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                record_id = len(records) + 1
                record = FinanceRecord(record_id, float(row['amount']), row['category'], row['date'], row['description'])
                records.append(record)
        print("Финансовые записи импортированы успешно!")
    except FileNotFoundError:
        print("Файл не найден.")

def export_finance_records_to_csv(records):
    filename = input("Введите имя CSV файла: ")
    with open(filename, 'w', newline='') as file:
        fieldnames = ['id', 'amount', 'category', 'date', 'description']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record.to_dict())
    print("Финансовые записи экспортированы успешно!")

def manage_finance():
    records = load_finance_records()
    while True:
        print("Управление финансовыми записями:")
        print("1. Добавить новую запись")
        print("2. Просмотреть все записи")
        print("3. Генерация отчётов")
        print("4. Импорт записей из CSV")
        print("5. Экспорт записей в CSV")
        print("6. Назад")
        choice = input("Введите номер действия: ")
        if choice == '1':
            add_finance_record(records)
        elif choice == '2':
            view_finance_records(records)
        elif choice == '3':
            generate_finance_report(records)
        elif choice == '4':
            import_finance_records_from_csv(records)
        elif choice == '5':
            export_finance_records_to_csv(records)
        elif choice == '6':
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")
        save_finance_records(records)

# Функция для калькулятора
def calculator():
    while True:
        print("Калькулятор:")
        print("Введите выражение для вычисления или 'exit' для выхода:")
        expression = input("Введите выражение: ")
        if expression.lower() == 'exit':
            break
        try:
            result = eval(expression)
            print(f"Результат: {result}")
        except Exception as e:
            print(f"Ошибка: {e}")

# Основное меню
def main_menu():
    print("Добро пожаловать в Персональный помощник!")
    print("Выберите действие:")
    print("1. Управление заметками")
    print("2. Управление задачами")
    print("3. Управление контактами")
    print("4. Управление финансовыми записями")
    print("5. Калькулятор")
    print("6. Выход")

def main():
    while True:
        main_menu()
        choice = input("Введите номер действия: ")
        if choice == '1':
            manage_notes()
        elif choice == '2':
            manage_tasks()
        elif choice == '3':
            manage_contacts()
        elif choice == '4':
            manage_finance()
        elif choice == '5':
            calculator()
        elif choice == '6':
            print("До свидания!")
            break
        else:
            print("Неверный выбор. Пожалуйста, попробуйте снова.")

if __name__ == "__main__":
    main()
