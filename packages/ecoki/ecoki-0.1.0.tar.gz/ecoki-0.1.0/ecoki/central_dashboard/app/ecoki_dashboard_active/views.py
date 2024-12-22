from django.shortcuts import redirect, render,get_object_or_404
#from django.utils.text import unescape_entities
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import Context

# Create your views here.
from django.template.loader import get_template
from django.template import Context
from django.http.response import HttpResponse

from django.forms.models import model_to_dict
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings

from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Pipeline, ActiveBB, BB
from .serializers import PipelineSerializer

from rest_framework import serializers

import requests
import json
import base64
import os
import pathlib
from django.utils.html import strip_tags

from .forms import ckeditor

# To get all the pipelines that are available in API
from ecoki.central_dashboard.app.ecoki_app.views import getpipelines

# for images to be read directly without using static
from PIL import Image
from io import BytesIO
import base64

import itertools

# To get status codes of a BB
from ecoki.common.status_code import Status

# dir paths
ecoki_dir = (pathlib.Path(__file__) / ".." / ".." / ".." / "..").resolve()
coded_bb_dir = (ecoki_dir / "building_blocks" / "code_based").resolve()
non_coded_bb_dir = (ecoki_dir / "building_blocks" / "non_code_based").resolve()
success_story_dir = (ecoki_dir / "success_story" / "success_stories").resolve()
ener_eff_examples_dir = (ecoki_dir / "success_story" / "energy_efficiency_examples").resolve()
ener_eff_scenario_dir = (ecoki_dir / "energy_efficiency_scenarios").resolve()

pipeline_tags = {
    "custom": {"name": "custom pipeline", "color": "green"},
    "ecoki": {"name": "ecoKI pipeline", "color": "maroon"}
}

category_tags = {
    "Data Integration": {"color": "orange"},
    "Modelling": {"color": "purple"},
    "Optimization": {"color": "green"},
    "Process Assessment": {"color": "blue"},
    "Process Steering": {"color": "red"}
}

app_context_tags = {}

def read_json(path):
    with open(path) as f:
        return json.load(f)

def save_file(path, data):
    with open(path, 'w') as f:
        f.write(data)
        f.close()

def get_bb_type(bb_category):
    bb_type = None
    for typ in ['ecoki', 'custom']:
        response = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/'+typ+'/overview')
        if bb_category in response.json()["payload"][typ+'_pipelines']:
            bb_type = typ
    return bb_type 
     
def get_active_pipelines():
    context = {}
    # For pipelines list on side navigation bar
    context["all_pipelines"] = getpipelines()
    return context

def image_to_base64(image):
    buff = BytesIO()
    image.save(buff, format="PNG")
    img_str = base64.b64encode(buff.getvalue())
    img_str = img_str.decode("utf-8")  # convert to str and cut b'' chars
    return img_str

# Function to navigate through the folders retrieving the data from the building blocks by providing the path:
@login_required
def retrieve_data(request,building_block_path):
    bb_name_bb_popup_data = {}
    bb_category_bb_markdown_data = {}
    bb_category_bb_url_data = {}
    bb_category_bb_description = {}
    primary_folders_names = []
    bb_names = []
    bb_popup_data = []
    bb_markdown_data = []
    bb_categories_names = []
    bb_urls = []

    for file in os.listdir(building_block_path):
        level2= file.replace("_"," ").title()
        primary_folders_names.append(level2)
        bb_name_bb_popup_data[level2] = []      # create a new key and assign an empty list as its value
        filename = os.fsdecode(file)
        current_path = (building_block_path / filename).resolve()

        for file_category in os.listdir(current_path):
            if not os.path.isdir(os.path.join(current_path, file_category)):
                continue
            current_category_path = (current_path / file_category).resolve()
            level3 = filename.replace("_"," ").title()
            level4 = file_category.replace("_"," ").title()
            if level4 == ".Gitkeepf":
                continue
            if level4 == ".DS_Store":
                continue
            bb_category_bb_markdown_data[level4] = []
            bb_category_bb_url_data[level4] = []
            bb_category_bb_description[level4] = []
            
            if os.path.isdir(current_category_path):

                # look for markdown files inside
                for file in os.listdir(current_category_path):
                    if file.endswith(".md"):
                        #jsonify
                        md = open((building_block_path / filename / file_category / file).resolve(),encoding="utf-8").read()
                        section = md.split("######") 
                        for index,description in enumerate(section):
                            if index == 0:
                                bb_popup_data.append(description) 
                                bb_category_bb_markdown_data[level4].append(description)                                                          
                            else:
                                bb_markdown_data.append(description)
                                bb_category_bb_description[level4].append(description)
                        
                        if level3 in bb_names:
                            bb_categories_names.append(level4)
                            bb_name_bb_popup_data[level3].append(level4)
                        else:
                            bb_names.append(level3)
                            bb_categories_names.append(level4)
                            bb_name_bb_popup_data[level3].append(level4)
                        bb_urls.append(request.get_full_path()+ str(level4))
                        bb_category_bb_url_data[level4].append(request.get_full_path()+ str(level4))
    
    bb_categories_and_markdown_zip = zip(bb_popup_data, bb_categories_names, bb_urls)     
       
    # Entering the category card names to the DB
    for i in bb_categories_names:
        BB.objects.get_or_create(bbname=i.title())
    return primary_folders_names,bb_name_bb_popup_data,bb_category_bb_markdown_data,bb_category_bb_url_data,bb_categories_and_markdown_zip,bb_category_bb_description

# For removing the blocks deleted by user
def delete_blocks(bb_category):
    bb = BB.objects.all().values_list('bbname',flat=True)
    for i,card in enumerate(bb): 
        if card == bb_category: 
            d=ActiveBB.objects.filter(activebb=card)
            d.delete()                  
      
# Adding blocks on the top naviagtion bar   
def add_navbar_blocks(bb_category=None):
    list = []
    list_nc = [] 
    bb = BB.objects.all().values_list('bbname',flat=True)  
    for i,card in enumerate(bb):
        # if data in context['bb_categories']: 
        if card == bb_category:      
            ActiveBB.objects.get_or_create(activebb=card)  
    a= ActiveBB.objects.all().values_list('activebb',flat=True)     
    for j in a:
        if j in ('Energy Efficiency Levers Library','Energy Relevant Data Guideline'): 
            list_nc.append(j)
        else:
            list.append(j)
                
    return list, list_nc    
        
    # Uncomment the below code to delete the pipeline structure in building blocks if user is not manually deleting
    # c = ActiveBB.objects.all()
    # c.delete()

# Function to retrieve data from pipelines
def retrieve_data_p(bb_category, bb_type):
    popup = []
    brief_desc = []
    url_popup = []
    url_desc = []
    url_del = []
    url_conf = []
    url_dupl = []
    categories_names = []
    pl_tags = []
    cat_tags = []

    if bb_type is not None:
        response = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/'+bb_type+'/overview')
        pipeline_list = response.json()['payload'][bb_type+'_pipelines']
        
        for pipeline_name in pipeline_list:
            response = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/'+bb_type+'/'+pipeline_name)
            meta_data = response.json()['payload']
            if bb_category == pipeline_name:
                brief_desc.append(meta_data)
                url_desc.append("/active/pipeline/"+ str(bb_category) + "/1/yes/no/trigger")
                url_conf.append("/active/pipeline/"+ str(bb_category) + "/0/no/no/configure/")
                url_dupl.append("/active/pipeline/"+ str(bb_category) + "/0/no/yes/configure/")
                url_del.append("/active/pipeline/"+ str(bb_category) + "/1/custom_delete")
            elif bb_category is None:
                response = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/'+bb_type+'/'+pipeline_name)
                meta_data = response.json()['payload']
                popup.append(meta_data['short_description'])
                url_popup.append("/active/building_blocks_overview/"+ str(pipeline_name))
            
            categories_names.append(pipeline_name)# Bode: problem here?
            pl_tags.append([pipeline_tags[bb_type]['name'], pipeline_tags[bb_type]['color']])
            if meta_data['category']:
                cats_dict = {}
                for cat in meta_data['category']:
                    if cat in category_tags.keys():
                        cats_dict[cat] = category_tags[cat]['color']
                    else:
                        app_context_tags[cat] = {}
                        app_context_tags[cat]['color'] = "brown"
                        cats_dict[cat] = app_context_tags[cat]['color']
                cat_tags.append(cats_dict)
            else:
                cat_tags.append({"no_category": ""})

    return zip(brief_desc, url_desc, url_conf, url_dupl, url_del), zip(pl_tags, categories_names, popup, url_popup, cat_tags)
                        
# Function to retrieve data from success stories and energy scenarios
def retrieve_data_se(bb_category, path):
    popup = []
    markdown = []
    url_popup = []
    url_desc = []
    categories_names = []
    jpglist=[]
    indexlist=[]
    indexing = 0
    pointerlist = []

    if os.path.isdir(path):
        for folder_name in os.listdir(path):
            folder_path = os.path.join(path, folder_name)
            if not os.path.isdir(folder_path):
                print(f"Folder {folder_name} does not exist")
                continue
            elif os.path.isdir(folder_path) and not os.listdir(folder_path):
                print(f"Empty folder found: {folder_name}")
                continue

            if "energy_efficiency_scenarios" in str(path) or "success_story" in str(path) :
                level2 = folder_name.replace("_"," ").title()
            else:
                level2 = folder_name
            
            # look for markdown files inside
            md = open((path / folder_name / 'README.md').resolve(),encoding="utf-8").read()
            section = md.split("######")
            for index, description in enumerate(section):
                if index == 0:
                    popup.append(description)
                    if bb_category is None:
                        url_popup.append("/active/building_blocks_overview/"+ str(level2))
                else:
                    if bb_category == level2:
                        markdown.append(description)
                        url_desc.append("/active/pipeline/"+ str(bb_category) + "/" + str(index) + "/trigger")
            for f in os.listdir((path / folder_name).resolve()):
                if f.endswith(".jpg"):
                    jpg = Image.open((path / folder_name / f).resolve())
                    jpglist.append(image_to_base64(jpg))
            indexlist.append(indexing)
            indexing = indexing+1
            categories_names.append(level2)# Bode: problem here?

        # Entering the category card names to the DB
        for pointer,i in enumerate(categories_names):
            if "energy_efficiency_scenarios" in str(path) or "success_story" in str(path) :
                pointerlist.append(pointer)
                BB.objects.get_or_create(bbname=i.title())
            else:
                BB.objects.get_or_create(bbname=i)
    return zip(markdown, url_desc), zip(categories_names, popup, url_popup), zip(categories_names, popup, url_popup, jpglist, indexlist),pointerlist

# Create your views here.

def view_base(request): 
    return render(request,'app_base.html', get_active_pipelines())
    
#def view_ecoki_coffee_roasting_example(request):
#    return render(request,'ecoki_coffee_roasting_example.html')

@login_required
def view_ecoki_test(request):
    return render(request,'ecoki_test.html', get_active_pipelines())

@login_required
def view_docs_template(request):
    return render(request,'docs_template.html', get_active_pipelines())

@login_required
def view_success_stories_template(request):
    context = get_active_pipelines()
            
    # Reading the success story description
    # go through all subfolders in this path
    retrieved = retrieve_data_se(path=success_story_dir, bb_category=None)
    context["names_and_markdown_ss"] = retrieved[2]
    context['pointer'] = retrieved[3] 

    # Reading the energy efficiency examples
    retrieved = retrieve_data_se(path=ener_eff_examples_dir, bb_category=None)
    context["names_and_markdown_eee"] = retrieved[2]
    context['pointer1'] = retrieved[3]   
         
    context['list'], context['list_nc'] = add_navbar_blocks(bb_category=None)   
    return render(request,'success_stories_template.html', context)

@login_required
def view_building_blocks_overview_template(request,bb_category=None, removed=None):
    context = get_active_pipelines()
    
    try:
        # common key names for bb values
        bb_items = ['primary_folders', 'bb_name_bb_popup', 'bb_category_bb_markdown', 'bb_category_bb_url', 'bb_categories_and_markdown']
        # postfixes to distinguish coded and non coded bb values returned for process assessment, data integration, modelling, optimisation and process steering
        post_fixes = ['', '_nc', '_dat', '_dat_nc', '_mod', '_mod_nc', '_opt', '_opt_nc', '_ps', '_ps_nc']
        # directory paths for coded and non coded bbs
        dirs = [(coded_bb_dir / "process_assessment").resolve(), (non_coded_bb_dir / "process_assessment").resolve(), (coded_bb_dir / "data_integration").resolve(), (non_coded_bb_dir / "data_integration").resolve(),
		        (coded_bb_dir / "modelling").resolve(), (non_coded_bb_dir / "modelling").resolve(), (coded_bb_dir / "optimization").resolve(), (non_coded_bb_dir / "optimization").resolve(),
				(coded_bb_dir / "process_steering").resolve(), (non_coded_bb_dir / "process_steering").resolve()]
        for post_fix, dir_path in zip(post_fixes, dirs):
            bb_keys = []
            for item in bb_items:
                # Creating keys for context dict variable
                bb_keys.append(f'{item}{post_fix}')
            # Retrieving values from the function
            context[bb_keys[0]], context[bb_keys[1]], context[bb_keys[2]], context[bb_keys[3]], context[bb_keys[4]], bb_markdown_data = retrieve_data(request, dir_path)
        context['list'], context['list_nc'] = add_navbar_blocks(bb_category)

        if removed == 'removed':
            delete_blocks(bb_category)
            return redirect('/active/building_blocks_overview/') # redirecting to main BB overview page after removal
        else:
            return render(request,'building_blocks_overview_template.html', context)
    except:
        print("Exception on accessing the contents on the content dashboard")
        return render(request,'building_blocks_overview_template.html', context)
        
@login_required
def activebb_template(request, bb_category):
    # For creating the pipeline navigation bar with the blocks(cards) that are opened
    context = get_active_pipelines()
    context['disable_create_button'] = False
    if bb_category in context['all_pipelines']:
        context['disable_create_button'] = True
    context['markdown_descriptions']=[]
    context['pipeline_markdown_descriptions']=[]
    context['list']=[] 
    context['list_nc']=[]

    # directory paths for coded and non coded bbs
    dirs = [(coded_bb_dir / "process_assessment").resolve(), (non_coded_bb_dir / "process_assessment").resolve(), (coded_bb_dir / "data_integration").resolve(), (non_coded_bb_dir / "data_integration").resolve(),
            (coded_bb_dir / "modelling").resolve(), (non_coded_bb_dir / "modelling").resolve(), (coded_bb_dir / "optimization").resolve(), (non_coded_bb_dir / "optimization").resolve(),
            (coded_bb_dir / "process_steering").resolve(), (non_coded_bb_dir / "process_steering").resolve()]

    for bb_path in dirs:
        # depending on name matching, coded or non coded bb values returned for process assessment, data integration, modelling, optimisation or process steering
        for name, desc in retrieve_data(request, bb_path)[5].items():
            if name == bb_category:
                context['markdown_descriptions']= desc
                break

    bb_type = get_bb_type(bb_category)
    # Reading the description
    context['pipelines_markdown_url'] = retrieve_data_p(bb_category, bb_type)[0]
    
    url_keys = ['energy_markdown_url', 'ss_markdown_url', 'eee_markdown_url']
    dirs = [ener_eff_scenario_dir, success_story_dir, ener_eff_examples_dir]
    for url_key, dir_path in zip(url_keys, dirs):
        # Reading the description
        context[url_key] = retrieve_data_se(bb_category, dir_path)[0]
    
    if bb_type is None:
        context['list'], context['list_nc'] = add_navbar_blocks(bb_category)    

    return render(request,'activebb_template.html', context)

@login_required
def view_config_gui_template(request, id, bbid):
    print("view_config_gui_template")
    pipeline_details = {}
    context = get_active_pipelines()
            
    visualise = requests.post('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/'+ id + '/run_interactive')
    
    if  visualise.status_code == 200:  
        return redirect(f"/active/pipeline/{id}/{bbid}/")
    else:
        context["data1"] = "Error on running the pipeline to obtain the visualisation"
        return render(request, 'activebb_template.html' , context)

@login_required    
def view_visualize_template(request,id,bbid):
    # get the Pipeline object with the name "id"
    context = get_active_pipelines()
    pipeline_details = {}
    for x in context["all_pipelines"]:
        if x == id:
            visualise = requests.post('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/'+ x + '/run')
            
    if  visualise.status_code == 200:  
        return redirect(f"/active/pipeline/{id}/{bbid}/")
    else:
        context["data1"] = "Error on running the pipeline to obtain the visualisation"
        return render(request, 'activebb_template.html' , context)

def clean_topology(json_obtained):
    cleaned_pipelinedata = {}
    node_names = []
    for each in json_obtained:
        if each == "topology":
            for node in json_obtained['topology']['nodes']:
                node_names.append(node['name'])
                for key in ('description', 'category', 'executor_module', 'executor_class', 'ports', 'visualization_endpoint'):
                    node.pop(key, None)                                
            for connection in json_obtained['topology']['connections']:
                connection.pop('ports', None)
            cleaned_pipelinedata[each] = json_obtained[each]
        elif each == "executor_module":
            cleaned_pipelinedata[each] = "ecoki.pipeline_framework.pipeline_executor.local_pipeline_executor"
        elif each == "executor_class":
            cleaned_pipelinedata[each] = "LocalPipelineExecutor"
        else:
            cleaned_pipelinedata[each] = json_obtained[each] 
    return cleaned_pipelinedata, node_names            

@login_required
def view_pipeline_save(request,id,bbid):
    context = get_active_pipelines()
    bb_type = get_bb_type(id)    
    if bb_type == "custom":
        retrievejson = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/'+id)
        if retrievejson.status_code == 200:
            addpipelinedata, node_names = clean_topology(retrievejson.json()["payload"])
            response = requests.put('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/custom/update/'+id+'/content?overwrite=true', json.dumps(addpipelinedata))
            context['save_message'] = "Custom pipeline %s settings updated!"%(id)
            response = view_pipeline_template(request,id,bbid,context)
            return response
        else:
            context["data1"] = "Error on running the save pipeline button"
            return render(request, 'activebb_template.html' , context)

@login_required
def view_pipeline_template(request,id,bbid,additional_context={}):
    try:
        context = get_active_pipelines()
        bb_type = get_bb_type(id)
        context['pipeline_type'] = bb_type
        context['is_interactive'] = False
        # add new context variables and init them
        context['bb_names'] = []
        context['number_bbtext'] = []
        last_completed_bb = None
        bb_names = []
        bb_descriptions = []
        htmls = []
        number_bbtext = []
        bb_exc_status_icons = []

        context["name"] = id
        set = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/'+ id)
        # parse the JSON response and retrieve the pipeline topology
        topology = set.json()["payload"]["topology"]
        i=0
        for bb in topology["nodes"]:
            bb_descriptions.append(bb["description"])
            number_bbtext.append(str(i))  
            bb_names.append(bb["name"])
            # ---------------------------------- change from Xinyu start --------------------------------
            # if a BB has an interactive GUI, it will be displayed in dashboard first
            htmls.append(bb["interactive_gui_endpoint"])
            # ---------------------------------- change from Xinyu end --------------------------------
            if bb['interactive_configuration'] and bb["interactive_gui_endpoint"]:
                context['is_interactive'] = True

            if Status(bb['execution_status']).name == 'WAITING':
                bb_exc_status_icons.append("inactive")
            elif Status(bb['execution_status']).name == 'RUNNING':
                bb_exc_status_icons.append("config")
            elif Status(bb['execution_status']).name == 'FINISHED':
                bb_exc_status_icons.append("success")
            elif Status(bb['execution_status']).name == 'FAILURE':
                bb_exc_status_icons.append("fail")
            i=i+1                        

        if bb_names:
            # set context variables
            context['bb_names'] = bb_names
            context["current_description"] = bb_descriptions[int(bbid)]
            context["current_html"] = htmls[int(bbid)]
            context['number_bbtext'] = number_bbtext
            context['bb_exc_status_icons'] = bb_exc_status_icons
            split_url = request.path.strip('/').split('/')
            context['url'] = split_url[-2] if split_url[-1] == "save" else split_url[-1]
            context['save_settings'] = "yes" if split_url[-1] == "save" else "no" 
            context['save_message'] = additional_context['save_message'] if split_url[-1] == "save" else ''  
            
            # highlighting the active building block in navbar
            context["bb_ids_names_text_icons"] = zip(context['number_bbtext'], context['bb_names'], context['bb_exc_status_icons'])

            current_bb = int(bbid)
        else:
            current_bb = 0
        context['current_bb'] = current_bb

        # ---------------------------------- change from Xinyu start --------------------------------
        # ---------------------------------- update html with visualization, if results of BB are available
        current_bb_name = context['bb_names'][current_bb]
        current_bb_info = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/' + id + '/nodes/' + current_bb_name)
        current_bb_info = current_bb_info.json()
        current_bb_visualization = current_bb_info["payload"]["visualizer_module"]

        if current_bb_visualization:
            bb_execution_status = current_bb_info["payload"]["execution_status"]
            if bb_execution_status == 1:
                context['visualizer'] = True
                context['current_html'] = current_bb_info["payload"]["visualization_endpoint"]
        # ---------------------------------- change from Xinyu end --------------------------------
        # give it to the template as an additional context. all model fields/attributes are available in the html-file
        return render(request,'pipeline_template.html', context)
        
    except Exception as e:
        print('An Exception ocurred when communicating with the pipeline class')

@login_required
def view_pipeline_configure(request,id,bbid,active,duplicate):
    context = get_active_pipelines()
    context['current_bb'] = bbid
    context["name"] = id
    context['settings'] = []
    context["addpipelinedata"] = {}
    context['active'] = active
    context['duplicate'] = duplicate
    addpipelinedata = {}
    all_pipeline_names = {}

    try:
        response = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/ecoki/overview')
        all_pipeline_names['ecoki'] = response.json()['payload']['ecoki_pipelines']
        response = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/custom/overview')
        all_pipeline_names['custom'] = response.json()['payload']['custom_pipelines']
        context['all_pipeline_names'] = all_pipeline_names

        retrievejson = None
        if active == "no":
            bb_type = get_bb_type(id)
            retrievejson = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/'+bb_type+'/'+context["name"]+'/content')
        else:
            retrievejson = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/'+context["name"])

        if retrievejson.status_code == 200:
            addpipelinedata, node_names = clean_topology(retrievejson.json()["payload"])
            context['settings'] = node_names
            addpipelinedata["execution_status"] = retrievejson.json()['payload']["execution_status"]
            # convert my_data to a JSON string with indentation
            context['form'] = json.dumps(addpipelinedata, indent=2)
            return render(request, 'pipeline_configure.html', context)

        else:
            context['data1'] = "The selected pipeline doesnot exist"
            return render(request, 'activebb_template.html', context)

    except:
        context['data1'] = "An Exception occured while trying to connect to RESTAPI-shell."
        return render(request, 'activebb_template.html', context)

@login_required
def view_pipeline_delete(request, id, bbid):
    context = get_active_pipelines()
    try:
        deleted = requests.delete('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/?pipeline_name=' + id)
        context['data1'] = '%s. Refreshing navigation bar... <meta http-equiv="refresh" content="1;url=http:/">'%(deleted.json()["execution_status"]["message"])
        return render(request, 'activebb_template.html', context)
    except:
        context['data1'] = "Pipeline deletion didnot work"
        return render(request, 'activebb_template.html', context)

@login_required
def view_custom_pipeline_delete(request, id, bbid):
    context = get_active_pipelines()
    try:
        # delete from active PLs list before deleting folder
        if id in context["all_pipelines"]:
            deleted = requests.delete('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/?pipeline_name=' + id)
        deleted = requests.delete('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/custom/delete/' + id)
        context['data1'] = '%s. Refreshing navigation bar... <meta http-equiv="refresh" content="1;url=/active/pipeline_list_overview/">'%(deleted.json()["execution_status"]["message"])
        return render(request, 'activebb_template.html', context)
    except:
        context['data1'] = "Custom Pipeline deletion didnot work"
        return render(request, 'activebb_template.html', context)
        
@login_required
def view_pipeline_trigger(request, id, bbid, active, duplicate):
    context = get_active_pipelines()
    context['settings'] = []
    context['current_bb'] = bbid
    addpipelinedata = {}
    bb_type = get_bb_type(id)

    if request.method == "POST":
        # runs when saving and restarting an active pipeline
        try:
            # Stripping the <p> and <br> tags from the data retrieved from UI and then loading in json format
            retrieved_values = request.POST.getlist('JSONDATA')
            if duplicate == "no":
                retrieved_form = json.loads(retrieved_values[0].replace(u'\xa0', u' '))
            else:
                duplicate_pipeline_name = retrieved_values[0]
                retrieved_form = json.loads(retrieved_values[1])
                retrieved_form['name'] = duplicate_pipeline_name

            addpipelinedata["jsondata"] = retrieved_form
            bb_type = "custom"
            resp_message = ""
            # check for id in custom pipelines dir
            response = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/custom/overview')
            if id in response.json()["payload"]["custom_pipelines"]:
                # if the name in settings.json same as the pipeline id, rewrite the settings.json
                if addpipelinedata["jsondata"]["name"] == id:
                    response = requests.put('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/custom/update/'+id+'/content?overwrite=true', json.dumps(addpipelinedata["jsondata"]))
                    resp_message = "Pipeline %s updated"%(id)
                else:
                    # if a folder of the name in settings.json does not exist in custom pipeline dir, create it
                    response = requests.put('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/custom/update/'+id+'/content?pipeline_new_name='+addpipelinedata["jsondata"]["name"]+'&overwrite=false', json.dumps(addpipelinedata["jsondata"]))
                    id = addpipelinedata["jsondata"]["name"]
                    resp_message = "Pipeline %s added"%(id)
            else:
                # if id doesn't exist in ecoki pipeline dir, only then create one in custom pipeline dir
                if addpipelinedata["jsondata"]["name"] != id:
                    response = requests.put('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/ecoki/update/'+id+'/content?pipeline_new_name='+addpipelinedata["jsondata"]["name"], json.dumps(addpipelinedata["jsondata"]))
                    id = addpipelinedata["jsondata"]["name"]
                    resp_message = "Pipeline %s added"%(id)

            if active == "no":
                context['data1'] = '%s. Refreshing navigation bar... <meta http-equiv="refresh" content="1;url=http:/">'%(resp_message)
                return render(request, 'activebb_template.html', context)
                    
        except:
            context['data1'] = "Please check the data entered in the editor"
            return render(request, 'activebb_template.html', context)

    if active == 'yes':
        try:
            response = requests.put('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/?pipeline_type='+bb_type+'&pipeline_name='+id)  
            if response.status_code == 200:
                resp_message = ""
                if id in context['all_pipelines']:
                    resp_message = "Pipeline %s updated"%(id)
                else:
                    resp_message = "Pipeline %s added"%(id)
                context['data1'] = '%s. Refreshing navigation bar... <meta http-equiv="refresh" content="1;url=http:/">'%(resp_message)
                return render(request, 'activebb_template.html', context)
            else:
                context['data1'] = response.json()["execution_status"]["message"]
                return render(request, 'activebb_template.html', context)
        except:
            context['data1'] = "An Exception occured while trying to connect to RESTAPI-shell. Make sure that its running on localhost:5000 to be able to start pipelines from the dashboard"
            return render(request, 'activebb_template.html', context)
        
@login_required
def build_new_pipeline(request,new=None,pipeline=None,build=None):
    context = get_active_pipelines()
    all_pipeline_names = {}
    
    if request.method == "POST":
        try:
            retrieved_values = request.POST.get('JSONDATA')
            retrieved_form = json.loads(retrieved_values.replace(u'\xa0', u' '))
            id = retrieved_form['name']
            resp_message = ""
            response = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/custom/overview')
            if id in response.json()["payload"]["custom_pipelines"]:
                response = requests.put('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/custom/update/'+id+'/content?overwrite=true', json.dumps(retrieved_form))
                resp_message = "Pipeline %s updated"%(id)
            else:
                response = requests.post('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/custom/add/'+id+'/content?overwrite=false', json.dumps(retrieved_form))
                resp_message = "Pipeline %s added"%(id)
        
            context['data1'] = '%s. Refreshing navigation bar... <meta http-equiv="refresh" content="1;url=http:/">'%(resp_message)
            return render(request, 'activebb_template.html', context)
        except:
            context["data1"] = "Please check the data entered in the editor"
            return render(request, 'activebb_template.html', context)
    else:    
        response = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/ecoki/overview')
        all_pipeline_names['ecoki'] = response.json()['payload']['ecoki_pipelines']
        response = requests.get('http://'+str(settings.shell_host)+':'+str(settings.shell_port)+'/api/v1/pipelines/custom/overview')
        all_pipeline_names['custom'] = response.json()['payload']['custom_pipelines']
        context['all_pipeline_names'] = all_pipeline_names
        return render(request,'build_pipeline_template.html', context)

@login_required
def view_pipeline_list(request, bb_category=None, removed=None):
    context = get_active_pipelines()
    context['pipeline_tags'] = pipeline_tags
    context['category_tags'] = category_tags
    app_context_tags.clear()
                 
    pipeline_data = []
    # Data required for the Pipeline:
    pipeline_data.append(retrieve_data_p(bb_category, "ecoki")[1])
    # Data required for the Custom Pipeline:
    pipeline_data.append(retrieve_data_p(bb_category, "custom")[1])    
    pipeline_data = itertools.chain.from_iterable(pipeline_data)
    
    pipeline_list_template_data = []
    for (pl_tag,name,description,url,cat_tag) in pipeline_data:
        pipeline_dict = {}
        pipeline_dict['type'] = pl_tag[0]
        pipeline_dict['color'] = pl_tag[1]
        pipeline_dict['name'] = name
        pipeline_dict['description'] = description
        pipeline_dict['url'] = url
        pipeline_dict['categories'] = cat_tag
        pipeline_list_template_data.append(pipeline_dict)
        
    context["pipeline_list_template_data"] = pipeline_list_template_data
    context['app_context_tags'] = app_context_tags
    
    return render(request,'pipeline_list.html', context)



@login_required
def view_energy_overview_template(request):
    context = get_active_pipelines()
            
    # Reading the energy scenario description
    # go through all subfolders in this path
    retrieved = retrieve_data_se(path=ener_eff_scenario_dir, bb_category=None)
    context["names_and_markdown_energy"] = retrieved[2]
    context['pointer'] = retrieved[3]        
    context['list'], context['list_nc'] = add_navbar_blocks(bb_category=None)   
    
    return render(request,'energy_overview_template.html',context)

# adds api routes for creating pipeline objects. see README for a description how to use it from external
@api_view(['POST'])
def add_items(request):
    item = PipelineSerializer(data=request.data)

    # # validating for already existing data
    # if Pipeline.objects.filter(**request.data).exists():
    #     raise serializers.ValidationError('This data already exists')
    try:

        if Pipeline.objects.filter(name=request.data["name"]).exists():

            a=1

    except:
        raise serializers.ValidationError('This pipeline information you provided is invalid. Please check for missing fields. The data that was sent is:  '+str(request.data))

    if Pipeline.objects.filter(name=request.data["name"]).exists():

        raise serializers.ValidationError('This pipeline with the name ' + request.data["name"]+ ' already exists')

    if item.is_valid():
        item.save()
        return Response(item.data)
    else:
        #return Response(status=status.HTTP_404_NOT_FOUND)
        raise serializers.ValidationError('This pipeline information you provided is invalid. Please check for empty fields. The data that was sent is:  '+str(request.data))

@api_view(['GET'])
def ApiOverview(request):
    api_urls = {
        'all_items': '/',
        'Search by Category': '/?category=category_name',
        'Search by Subcategory': '/?subcategory=category_name',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/item/pk/delete'
    }

    return Response(api_urls)


from django.shortcuts import render
from django.views.static import serve
import os
from django.conf import settings



@login_required
def view_faq_template(request):
    return render(request,'faq_template.html', get_active_pipelines())

# Existing imports and code...
@login_required
def view_docs_template(request):
    """
    Render the documentation template.
    
    Parameters
    ----------
    request : django.http.HttpRequest
        The HTTP request object.
    
    Returns
    -------
    django.http.HttpResponse
        The HTTP response containing the rendered documentation template.
    """
    return render(request, 'docs_template.html', get_active_pipelines())


from django.shortcuts import render
from django.views.static import serve
import os
from django.conf import settings

# Existing imports and code...


from django.shortcuts import render
from django.views.static import serve
import os
from django.conf import settings

# Existing imports and code...

def view_docs_template(request):
    """
    Render the documentation template.
    
    Parameters
    ----------
    request : django.http.HttpRequest
        The HTTP request object.
    
    Returns
    -------
    django.http.HttpResponse
        The HTTP response containing the rendered documentation template.
    """
    return render(request, 'docs_template.html')


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
    doc_root = os.path.join(settings.BASE_DIR,'docs/_build/html')

    return serve(request, path, document_root=doc_root)

