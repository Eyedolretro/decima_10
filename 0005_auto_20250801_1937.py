from django.db import migrations

def set_default_chef_projet(apps, schema_editor):
    Projet = apps.get_model('issues', 'Projet')
    User = apps.get_model('auth', 'User')
    default_user = User.objects.first()  # Ici tu peux choisir un utilisateur spécifique

    for projet in Projet.objects.filter(chef_projet__isnull=True):
        projet.chef_projet = default_user
        projet.save()

class Migration(migrations.Migration):

    dependencies = [
        ('issues', 'dernier_numero_de_migration'),  # Mets ici la dernière migration appliquée
    ]

    operations = [
        migrations.RunPython(set_default_chef_projet),
    ]
