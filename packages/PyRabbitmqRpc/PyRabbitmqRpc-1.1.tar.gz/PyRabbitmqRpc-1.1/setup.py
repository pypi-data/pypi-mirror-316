from distutils.core import setup
setup(
  name='PyRabbitmqRpc',         # How you named your package folder (MyLib)
  packages=['PyRabbitmqRpc'],   # Chose the same as "name"
  version='1.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description='This package mainly provides a solution for developers to implement RPC functionality using RabbitMQ.',   # Give a short description about your library
  author='NAIVEKAY',                   # Type in your name
  author_email='genzhengmiaobuhong@163.com',      # Type in your E-Mail
  url='https://github.com/liu-xiaokai/PyRabbitmqRpc',   # Provide either the link to your github or to your website
  download_url='https://github.com/liu-xiaokai/PyRabbitmqRpc/archive/refs/heads/main.zip',    # I explain this later on
  keywords=['RPC', 'RABBITMQ', 'Python'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'validators',       # 可以加上版本号，如validators=1.5.1
          'beautifulsoup4',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
