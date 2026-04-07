from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import KYCApplication
from .serializers import KYCApplicationSerializer, KYCStatusSerializer


class KYCSubmitView(APIView):
    """Submit a new KYC application."""

    def post(self, request):
        serializer = KYCApplicationSerializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save(
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')[:500]
            )
            return Response({
                'success': True,
                'message': 'KYC application submitted successfully.',
                'reference': application.application_reference,
                'status': application.status,
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'errors': serializer.errors,
        }, status=status.HTTP_400_BAD_REQUEST)

    def get_client_ip(self, request):
        x_forwarded = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded:
            return x_forwarded.split(',')[0]
        return request.META.get('REMOTE_ADDR')


class KYCStatusView(APIView):
    """Check the status of a KYC application by reference or email."""

    def get(self, request):
        reference = request.query_params.get('ref')
        email = request.query_params.get('email')

        if not reference and not email:
            return Response({'error': 'Provide ref or email.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            if reference:
                app = KYCApplication.objects.get(application_reference=reference)
            else:
                app = KYCApplication.objects.get(email=email)
            serializer = KYCStatusSerializer(app)
            return Response(serializer.data)
        except KYCApplication.DoesNotExist:
            return Response({'error': 'Application not found.'}, status=status.HTTP_404_NOT_FOUND)
