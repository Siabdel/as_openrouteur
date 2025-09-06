# Créer la structure de base du projet Django
mkdir -p pr_openrouter/llmchat/vue_app/src/components
mkdir -p pr_openrouter/static/{css,js,sounds}
mkdir -p pr_openrouter/templates
mkdir -p pr_openrouter/media

# Créer les fichiers Python de base
touch pr_openrouter/manage.py
touch pr_openrouter/pr_openrouter/__init__.py
touch pr_openrouter/pr_openrouter/settings.py
touch pr_openrouter/pr_openrouter/urls.py
touch pr_openrouter/pr_openrouter/wsgi.py

# Créer les fichiers de l'application Django
touch pr_openrouter/llmchat/__init__.py
touch pr_openrouter/llmchat/admin.py
touch pr_openrouter/llmchat/apps.py
touch pr_openrouter/llmchat/models.py
touch pr_openrouter/llmchat/serializers.py
touch pr_openrouter/llmchat/urls.py
touch pr_openrouter/llmchat/views.py

# Créer les fichiers de l'application Vue.js
touch pr_openrouter/llmchat/vue_app/index.html
touch pr_openrouter/llmchat/vue_app/src/app.js
touch pr_openrouter/llmchat/vue_app/src/styles.css
touch pr_openrouter/llmchat/vue_app/src/components/ApiKeyModal.vue
touch pr_openrouter/llmchat/vue_app/src/components/LeavePageModal.vue
touch pr_openrouter/llmchat/vue_app/src/components/ModelSettingsModal.vue
touch pr_openrouter/llmchat/vue_app/src/components/ChatHistory.vue
touch pr_openrouter/llmchat/vue_app/src/components/ChatMessages.vue
touch pr_openrouter/llmchat/vue_app/src/components/ChatInput.vue

# Créer les fichiers de templates Django
touch pr_openrouter/templates/base.html
touch pr_openrouter/templates/home_page.html

# Créer les fichiers statiques (vous devrez copier les sons manuellement)
touch pr_openrouter/static/css/styles.css
touch pr_openrouter/static/js/vue-app.js
