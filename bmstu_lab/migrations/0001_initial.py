# Generated by Django 4.1 on 2023-09-19 09:37

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Employee",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("full_name", models.CharField(max_length=255)),
                ("post", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "employee",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="GeographicalObject",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("type", models.CharField(max_length=255)),
                ("feature", models.CharField(max_length=255)),
                ("size", models.IntegerField()),
                ("named_in", models.IntegerField()),
                ("named_for", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "geographical_object",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Location",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("landing_date", models.DateField()),
                ("location", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "location",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="PositionOfLocations",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("data_begin_movement", models.DateField()),
                ("data_end_movement", models.DateField()),
                ("purpose", models.CharField(max_length=255)),
                ("results", models.CharField(max_length=255)),
                ("distance_traveled", models.FloatField()),
            ],
            options={
                "db_table": "position_of_locations",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Status",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("status_task", models.CharField(max_length=255)),
                ("status_mission", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "status",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Transport",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=255)),
                ("type", models.CharField(max_length=255)),
                ("describe", models.CharField(blank=True, max_length=255, null=True)),
            ],
            options={
                "db_table": "transport",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Users",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("login", models.CharField(max_length=255)),
                ("password", models.CharField(max_length=255)),
                ("admin", models.BooleanField()),
            ],
            options={
                "db_table": "users",
                "managed": False,
            },
        ),
        migrations.CreateModel(
            name="Viewer",
            fields=[
                ("id", models.BigAutoField(primary_key=True, serialize=False)),
                ("full_name", models.CharField(max_length=255)),
            ],
            options={
                "db_table": "viewer",
                "managed": False,
            },
        ),
        migrations.RunSQL(
            """
                                        -- СВЯЗЫВАНИЕ БД ВНЕШНИМИ КЛЮЧАМИ --
                ALTER TABLE position_of_locations
                ADD CONSTRAINT FR_position_of_locations_of_geographical_object
                    FOREIGN KEY (id_geographical_object) REFERENCES geographical_object (id);

                ALTER TABLE position_of_locations
                ADD CONSTRAINT FR_position_of_locations_of_transport
                    FOREIGN KEY (id_transport) REFERENCES transport (id);

                ALTER TABLE position_of_locations
                ADD CONSTRAINT FR_position_of_locations_of_location
                    FOREIGN KEY (id_location) REFERENCES location (id);

                ALTER TABLE location
                ADD CONSTRAINT FR_location_of_status
                    FOREIGN KEY (id_status) REFERENCES status (id);

                ALTER TABLE location
                ADD CONSTRAINT FR_location_of_viewer
                    FOREIGN KEY (id_viewer) REFERENCES viewer (id);

                ALTER TABLE location
                ADD CONSTRAINT FR_location_of_employee
                    FOREIGN KEY (id_employee) REFERENCES employee (id);

                ALTER TABLE viewer
                ADD CONSTRAINT FR_viewer_of_users
                    FOREIGN KEY (id_user) REFERENCES users (id);

                ALTER TABLE employee
                ADD CONSTRAINT FR_employee_of_users
                    FOREIGN KEY (id_user) REFERENCES users (id);
             """),
    ]
