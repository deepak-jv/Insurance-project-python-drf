from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from User.permission import CustomPermission
from User.renderers import UserRenderer
from User.serializers import UserProfileSerializer
from rest_framework import viewsets, status
from .serializers import *
from User.views import UserDetailView
from .models import *


class PolicyViewSet(viewsets.ModelViewSet):
    permission_classes = [CustomPermission]
    queryset = Policy.objects.all()
    serializer_class = PolicySerializer
    renderer_classes = [UserRenderer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        created_instance = serializer.instance
        serialized_data = serializer.data

        serialized_data['User'] = {
            'id': created_instance.user.id,
            'email': created_instance.user.email,
            'name': created_instance.user.name,
            'role': created_instance.user.role,
            'mob_num': created_instance.user.mob_num
        }
        serialized_data['message'] = {
            'success': True
        }
        return Response(serialized_data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        user = None
        for s in serializer.data:
            user_id = s['user']
            user = UserDetailView.get_object(serializer, user_id)
            user = UserProfileSerializer(user)
        response_data = super(PolicyViewSet, self).list(request, *args, **kwargs)

        data = {
            "message": "Success",

            "policy": [{
                "id": obj['id'],
                "name": obj['name'],
                "description": obj['description'],
                "user": user.data
            } for obj in response_data.data]
        }

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        path_user_id = kwargs.get('profile_pk')
        pk = serializer.data['user']
        try:
            if path_user_id != pk:
                raise Exception("user doesn't have the required policy")

            user = UserDetailView.get_object(serializer, pk)
            user = UserProfileSerializer(user)

            # response_data = super(PolicyViewSet, self).list(request, *args, **kwargs)

            data = {
                "message": "Success",

                "policy": {
                    "id": serializer.data['id'],
                    "name": serializer.data['name'],
                    "description": serializer.data['description'],
                    "user": user.data
                }
            }

            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Object deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class Claim(viewsets.ModelViewSet):
    permission_classes = [CustomPermission]
    queryset = Claim.objects.all()
    serializer_class = ClaimSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        serializer_instance = serializer.instance
        serializer_data = serializer.data

        serializer_data['policy'] = {
            'id': serializer_instance.policy.id,
            'name': serializer_instance.policy.name,
            'description': serializer_instance.policy.description,
            'user': {
                'id': serializer_instance.policy.user.id,
                'email': serializer_instance.policy.user.email,
                'name': serializer_instance.policy.user.name,
                'role': serializer_instance.policy.user.role,
                'mob_num': serializer_instance.policy.user.mob_num
            }
        }
        serializer_data['message'] = {
            'success': True
        }

        return Response(serializer_data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        policy = None
        user = None
        for s in serializer.data:
            policy_id = s['policy']

            policy = Policy.objects.get(id=policy_id)
            policy = PolicySerializer(policy)

            user_id = policy.data['user']
            user = UserDetailView.get_object(serializer, user_id)
            user = UserProfileSerializer(user)

        response_data = super(Claim, self).list(request, *args, **kwargs)

        data = {
            "message": "Success",

            "claim": [{
                "id": claim['id'],
                "name": claim['name'],
                "description": claim['description'],
                "policy":
                    {
                        'id': policy.data['id'],
                        'name': policy.data['name'],
                        'description': policy.data['description'],
                        'user': user.data
                    }

            } for claim in response_data.data]
        }

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        claim = serializer.data
        policy_id = int(claim['policy'])
        policy = Policy.objects.get(id=policy_id)
        policy_serializer = PolicySerializer(policy)
        pk = policy_serializer.data['user']
        user = UserDetailView.get_object(serializer, pk)

        try:
            if user.id != pk:
                raise Exception("user doesn't have the required policy")

            user = UserDetailView.get_object(serializer, pk)
            user = UserProfileSerializer(user)
            response_data = super(Claim, self).list(request, *args, **kwargs)

            data = {
                "message": "Success",

                "claim": [{
                    "id": obj['id'],
                    "name": obj['name'],
                    "description": obj['description'],
                    "policy":
                        {
                            'id': policy_serializer.data['id'],
                            'name': policy_serializer.data['name'],
                            'description': policy_serializer.data['description'],
                            'user': user.data
                        }

                } for obj in response_data.data]
            }

            return Response(data)
        except Exception as e:
            return Response({'error': str(e)}, status=400)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Object deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class Payment(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        serializer = self.get_serializer(queryset, many=True)
        policy = None
        user = None
        for s in serializer.data:
            policy_id = s['policy']

            policy = Policy.objects.get(id=policy_id)
            policy = PolicySerializer(policy)

            user_id = policy.data['user']
            user = UserDetailView.get_object(serializer, user_id)
            user = UserProfileSerializer(user)

        response_data = super(Payment, self).list(request, *args, **kwargs)

        data = {
            "message": "Success",

            "payment": [{
                "id": payment['id'],
                "amount": payment['amount'],
                "policy":
                    {
                        'id': policy.data['id'],
                        'name': policy.data['name'],
                        'description': policy.data['description'],
                        'user': user.data
                    }

            } for payment in response_data.data]
        }

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        payment = serializer.data
        policy_id = int(payment['policy'])
        policy = Policy.objects.get(id=policy_id)
        policy_serializer = PolicySerializer(policy)
        pk = policy_serializer.data['user']
        user = UserDetailView.get_object(serializer, pk)
        user = UserProfileSerializer(user)
        response_data = super(Payment, self).list(request, *args, **kwargs)

        data = {
            "message": "Success",

            "payment": [{
                "id": payment['id'],
                "amount": payment['amount'],
                "policy":
                    {
                        'id': policy_serializer.data['id'],
                        'name': policy_serializer.data['name'],
                        'description': policy_serializer.data['description'],
                        'user': user.data
                    }

            } for obj in response_data.data]
        }

        return Response(data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'Object deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
