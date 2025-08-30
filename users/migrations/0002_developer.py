
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('company', models.CharField(blank=True, max_length=100)),
                ('website', models.URLField(blank=True)),
                ('description', models.TextField(blank=True, help_text='Brief description of how you plan to use the API')),
                ('api_key', models.CharField(editable=False, max_length=40, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('requests_per_hour', models.PositiveIntegerField(default=1000)),
                ('requests_per_day', models.PositiveIntegerField(default=10000)),
            ],
            options={
                'db_table': 'developers',
                'ordering': ['-created_at'],
            },
        ),
    ]