# 🚀 Flujo de trabajo con Git para el equipo

Este documento explica cómo usaremos **Git y las ramas** en el proyecto **Plataforma Onboarding Créditos PYMES**.

---

## 📌 Ramas principales

- **main** → Código estable, listo para producción.  
- **develop** → Rama de integración, donde se unen las nuevas funcionalidades antes de pasarlas a `main`.  

⚠️ Nunca trabajes directamente en `main` ni en `develop`.

---

## 📌 Flujo de trabajo (resumen)

1. Crear una rama `feature/*` desde `develop`.  
2. Hacer los cambios y commits en tu `feature/*`.  
3. Subir la rama al repositorio.  
4. Abrir una **Pull Request (PR)** hacia `develop`.  
5. Otro miembro del equipo revisa y aprueba.  
6. Hacer merge en `develop`.  
7. Cuando todo esté probado → `develop` se une a `main`.  

---

## 📌 Comandos paso a paso

### 1. Clonar el repositorio
```bash
git clone https://github.com/m41k80/onboarding-credito-pymes.git
cd onboarding-credito-pymes
git branch -a   # Ver ramas disponibles
```

### 2. Crear una nueva rama de feature
```bash
git checkout develop            # Cambiar a develop
git pull origin develop         # Actualizar develop
git checkout -b feature/nombre  # Crear nueva rama
```

Ejemplo:
```bash
git checkout -b feature/frontend-formulario
```

### 3. Hacer commits en tu rama
```bash
git add .
git commit -m "Agregado formulario de solicitud en frontend"
git push origin feature/frontend-formulario
```

### 4. Abrir una Pull Request (PR)
- Ir a GitHub → pestaña **Pull requests** → “New pull request”.  
- Base branch: `develop`  
- Compare branch: `feature/nombre`  
- Agregar título y descripción clara.  

### 5. Actualizar tu entorno antes de nueva tarea
```bash
git checkout develop
git pull origin develop
```

---

## 📌 Reglas del equipo

1. Nunca trabajes directo en `main`.  
2. Siempre crea ramas desde `develop`.  
3. Un commit = un cambio claro y con buen mensaje.  
4. Siempre abrir una Pull Request para cada feature.  
5. Otro miembro debe revisar tu PR antes de hacer merge.  
6. Después de merge, puedes borrar tu rama `feature/*`.

---

## 📌 Ejemplo de flujo completo

```bash
# 1. Cambiar a develop y actualizar
git checkout develop
git pull origin develop

# 2. Crear rama para la tarea
git checkout -b feature/backend-auth

# 3. Hacer cambios y subir
git add .
git commit -m "Implementación login con JWT"
git push origin feature/backend-auth

# 4. Abrir PR en GitHub: feature/backend-auth -> develop
```

---

✅ Con este flujo aseguramos que el código sea ordenado, revisado y estable antes de llegar a producción gracias.
