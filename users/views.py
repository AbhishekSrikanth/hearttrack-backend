from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import update_last_login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework import generics, permissions

from users.models import CustomUser
from users.serializers import UserSerializer, AdminCreateUserSerializer


class UserListView(generics.ListAPIView):
    """
    View to list all users in the application.
    This view is restricted to admin users only.
    Attributes:
        queryset (QuerySet): The queryset of all CustomUser objects.
        serializer_class (Serializer): The serializer class used to serialize the user data.
        permission_classes (list): The list of permission classes
          that are required to access this view.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # Only admins can list users
    permission_classes = [permissions.IsAdminUser]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    API view to retrieve, update, or delete a user instance.
    This view allows authenticated users to view, update, or delete their own user details.
    Attributes:
        queryset (QuerySet): QuerySet of all CustomUser instances.
        serializer_class (Serializer): Serializer class used to serialize and deserialize user data.
        permission_classes (list): List of permission classes that determine access to this view.
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    # Authenticated users can view/update themselves
    permission_classes = [permissions.IsAuthenticated]


class AdminCreateUserView(generics.CreateAPIView):
    """
    AdminCreateUserView is a view that allows admin users to create new users.
    Attributes:
        queryset (QuerySet): A queryset of all CustomUser objects.
        serializer_class (Serializer): The serializer class used to validate and save the user data.
        permission_classes (list): A list of permission classes that restrict access to admin users only.
    """
    queryset = CustomUser.objects.all()
    serializer_class = AdminCreateUserSerializer
    # Only admins can create users
    permission_classes = [permissions.IsAdminUser]


class LoginView(APIView):
    """
    LoginView handles user authentication.
    This view allows any user to attempt to log in by providing a username and password.
    If the credentials are valid and the user is active, the user is logged in and their last login time is updated.
    Methods:
        post(request):
            Authenticates the user with the provided username and password.
            Returns a success message if the login is successful.
            Returns an error message if the credentials are invalid or the user is inactive.
    Attributes:
        permission_classes (list): Specifies that any user is allowed to access this view.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle POST request for user login.
        This method authenticates a user based on the provided username and password.
        If the user is authenticated and active, they are logged in and their last login time is updated.
        Appropriate responses are returned based on the authentication and user status.
        Args:
            request (Request): The HTTP request object containing the username and password.
        Returns:
            Response: A Response object with a message indicating the result of the login attempt.
                - HTTP 200 OK: If login is successful.
                - HTTP 403 FORBIDDEN: If the user is inactive.
                - HTTP 401 UNAUTHORIZED: If the username or password is invalid.
        """
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                update_last_login(None, user)
                # Return user details
                return Response({
                    "message": "Login successful",
                    "user": {
                        "id": user.id,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "role": user.role
                    }
                })
            else:
                return Response({"error": "User is inactive"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"error": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    """
    LogoutView handles the user logout process.
    Methods:
        post(request):
            Logs out the user and returns a success message.
            Args:
                request (HttpRequest): The HTTP request object.
            Returns:
                Response: A response object with a success message and HTTP status 200.
    """

    def post(self, request):
        """
        Handle POST request to log out the user.
        This method logs out the user by calling the `logout` function and returns
        a response indicating that the logout was successful.
        Args:
            request (HttpRequest): The HTTP request object.
        Returns:
            Response: A response object with a message indicating successful logout
                      and an HTTP status code 200 (OK).
        """
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
