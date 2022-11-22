Para correr el ejecutable en windows es necesario descargar todos los archivos, ya que Unity necesita que esten todos los archivos para poderse ejecutar.
## Ejemplo archivos
![image](https://user-images.githubusercontent.com/84719490/203210631-31e3f736-fab3-4410-832b-c1bfaf077eee.png)
- Abrir <b>ActividadIntegradora.exe</b>
## NOTA: PARA QUE EL EJECUTABLE CORRA CORRECTAMENTE, ES NECESARIO TENER CORRIENDO EL SERVIDOR DE FLASK
- En el siguiente enlace se encuentra el server y la explicación de como correrlo.
<a href="https://github.com/SergioGonzalez24/Movilidad-Urbana-MSMGC-GPO-302/tree/main/ActividadIntegradora/Server">  Actividad Integradora </a>
- Para correr la flask app:

```
if __name__=='__main__':
    app.run(host="localhost", port=8585, debug=True)
```
you can run it using: 

```
python server_flask.py
```
