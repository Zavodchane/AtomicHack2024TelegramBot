# Телеграмм бот для хакатона Атомик Хак 2.0
## Возможности бота
- [x] <b>Определение дефектов сварных швов</b>
- [x] <b>Отправление дефектов на картике и создание csv файла с точным указанием места</b>
- [x] <b>Сбор статистики по запросам</b>
- [x] <b>Выдача статистики пользователю</b>

## Пример работы системы
![image](https://github.com/Zavodchane/AtomicHack2024TelegramBot/assets/73135012/1e64b66a-f9a0-4650-8162-ca706ab19c00)
![image](https://github.com/Zavodchane/AtomicHack2024TelegramBot/assets/73135012/05f2f444-4ccc-4dc5-b16a-399d09db2251)
![image](https://github.com/Zavodchane/AtomicHack2024TelegramBot/assets/73135012/0f34bdae-3d68-402a-99cc-385419feae06)

## ER-модель
![image](https://github.com/Zavodchane/AtomicHack2024TelegramBot/assets/73135012/a6bdd13d-30b4-4355-9c96-d55c953744e2)

## Запуск бота
1. Склонируйте репозиторий:

```shell
git clone https://github.com/Zavodchane/AtomicHack2024TelegramBot
```

2. Перейдите в него:

```shell
cd AtomicHack2024TelegramBot
```

3. Заполните пустые поля в .prod.env


4. Установите зависимости:

```shell
pip install -r requirements.txt
```

5. Запустите:

```shell
python3 src/main.py
```
