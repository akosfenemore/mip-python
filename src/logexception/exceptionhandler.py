
'''
Create exceptions based on your inputs. Please follow the tasks below.

 - Capture and handle system exceptions
 - Create custom user-based exceptions
'''


class CustomUserException(Exception):
    def __init__(self, *args, **kwargs):
        print('Check path for file!')
