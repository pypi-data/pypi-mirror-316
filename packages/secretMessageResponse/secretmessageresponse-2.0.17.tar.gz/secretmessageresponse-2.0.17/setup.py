from distutils.core import setup
 
setup(
    name='secretMessageResponse',  
    version='2.0.17',  
    description='此库为接收消息专用，使用前请更新库同步最新消息，上级会将回复信息更新到最新库中。此库 只查看回复消息，不发送消息。',  
    author='Dylan', 
    author_email='Dylan@secretplace.com',
    py_modules=['secretMessageResponse.printMessage'],  
)