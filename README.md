# ORCP — Optical Recognition of Cars and Prices

![Image alt](https://github.com/Zetis659/ORCP/blob/main/ORCP.png)

**ORCP** - это проект, цель которого - автоматизировать процесс идентификации автомобилей и определения их стоимости с использованием технологии оптического распознавания.
Этот проект включает в себя: сбор данных, обучение моделей и развёртывание Telegram бота для предоставления пользователям информации о марке и модели автомобиля, а так же его стоимости на основе фотографий автомобиля.
**Суть:** Пользователь отправляет фото автомобиля в Telegram бот **ORCP**, а бот использует обученную нейросеть классификации и детекции, которая определяет какая это марка, модель и поколение, а так же указывает рыночную стоимость автомобиля с помощью загруженной базы с сайта "auto.ru".
### ORCP vs умная камера Алисы
Примеры, в которых **ORCP** справился лучше в классификации авто, чем умная камера Алисы.

<figure>
  <img src="https://github.com/Zetis659/ORCP/blob/main/hongqi_ORCP.png" width="600">
  <figcaption>Умная камера Алисы <b>НЕ верно определила</b> авто</figcaption>
</figure>

<figure>
  <figcaption>Умная камера Алисы <b>НЕ смогла определить</b> модель авто:</figcaption>
  <img src="https://github.com/Zetis659/ORCP/blob/main/lixiang_ORCP.png" width="650">
</figure>

<figure>
  <img src="https://github.com/Zetis659/ORCP/blob/main/kaiyi_ORCP.png" width="700">
  <figcaption>Умная камера Алисы НЕ смогла определить модель авто</figcaption>
</figure>



**Ссылки:**
- [Бот ORCP в Telegram](https://t.me/ORCPbot)
- [Веса моей модели классификации](https://drive.google.com/file/d/1E1mIXgHqpur8e2woJ86jKX7pHcCcFJic/view?usp=drive_link)
- [Веса модели классификации YOLOv8x](https://drive.google.com/file/d/1LpgIJ9-WWDXMlXnDWocDf65ep80nOB77/view?usp=drive_link)
- [Веса модели детекции YOLOv8x](https://drive.google.com/file/d/1S42IQZKm2Mnw6nsbGeST4Ao9LtwmlIYH/view?usp=drive_link)
- [База загруженных авто](https://drive.google.com/file/d/1s6hamNrSZACgzBNVL7jES3M25XLlGWFT/view?usp=drive_link)
- [Ссылки на фото китайских авто](https://drive.google.com/file/d/1-SriKOyJjJq_0TyK8bfAamKST8dGv6js/view?usp=sharing)
- [Загруженные фото китайских авто для модели](https://drive.google.com/file/d/1220iqpGq6Xhwf4KEH9yDBuEo5QxL2IH9/view?usp=sharing)
- [Отобранные фото китайских авто для модели](https://drive.google.com/file/d/1uqsQV7Pkog9XilNDuZtm96ZEkBMcwA-1/view?usp=sharing)


## Table of Contents
- [ORCP — Optical Recognition of Cars and Prices](#orcp--optical-recognition-of-cars-and-prices)
    - [ORCP vs умная камера Алисы](#orcp-vs-умная-камера-алисы)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Usage](#usage)
    - [Parsing](#parsing)
      - [Необходимые библиотеки:](#необходимые-библиотеки)
      - [Необходимое стороннее ПО:](#необходимое-стороннее-по)
    - [Model Training - YOLOv8](#model-training---yolov8)
      - [Необходимые библиотеки:](#необходимые-библиотеки-1)
      - [Мой PC билд:](#мой-pc-билд)
    - [Telegram bot](#telegram-bot)
      - [Необходимые библиотеки:](#необходимые-библиотеки-2)
  - [1. Data Collection](#1-data-collection)
      - [Структура парсинга данных:](#структура-парсинга-данных)
      - [Структура хранения данных:](#структура-хранения-данных)
    - [1.0 Preparing for parsing](#10-preparing-for-parsing)
    - [1.1 Parsing brands](#11-parsing-brands)
    - [1.2 Parsing models](#12-parsing-models)
    - [1.3 Parsing generations](#13-parsing-generations)
    - [1.4 Parsing ALL cars](#14-parsing-all-cars)
  - [2. Model Training - YOLOv8](#2-model-training---yolov8)
      - [Cтруктура работы с данными:](#cтруктура-работы-с-данными)
    - [2.1 Download photos](#21-download-photos)
    - [2.2 Select photos](#22-select-photos)
    - [2.3 Prepare photos](#23-prepare-photos)
    - [2.4 Model fit](#24-model-fit)
    - [2.5 Predict](#25-predict)
    - [2.6 Analysis](#26-analysis)
  - [3. Telegram Bot](#3-telegram-bot)
    - [3.1 Description of modules](#31-description-of-modules)
    - [3.2 Логика работы бота:](#32-логика-работы-бота)
    - [З.3 Launching the bot](#з3-launching-the-bot)
  - [License](#license)
## Project Overview
**ORCP** включает в себя три основных этапа разработки:

1. **Сбор данных**: Написание парсера, который сохраняет информацию об авто по различным параметрам: стоимость, объём двигателя, транспортный налог и т.д. Помимо этого парсер сохраняет ссылки на фотографии авто в текстовые файлы для дальнейшего обучения.
2. **Обучение модели**: Используя скачанные ссылки, загрузка фотографий автомобилей, отбор подходящих фотографий для обучения, разделение на обучающую и тестовую выборки и обучение на этих данных модели.
3. **Telegram bot**: Реализация Telegram бота, позволяющего взаимодействовать с пользователями. Пользователи могут отправлять фотографии боту, который используя обученные модели, будет предоставлять информацию о марке, модели, годах выпуска и стоимости авто.

## Usage
Использовать репозиторий **ORCP** можно по разному, по этому напишу отдельно про каждый этап. Как уже было указано выше, данный проект разделён на 3 раздела. У каждого раздела, есть своя папка, которая находится в **SRC**, а именно **Parsing**, **YOLOv8** и **Bot**. Основные детали при их использовании будут указаны ниже.
### Parsing
В папке Parsing, есть несколько модулей, с помощью которых можно загружать информацию об автомобилях с сайта "auto.ru". Здесь будут указаны необходимые библиотеки, которые нужны для запуска парсера, а так же дополнительное ПО. 

Для более подробного описания, а так же просмотра логики парсинга, откройте пункт [Data Collection](#1-data-collection)

**Парсер будет корректно работать, только при выполнении всех условий ↓ УКАЗАННЫХ НИЖЕ ↓**
#### Необходимые библиотеки:
> **fake_useragent** - замена агента браузера, при парсинге
> 
> **user_agents** - фильтрация мобильных агентов
> 
> **requests** - запросы на сайт
> 
> **tqdm** - подсчёт оставшегося времени, при парсинге
> 
> **random** - генерация случайных чисел, при смене IP
> 
> **genericpath** - проверка существования папки
> 
> **sys** - импорт модулей из разных папок
>
> **os** - указание пути для файлов
>
> **time** - подсчёт затраченного времени
>
> **csv** - сохранение *csv* файлов

#### Необходимое стороннее ПО:
Для постоянного изменения IP во избежании появления *капчи* использовался: ~~Tor~~ "луковый" браузер. **Без данного ПО, код работать НЕ будет!**

Для того, чтобы контролируемо менять IP адрес нужно:
1. Установить "луковый" браузер
2. В папке "лукового" браузера найти конфигурационный файл *torrc*
3. В данном файле прописать дополнительные порты. Я добавил 100 портов, начиная с "SocksPort 9050" и заканчивая "SocksPort 9149". Каждый порт должен идти с новой строчки. Сохранить *torrc*.
4. Перед парсингом нужно: запустить и подключиться к сети "луковым" браузером. Браузер должен быть подключен к сети одним из мостов (obfs4).

**Парсер будет корректно работать, только при выполнении всех условий ↑ УКАЗАННЫХ ВЫШЕ ↑**
___
### Model Training - YOLOv8
В качестве основы, для классификации и детекции автомобилей, мне послужила модель нейросети **YOLOv8**.

Для более подробного описания загрузки данных, а так же обучения модели, откройте пункт [Model Training - YOLOv8](#2-model-training---yolov8)
#### Необходимые библиотеки:
> **torch == 2.0.1** - фреймворк для работы с нейросетями
>
> **nvidia-cuda == 11.7** - для использования видеокарт nvidia при обучении
>
> **ultralytics** - для импорта модели YOLO
>
> **requests** - для запросов на сайт
>
> **os** - указание пути файлов
>
> **shutil** - создание копий исходных файлов
>
> **time** - подсчёт затраченного времени
>
> **random** - генерация случайных числе, при выборе train/test
#### Мой PC билд:
- OS: **Manjaro Linux 23.0.3 Uranos, GNOME 44.5, Core 6.1.55-1-MANJARO**
- GPU: **Nvidia RTX 2070 8Gb**
- Nvidia driver: **470.199.02**, CUDA 11.4 (Pre-installed)
- CUDA: **11.8** (Installed after Nvidia driver)
- CUDNN: **8.6** (Installed after CUDA)
- Python: **3.10.12**

___
### Telegram bot
Для использования Telegram бота, основным инструментом была библиотека aoigram 3.0 и библиотека asyncio - для выполнения асинхронных задач.

Для более подробного описания реализации Telegram бота, откройте пункт [Telegram Bot](#3-telegram-bot)
#### Необходимые библиотеки:
> **torch == 2.0.1** - фреймворк для работы с нейросетями
>
> **nvidia-cuda == 11.7** - для использования видеокарт nvidia при обучении
>
> **ultralytics** - для импорта модели YOLO
>
> **aiogram == 3.00** - для использования Telegram API
>
> **asyncio** - для асинхронных функций бота (приём сообщений, фото и т.д.)
>
> **pandas** - для работы с *csv* файлами
>
> **sys** - импорт модулей из разных папок
>
> **os** - указание пути для файлов
>
> **time** - подсчёт затраченного времени
>
> **datetime** - сохранение фото в формате Y-m-d_H-M-S
> ___

## 1. Data Collection
**В данном разделе находится подробное описание парсинга различных автомобильных параметров, таких как: тип кузова, объём двигателя, стоимость и т.д. А так же парсинга ссылок на фотографии, с помощью которых возможно дальнейшее обучение модели классификации.**

Для сбора данных мной был выбран сайт "auto.ru", так как это один из самых популярных сайтов для продажи авто. На момент парсинга (август 2023) на данной площадке было ≈370 000 объявлений о продаже авто, а на момент написания README (октябрь 2023) ≈410 000 объявлений.

Для использования парсера, нужно выполнить все пункты в разделе [Usage → Parsing](#parsing), а именно: установку "лукового" браузера, открытие портов и т.д. Перед парсингом необходимо запустить "луковый" браузер и подключиться, через него к сети используя мосты. 

Для удобства использования, все модули и данные имеющие отношение к парсингу расположены в: SRC/Parsing. А все модули python для парсинга находятся в папке: SRC/Parsing/Proxy, так как для парсинга используется proxy. Кроме того в данном разделе, модули специально названы в алфавитном порядке, для удобного последовательного запуска. Рекомендуемый порядок запуска: a1.., a2.., b1.., c1.. и т.д.
#### Структура парсинга данных:
**Бренд → Модель → Поколение → Страница → Объявление → Данные**

#### Структура хранения данных:
В файле brands.txt - список всех брендов:

**Бренды** → **SRC/Parsing/Results/Cars/Brands/brands.txt**

У каждого бренда свой файл с моделями, в данном файле все модели конкретного бренда:

**Модели** → ORCP/SRC/Parsing/Results/Cars/Models/**БРЕНД.txt**, примеры:

Модели бренда **Toyota**: SRC/Parsing/Results/Cars/Models/**TOYOTA**.txt,
Модели бренда **Haval**: SRC/Parsing/Results/Cars/Models/**HAVAL**.txt - и т.д. 

У каждой модели свой файл с названиями поколений, в данном файле все поколения конкретной модели:

**Названия поколений** → SRC/Parsing/Results/Cars/**Generations_names**/**БРЕНД_МОДЕЛЬ.txt**, примеры:

Поколения модели Audi A4: SRC/Parsing/Results/Cars/Generations_names/**AUDI_A4.txt**
Поколения модели Geely Coolray: SRC/Parsing/Results/Cars/Generations_names/**GEELY_COOLRAY.txt**

У каждой модели свой файл с кодами поколениями (для базы), в данном файле все поколения конкретной модели:

**Коды поколений** → SRC/Parsing/Results/Cars/**Generations**/**БРЕНД_МОДЕЛЬ.txt**, примеры:

Поколения модели Audi A4: SRC/Parsing/Results/Cars/Generations/**AUDI_A4.txt**
Поколения модели Geely Coolray: SRC/Parsing/Results/Cars/Generations/**GEELY_COOLRAY.txt**

Папка для хранения бэкапов:

**BackUps** → **SRC/Parsing/Results/Cars/BackUps**

Папка для быстрого продолжения парсинга, при возникновении ошибок:

**Parsing_failure** - **SRC/Parsing/Results/Cars/Parsing_failure**

Более подробное описание будет ↓ ниже ↓
### 1.0 Preparing for parsing
После того, как все условия использования были выполнены, можно проверить корректно ли работают порты. Для этого вы можете запустить файл: Helper/tor_ip.py и если при каждом новом запуске ваш IP изменяется, то всё было настроено верно.

Если всё работает, то можно приступить к подготовке к парсингу. Начать следует с модуля *a1_preparation_to_parsing_PROXY.py*. В данном файле нужно:
1. Добавить модуль, в системный путь python (sys.path.append...) изменить на свой путь
2. Изменить переменную заголовка header, на актуальную. В противном случае *капча* будет постоянно прерывать парсинг. Для этого нужно:
   1. Открыть сайт "auto.ru", и перейти в раздел объявления
   2. Выбрать любую марку и модель авто, затем нажать на кнопку показать *n* предложений
   3. Открыть инструменты разработчика (обычно f12), затем выбрать пункт сеть
   4. Прокрутить страницу вниз и нажать на кнопку любой следующей страницы в поиске (например 2)
   5. После загрузки страницы в инструментах разработчика для удобства отфильтровать данные по убыванию размера и нажать на файл .json с названием "listing"
   6. Выбрать пункт заголовки и в нём найти подпункт: заголовки запроса
   7. Нажать на кнопку необработанные заголовки при наличии и скопировать все заголовки
   8. Вставить заголовки в переменную header 
   9. Удалить одну или несколько первых строк, так, чтобы первая строка была: "Host: auto.ru"

Запустите данный python модуль и если вы видите в терминале, вывод .json файла и далее надпись: "The header is set correctly!!!" - значит вы выполнили всё верно.

### 1.1 Parsing brands
После того, как подготовка была успешно завершена, можно приступить к парсингу. Для этого нужно запустить модуль: a2_parsing_brands_PROXY.py, который будет парсить 99 страниц сайта - это максимальное количество отображаемых страниц. На каждой странице расположены несколько объявлений, чаще всего их 37. При нахождении бренда, который ещё не был записан, он записывается в отдельный файл.

**Логика:**

**Первый цикл** бежит по 99 страницам, отсортированных по дате размещения, **второй цикл** бежит по объявлениям авто на каждой странице ~37 объявлений с авто, и **если  бренда ещё не было в списке, то добавить бренд в список и сохранить в список**. Файл называется brands.txt, находится в папке: SRC/Parsing/Results/Cars/Brands/brands.txt

**Рекомендую** сразу дублировать загруженные данные в папку:
SRC/Parsing/Results/Cars/BackUps, так как это будет удобно использовать в повторных парсингах при ошибках.

При необходимости можно изменить сортировку авто, для этого нужно изменить значение ключа "sort" в переменной params. Примеры сортировок: cr_date-desc - по дате размещения, autoru_exclusive-desc - по уникальности, fresh_relevance_1-desc - по актуальности
### 1.2 Parsing models
После того, как бренды были загружены в файл brands.txt, можно парсить сайт по моделям. Для этого нужно запустить модуль: *b1_parsing_models_PROXY.py*

**Логика:**

**Первый цикл** бежит по списку с брендами, который уже был загружен, **второй цикл** бежит по списку доступных страниц для данного бренда, **третий цикл** по объявлениям ~ 37 на странице. **Если модели ещё не было, то сохранить в файл с названием бренда.** Сортирую авто **по уникальности.**

Примеры: SRC/Parsing/Results/Cars/Models/GEELY.txt,
SRC/Parsing/Results/Cars/Models/HAVAL.txt

Во время парсинга моделей сохраняется файл, в котором будет указано, какие бренды и модели уже были загружены. Он расположен в: SRC/Parsing/Results/Cars/Parsing_failure/Models_fail.txt. При возникновении ошибки можно воспользоваться данным файлом,и удалить из файла brands.txt уже загруженные бренды, чтобы повторно не парсить одно и тоже. Не забывайте делать backup файлов перед его редактированием (дублирование в папку BackUps), потому что в дальнейшем, они понадобятся в исходном виде!

### 1.3 Parsing generations
После того, как были загружены бренды и модели, можно парсить сайт по поколениям данных автомобилей. Для этого нужно запустить модуль: *c1_parsing_generations_PROXY.py*

**Логика:**

**Первый цикл** бежит по списку с брендами, **второй цикл** по списку моделей, **третий** по страницам модели, **четвёртый** по объявлениям на каждой странице. **Если поколения ещё не было, то сохранить в файл с названием бренда и модели**. В папку **Generations** сохраняются **закодированные названия поколений**. Пример: SRC/Parsing/Results/Cars/Generations/HAVAL_F7.txt  **(21569049, 23206512)**. В папку **Generations_names** сохраняются **названия поколений**. Пример: SRC/Parsing/Results/Cars/Generations_names/HAVAL_F7.txt **(I,
I Рестайлинг)**

Во время парсинга поколений сохраняется файл, в котором будет указано, какие бренды модели и поколения уже были загружены. Он расположен в: SRC/Parsing/Results/Cars/Parsing_failure/Generations_fail.txt. При возникновении ошибки можно воспользоваться данным файлом,и удалить из файла brands.txt уже загруженные бренды, и модели из файла с моделями, чтобы повторно не парсить одно и тоже. Не забывайте делать backup файлов перед его редактированием (дублирование в папку BackUps), потому что в дальнейшем, они понадобятся в исходном виде!
### 1.4 Parsing ALL cars
После того, как были загружены бренды, модели и поколения можно приступить к парсингу всех автомобилей. Парсинг включает в себя 39 различных параметров, таких как: стоимость, объём двигателя, транспортный налог, тип кузова, разгон до сотни и многие другие. По мимо парсинга параметров авто, одновременно с ним происходит парсинг фотографий авто, а именно ссылок на фотографии. Ссылки на фото сохраняются в разных файлах с тремя разными разрешениями фотографий, а именно: 320x240, 456x342, 1200x900. Для парсинга нужно запустить модуль: *d1_parsing_all_cars_PROXY.py*

Если вы корректировали файлы с брендами, моделями и поколениями, при ошибках в парсинге, то нужно заменить эти файлы, на оригинальные исходные файлы из папки **BackUps**

**Логика:**

**Первый цикл** бежит по списку с брендами, **второй** с моделями, **третий** с поколениями, **четвёртый** со страницами и **пятый** с объявлениями на каждой странице.
Каждый автомобиль соответствует одной строке в *csv* файле. Данные сохраняются в файл: SRC/Parsing/Results/Data/all_cars.csv

Ссылки на фото сохраняются в папке: **SRC/Parsing/Results/Photo_links**

Структура файла с ссылками: **БРЕНД_МОДЕЛЬ_ПОКОЛЕНИЕ_ГОД ВЫПУСКА-ГОД ОКОНЧАНИЯ-РАЗРЕШЕНИЕ ФОТО.txt**

Например ссылки на Haval F7 I поколения в разрешении 320x240 сохраняются в файл: **SRC/Parsing/Results/Photo_links/HAVAL/F7/HAVAL_F7_I_2018-2022-320x240.txt**

На всякий случай я оставил в проекте модуль *d2_parsing_all_cars.py*. В нём дублирован модуль d1 с загрузкой всех авто, но без использования "лукового" браузера и прокси. Скорее всего данный модуль будет бесполезен, так как на октябрь 23 года, сайт "auto.ru" очень быстро блокирует (отправляет капчу) при парсинге с одного IP.

- [Ссылки на фото китайских авто](https://drive.google.com/file/d/1-SriKOyJjJq_0TyK8bfAamKST8dGv6js/view?usp=sharing)
- [База загруженных авто](https://drive.google.com/file/d/1s6hamNrSZACgzBNVL7jES3M25XLlGWFT/view?usp=drive_link)
## 2. Model Training - YOLOv8
**В данном разделе находится подробное описание загрузки фотографий из списка уже загруженных ссылок, селекция фото, анализ стоимости авто с созданием баз со средней стоимостью авто, а так же обучение нейронной сети, с помощью модели YOLOv8**.

Для удобства использования, все модули и данные имеющие отношение к загрузке фото и обучение модели YOLOv8 расположены в: SRC/YOLOv8, исключая папку *Analysis*. Кроме того в данном разделе, модули специально названы в алфавитном порядке, для удобного последовательного запуска. Рекомендуемый порядок запуска: a1.., a2.., b1.., c1.. и т.д.


#### Cтруктура работы с данными:
**Парсинг** → **Загрузка фото** → **Отбор фото** → **Обучение модели на фото**

### 2.1 Download photos
Для загрузки фотографий нужно воспользоваться модулем: *a1_download_one_brand.py*
Для этого вам нужно указать в нём 3 параметра:
1. Максимальное количество картинок для 1 модели авто - *pictures_quantity*
2. Размер картинки - *picture_size*
3. Бренд авто (название папки) - *car_brand*
После того, как вы указали значения, во всех переменных, запустите модуль. Все фотографии будут загружены в папку: Downloads/CAR_BRAND/MODEL/БРЕНД_МОДЕЛЬ_ПОКОЛЕНИЕ_ГОД ВЫПУСКА-ГОД ОКОНЧАНИЯ-РАЗРЕШЕНИЕ ФОТО"**
Если в текстовом файле с ссылками было менее 500 ссылок, то модуль скачает все доступные фото.

Пример пути сохранённой фото: Downloads/GEELY/COOLRAY/GEELY_COOLRAY_I_2019--456x342n/7.jpg

В своей модели я использовал "средний" вариант фото с разрешением 456x342. Для улучшения качества модели можно попробовать, работать с более высоким разрешением, но в таком случае на обучении модели потребуется гораздо больше времени, по этому рекомендую выбирать разрешение фото, в зависимости от производительности вашей системы.
- [Загруженные фото китайских авто для модели](https://drive.google.com/file/d/1220iqpGq6Xhwf4KEH9yDBuEo5QxL2IH9/view?usp=sharing)
### 2.2 Select photos
Для того чтобы отобрать фотографии рекомендую сразу дублировать загруженные фотографии в папку: SRC/YOLOv8/Selected_photos

В данном случае для относительно качественного отбора, я вручную отбирал нужные фото, а ненужные удалял из папки Selected_photos

**Критерии отбора:**
1. Только **экстерьер** (все фото салона, руля и тд - удалить)
2. Не должно быть открытых элементов авто. (открытые двери, капот, багажник - удалить)
3. Автомобиль должен **полностью** попадать в кадр (не должна быть обрезана часть автомобиля)
4. Фотография не должна быть перевёрнута на 90/180 градусов, а так же сильно наклонена как по горизонтали, так и по вертикали.
5. Фото должно быть сделано в светлое время суток, либо же при хорошем искусственном освещении (тёмные фото - удалить)
6. В кадре должно быть минимальное количество посторонних предметов, а так же других авто (по возможности)
7. Фотография должна быть хорошего качества (очень мыльные или зернистые фото - удалить)
8. Узкие вертикальные фото - не подходят, (разрешение +- 130x320 - удалить)

- [Отобранные фото китайских авто для модели](https://drive.google.com/file/d/1uqsQV7Pkog9XilNDuZtm96ZEkBMcwA-1/view?usp=sharing)
### 2.3 Prepare photos
После того, как все фотографии были отобраны, их нужно подготовить для модели YOLOv8, для этого нужно воспользоваться модулем *b1_divide_photo.py*. При запуске данного модуля все фото из папки: SRC/YOLOv8/Selected_photos будут копированы папку SRC/YOLOv8/Prepared_photos и там разделены по папкам train  и test с соотношением 70/30. Помимо этого будет немного изменена структура пути к фото, а именно удалены папки бренда и модели из пути, например:
Было в Selected_photos - SRC/YOLOv8/Selected_photos/HAVAL/F7/HAVAL_F7_I_2018-2022-456x342n/1.jpg ... 500.jpg - 
Стало в Prepared_photos/train - SRC/YOLOv8/Prepared_photos/train/HAVAL_F7_I_2018-2022-456x342n/1.jpg ... 350.jpg
Стало в Prepared_photos/test - SRC/YOLOv8/Prepared_photos/test/HAVAL_F7_I_2018-2022-456x342n/351.jpg ... 500.jpg

### 2.4 Model fit
Для обучения, потребуется скачать с [официального сайта](https://docs.ultralytics.com/models/yolov8/#supported-tasks), модель yolov8 для [классификации](https://drive.google.com/file/d/1LpgIJ9-WWDXMlXnDWocDf65ep80nOB77/view?usp=drive_link), а так же модель для [детекции](https://drive.google.com/file/d/18XcWiMNFVNzdOjUFOv8CkkYKA16to93-/view?usp=drive_link), она понадобится позже. На сайте есть разные варианты моделей от n - нано, самая маленькая модель, до x - extra. Я использовал YOLOv8x.
После загрузки модели, помещаю их в Models/Classification/yolov8x-cls.pt - для классификации, и Models/Detection/yolov8x.pt - для детекции. Две модели нужны для того, чтобы сначала распознать (понять), есть ли на изображении авто, а уже после производить его классификацию.

После того, как модели были загружены и размещены в указанные выше директории, нужно воспользоваться модулем *c1_fit_model.py*.

В данном модуле можно изменить размер изображений, для обучения - *imgsz* и количество эпох обучения - *epochs*

В лучшей модели я использовал *imgsz* = 320, *epochs* = 80, хотя если смотреть по цифрам, то после 30 эпохи показатели модели, практически не улучшаются, но по субъективным ощущениям модель с 80 эпохами работает лучше, чем с 30.

После запуска модуля и обучения модели, будет создана папка с результатами обучения: runs/classify/train. Наилучшие веса модели будут в: runs/classify/train/weights/best.pt

После обучения рекомендую переименовать и перенести лучшую модель в папку: Models/Classification

### 2.5 Predict
С помощью модуля: SRC/YOLOv8/d1_predict_car.py можно классифицировать авто на локальной машине.

С помощью модуля: SRC/YOLOv8/d2_detect_car.py можно произвести детекцию авто на локальной машине.

### 2.6 Analysis
Для того, чтобы подгружать среднюю стоимость авто, нужно воспользоваться модулем: Analysis/Prices/*cost_collection.py*
При запуске данный модуль загружает собранные данные о всех машинах из файла: SRC/Parsing/Results/Data/*all_cars.csv* и создаёт 6 различных файлов со стоимостью авто, в зависимости от его статуса:
1. **BM.csv** (Brands Models) - все модели. Используется, так как не у всех авто указано поколение
2. **BMG.csv** (Brands Models Gens) - все модели со всеми указанными поколениями
3. **NBM.csv** (New Brands Models) - только новые модели
4. **NBMG.csv** (New Brands Models Gens) - только новые модели с указанными поколениями
5. **UBM.csv** (Used Brands Models) - только подержанные модели
6. **UBMG.csv** (Used Brands Models Gens) - только подержанные авто с указанными поколениями

В файле Analysis/PDA.ipynb краткий первичный анализ полученных данных.
## 3. Telegram Bot
**В данном разделе находится структура бота, а так же описание его модулей. Данный бот работает с помощью библиотеки aiogram 3.0, а так же библиотеки асинхронных функция asyncio**

Для удобства использования, все модули и данные имеющие отношение к настройке и запуску бота расположены в: SRC/Bot, исключая папку *Analysis*.

### 3.1 Description of modules
- **main.py** - основной связующий файл для запуска и работы бота.
- **handlers.py** - обработчики всех кнопок, а так же сообщений в боте в том числе и фотографий.
- **detection.py** -  Детектирование авто на фотографии.
- **predictions.py** - При наличии авто на фото: определение бренда и модели авто, а так же загрузка данных о стоимости из базы.
- **keybords.py** - кнопки, реплай, а так же инлайн клавиатуры.
- **settings.py** - API ключ для телеграм бота.

**Структура бота:**

**main.py** → **settings.py** - импорт API ключа.

**main.py** → **handlers.py** → **settings.py** - импорт API ключа.

**main.py** → **handlers.py** → **keyboards.py** - импорт клавиатур.

**main.py** → **handlers.py** → **detection.py** - возврат результатов модели детекции.

**main.py** → **handlers.py** → **predictions.py** - возврат результатов модели классификации.

### 3.2 Логика работы бота:
1. Постоянная обработка сообщений от пользователя, как текстовых, так и нажатий на клавиатуры, а так же обработка фото
2. При отправке пользователем фотографии, сначала она обрабатывается модулем *detection.py*, для того чтобы обнаружить или не обнаружить авто на фото.
3. Если модель обнаружила авто на фото, то нужно отправить пользователю вероятности совпадения авто из модуля *predictions.py*, а так же данные о стоимости авто из одного из 6 *.csv* фалов, расположенных в папке: Analysis/Prices. Логика выбора прописана в файле *predictions.py* 

### З.3 Launching the bot
Для запуска бота потребуется:
1. Открыть телеграм и найти там [BotFather](https://t.me/BotFather) - бот для создания других ботов
2. Создать бота (выбрать имя, адрес и т.д)
3. Получить API ключ для бота
4. Вставить свой API ключ в файл SRC/Bot/core/*settings.py*
5. Запустить модуль *main.py*

## License
License
ORCP is licensed under the MIT License - see the LICENSE file for details.
