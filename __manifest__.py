# -*- coding: utf-8 -*-

{
    'name': "To-do Checklist",

    'summary': """To Do List for Personal use, Projects, Tasks, and Subtasks""",
    'description':
    """This Module helps to get to know actual time of assigning task and get reminder. Whenever we will assign task to employees and give expected time then we will know that task's actual time.""",
    'author': "Kevin Zamzami",
    'website': "https://www.instagram.com/kevinzmi/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'project', 'hr_attendance', 'hr_timesheet'],
    # always loaded
   'data': [
             'security/ir.model.access.csv',
             'views/menu.xml',
             'views/todo_checklist_view.xml',
             'views/todo_checklist_tags_views.xml',
                    ],
    
    'application': True,
}
