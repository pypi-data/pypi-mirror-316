from g4f.client import Client

def r(req=None, model_id=1):
    # Словарь моделей
    model_dict = {
        1: "gpt-4",
        2: "gpt-4o-mini",
        3: "gpt-3.5-turbo",
        4: "gpt-4o",
        5: "llama-3.1-70b",
    }

    model = model_dict.get(model_id, "gpt-4")
    chat_history = []  # История сообщений

    print(f"Вы используете модель: {model}. Введите 'exit', чтобы выйти.\n")

    # Цикл общения
    while True:
        # Ввод сообщения пользователя
        user_input = input("Вы: ")
        if user_input.lower() == "exit":
            print("Чат завершён.")
            break

        # Добавляем сообщение пользователя в историю
        chat_history.append({"role": "user", "content": user_input})

        try:
            # Создаем клиент и отправляем запрос
            client = Client()
            response = client.chat.completions.create(
                model=model,
                messages=chat_history,
            )

            # Ответ модели
            reply = response.choices[0].message.content

            # Добавляем ответ модели в историю
            chat_history.append({"role": "assistant", "content": reply})

            # Выводим ответ
            print(f"Модель: {reply}")

        except Exception as e:
            print(f"Ошибка: {e}")
            break


def info():
    print("""
        1: "gpt-4",
        2: "gpt-4o-mini",
        3: "gpt-3.5-turbo",
        4: "gpt-4o",
        5: "llama-3.1-70b"
    """)

