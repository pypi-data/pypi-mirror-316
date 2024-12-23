from g4f.client import Client


def r(req=None, model_id=1):
    if req is None:
        req = input("Введите запрос: ")

    # Словарь моделей
    model_dict = {
        1: "gpt-4",
        2: "gpt-4o-mini",
        3: "gpt-3.5-turbo",
        4: "gpt-4o",
        5: "llama-3.1-70b",
    }

    model = model_dict.get(model_id, "gpt-4")

    client = Client()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": req}],
    )
    print(response.choices[0].message.content)


def info():
    print("""
        1: "gpt-4",
        2: "gpt-4o-mini",
        3: "gpt-3.5-turbo",
        4: "gpt-4o",
        5: "llama-3.1-70b"
    """)


r()