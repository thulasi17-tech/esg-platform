from django.urls import path

from .views import (
    EmissionSummaryView,
    TopEmissionCategoriesView,
    FlaggedRecordsView,
    AlertsView
)

urlpatterns = [

    path(
        'summary/',
        EmissionSummaryView.as_view()
    ),

    path(
        'top-categories/',
        TopEmissionCategoriesView.as_view()
    ),

    path(
        'flagged-records/',
        FlaggedRecordsView.as_view()
    ),

    path(
        'alerts/',
        AlertsView.as_view()
    ),
]