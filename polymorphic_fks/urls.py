from django.urls import path

from .views import HomeView, CheckrunsWithGenericFk, CheckrunsWithMultipleFks, \
    CheckrunsWithFksInChildTables, CheckrunsWithDjangoPolymorphic, OgcServiceDetailView, LayerDetailView, \
    FeatureTypeDetailView, DatasetMetadataDetailView, ServiceMetadataDetailView, LayerMetadataDetailView, \
    FeatureTypeMetadataDetailView, CheckrunsWithFkLookupTable

app_name = 'polymorphic_fks'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),

    # resources
    path('ogcservice/<pk>', OgcServiceDetailView.as_view(), name='ogcservice-detail'),
    path('layer/<pk>', LayerDetailView.as_view(), name='layer-detail'),
    path('featuretype/<pk>', FeatureTypeDetailView.as_view(), name='featuretype-detail'),
    path('dataset-metadata/<pk>', DatasetMetadataDetailView.as_view(), name='dataset-metadata-detail'),
    path('service-metadata/<pk>', ServiceMetadataDetailView.as_view(), name='service-metadata-detail'),
    path('layer-metadata/<pk>', LayerMetadataDetailView.as_view(), name='layer-metadata-detail'),
    path('featuretype-metadata/<pk>', FeatureTypeMetadataDetailView.as_view(), name='featuretype-metadata-detail'),

    # references
    path('checkruns-with-generic-fk/', CheckrunsWithGenericFk.as_view(), name='checkruns-with-generic-fk'),
    path('checkruns-with-multiple-fks/', CheckrunsWithMultipleFks.as_view(), name='checkruns-with-multiple-fks'),
    path('checkruns-with-fk-lookup-table/', CheckrunsWithFkLookupTable.as_view(),
         name='checkruns-with-fk-lookup-table'),
    path('checkruns-with-fks-in-child-tables/', CheckrunsWithFksInChildTables.as_view(),
         name='checkruns-with-fks-in-child-table'),
    path('checkruns-with-django-polymorphic/', CheckrunsWithDjangoPolymorphic.as_view(),
         name='checkruns-with-django-polymorphic'),
]
