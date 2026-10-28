from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0001_initial'),
        ('doctors', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Mapping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('doctor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mappings', to='doctors.doctor')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='mappings', to='patients.patient')),
            ],
            options={
                'ordering': ['-assigned_at'],
            },
        ),
        migrations.AddConstraint(
            model_name='mapping',
            constraint=models.UniqueConstraint(fields=('patient', 'doctor'), name='one_doctor_per_patient'),
        ),
    ]
