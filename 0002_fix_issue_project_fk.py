from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('issues', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='project',
            field=models.ForeignKey(
                to='issues.Projet',
                on_delete=models.CASCADE,
                related_name='issues',
                null=True,
                blank=True,
            ),
        ),
    ]
