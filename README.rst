Webapp Manifest Generator
#########################

This is a tiny project to generate webapp.manifest files, served with the
appropriate Content-Type, on a multidomain server.

Make it run
===========

Create a virtualenv for it::

    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt
    $ python generator/web.py

Deploy
======

If you want to deploy this, you can use the following configuration:

A DNS entry in bind::
    
    *.webapp                    IN  A      your ip

A supervisor file::

    [program:webapp.lolnet.org]
    command=/path/to/venv/bin/gunicorn -c /path/to/config.conf generator.web:app
    directory=/path/to/git/repo/
    user=www-data
    autostart=true
    autorestart=true
    redirect_stderr=True


A gunicorn file::

    backlog = 2048
    daemon = False
    debug = True
    workers = 3
    logfile = "/home/www/logs/yourlog.gunicorn.log
    loglevel = "info"
    bind = "unix:/home/www/yourhost.org/gunicorn.sock"

An nginx file::

   server {                                                               
        server_name *.yourhost.org;                               
        keepalive_timeout 5;                                           
                                                                       
        location /static/ {                                            
                alias   /path/to/git/static/;           
        }                                                                    
                                                                             
        location / {                                                         
                proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for; 
                proxy_set_header Host $http_host;                            
                proxy_redirect off;                                          
                proxy_connect_timeout 90;                                    
                proxy_send_timeout 180;                                      
                proxy_read_timeout 180;                                      
                proxy_buffer_size 16k;                                       
                proxy_buffers 8 16k;                                         
                proxy_busy_buffers_size 32k;                                 
                proxy_intercept_errors on;                                   
                if (!-f $request_filename) {                                 
                    proxy_pass http://webapp_backend;                        
                    break;                                                   
                }                                                            
        }                                                                    
    }                                                                            
                                                                                 
    upstream webapp_backend {                                                    
            server unix:/path/to/the/socket.sock;               
    }                                                                            
