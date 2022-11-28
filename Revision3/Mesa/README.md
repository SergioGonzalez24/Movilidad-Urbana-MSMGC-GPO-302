## MESA

![Captura de pantalla (369)](https://user-images.githubusercontent.com/84719490/204271108-10b2ba5c-a13b-475f-b2c0-e9728e816a47.png)


- Para correr la flask app:

```
if __name__=='__main__':
    app.run(host="localhost", port=8000, debug=True)
```
you can run it using: 

```
python server_flask.py
```

- To run a flask app on a different host or port:

```
flask run --host=0.0.0.0 --port=8000
```

- Para correr la visualización de mesa:

```
python mesaServer.py
```
