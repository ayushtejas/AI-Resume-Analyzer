from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializer import JobDescriptionSerializer, JobDescription, ResumeSerializer, Resume
from .analyzer import process_resume
# Create your views here.
class JobDescriptionApi(APIView):
    def get(self, request):
        queryset = JobDescription.objects.all()
        serializer = JobDescriptionSerializer(queryset, many = True)
        return Response({
            'status': True,
            'data' : serializer.data
        })

class AnalyseResumeAPI(APIView):
    def post(self, request):
        try:
            data = request.data
            if not data.get('job_description'):
                return Response({
                    'status': True,
                    'message' : 'Job Description is required',
                    'data': {}
                })
            serializer = ResumeSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'status': False,
                    'message' : 'error',
                    'data': serializer.errors
                })
            serializer.save()
            _data = serializer.data
            resume_instance = Resume.objects.get(id= _data['id'])
            resume_path = resume_instance.resume.path
            data = process_resume(resume_path, JobDescription.objects.get(id=data.get('job_description')).job_description)
            print(resume_path)
            return Response({
                    'status': True,
                    'message' : 'Resume Analysed',
                    'data': data
                })
        except Exception as e:
            return Response({
                    'status': False,
                    'message' : 'error',
                })
