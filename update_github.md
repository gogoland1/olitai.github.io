# Pasos para actualizar los cambios en GitHub

Sigue estos pasos para subir los cambios realizados en la tabla periódica de los océanos y la integración en oceano-ritmos:

1. Abre una terminal o línea de comandos en la carpeta `D:\olitai.github.io`

2. Verifica los cambios realizados:
```
git status
```

3. Añade todos los archivos modificados:
```
git add .
```

4. Crea un commit con un mensaje descriptivo:
```
git commit -m "Añadida tabla periódica de los océanos interactiva con información detallada del hidrógeno"
```

5. Sube los cambios a GitHub:
```
git push origin main
```

Si se solicitan credenciales, proporciona tu nombre de usuario y contraseña o token de GitHub.

## Resumen de los cambios realizados:

1. Se añadió una nueva sección en la página oceano-ritmos.html con un enlace a la tabla periódica de los océanos
2. Se mejoró la tabla periódica (tabla-periodica-oceanos-html.html) para hacerla interactiva
3. Se añadió información detallada sobre el hidrógeno en español
4. Se implementó un sistema que permite fácilmente añadir información para más elementos en el futuro

## Para añadir más elementos en el futuro:

Para añadir interactividad a más elementos, como oxígeno, carbono, etc., necesitarás:

1. Añadir un nuevo template dentro del div `elementTemplates` siguiendo el formato:
```html
<div id="simbolo-info">
    <!-- Información detallada del elemento -->
</div>
```

2. Asegúrate de que el ID siga el formato `[simbolo]-info`, donde `[simbolo]` debe estar en minúsculas y coincidir exactamente con el símbolo químico del elemento (por ejemplo, `o-info` para oxígeno, `c-info` para carbono).

El código JavaScript ya está configurado para detectar automáticamente estos elementos y hacer que sean interactivos.
