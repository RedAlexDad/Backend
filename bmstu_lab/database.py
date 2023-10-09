import psycopg2

class Database():
    # Подключение к БД
    def connect(self):
        try:
            # Подключение к базе данных
            self.connection = psycopg2.connect(
                # connect_timeout=1,
                host='localhost',
                port=5432,
                user='postgres',
                password='postgres',
                database='mars',
            )

            print("[INFO] Успешное подключение к базе данных")

        except Exception as ex:
            print("[INFO] Ошибка при работе с PostgreSQL:", ex)

    # Удаление БД
    def drop_table(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""
                    DROP TABLE geographical_object, transport, location, mars_station, employee, users CASCADE;
                """)

            # Подтверждение изменений
            self.connection.commit()
            print("[INFO] Успешно удалены таблицы в базе данных")

        except Exception as ex:
            print("[INFO] Ошибка при работе с PostgreSQL:", ex)

    # Создание таблицы БД и связанные таблицы
    def create_table(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute("""          
                    -- Географические объекты
                    CREATE TABLE geographical_object (
                        id SERIAL PRIMARY KEY,
                        feature VARCHAR NOT NULL,
                        type VARCHAR NOT NULL,
                        size INT NULL,
                        describe VARCHAR NULL,
                        url_photo VARCHAR NULL,
                        -- Доступен / недоступен
                        status BOOLEAN NOT NULL
                    );
                    
                    -- Транспортом могжет быть: посадочные, марсоходы, марсолеты и т.д.
                    CREATE TABLE transport (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR NOT NULL,
                        type VARCHAR NOT NULL,
                        describe VARCHAR NULL,
                        url_photo VARCHAR NULL
                    );
                    
                    -- Местоположение
                    CREATE TABLE location (
                        id SERIAL PRIMARY KEY,
                        id_geographical_object INT NOT NULL,
                        id_mars_station INT NOT NULL,
                        -- Порядковый номер
                        sequence_number INT NOT NULL
                    );
                    
                    -- Марсианская станция
                    CREATE TABLE mars_station (
                        id SERIAL PRIMARY KEY,
                        type_status VARCHAR NOT NULL,
                        data_create DATE NOT NULL,
                        data_from DATE NOT NULL,
                        data_close DATE NOT NULL,
                        id_employee INT NOT NULL,
                        id_transport INT NOT NULL,
                        -- СТАТУС (ДЛЯ ЗАЯВКИ)
                        -- status_task
                        -- 1: Введен: Заявка только что создана и ожидает обработки.
                        -- 2: В работе: Заявка была принята и находится в процессе выполнения.
                        -- 3: Завершена: Заявка успешно выполнена.
                        -- 4: Отменена: Заявка была отменена по каким-либо причинам.
                        -- 5: Удалена: Заявка была удалена из системы.
                        -- status_mission
                        -- 1: Успех
                        -- 2: Потеря
                        -- 3: Работает
                        status_task INT NOT NULL,
                        status_mission INT NOT NULL
                    );
                    
                    CREATE TABLE employee (
                        id SERIAL PRIMARY KEY,
                        full_name VARCHAR NOT NULL,
                        post VARCHAR NOT NULL,
                        name_organization VARCHAR NOT NULL,
                        address VARCHAR NULL,
                        id_user INT NOT NULL
                    );
                    
                    CREATE TABLE users (
                        id SERIAL PRIMARY KEY,
                        login VARCHAR NOT NULL,
                        password VARCHAR NOT NULL,
                        admin BOOLEAN NOT NULL
                    );
                                        
                                                        -- СВЯЗЫВАНИЕ БД ВНЕШНИМИ КЛЮЧАМИ --
                    ALTER TABLE location
                    ADD CONSTRAINT FR_location_of_geographical_object
                        FOREIGN KEY (id_geographical_object) REFERENCES geographical_object (id);
                    
                    ALTER TABLE location
                    ADD CONSTRAINT FR_location_of_mars_station
                        FOREIGN KEY (id_mars_station) REFERENCES mars_station (id);
                    
                    ALTER TABLE mars_station
                    ADD CONSTRAINT FR_mars_station_of_transport
                        FOREIGN KEY (id_transport) REFERENCES transport (id);
                    
                    ALTER TABLE mars_station
                    ADD CONSTRAINT FR_mars_station_of_scientist
                        FOREIGN KEY (id_employee) REFERENCES employee (id);
                    
                    ALTER TABLE employee
                    ADD CONSTRAINT FR_employee_organization_of_users
                        FOREIGN KEY (id_user) REFERENCES users (id);
            """)

            # Подтверждение изменений
            self.connection.commit()
            print("[INFO] Успешно созданы таблицы в базе данных")

        except Exception as ex:
            print("[INFO] Ошибка при работе с PostgreSQL:", ex)

    def insert_default_value(self):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """
                        -- ПОЛЬЗОВАТЕЛЬ (АУТЕНФИКАЦИЯ)
                        INSERT INTO users (login, password, admin) VALUES
                            ('user001', '123456', false),
                            ('user002', '123456', false),
                            ('user003', '123456', true),
                            ('user004', '123456', true);
                        
                        -- Начальник (ПРИНМАЮЩИЙ ЗАКАЗЧИКА) и Ученые (ЗАКАЗЧИК)
                        INSERT INTO employee (full_name, post, name_organization, address, id_user) VALUES
                            ('Джон Гротцингер', 'Профессор геологии, главный ученый миссии марсохода Curiosity', 'Калифорнийский технологический институт (Caltech)', '', 1),
                            ('Сергей Павлович Королев', 'Руководитель', 'Главное управление по ракетостроению и ракетным двигателям (ГУРРД)', '', 2),
                            ('Джеймс М. Бегс', 'Руководитель NASA', 'NASA', '', 3),
                            ('Георгий Тимофеевич Береговой', 'Начальник', 'Межпланетный отдел Центрального научно-исследовательского института машиностроения (ЦНИИмаш) имени академика М. В. Хруничева', '', 4);
                        
                        -- ГЕОГРАФИЧЕСКИЙ ОБЪЕКТ (УСЛУГА)
                        INSERT INTO geographical_object (feature, type, size, describe, url_photo, status) VALUES
                            ('Acidalia Planitia', 'Planitia, planitiae', 2300,
                             'обширная тёмная равнина на Марсе. Размер — около 3 тысяч км, координаты центра — 50° с. ш. 339°. Расположена между вулканическим регионом Тарсис и Землёй Аравия, к северо-востоку от долин Маринера. На севере переходит в Великую Северную равнину, на юге — в равнину Хриса; на восточном краю равнины находится регион Кидония. Диаметр около 3000 км.',
                             'http://themis.asu.edu/files/feature_thumbnails/002acidaliaTN1.jpg',
                             true),
                            ('Alba Patera', 'Patera, paterae', 530,
                             'Огромный низкий вулкан, расположенный в северной части региона Фарсида на планете Марс. Это самый большой по площади вулкан на Марсе: потоки извергнутой из него породы прослеживаются на расстоянии как минимум 1350 км от его пика.',
                             'https://upload.wikimedia.org/wikipedia/commons/thumb/2/22/Tharsis_-_Valles_Marineris_MOLA_shaded_colorized_zoom_32.jpg/1280px-Tharsis_-_Valles_Marineris_MOLA_shaded_colorized_zoom_32.jpg',
                             true),
                            ('Albor Tholus', 'Tholus, tholi', 170,
                             'Потухший вулкан нагорья Элизий, расположенный на Марсе. Находится к югу от соседних горы Элизий и купола Гекаты. Вулкан достигает 4,5 километров в высоту и 160 километров в диаметре основания.',
                             'https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Albor_Tholus_THEMIS.jpg/800px-Albor_Tholus_THEMIS.jpg',
                             true),
                            ('Amazonis Planitia', 'Planitia, planitiae', 2800,
                             'Слабоокрашенная равнина в северной экваториальной области Марса. Довольно молода, породы имеют возраст 10-100 млн. лет. Часть этих пород представляют собой застывшую вулканическую лаву.',
                             'https://upload.wikimedia.org/wikipedia/commons/3/31/26552sharpridges.jpg',
                             true),
                            ('Arabia Terra', 'Terra, terrae', 5100,
                             'Большая возвышенная область на севере Марса, которая лежит в основном в четырехугольнике Аравия, но небольшая часть находится в четырехугольнике Маре Ацидалиум. Она густо изрыта кратерами и сильно разрушена.',
                             'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Eden_Patera_THEMIS_day_IR.jpg/1189px-Eden_Patera_THEMIS_day_IR.jpg',
                             true);
                        
                        -- ТРАНСПОРТ (ДОП. ИНФА К УСЛУГЕ)
                        INSERT INTO transport (name, type, describe, url_photo) VALUES
                            ('Mars Pathfinder Rover (USA)', 'Rover', '', 'https://slideplayer.biz.tr/slide/5582070/17/images/5/Pathfinder+%28İzci%29+uzay+aracı.jpg'),
                            ('Viking 1 Lander (USA)', 'Spacecraft', '', 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Viking_spacecraft.jpg/1304px-Viking_spacecraft.jpg'),
                            ('Viking 2 Lander (USA)', 'Spacecraft', '', 'https://upload.wikimedia.org/wikipedia/commons/thumb/7/75/Viking_spacecraft.jpg/1304px-Viking_spacecraft.jpg'),
                            ('Mars 6 Lander (USSR)', 'Spacecraft', '', 'https://upload.wikimedia.org/wikipedia/commons/9/90/Mars_6.jpg'),
                            ('Mars 2 Lander (USSR)', 'Spacecraft', '', 'https://upload.wikimedia.org/wikipedia/commons/1/13/Mars3_iki.jpg');
                        
                        -- МАРСИАНСКАЯ СТАНЦИЯ (ЗАЯВКА)
                        -- Примечание:
                        -- Тип заявки (например, исследовательская, коммерческая и т. д.)
                        -- status_task
                        -- 1: Введен: Заявка только что создана и ожидает обработки.
                        -- 2: В работе: Заявка была принята и находится в процессе выполнения.
                        -- 3: Завершена: Заявка успешно выполнена.
                        -- 4: Отменена: Заявка была отменена по каким-либо причинам.
                        -- 5: Удалена: Заявка была удалена из системы.
                        -- status_mission
                        -- 1: Успех
                        -- 2: Потеря
                        -- 3: Работает
                        INSERT INTO mars_station (type_status, data_create, data_from, data_close, id_employee, id_transport, status_task, status_mission) VALUES
                            ('Исследовательская', '1972-09-01', '1973-11-04', '1975-05-08', 1, 1, 1, 3),
                            ('Коммерческая', '1975-05-08', '1976-11-07', '1977-11-01', 2, 2, 2, 3),
                            ('Коммерческая', '1982-07-15', '1983-07-11', '1984-01-06', 3, 3, 3, 2),
                            ('Исследовательская', '1968-06-17', '1969-04-09', '1970-03-03', 1, 4, 4, 3),
                            ('Исследовательская', '1988-03-18', '1989-05-05', '1990-05-07', 4, 5, 5, 1);
                        
                        -- МЕСТОПОЛОЖЕНИЕ (ВСПОМОГАТЕЛЬНАЯ ТАБЛИЦА ДЛЯ М-М УСЛУГА-ЗАЯВКА)
                        INSERT INTO location (id_geographical_object, id_mars_station, sequence_number) VALUES
                            (1, 1, 1),
                            (2, 2, 1),
                            (3, 3, 1),
                            (4, 4, 1),
                            (5, 5, 1);
                    """)

                # Подтверждение изменений
                self.connection.commit()
                print("[INFO] location, geografic_object: Данные успешно вставлены")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[INFO] location, geografic_object: Ошибка при заполнение данных:", ex)

    def close(self):
        # Закрытие соединения
        if self.connection:
            self.connection.close()
            print("Соединение с базой данных закрыто")

    def update_status_delete_geografical_object(self, status, id_geografical_object):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(
                    """UPDATE geographical_object SET status = %s WHERE id = %s;""",
                    (status, id_geografical_object)
                )

                # Подтверждение изменений
                self.connection.commit()
                print("[INFO] [Status] Данные успешно обновлено")
        except Exception as ex:
            # Откат транзакции в случае ошибки
            self.connection.rollback()
            print("[INFO] [Status] Ошибка при обновление данных:", ex)