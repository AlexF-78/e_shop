from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Очистка базы и заполнение тестовыми данными из фикстур'

    def handle(self, *args, **options):
        self.stdout.write('Очистка базы данных...')
        call_command('flush', '--no-input')

        self.stdout.write('Загрузка тестовых данных из фикстур...')
        call_command('loaddata', 'catalog/fixtures/category_fixture.json')
        call_command('loaddata', 'catalog/fixtures/product_fixture.json')

        self.stdout.write(self.style.SUCCESS('База успешно очищена и заполнена тестовыми данными!'))
