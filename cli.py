import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def print_header(text):
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def print_success(message):
    print(f"[УСПЕХ] {message}")

def print_error(message):
    print(f"[ОШИБКА] {message}")

def print_info(message):
    print(f"[ИНФО] {message}")

def print_response(method, endpoint, status_code, response_data):
    print("\n" + "─" * 60)
    print(f"[{method}] {endpoint}")
    
    if 200 <= status_code < 300:
        status_label = "OK"
    elif 400 <= status_code < 500:
        status_label = "WARN"
    else:
        status_label = "ERR"
    print(f"Статус: {status_code} ({status_label})")
    
    print("\nОтвет сервера:")
    if isinstance(response_data, dict) and "detail" in response_data:
        print(f"  {response_data['detail']}")
    else:
        print(json.dumps(response_data, indent=2, ensure_ascii=False))
    
    print("─" * 60 + "\n")

def print_room_card(room):
    print("\n┌" + "─" * 58 + "┐")
    print(f"│ Комната: {room['name']:<47} │")
    print("├" + "─" * 58 + "┤")
    print(f"│ ID: {room['id']:<52} │")
    print(f"│ Вместимость: {room['capacity']:<43} │")
    equipment = ", ".join(room.get("equipment", [])) if room.get("equipment") else "нет"
    print(f"│ Оборудование: {equipment:<42} │")
    print("└" + "─" * 58 + "┘")

def print_booking_card(booking):
    print("\n┌" + "─" * 58 + "┐")
    print(f"│ Бронирование #{booking['id']:<42} │")
    print("├" + "─" * 58 + "┤")
    print(f"│ ID комнаты: {booking['room_id']:<44} │")
    print(f"│ Пользователь: {booking['user_name']:<42} │")
    
    start = booking['start_time'].replace('T', ' ') if 'T' in booking['start_time'] else booking['start_time']
    print(f"│ Начало: {start:<48} │")
    
    end = booking['end_time'].replace('T', ' ') if 'T' in booking['end_time'] else booking['end_time']
    print(f"│ Конец: {end:<49} │")
    
    print(f"│ Статус: {booking['status']:<48} │")
    print("└" + "─" * 58 + "┘")

def print_rooms_list(rooms):
    if not rooms:
        print_info("Нет доступных комнат")
        return
    
    print_header(f"Список комнат (всего: {len(rooms)})")
    for i, room in enumerate(rooms, 1):
        print(f"\n  {i}. {room['name']} (ID: {room['id']}, вместимость: {room['capacity']} чел.)")
        if room.get('equipment'):
            print(f"     Оборудование: {', '.join(room['equipment'])}")

def print_room_detail(room_id, room):
    print_header(f"Комната #{room_id}")
    print_room_card(room)

def print_bookings_list(bookings, date_str, room_id):
    print_header(f"Расписание комнаты #{room_id} на {date_str}")
    
    if not bookings:
        print_info(f"На {date_str} бронирований нет")
        return
    
    print(f"\n  Всего бронирований: {len(bookings)}")
    for i, booking in enumerate(bookings, 1):
        start = booking['start_time'].replace('T', ' ') if 'T' in booking['start_time'] else booking['start_time']
        end = booking['end_time'].replace('T', ' ') if 'T' in booking['end_time'] else booking['end_time']
        print(f"\n  {i}. Бронирование #{booking['id']}")
        print(f"     Пользователь: {booking['user_name']}")
        print(f"     Время: {start} -> {end}")
        print(f"     Статус: {booking['status']}")

def print_booking_created(booking):
    print_success("Бронирование успешно создано!")
    print_booking_card(booking)

def menu():
    print("\n" + "=" * 60)
    print("  СИРИУС.АРЕНДА — Терминал управления")
    print("=" * 60)
    print("\n  Основные операции:")
    print("  " + "─" * 25)
    print("  1. Список всех комнат")
    print("  2. Информация о комнате")
    print("  3. Создать комнату")
    print("  4. Редактировать комнату")
    print("  5. Удалить комнату")
    print("\n  Бронирования:")
    print("  " + "─" * 25)
    print("  6. Забронировать пространство")
    print("  7. Расписание комнаты на дату")
    print("  8. Отменить бронирование")
    print("\n  Система:")
    print("  " + "─" * 25)
    print("  9. Выйти")
    print("\n" + "─" * 60)
    return input("Выберите команду: ").strip()

def input_datetime(prompt_label):
    print(f"\nВвод даты и времени для: {prompt_label}")
    print("  (введите значения по отдельности)")
    print("  " + "─" * 40)
    
    while True:
        try:
            year = int(input("    Год (2026-2100): ").strip())
            if year < 2026 or year > 2100:
                print_error("Год должен быть в пределах 2026-2100!")
                continue
                
            month = int(input("    Месяц (1-12): ").strip())
            if month < 1 or month > 12:
                print_error("Месяц должен быть от 1 до 12!")
                continue
                
            day = int(input("    День (1-31): ").strip())
            if day < 1 or day > 31:
                print_error("День должен быть от 1 до 31!")
                continue
                
            hour = int(input("    Час (0-23): ").strip())
            if hour < 0 or hour > 23:
                print_error("Час должен быть от 0 до 23!")
                continue
                
            minute = int(input("    Минуты (0-59): ").strip())
            if minute < 0 or minute > 59:
                print_error("Минуты должны быть от 0 до 59!")
                continue
            
            dt = datetime(year, month, day, hour, minute)
            return dt.isoformat()
            
        except ValueError:
            print_error("Ошибка! Вводите только целые числа. Попробуйте заново.\n")

def get_user_input(prompt, required=True):
    while True:
        value = input(prompt).strip()
        if required and not value:
            print_error("Это поле обязательно для заполнения!")
            continue
        return value

def wait_for_enter():
    input("\nНажмите Enter для продолжения...")

def main():
    while True:
        choice = menu()
        
        if choice == "1":
            try:
                res = requests.get(f"{BASE_URL}/rooms")
                if res.status_code == 200:
                    rooms = res.json()
                    print_rooms_list(rooms)
                else:
                    print_response("GET", "/rooms", res.status_code, res.json())
            except requests.exceptions.ConnectionError:
                print_error("Не удалось подключиться к серверу. Убедитесь, что бэкенд запущен!")
            wait_for_enter()
                
        elif choice == "2":
            try:
                room_id = int(get_user_input("Введите ID комнаты: "))
                res = requests.get(f"{BASE_URL}/rooms/{room_id}")
                if res.status_code == 200:
                    room = res.json()
                    print_room_detail(room_id, room)
                else:
                    print_response("GET", f"/rooms/{room_id}", res.status_code, res.json())
            except ValueError:
                print_error("ID комнаты должен быть целым числом!")
            except requests.exceptions.ConnectionError:
                print_error("Нет связи с сервером.")
            wait_for_enter()
                
        elif choice == "3":
            try:
                print_header("Создание новой комнаты")
                name = get_user_input("  Название комнаты: ")
                capacity = int(get_user_input("  Вместимость (чел): "))
                equip_input = get_user_input("  Оборудование (через запятую, необязательно): ", required=False)
                equip = [e.strip() for e in equip_input.split(",") if e.strip()] if equip_input else []
                
                data = {"name": name, "capacity": capacity, "equipment": equip}
                res = requests.post(f"{BASE_URL}/rooms", json=data)
                
                if res.status_code == 201:
                    print_success(f"Комната '{name}' успешно создана!")
                    print_room_card(res.json())
                else:
                    print_response("POST", "/rooms", res.status_code, res.json())
            except ValueError:
                print_error("Вместимость должна быть целым числом!")
            except requests.exceptions.ConnectionError:
                print_error("Нет связи с сервером.")
            wait_for_enter()

        elif choice == "4":
            try:
                print_header("Редактирование комнаты")
                room_id = int(get_user_input("  ID редактируемой комнаты: "))
                
                check = requests.get(f"{BASE_URL}/rooms/{room_id}")
                if check.status_code != 200:
                    print_error(f"Комната #{room_id} не найдена!")
                    wait_for_enter()
                    continue
                
                old_room = check.json()
                print_info(f"Редактируем комнату: {old_room['name']}")
                
                name = get_user_input("  Новое название: ")
                capacity = int(get_user_input("  Новая вместимость (чел): "))
                equip_input = get_user_input("  Новое оборудование (через запятую, необязательно): ", required=False)
                equip = [e.strip() for e in equip_input.split(",") if e.strip()] if equip_input else []
                
                data = {"name": name, "capacity": capacity, "equipment": equip}
                res = requests.put(f"{BASE_URL}/rooms/{room_id}", json=data)
                
                if res.status_code == 200:
                    print_success(f"Комната #{room_id} успешно обновлена!")
                    print_room_card(res.json())
                else:
                    print_response("PUT", f"/rooms/{room_id}", res.status_code, res.json())
            except ValueError:
                print_error("ID и вместимость должны быть целыми числами!")
            except requests.exceptions.ConnectionError:
                print_error("Нет связи с сервером.")
            wait_for_enter()
                
        elif choice == "5":
            try:
                print_header("Удаление комнаты")
                room_id = int(get_user_input("  ID удаляемой комнаты: "))
                
                confirm = input(f"  Удалить комнату #{room_id}? (y/N): ").strip().lower()
                if confirm != 'y':
                    print_info("Удаление отменено")
                    wait_for_enter()
                    continue
                
                res = requests.delete(f"{BASE_URL}/rooms/{room_id}")
                
                if res.status_code == 200:
                    print_success(res.json().get("detail", f"Комната #{room_id} удалена"))
                else:
                    print_response("DELETE", f"/rooms/{room_id}", res.status_code, res.json())
            except ValueError:
                print_error("ID комнаты должен быть целым числом!")
            except requests.exceptions.ConnectionError:
                print_error("Нет связи с сервером.")
            wait_for_enter()
                
        elif choice == "6":
            try:
                print_header("Создание бронирования")
                room_id = int(get_user_input("  ID комнаты: "))
                
                check = requests.get(f"{BASE_URL}/rooms/{room_id}")
                if check.status_code != 200:
                    print_error(f"Комната #{room_id} не найдена!")
                    wait_for_enter()
                    continue
                
                print_info(f"Бронирование комнаты: {check.json()['name']}")
                user = get_user_input("  Имя пользователя: ")
                
                start_dt = input_datetime("НАЧАЛО")
                end_dt = input_datetime("ОКОНЧАНИЕ")
                
                data = {
                    "room_id": room_id,
                    "user_name": user,
                    "start_time": start_dt,
                    "end_time": end_dt
                }
                
                print("\n  Проверка данных:")
                print(f"    Комната: {room_id}")
                print(f"    Пользователь: {user}")
                print(f"    Начало: {start_dt}")
                print(f"    Конец: {end_dt}")
                
                confirm = input("\n  Подтвердить бронирование? (y/N): ").strip().lower()
                if confirm != 'y':
                    print_info("Бронирование отменено")
                    wait_for_enter()
                    continue
                
                res = requests.post(f"{BASE_URL}/bookings", json=data)
                
                if res.status_code == 201:
                    print_booking_created(res.json())
                else:
                    print_response("POST", "/bookings", res.status_code, res.json())
            except ValueError:
                print_error("ID комнаты должен быть целым числом!")
            except requests.exceptions.ConnectionError:
                print_error("Нет связи с сервером.")
            wait_for_enter()
            
        elif choice == "7":
            try:
                print_header("Просмотр расписания")
                room_id = int(get_user_input("  ID комнаты: "))
                
                check = requests.get(f"{BASE_URL}/rooms/{room_id}")
                if check.status_code != 200:
                    print_error(f"Комната #{room_id} не найдена!")
                    wait_for_enter()
                    continue
                
                print_info(f"Комната: {check.json()['name']}")
                print("\n  Введите дату для просмотра расписания:")
                year = int(get_user_input("    Год: "))
                month = int(get_user_input("    Месяц (1-12): "))
                day = int(get_user_input("    День (1-31): "))
                
                date_str = f"{year:04d}-{month:02d}-{day:02d}"
                res = requests.get(f"{BASE_URL}/rooms/{room_id}/bookings", params={"date": date_str})
                
                if res.status_code == 200:
                    bookings = res.json()
                    print_bookings_list(bookings, date_str, room_id)
                else:
                    print_response("GET", f"/rooms/{room_id}/bookings", res.status_code, res.json())
            except ValueError:
                print_error("Все параметры должны быть целыми числами!")
            except requests.exceptions.ConnectionError:
                print_error("Нет связи с сервером.")
            wait_for_enter()
                    
        elif choice == "8":
            try:
                print_header("Отмена бронирования")
                booking_id = int(get_user_input("  ID бронирования: "))
                
                confirm = input(f"  Отменить бронирование #{booking_id}? (y/N): ").strip().lower()
                if confirm != 'y':
                    print_info("Отмена отменена")
                    wait_for_enter()
                    continue
                
                res = requests.delete(f"{BASE_URL}/bookings/{booking_id}")
                
                if res.status_code == 200:
                    print_success(res.json().get("detail", f"Бронирование #{booking_id} отменено"))
                else:
                    print_response("DELETE", f"/bookings/{booking_id}", res.status_code, res.json())
            except ValueError:
                print_error("ID бронирования должен быть целым числом!")
            except requests.exceptions.ConnectionError:
                print_error("Нет связи с сервером.")
            wait_for_enter()
                
        elif choice == "9":
            print("\n" + "=" * 60)
            print("До свидания!")
            print("=" * 60 + "\n")
            break
            
        else:
            print_error("Неизвестная команда! Попробуйте снова.")
            wait_for_enter()

if __name__ == "__main__":
    main()