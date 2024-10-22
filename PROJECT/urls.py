from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

def custom_upload_function(request):
    if request.method == "POST" and request.FILES['file']:
        # Get the uploaded file
        uploaded_file = request.FILES['file']
        
        # Save the file to the default storage (or a custom storage if needed)
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        
        # Return success message or handle the uploaded file as needed
        return HttpResponse(f"File '{filename}' uploaded successfully!")
    
    # Render an upload form for GET requests
    return render(request, 'upload.html')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app_main.urls')),
    path('users/', include('app_users.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),  # CKEditor 5 URLs
    path("upload/", custom_upload_function, name="custom_upload_function"),
] 

# Serve media and static files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
