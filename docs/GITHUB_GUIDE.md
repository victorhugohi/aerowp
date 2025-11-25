# Guía para Actualizar el Proyecto en GitHub

Sigue estos pasos cada vez que realices cambios en tu código y quieras subirlos a GitHub.

## 1. Verificar Cambios
Abre la terminal en la carpeta de tu proyecto y escribe:
```bash
git status
```
Esto te mostrará qué archivos han sido modificados (en rojo).

## 2. Preparar los Cambios (Stage)
Para incluir todos los archivos modificados en la próxima "foto" (commit) del proyecto:
```bash
git add .
```

## 3. Guardar los Cambios (Commit)
Crea un punto de guardado con un mensaje descriptivo de lo que hiciste:
```bash
git commit -m "Descripción breve de los cambios"
```
*Ejemplo: `git commit -m "Actualizar el pie de página"`*

## 4. Subir a GitHub (Push)
Envía tus cambios guardados al servidor de GitHub:
```bash
git push
```

---

## Resumen Rápido
```bash
git add .
git commit -m "Tus cambios aquí"
git push
```
