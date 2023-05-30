from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from insurance import views
from insurance.views import PolicyViewSet, Claim

router = DefaultRouter()
router.register('policies', views.PolicyViewSet, basename='policy')
router.register('claims', views.Claim)
router.register('payments', views.Payment)

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include(router.urls)),
    path('customers/<int:profile_pk>/policies/<int:pk>/', PolicyViewSet.as_view({'get': 'retrieve'}), name='policy-detail'),
    path('customers/<int:profile_pk>/claims/<int:pk>/', Claim.as_view({'get': 'retrieve'}), name='claim-detail'),

]
