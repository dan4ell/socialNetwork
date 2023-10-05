# from functools import wraps
# from django.http import request
#
# def check_themes(func):
#     @wraps(func)
#     def wrapper(request, *args, **kwargs):
#         user = request.user
#         if user.theme == 'Classic':
#             request.theme = user.theme
