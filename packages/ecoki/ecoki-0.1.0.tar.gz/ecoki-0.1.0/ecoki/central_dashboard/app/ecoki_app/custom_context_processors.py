from ecoki_dashboard_active.models import Pipeline

def pipelines_adder(request):
    return {
        #here add the model objects
       #"all_pipelines": ["amazing pipeline","simple pipeline","pp1"],
        #"all_pipelines": ["amazing pipeline", "simple pipeline", "pp1"],
        "all_pipelines": Pipeline.objects.all(),
    }