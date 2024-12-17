# Бронирование помещения

> Данное приложение - простой и прозрачный механизм, который позволяет бронировать помещения на определённый период времени.
> 
> Приложение работает посредством API.

#### *Google API в проекте*

*За счёт интеграции с Google API в проекте есть возможность формировать отчёт в гугл-таблицу с количеством бронирований каждой переговорки за указанный период.*



## Автор 
- Кобелев Андрей Андреевич  
    - [email](mailto:andrey.pydev@gmail.com)
  
## Технологии  
- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/index.html)
- [SQLAlchemy](https://docs.sqlalchemy.org/en/20/)
- [aiosqlite](https://aiosqlite.omnilib.dev/en/stable/index.html)
- [Uvicorn](https://www.uvicorn.org/)
- [Aiogoogle](https://aiogoogle.readthedocs.io/en/latest/#)

## Как запустить проект: 
  
Клонировать репозиторий и перейти в него в командной строке:  
  
```  
git clone https://github.com/andrey-kobelev/room_reservation.git
```  
  
```  
cd room_reservation
```  
  
Cоздать и активировать виртуальное окружение:  
  
```  
python3 -m venv env  
```  
  
```  
source env/bin/activate  
```  
  
Установить зависимости из файла requirements.txt:  
  
```  
python3 -m pip install --upgrade pip  
```  
  
```  
pip install -r requirements.txt  
```
### Настройка базы данных

Выполните все не применённые миграции:

```bash
alembic upgrade head
```

### Команда запуска приложения

В корневой директории проекта выполните команду запуска проекта

```
uvicorn app.main:app --reload
```


## Справка

После запуска сервера Uvicorn будет  доступна документация в двух форматах:
- [документация Swagger](http://127.0.0.1:8000/docs)
- [документация ReDoc](http://127.0.0.1:8000/redoc)



