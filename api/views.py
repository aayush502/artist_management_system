from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.serializers import UserSerializer
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from rest_framework import status

@api_view(['GET'])
def userList(request):
    with connection.cursor() as cursor:
        cursor.execute("select id, first_name, last_name, email, dob,\
                        gender, phone, address, role from users_user")
        users = cursor.fetchall()
        users_dict_list = [
            {
                'id': user[0],
                'first_name': user[1],
                'last_name': user[2],
                'email': user[3],
                'dob': user[4],
                'gender': user[5],
                'phone': user[6],
                'address': user[7],
                'role': user[8],
            }
            for user in users
        ]
        serializer = UserSerializer(users_dict_list, many=True)
        return Response(serializer.data)


def get_user(pk):
    with connection.cursor() as cursor:
        cursor.execute('select first_name, last_name, email, phone, dob, gender, address, role\
                       from users_user where id=%s', [pk])
    return cursor.fetchone()


@api_view(['patch'])
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(instance=user, data=request.data)
    if serializer.is_valid():
        updated_data = {
        'first_name': request.data.get('first_name'),
        'last_name': request.data.get('last_name'),
        'email': request.data.get('email'),
        'dob': request.data.get('dob'),
        'gender': request.data.get('gender'),
        'phone': request.data.get('phone'),
        'address': request.data.get('address'),
        'role': request.data.get('role'),
    }

    # Construct the SQL query with placeholders for the parameters
    query = """
    UPDATE users_user
    SET first_name = %s, last_name = %s, email = %s, dob = %s, gender = %s, phone = %s, address = %s, role = %s
    WHERE id = %s
    """

    # Execute the query with parameter values
    with connection.cursor() as cursor:
        cursor.execute(query, [
            updated_data['first_name'],
            updated_data['last_name'],
            updated_data['email'],
            updated_data['dob'],
            updated_data['gender'],
            updated_data['phone'],
            updated_data['address'],
            updated_data['role'],
            pk,  # User ID to identify the user to be updated
        ])

    if cursor.rowcount > 0:
        return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "No changes made to the user"}, status=status.HTTP_304_NOT_MODIFIED)
    
@api_view(['DELETE'])
def deleteUser(request, pk):
    query = """
        delete from users_user where id = %s    
        """
    with connection.cursor() as cursor:
        cursor.execute(query, [pk])

    if cursor.rowcount > 1:
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "No changes made"}, status=status.HTTP_304_NOT_MODIFIED)


    

