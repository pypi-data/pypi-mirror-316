# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import django
import datetime

# Add the parent directory of 'ecoki_app' to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

os.environ['DJANGO_SETTINGS_MODULE'] = 'ecoki_app.settings'
django.setup()

project = 'Documentation'
copyright = '2024, Abhijeet Pendyala'
author = 'Abhijeet Pendyala'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages',
]

# Napoleon settings
napoleon_google_docstring = False
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

templates_path = ['_templates', os.path.join(os.path.dirname(__file__), '..', 'ecoki_dashboard_active', 'templates')]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'  # Using Read the Docs theme for better readability

# Green color of of the text Documentation with home button
html_theme_options = {
    'style_nav_header_background': '#004d00 ',  # EcoKI green color
    'style_external_links': True,
}

#Custom CSS to increase width
html_css_files = [
    #'css/custom.css',
    '_static/css/baselines_theme.css',
]

# # Create a custom CSS file
# with open('_static/css/custom.css', 'w') as f:
#     f.write("""
            
#         /* Change color of menu section headers */
#         .wy-menu-vertical .caption {
#             color: white !important; /* White text for better contrast */
#             background-color: var(--main-bg-color) !important; /* Dark green */
#             font-weight: bold;
#             padding: 5px;
#             border-radius: 4px; /* Add slight rounding if desired */
#         }

#         /* Adjust hover effects for menu section headers */
#         .wy-menu-vertical .caption:hover {
#             background-color: var(--hover-color) !important; /* Lighter green */
#         }

#         .wy-side-nav-search {
#             background-color: #004d00 !important; /* Dark green */
#         }

#         /* Change the main menu link color */
#         .wy-menu-vertical a {
#             color: white !important;
#             background-color: var(--main-bg-color) !important; /* Dark green */
#             padding: 5px 10px; /* Reduce padding for smaller blocks */
#             border-radius: 4px; /* Add subtle rounding */
#             opacity: 0.8; /* Slight transparency */
#             transition: all 0.2s ease-in-out;
#         }
        
#         /* Add a gradient to top-level menu items (Level 1) */
#         .wy-menu-vertical li.toctree-l1 > a {
#             background: linear-gradient(90deg, #004d00, #006600) !important; /* Dark green gradient */
#             color: white !important; /* White text for readability */
#             padding: 5px 10px; /* Consistent padding */
#             border-radius: 4px; /* Slightly rounded corners */
#             transition: background 0.3s ease, color 0.3s ease; /* Smooth transition */
#         }

#         /* Add a gradient to second-level submenu items (Level 2) */
#         .wy-menu-vertical li.toctree-l2 > a {
#             background: linear-gradient(90deg, #006600, #009900) !important; /* Lighter green gradient */
#             color: white !important;
#             padding: 4px 10px;
#             border-radius: 4px;
#             transition: background 0.3s ease, color 0.3s ease;
#         }
        
#         /* Level 3 menu items */
#         .wy-menu-vertical li.toctree-l3 > a {
#         background: linear-gradient(90deg, #009900, #00cc00) !important; /* Lighter green gradient */
#         color: white !important;
#         padding: 4px 10px;
#         border-radius: 4px;
#         font-size: 0.9em; /* Slightly smaller text size */
#         transition: background 0.3s ease, color 0.3s ease;
#         }

# /* Level 4 menu items */
#         .wy-menu-vertical li.toctree-l4 > a {
#         background: linear-gradient(90deg, #00cc00, #00ff00) !important; /* Very light green gradient */
#         color: white !important;
#         padding: 4px 10px;
#         border-radius: 4px;
#         font-size: 0.85em; /* Smaller text for deeper levels */
#         transition: background 0.3s ease, color 0.3s ease;
#         }


#         /* Highlight the current menu item */
#         .wy-menu-vertical li.current > a {
#             background-color: #002200 !important; /* Highlighted dark green for active state */
#             color: white !important; /* White text */
#             font-weight: bold; /* Make the text bold for clarity */
#             border-left: 4px solid #00cc00; /* Add a green border to indicate selection */
#             box-shadow: inset 0 0 5px rgba(0, 255, 0, 0.5); /* Subtle glow effect */
#         }

#         /* Hover effects for menu items */
#         .wy-menu-vertical a:hover {
#             background-color: #007700 !important; /* Lighter green on hover */
#             color: white !important; /* Ensure hover text stays white */
#             border-left: 4px solid #00cc00; /* Add a hover indicator */
#             transition: background-color 0.2s ease, border-left 0.2s ease;
#         }

        
#         /* Active menu item styling */
#         .wy-menu-vertical li.current > a {
#         background-color: #003300 !important; /* Even darker green for active item */
#         color: white !important;
#         opacity: 1; /* Full visibility for active state */
#         font-weight: bold; /* Highlight text */
#         border-left: 4px solid #007700; /* Add a subtle indicator */
#         }
#         /* Prevent code blocks from overflowing */
#         /* Ensure code blocks wrap and scroll properly */
#         pre, code {
#         white-space: pre-wrap; /* Allow wrapping */
#         word-wrap: break-word; /* Break long words */
#         overflow-x: auto; /* Add horizontal scroll if necessary */
#         max-width: 100%; /* Restrict to container width */
#         background-color: #f8f8f8; /* Neutral background */
#         padding: 10px; /* Add padding for readability */
#         border-radius: 5px; /* Rounded corners for better aesthetics */
#         border: 1px solid #ddd; /* Subtle border */
#         }

#         /* For wider screens */
#         .wy-nav-content {
#         max-width: 1600px !important; /* Adjust to your desired width */
#         padding: 20px;
#         }


        
#     """)
    
    
html_static_path = ['_static']

# Add Django settings configuration
from django.conf import settings
from django.core.wsgi import get_wsgi_application

# Initialize Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecoki_app.settings')
application = get_wsgi_application()


# Configure Sphinx to use Django's static file handling
html_static_path = ['_static']
# Ensure the html_extra_path exists or update it to the correct path
html_extra_path = [os.path.join(os.path.dirname(__file__), '_build', 'html')]
if not os.path.exists(html_extra_path[0]):
    os.makedirs(html_extra_path[0])
    
    
    

def setup(app):
    """
    Custom Sphinx extension to serve the documentation.

    This function sets up a custom Sphinx extension that integrates
    the generated HTML documentation with the Django dashboard.

    Parameters
    ----------
    app : sphinx.application.Sphinx
        The Sphinx application object.

    Returns
    -------
    dict
        A dictionary containing metadata about the extension.
    """
    from django.urls import path, re_path
    from django.views.static import serve
    from django.conf import settings
    import importlib
    
    app.add_css_file("_static/css/baselines_theme.css")


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
        doc_root = os.path.join(settings.BASE_DIR, 'docs/', '_build', 'html')
        return serve(request, path, document_root=doc_root)

    # Import the ROOT_URLCONF module
    urlconf_module = importlib.import_module(settings.ROOT_URLCONF)

    # Add the documentation URL to Django's URL patterns
    urlconf_module.urlpatterns += [
        re_path(r'^docs/(?P<path>.*)$', serve_docs, name='serve_docs'),
    ]

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }


# Version Management
# Dynamically read version from a file
version_file = os.path.join(os.path.dirname(__file__), "../../../../version.txt")
with open(version_file) as file_handler:
    __version__ = file_handler.read().strip()

version = "develop (" + __version__ + ")"
release = __version__


# Spelling and Copybutton for the documentation
try:
    import sphinxcontrib.spelling
    extensions.append("sphinxcontrib.spelling")
    # Configure spelling settings
    spelling_lang = 'en_US'  # Set spelling language
    spelling_show_suggestions = True  # Show spelling suggestions
except ImportError:
    pass

try:
    import sphinx_copybutton
    extensions.append("sphinx_copybutton")
except ImportError:
    pass

# Logo of the EcoKI for the sidebar
html_logo = "_static/img/logo.png"

# Pygments Style for Syntax Highlighting
pygments_style = "sphinx"

#Code Block Copy Button
extensions.append("sphinx_copybutton")

#Dynamic Copyright
copyright = f"2024-{datetime.date.today().year}, Abhijeet Pendyala"

#
# exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
