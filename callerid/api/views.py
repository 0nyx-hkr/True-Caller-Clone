from django.shortcuts import render,redirect

from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view,authentication_classes,permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .models import User,SpamNumbers,Contacts
from .serializers import UserSerializer,SpamNumberSerializer,SearchSerializer


@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token,_ = Token.objects.get_or_create(user=user)
        return Response({'data':serializer.data,'token':token.key}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_user(request):
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    user = User.objects.filter(phone_number=phone_number).first()
    if user is None:
        raise AuthenticationFailed("User not found")
    if not user.check_password(password):
        raise AuthenticationFailed("Incorrect Password")
    token, _ = Token.objects.get_or_create(user=user)
    response = Response()
    response.data =  {
        'id':user.id,
    }
    # response.set_cookie(key='token',value=token.key,secure=True)   Uncomment this if you want to send the token in cookies
    return response

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def mark_as_spam(request):
    # token = request.COOKIES.get('token')
    # if not token:
    #     raise AuthenticationFailed("UnAuthenticated")
    serializer = SpamNumberSerializer(data=request.data)
    if serializer.is_valid():
        phone_number = serializer.validated_data.get('phone_number')
        user_spam_number, created = SpamNumbers.objects.get_or_create(user=request.user, phone_number=phone_number)
        if created:
            # If the user_id and phone_number pair was not already present, increment the count of all rows where phone_number matches
            c = SpamNumbers.objects.filter(phone_number=phone_number).count()
            SpamNumbers.objects.filter(phone_number=phone_number).update(count= c)
            return Response({'message': 'Number marked as spam.'})
        else:
            return Response({'message':'Already marked as spam'},status=400)
    else:
        return Response(serializer.errors, status=400)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def search(request):
    serializer = SearchSerializer(data=request.query_params)
    if serializer.is_valid():
        query = serializer.validated_data.get('query')
        # Check if the query is a phone number or a name
        if query.isdigit():
            # It's a phone number
                user = User.objects.filter(phone_number=query)
                if user:
                    spam_likelihood = get_spam_likelihood(query)
                    return Response({'name': user.name, 'phone_number': user.phone_number, 'email': user.email, 'spam_likelihood': spam_likelihood})
                else:
                    contacts = Contacts.objects.filter(phone_number=query)
                    spam_likelihood = get_spam_likelihood(query)
                    return Response([{'name': contact.name, 'phone_number': contact.phone_number, 'spam_likelihood': spam_likelihood} for contact in contacts])
        else:
            # It's a name
            users = User.objects.filter(name__icontains=query)
            contacts = Contacts.objects.filter(name__icontains=query)
            return Response([{'name': user.name, 'phone_number': user.phone_number, 'email': user.email, 'spam_likelihood': get_spam_likelihood(user.phone_number)} for user in users] +
                            [{'name': contact.name, 'phone_number': contact.phone_number, 'spam_likelihood': get_spam_likelihood(contact.phone_number)} for contact in contacts])
    else:
        return Response(serializer.errors, status=400)

def get_spam_likelihood(phone_number):
    try:
        spam_number = SpamNumbers.objects.filter(phone_number=phone_number).first()
        total = User.objects.all().count()
        return spam_number.count/total
    except :
        return 0