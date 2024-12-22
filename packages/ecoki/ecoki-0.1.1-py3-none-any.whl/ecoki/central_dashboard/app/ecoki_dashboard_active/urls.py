"""ecoki_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from ecoki_dashboard_active import views as views

from django.urls import path, re_path
from django.views.static import serve
import os
from django.conf import settings

from django.urls import path, re_path
from ecoki_dashboard_active import views as views
from django.views.static import serve
import os

from django.urls import path, re_path
from ecoki_dashboard_active import views as views
from django.views.static import serve
import os

# Define the serve_docs function if not already defined
def serve_docs(request, path):
    """
    Serve the generated documentation files.
    
    Parameters
    ----------
    request : django.http.HttpRequest
        The HTTP request object.
    path : str
        The requested file path within the documentation.
    
    Returns
    -------
    django.http.HttpResponse
        The HTTP response containing the requested documentation file.
    """
    #doc_root = os.path.join(settings.BASE_DIR, 'ecoki', 'central_dashboard', 'app', '_build', 'html')
    doc_root = os.path.join(settings.BASE_DIR, '_build', 'html')

    return serve(request, path, document_root=doc_root)



# define urls
urlpatterns = [
    path('', views.view_base),
    #path('roasting_data/', views.view_ecoki_coffee_roasting_example),
    path('ecoki_test/', views.view_ecoki_test),

    path('pipeline/<str:id>/<bbid>/', views.view_pipeline_template),
    path('pipeline/<str:id>/<bbid>/save/', views.view_pipeline_save),
    path('pipeline/<str:id>/<bbid>/visualize/', views.view_visualize_template), # run is added to initiate the run of pipeline only when user wants visualisation
    path('pipeline/<str:id>/<bbid>/config_gui/', views.view_config_gui_template), # Run to see the GUI visualisation to see the configurations of the run
    path('pipeline/<str:id>/<bbid>/<active>/<duplicate>/configure/', views.view_pipeline_configure),
    path('pipeline/<str:id>/<bbid>/<active>/<duplicate>/trigger/', views.view_pipeline_trigger),#added for triggering pipeline
    path('pipeline/<str:id>/<bbid>/delete/', views.view_pipeline_delete),#added for deleting pipeline
    path('pipeline/<str:id>/<bbid>/custom_delete/', views.view_custom_pipeline_delete),#added for deleting custom pipeline
    
    # Added for pipelines to be displayed
    path('pipeline_list_overview/', views.view_pipeline_list),
    path('pipeline_list_overview/<bb_category>/', views.view_pipeline_list),
    path('pipeline_list_overview/<bb_category>/<removed>/', views.view_pipeline_list), 
    
    # Added for FAQs
    path('faq/', views.view_faq_template),
    
    # Added for Success Stories
    path('success_stories/', views.view_success_stories_template),
    
    path('building_blocks_overview/', views.view_building_blocks_overview_template),
    path('building_blocks_overview/<bb_category>/<removed>/', views.view_building_blocks_overview_template),
    path('building_blocks_overview/<bb_category>/', views.activebb_template), # This and above url directs to the description of the BBs, pipelines and energy efficiencies
    path('building_blocks_overview/<new>/<pipeline>/<build>/', views.build_new_pipeline), # added for building new pipeline

    # Added for Energy efficiency scenarios
    path('energy_overview/', views.view_energy_overview_template),

    # django rest framework_johannes routes
    path('ovr/bla/', views.ApiOverview, name='home'),
    path('createppl/', views.add_items, name='add-items'),
    
    # Serve documentation
    #path('docs/', views.view_docs_template, name='docs'),
    path('docs/', views.view_docs_template, name='docs'),
    path('docs/<path:path>', views.serve_docs, name='serve_docs'),
]
