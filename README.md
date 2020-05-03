# VirusHack project

> PPnP Team
>
> [![](https://img.shields.io/badge/PM%26BA-Pavel%20Krylov-lightgrey)](https://vk.com/pkryloff 'VK profile')
> [![](https://img.shields.io/badge/UX%2FUI-Leonid%20Kravtsov-green)](https://vk.com/kravtsovjr 'VK profile')
> [![](https://img.shields.io/badge/backend-Stepan%20Denisov-lightblue)](https://vk.com/sd.denisoff 'VK profile')
> [![](https://img.shields.io/badge/frontend-Matvey%20Kottsov-orange)](https://vk.com/kottsovcom 'VK profile')
> [![](https://img.shields.io/badge/DS%26ML-Denis%20Kozlov-blue)](https://vk.com/dkozl 'VK profile')

## Стек технологий

- python3
- Flask + addons
- Peewee ORM
- VK API
- MVC pattern


## Инструкция по запуску

1. Склонируйте репозиторий и перейдите в директорию с проектом
   
   Через SSH:
    ```
    git clone git@github.com:PPnP/VirusHack.git && cd VirusHack
    ```
   
   Через HTTPS:
    ```
    git clone https://github.com/PPnP/VirusHack.git && cd VirusHack
    ```
    
2. Создайте и активируйте виртуальное окружение
    ```
    virtualenv --python=python3 venv
    source venv/bin/activate
    ```

3. Установите зависимости
    ```
    pip3 install -r requirements.txt
    ```

4. Создайте таблицы в БД
    ```
    python3 manage.py migrate
    ```

5. Запустите веб-приложение
    ```
    python3 manage.py runserver
    ```

Developed by [PPnP team](https://ppnp.me 'team website')
