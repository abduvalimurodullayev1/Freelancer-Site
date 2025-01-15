from django.core.management.base import BaseCommand
from apps.users.models import Language  # Language modelingizni import qiling
import pycountry

class Command(BaseCommand):
    help = "Create all languages in the database using pycountry"

    def handle(self, *args, **options):
        languages = pycountry.languages
        created_count = 0
        skipped_count = 0

        for lang in languages:
            try:
                if hasattr(lang, 'name'):
                    language_name = lang.name
                    if not Language.objects.filter(name=language_name).exists():
                        Language.objects.create(name=language_name)
                        created_count += 1
                    else:
                        skipped_count += 1
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error adding language: {lang.name if hasattr(lang, 'name') else 'Unknown'}. {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"{created_count} languages successfully added."))
        self.stdout.write(self.style.WARNING(f"{skipped_count} languages were skipped (already exist)."))
