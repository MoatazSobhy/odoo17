{
    'name': 'To-Do List',
    'version': '17.0.0.1.0',
    'category': '',
    'author': 'Moataz Sobhy',
    'depends': ['base','mail', 'contacts'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/todo_task_view.xml',
        'reports/todo_task_report.xml',
     ],
    'assets' : {
        'web.assets_backend' : []
    },
    'application': True,
}
