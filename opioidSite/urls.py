from django.urls import path
from .views import indexPageView, showPrescriberPageView, showPrescriptionPageView
from .views import searchPrescriberPageView, searchPrescriptionPageView, aboutPageView
from .views import analysisPageView, addPrescriberPageView, editPrescriberPageView 
from .views import deletePrescriberPageView, viewAllPrescriptionsPageView, showPrescriptionDetailsPageView
from .views import viewAllPrescribersPageView, showPrescriberDetailsPageView

urlpatterns = [ 
    path("addPrescriber/", addPrescriberPageView, name="addPrescriber"),
    path("editPresciber/<int:pre_num>/", editPrescriberPageView, name="editPrescriber"),
    path("deletePresciber/<int:pre_num>/", deletePrescriberPageView, name="deletePrescriber"),
    path("searchPrescription/", searchPrescriptionPageView, name="searchPrescription"),
    path("viewAllPrescriptions/", viewAllPrescriptionsPageView, name="viewAllPrescriptions"),
    path("searchPrescriber/", searchPrescriberPageView, name="searchPrescriber"),
    path("viewAllPrescribers/", viewAllPrescribersPageView, name="viewAllPrescribers"),   
    path("showPrescriberDetails/<int:pre_num>/", showPrescriberDetailsPageView, name="showPrescriberDetails"), 
    path("showPrescriber/", showPrescriberPageView, name="showPrescriber"),
    path("showPrescriptionDetails/<str:drug>/", showPrescriptionDetailsPageView, name="showPrescriptionDetails"),
    path("showprescription/", showPrescriptionPageView, name="showPrescription"),
    path("about/", aboutPageView, name="about"),
    path("analysis/", analysisPageView, name="analysis"),
    path("", indexPageView, name="index"),
]