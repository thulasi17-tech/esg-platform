import pandas as pd

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import DataSource, RawRecord
from companies.models import Company
from emissions.models import NormalizedEmissionRecord

from django.contrib.auth.models import User


EMISSION_FACTORS = {
    'diesel': 2.68,
    'petrol': 2.31,
    'electricity': 0.82,
    'flight': 0.15,
    'hotel': 0.08,
}


class CSVUploadView(APIView):

    def post(self, request):

        try:

            file = request.FILES.get('file')

            company_id = request.data.get('company_id')

            source_type = request.data.get('source_type')

            if not file:
                return Response(
                    {"error": "No file uploaded"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            company = Company.objects.get(id=company_id)

            data_source = DataSource.objects.create(
                company=company,
                source_type=source_type,
                uploaded_by=User.objects.first(),
                original_file=file
            )

            file.seek(0)

            df = pd.read_csv(file)

            # Replace NaN values safely
            df = df.fillna("")

            for _, row in df.iterrows():

                RawRecord.objects.create(
                    data_source=data_source,
                    raw_json=row.to_dict(),
                    ingestion_status='PROCESSED'
                )

                self.normalize_record(
                    row=row,
                    company=company,
                    data_source=data_source
                )

            return Response(
                {"message": "File uploaded successfully"},
                status=status.HTTP_201_CREATED
            )

        except Exception as e:

            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def normalize_record(self, row, company, data_source):

        category = str(
            row.get('category', '')
        ).strip().lower()

        quantity = row.get('quantity', 0)

        try:
            quantity = float(quantity)
        except:
            quantity = 0

        unit = str(
            row.get('unit', '')
        ).strip().lower()

        activity_date_raw = row.get('activity_date')

        try:
            activity_date = pd.to_datetime(
                activity_date_raw
            ).date()
        except:
            activity_date = None

        scope = str(
            row.get('scope', 'Scope 3')
        ).strip()

        emission_factor = EMISSION_FACTORS.get(
            category,
            0
        )

        co2e = quantity * emission_factor

        is_flagged = False

        flag_reason = ""

        if quantity < 0:
            is_flagged = True
            flag_reason = "Negative quantity detected"

        if quantity > 100000:
            is_flagged = True
            flag_reason = "Suspiciously high quantity"
        if unit == '':
           is_flagged = True
           flag_reason = "Missing unit"

        if category not in EMISSION_FACTORS:
           is_flagged = True
           flag_reason = "Unknown emission category"

        NormalizedEmissionRecord.objects.create(
            company=company,
            data_source=data_source,
            scope=scope,
            category=category,
            activity_date=activity_date,
            normalized_value=quantity,
            normalized_unit=unit,
            emission_factor=emission_factor,
            co2e=co2e,
            status='FLAGGED' if is_flagged else 'PENDING',
            is_flagged=is_flagged,
            flag_reason=flag_reason
        )