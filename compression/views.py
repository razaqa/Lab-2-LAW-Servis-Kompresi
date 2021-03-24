from .serializers import ZipFileSerializer
from django.conf import settings
from django.http import HttpResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

import io
import os
import tarfile

class FileCompressionAPIView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request, format=None):
        serializer = ZipFileSerializer(data=request.data)

        if serializer.is_valid():
            saved_file = serializer.save()
            saved_filename = saved_file.__dict__["file"]
            saved_file_directory = '%s\\%s' % (settings.MEDIA_ROOT, saved_filename)

            file = request.data["file"]
            full_filename = file.name
            filename, base = os.path.splitext(full_filename)
            zipname = '%s.tar.gz' % (filename)

            file_bytes = io.BytesIO()
            tar = tarfile.open(zipname, "w:gz", file_bytes)
            tar.add(saved_file_directory, arcname=full_filename, recursive=False)
            tar.close()

            response = HttpResponse(file_bytes.getvalue(), content_type='application/x-gzip')
            response['Content-Disposition'] = 'attachment; filename="{0}"'.format(zipname)
            
            return response

        else:
           
            return Response(data={
                'message': "please use correct request (form data with 'file' field)"
            }, status=400)