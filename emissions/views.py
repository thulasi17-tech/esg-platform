from django.db.models import Sum
from django.db.models.functions import TruncMonth

from rest_framework.views import APIView
from rest_framework.response import Response

from .models import NormalizedEmissionRecord


class EmissionSummaryView(APIView):

    def get(self, request):

        records = NormalizedEmissionRecord.objects.all()

        total_emissions = records.aggregate(
            total=Sum('co2e')
        )['total'] or 0

        scope1 = records.filter(
            scope='Scope 1'
        ).aggregate(
            total=Sum('co2e')
        )['total'] or 0

        scope2 = records.filter(
            scope='Scope 2'
        ).aggregate(
            total=Sum('co2e')
        )['total'] or 0

        scope3 = records.filter(
            scope='Scope 3'
        ).aggregate(
            total=Sum('co2e')
        )['total'] or 0

        flagged_records = records.filter(
            status='FLAGGED'
        ).count()

        return Response({
            "total_emissions": total_emissions,
            "scope1": scope1,
            "scope2": scope2,
            "scope3": scope3,
            "flagged_records": flagged_records,
        })


class MonthlyEmissionTrendsView(APIView):

    def get(self, request):

        monthly_data = (
            NormalizedEmissionRecord.objects
            .annotate(month=TruncMonth('activity_date'))
            .values('month')
            .annotate(total_emissions=Sum('co2e'))
            .order_by('month')
        )

        return Response(list(monthly_data))


class TopEmissionCategoriesView(APIView):

    def get(self, request):

        categories = (
            NormalizedEmissionRecord.objects
            .values('category')
            .annotate(total_emissions=Sum('co2e'))
            .order_by('-total_emissions')[:5]
        )

        return Response(list(categories))


class FlaggedRecordsView(APIView):

    def get(self, request):

        flagged_count = NormalizedEmissionRecord.objects.filter(
            status='FLAGGED'
        ).count()

        return Response({
            "flagged_records": flagged_count
        })


class AlertsView(APIView):

    def get(self, request):

        alerts = NormalizedEmissionRecord.objects.filter(
            is_flagged=True
        ).values(
            'category',
            'scope',
            'co2e',
            'flag_reason'
        )

        data = []

        for alert in alerts:

            data.append({
                "category": alert["category"],
                "scope": alert["scope"],
                "co2e": alert["co2e"],
                "reason": alert["flag_reason"],
            })

        return Response(data)