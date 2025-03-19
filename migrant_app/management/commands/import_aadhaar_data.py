import os
import pandas as pd
from django.core.management.base import BaseCommand
from migrant_app.models import AadhaarDatabase
from datetime import datetime

class Command(BaseCommand):
    help = "Import Aadhaar dataset from CSV file into AadhaarDatabase"

    def handle(self, *args, **kwargs):
        file_path = "migrant_workers_north_india.csv"  # Ensure the file exists in your project root

        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR("❌ File not found: " + file_path))
            return

        df = pd.read_csv(file_path)

        for index, row in df.iterrows():
            try:
                # ✅ Ensure the date is formatted as "DD/MM/YYYY"
                dob = datetime.strptime(row["Date of Birth"], "%d-%m-%Y").strftime("%d/%m/%Y")

                # Add data to AadhaarDatabase
                record, created = AadhaarDatabase.objects.get_or_create(
                    aadhaar_number=row["Aadhaar Number"],
                    defaults={
                        "full_name": row["Full Name"],
                        "date_of_birth": dob,  # ✅ Stored in "DD/MM/YYYY" format
                        "address": row["Address"],
                    }
                )

                if created:
                    self.stdout.write(self.style.SUCCESS(f"✅ Added: {record.full_name}"))
                else:
                    self.stdout.write(self.style.WARNING(f"⚠️ Skipped (Already Exists): {record.full_name}"))

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"❌ Error importing row {index}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS("🚀 Aadhaar Database Import Completed!"))
