from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = 'Создает группу "Модератор продуктов" с необходимыми разрешениями'

    def handle(self, *args, **options):
        # Создаем или получаем группу
        moderators_group, created = Group.objects.get_or_create(name='Модератор продуктов')

        if created:
            self.stdout.write(
                self.style.SUCCESS('Создана группа "Модератор продуктов"')
            )
        else:
            self.stdout.write(
                self.style.WARNING('Группа "Модератор продуктов" уже существует')
            )

        # Необходимые разрешения
        permissions_codenames = [
            'can_unpublish_product',
            'can_delete_any_product',
            'delete_product',
        ]

        added_permissions = 0

        # Добавляем разрешения в группу
        for codename in permissions_codenames:
            try:
                permission = Permission.objects.get(codename=codename)
                moderators_group.permissions.add(permission)
                added_permissions += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Добавлено разрешение: {codename}')
                )
            except Permission.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'✗ Разрешение {codename} не найдено')
                )

        self.stdout.write(
            self.style.SUCCESS(
                f'Группа "Модератор продуктов" готова. Добавлено разрешений: {added_permissions}'
            )
        )
