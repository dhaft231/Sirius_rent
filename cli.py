import requests
import json
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"

def print_log(method, endpoint, status_code, response_data):
    """Красивое терминальное логирование ответов сервера"""
    print("\n" + "="*50)
    print(f"📡 [LOG] ИСХОДЯЩИЙ ЗАПРОС: {method} {endpoint}")
    print(f"📥 [LOG] СТАТУС ОТВЕТА СЕРВЕРА: {status_code}")
    print("📦 [LOG] ТЕЛО ОТВЕТА:")
    print(json.dumps(response_data, indent=2, ensure_ascii=False))
    print("="*50 + "\n")

def menu():
    print("=== ТЕРМИНАЛ УПРАВЛЕНИЯ СИРИУС.АРЕНДА ===")
    print("1. Показать список всех комнат")
    print("2. Создать новую комнату")
    print("3. Удалить комнату по ID")
    print("4. Создать новое бронирование")
    print("5. Отменить бронирование по ID")
    print("6. Выйти")
    return input("\nВыбери команду (> ): ")

def main():
    while True:
        choice = menu()
        
        if choice == "1":
            res = requests.get(f"{BASE_URL}/rooms")
            print_log("GET", "/rooms", res.status_code, res.json())
            
        elif choice == "2":
            name = input("Введите название комнаты: ")
            capacity = int(input("Введите вместимость (чел): "))
            equip = input("Оборудование (через запятую): ").split(",")
            equip = [e.strip() for e in equip if e.strip()]
            
            data = {"name": name, "capacity": capacity, "equipment": equip}
            res = requests.post(f"{BASE_URL}/rooms", json=data)
            print_log("POST", "/rooms", res.status_code, res.json())
            
        elif choice == "3":
            room_id = input("Введите ID удаляемой комнаты: ")
            res = requests.delete(f"{BASE_URL}/rooms/{room_id}")
            print_log("DELETE", f"/rooms/{room_id}", res.status_code, res.json())
            
        elif choice == "4":
            try:
                room_id = int(input("Введите ID комнаты: ")) 
                user = input("Ваше имя: ")
                start_str = input("Начало (ГГГГ-ММ-ДД ЧЧ:ММ): ")
                end_str = input("Окончание (ГГГГ-ММ-ДД ЧЧ:ММ): ")
                
                start_dt = datetime.strptime(start_str, "%Y-%m-%d %H:%M").isoformat()
                end_dt = datetime.strptime(end_str, "%Y-%m-%d %H:%M").isoformat()
                
                data = {
                    "room_id": room_id,
                    "user_name": user,
                    "start_time": start_dt,
                    "end_time": end_dt
                }
                res = requests.post(f"{BASE_URL}/bookings", json=data)
                print_log("POST", "/bookings", res.status_code, res.json())
            except ValueError:
                print("\n❌ Ошибка: Неверный формат ввода данных или даты!\n")
                
        elif choice == "5":
            booking_id = input("Введите ID бронирования для отмены: ")
            res = requests.delete(f"{BASE_URL}/bookings/{booking_id}")
            print_log("DELETE", f"/bookings/{booking_id}", res.status_code, res.json())
            
        elif choice == "6":
            print("Выключение терминала управления...")
            break
        else:
            print("\nНеизвестная команда! Попробуйте снова.\n")

if __name__ == "__main__":
    main()