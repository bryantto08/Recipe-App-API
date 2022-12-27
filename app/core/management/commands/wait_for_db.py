"""
Django Command to wait for the DB to be available
"""
import time
from django.core.management.base import BaseCommand
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError

class Command(BaseCommand):
    # Django command to wait for DB

    def handle(self, *args, **options):
        self.stdout.write("Waiting for database...")
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except(Psycopg2Error, OperationalError):
                self.stdout.write("Database unavailable waiting a few secs")
                time.sleep(2)

        self.stdout.write(self.style.SUCCESS("Database Available!"))
