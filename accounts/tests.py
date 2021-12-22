from unittest.mock import patch, MagicMock

from django.test                    import TestCase, Client
from django.core.files.uploadedfile import TemporaryUploadedFile

from rest_framework      import response
from rest_framework.test import APIClient

from accounts.models import Account, Feedback, FeedbackImage

class SignUpSignInTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        client = APIClient()

        # DB: User
        # user
        response = client.post(
            "/accounts/sign-up",
            data = {
                "username": "user",
                "password": "password for user"
            }
        )

        # admin user
        client.post(
            "/accounts/sign-up",
            {
                "username": "admin user",
                "password": "password for admin user"
            }
        )
        admin_user = Account.objects.filter(username="admin user").update(is_staff=True)

    def test_sign_up_201(self):
        client = APIClient()

        response = client.post(
            "/accounts/sign-up",
            data = {
                "username": "new user",
                "password": "password for new user"
            }
        )

        if response.json().get("access"):
            response.json()["access"] = "access token"

        if response.json().get("refresh"):
            response.json()["refresh"] = "refresh token"

        self.assertEqual(
            response.json(),
            {
                "access" : "access token",
                "refresh" : "refresh token"
            }
        )

        self.assertEqual(
            response.status_code, 201
        )

    def test_sign_up_400_account_with_this_username_already_exists(self):
        client = APIClient()

        response = client.post(
            "/accounts/sign-up",
            {
                "username": "user",
                "password": "password for user"
            },
        )

        self.assertEqual(
            response.json(),
            {
                "username": [
                    "account with this username already exists."
                ]
            }
        )

        self.assertEqual(
            response.status_code, 400
        )

    def test_sign_in_200(self):
        client = APIClient()

        response = client.post(
            "/accounts/sign-in",
            {
                "username": "user",
                "password": "password for user"
            }
        )

        if response.json().get("access"):
            response.json()["access"] = "access token"

        if response.json().get("refresh"):
            response.json()["refresh"] = "refresh token"

        self.assertEqual(
            response.json(),
            {
                "access" : "access token",
                "refresh" : "refresh token"
            }
        )

        self.assertEqual(
            response.status_code, 200
        )
    
    def test_sign_in_401_no_active_account_found_with_given_credentials(self):
        client = APIClient()

        response = client.post(
            "/accounts/sign-in",
            {
                "username": "new user",
                "password": "password for new user" 
            }
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "No active account found with the given credentials"
            }
        )

        self.assertEqual(
            response.status_code, 401
        )

    def test_reissue_access_token_with_refresh_token_200(self):
        client = APIClient()

        response_signin = client.post(
            "/accounts/sign-in",
            {
                "username": "user",
                "password": "password for user"
            }
        )
        refresh_token = response_signin.json().get("refresh")

        response = client.post(
            "/accounts/token/refresh",
            {
                "refresh": refresh_token,
            }
        )

        if response.json().get("access"):
            response.json()["access"] = "access token"

        self.assertEqual(
            response.json(),
            {
                "access" : "access token"
            }
        )

        self.assertEqual(
            response.status_code, 200
        )

    def test_reissue_access_token_with_refresh_token_401_with_invalid_refresh_token(self):
        client = APIClient()

        response = client.post(
            "/accounts/token/refresh",
            {
                "refresh": "invalid refresh token",
            }
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "Token is invalid or expired",
                "code": "token_not_valid"
            }
        )

        self.assertEqual(
            response.status_code, 401
        )

    def test_reissue_access_token_with_refresh_token_400_with_no_refresh_token(self):
        client = APIClient()

        response = client.post(
            "/accounts/token/refresh",
            {
                # no refresh token
            }
        )

        self.assertEqual(
            response.json(),
            {
                "refresh": [
                    "This field is required."
                ]
            }
        )

        self.assertEqual(
            response.status_code, 400
        )

    def test_authentication_200_passes_permssion_classes_isauthenticated_with_access_token(self):
        client = APIClient()

        response_signin = client.post(
            "/accounts/sign-in",
            {
                "username": "user",
                "password": "password for user"
            }
        )
        access_token = response_signin.json().get("access")

        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)
        response = client.get(
            '/accounts/permission-classes-isauthenticated'
        )

        self.assertEqual(
            response.json(), {}
        )

        self.assertEqual(
            response.status_code, 200
        )

    def test_authentication_401_fails_permssion_classes_isauthenticated_with_invalid_access_token(self):
        client = APIClient()

        response_signin = client.post(
            "/accounts/sign-in",
            {
                "username": "user",
                "password": "password for user"
            }
        )
        access_token         = response_signin.json().get("access")
        invalid_access_token = access_token[:len(access_token)//2]

        client.credentials(HTTP_AUTHORIZATION="Bearer " + invalid_access_token)
        response = client.get(
            '/accounts/permission-classes-isauthenticated'
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "Given token not valid for any token type",
                "code": "token_not_valid",
                "messages": [
                    {
                        "token_class": "AccessToken",
                        "token_type": "access",
                        "message": "Token is invalid or expired"
                    }
                ]
            }
        )

        self.assertEqual(
            response.status_code, 401
        )

    def test_authentication_401_fails_permssion_classes_isauthenticated_with_invalid_type_access_token(self):
        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION="Bearer " + "invalid type access token")
        response = client.get(
            '/accounts/permission-classes-isauthenticated'
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "Authorization header must contain two space-delimited values",
                "code": "bad_authorization_header"
            }
        )

        self.assertEqual(
            response.status_code, 401
        )

    def test_authentication_401_fails_permssion_classes_isauthenticated_with_no_access_token(self):
        client = APIClient()

        # no access token
        client.credentials()
        response = client.get(
            '/accounts/permission-classes-isauthenticated'
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "Authentication credentials were not provided."
            }
        )

        self.assertEqual(
            response.status_code, 401
        )

    def test_authorization_200_passes_permission_classes_allowany_with_any_user(self):
        client = APIClient()

        # unauthenticated any user
        client.credentials()

        # permission classes: allowany
        response = client.get(
            '/accounts/permission-classes-allowany'
        )

        self.assertEqual(
            response.json(), {}
        )

        self.assertEqual(
            response.status_code, 200
        )

    def test_authorizaition_200_passes_permission_classes_isauthenticated_with_authenticated_user(self):
        client = APIClient()

        # authenticated user
        response_signin = client.post(
            "/accounts/sign-in",
            {
                "username": "user",
                "password": "password for user"
            }
        )
        access_token = response_signin.json().get("access")
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        # permission classes: isauthenticated
        response = client.get(
            '/accounts/permission-classes-isauthenticated'
        )

        self.assertEqual(
            response.json(), {}
        )

        self.assertEqual(
            response.status_code, 200
        )

    def test_authentication_200_passes_permission_classes_isadminuser_with_admin_user(self):
        client = APIClient()

        # admin user
        response_signin = client.post(
            "/accounts/sign-in",
            {
                "username": "admin user",
                "password": "password for admin user"
            }
        )
        access_token = response_signin.json().get("access")
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        # permission classes: isadminuser
        response = client.get(
            '/accounts/permission-classes-isadminuser'
        )

        self.assertEqual(
            response.json(), {}
        )

        self.assertEqual(
            response.status_code, 200
        ) 

    def test_authorization_403_fails_permission_classes_isadminuser_with_authenticated_user(self):
        client = APIClient()

        # authenticated user
        response_signin = client.post(
            "/accounts/sign-in",
            {
                "username": "user",
                "password": "password for user"
            }
        )
        access_token = response_signin.json().get("access")
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        # permission classes: isadminuser
        response = client.get(
            '/accounts/permission-classes-isadminuser'
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "You do not have permission to perform this action."
            }
        )

        self.assertEqual(
            response.status_code, 403
        )

class FeedbackTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        client = APIClient()
        
        # DB: User
        client.post(
            "/accounts/sign-up",
            data = {
                "username" : "user",
                "password" : "password for user"
            }
        )
        user = Account.objects.get(username="user")

        # DB: Feedback
        for i in range(1,4):
            feedback = Feedback.objects.create(
                tag     = "tag/" + str(i),
                title   = "title/" + str(i),
                content = "content/" + str(i),
                account = user
            )

            for j in range(0,2):
                FeedbackImage.objects.create(
                    image_path = "image_path/" + str((i*2)-1+j),
                    feedback   = feedback
                )

    def test_feedback_get_queryset_200(self):
        client = APIClient()

        response_signin = client.post(
            "/accounts/sign-in",
            data = {
                "username" : "user",
                "password" : "password for user"
            }
        )
        access_token = response_signin.json().get("access")
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        response = client.get(
            "/accounts/feedback",
        )

        for r in response.json():
            if r.get("create_at"):
                r["create_at"] = "create_at"

            if r.get("update_at"):
                r["update_at"] = "update_at"

        self.assertEqual(
            response.json(),
            [
                {
                    "id" : 1,
                    "tag": "tag/1",
                    "title": "title/1",
                    "content": "content/1",
                    "feedbackimage_set" : [
                        {
                            "id": 1,
                            "image_path": "image_path/1"
                        },
                        {
                            "id": 2,
                            "image_path": "image_path/2"
                        }
                    ],
                    "create_at": "create_at",
                    "update_at": "update_at",
                    "delete_at": None,
                    "is_deleted": False,
                    "is_solved": False
                },
                {
                    "id" : 2,
                    "tag": "tag/2",
                    "title": "title/2",
                    "content": "content/2",
                    "feedbackimage_set" : [
                        {
                            "id": 3,
                            "image_path": "image_path/3"
                        },
                        {
                            "id": 4,
                            "image_path": "image_path/4"
                        }
                    ],
                    "create_at": "create_at",
                    "update_at": "update_at",
                    "delete_at": None,
                    "is_deleted": False,
                    "is_solved": False
                },
                {
                    "id" : 3,
                    "tag": "tag/3",
                    "title": "title/3",
                    "content": "content/3",
                    "feedbackimage_set" : [
                        {
                            "id": 5,
                            "image_path": "image_path/5"
                        },
                        {
                            "id": 6,
                            "image_path": "image_path/6"
                        }
                    ],
                    "create_at": "create_at",
                    "update_at": "update_at",
                    "delete_at": None,
                    "is_deleted": False,
                    "is_solved": False
                }
            ]
        )

        self.assertEqual(
            response.status_code, 200
        )

    def test_feedback_get_object_200(self):
        client = APIClient()

        response_signin = client.post(
            "/accounts/sign-in",
            data = {
                "username" : "user",
                "password" : "password for user"
            }
        )
        access_token = response_signin.json().get("access")
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        response = client.get(
            "/accounts/feedback/1",
        )

        if response.json().get("create_at"):
            response.json()["create_at"] = "create_at"

        if response.json().get("update_at"):
            response.json()["update_at"] = "update_at"

        self.assertEqual(
            response.json(),
            {
                "id" : 1,
                "tag": "tag/1",
                "title": "title/1",
                "content": "content/1",
                "feedbackimage_set" : [
                    {
                        "id": 1,
                        "image_path": "image_path/1"
                    },
                    {
                        "id": 2,
                        "image_path": "image_path/2"
                    }
                ],
                "create_at": "create_at",
                "update_at": "update_at",
                "delete_at": None,
                "is_deleted": False,
                "is_solved": False
            }
        )

        self.assertEqual(
            response.status_code, 200
        )

    def test_feedback_get_object_not_found_404(self):
        client = APIClient()

        response_signin = client.post(
            "/accounts/sign-in",
            data = {
                "username" : "user",
                "password" : "password for user"
            }
        )
        access_token = response_signin.json().get("access")
        client.credentials(HTTP_AUTHORIZATION="Bearer " + access_token)

        response = client.get(
            "/accounts/feedback/4",
        )

        self.assertEqual(
            response.json(),
            {
                "detail" : "Not found."
            }
        )

        self.assertEqual(
            response.status_code, 404
        )

    @patch("accounts.utils.BaseS3.api_post", return_value=None)
    def test_feedback_post_201(self, mocked_api_post):
        client   = APIClient()
        user     = Account.objects.filter(username="user").first()
        image_1  = TemporaryUploadedFile("image.png", content_type="image/png", size=10, charset="utf8mb4")
        image_2  = TemporaryUploadedFile("image.png", content_type="image/png", size=10, charset="utf8mb4")

        client.force_authenticate(user=user)
        response = client.post(
            "/accounts/feedback",
            data = {
                "tag" : "new_tag",
                "title" : "new_title",
                "content" : "new_content",
                "feedbackimage_set_create" : [image_1, image_2]
            }
        )

        if response.json().get("create_at"):
            response.json()["create_at"] = "create_at"
        if response.json().get("update_at"):
            response.json()["update_at"] = "update_at"

        for r in response.json().get("feedbackimage_set"):
            if r.get("image_path"):
                r["image_path"] = "image_path"

        self.assertEqual(
            response.json(),
            {
                "id": 4,
                "tag": "new_tag",
                "title": "new_title",
                "content": "new_content",
                "feedbackimage_set" : [
                    {
                        "id": 7,
                        "image_path": "image_path"
                    },
                    {
                        "id": 8,
                        "image_path": "image_path"
                    }
                ],
                "create_at": "create_at",
                "update_at": "update_at",
                "delete_at": None,
                "is_deleted": False,
                "is_solved": False
            }
        )

        self.assertEqual(
            response.status_code, 201
        )

    @patch("accounts.views.BaseS3.api_post", return_value=None)
    def test_feedback_post_database_constraint_error_400(self, mocked_api_post):
        client = APIClient()
        user   = Account.objects.filter(username="user").first()

        client.force_authenticate(user=user)
        response = client.post(
            "/accounts/feedback",
            data = {
                "tag": "table - feedback, column - tag, constraint - max length 20, error - max_length exceeds",
                "title": "table - feedback, column - title, constraint - max length 100, error - max_length exceeds",
                "content": """table - feedback, column - title, constraint - max length 100, error - max_length exceeds,
                test data - This is test.This is test.This is test.This is test.This is test.This is test.
                This is test.This is test.This is test.This is test.This is test.This is test.This is test."""
            }
        )

        self.assertEqual(
            response.json(),
            {
                "tag": [
                    "Ensure this field has no more than 20 characters."
                ],
                "title": [
                    "Ensure this field has no more than 20 characters."
                ],
                "content": [
                    "Ensure this field has no more than 100 characters."
                ]
            }
        )

        self.assertEqual(
            response.status_code, 400
        )

    @patch("accounts.views.BaseS3.api_post", return_value=None)
    @patch("accounts.views.BaseS3.api_delete", return_value=None)
    def test_feedback_put_200_create_feedbackimage(self, mocked_api_post, mocked_api_delete):
        client   = APIClient()
        user     = Account.objects.filter(username="user").first()
        image_1  = TemporaryUploadedFile("image.png", content_type="image/png", size=10, charset="utf8mb4")
        image_2  = TemporaryUploadedFile("image.png", content_type="image/png", size=10, charset="utf8mb4")

        client.force_authenticate(user=user)
        response = client.put(
            "/accounts/feedback/1",
            data = {
                "tag" : "updated_tag",
                "title" : "updated_tag",
                "content" : "updated_tag",
                "feedbackimage_set_create" : [image_1, image_2]
            }
        )

        if response.json().get("create_at"):
            response.json()["create_at"] = "create_at"
        if response.json().get("update_at"):
            response.json()["update_at"] = "update_at"

        for r in response.json().get("feedbackimage_set"):
            if r.get("image_path"):
                if r.get("id") in [9, 10]:
                    r["image_path"] = "image_path"

        self.assertEqual(
            response.json(),
            {
                "id": 1,
                "tag": "updated_tag",
                "title": "updated_tag",
                "content": "updated_tag",
                "feedbackimage_set":[
                    {
                        "id": 1,
                        "image_path": "image_path/1"
                    },
                    {
                        "id": 2,
                        "image_path": "image_path/2"
                    },
                    {
                        "id": 9,
                        "image_path": "image_path"
                    },
                    {
                        "id": 10,
                        "image_path": "image_path"
                    }
                ],
                "create_at": "create_at",
                "update_at": "update_at",
                "delete_at": None,
                "is_deleted": False,
                "is_solved": False
            }
        )

        self.assertEqual(
            response.status_code, 200
        )
    
    @patch("accounts.views.BaseS3.api_post", return_value=None)
    @patch("accounts.views.BaseS3.api_delete", return_value=None)
    def test_feedback_put_200_delete_feedbackimage(self, mocked_api_post, mocked_api_delete):
        client = APIClient()
        user   = Account.objects.filter(username="user").first()
        
        client.force_authenticate(user=user)
        response = client.put(
            "/accounts/feedback/2",
            data = {
                "tag" : "updated_tag",
                "title" : "updated_tag",
                "content" : "updated_tag",
                "feedbackimage_set_delete" : [
                    {
                        "id" : 3,
                        "image_path" : "image_path/3"
                    },
                ]
            },
            format = "json"
        )

        if response.json().get("create_at"):
            response.json()["create_at"] = "create_at"
        if response.json().get("update_at"):
            response.json()["update_at"] = "update_at"

        self.assertEqual(
            response.json(),
            {
                "id": 2,
                "tag": "updated_tag",
                "title": "updated_tag",
                "content": "updated_tag",
                "feedbackimage_set":[
                    {
                        "id": 4,
                        "image_path": "image_path/4"
                    }
                ],
                "create_at": "create_at",
                "update_at": "update_at",
                "delete_at": None,
                "is_deleted": False,
                "is_solved": False
            }
        )

        self.assertEqual(
            response.status_code, 200
        )

    @patch("accounts.views.BaseS3.api_post", return_value=None)
    @patch("accounts.views.BaseS3.api_delete", return_value=None)
    def test_feedback_put_not_found_404(self, mocked_api_post, mocked_api_delete):
        client = APIClient()
        user   = Account.objects.filter(username="user").first()

        client.force_authenticate(user=user)
        response = client.put(
            "/accounts/feedback/5",
            data = {
                "tag" : "updated_tag",
                "title" : "updated_tag",
                "content" : "updated_tag",
                "feedbackimage_set_create" : [],
                "feedbackimage_set_delete" : []
            },
            format = "json"
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "Not found"
            }
        )

        self.assertEqual(
            response.status_code, 404
        )

    @patch("accounts.utils.BaseS3.api_delete", return_value=None)
    def test_feedback_delete_200(self, mocked_api_delete):
        client = APIClient()
        user   = Account.objects.filter(username="user").first()

        client.force_authenticate(user=user)
        response = client.delete(
            "/accounts/feedback/1"
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "Deleted"
            }
        )

        self.assertEqual(
            response.status_code, 200
        )

    @patch("accounts.utils.BaseS3.api_delete", return_value=None)
    def test_feedback_delete_404_not_found(self, mocked_api_delete):
        client = APIClient()
        user   = Account.objects.filter(username="user").first()

        client.force_authenticate(user=user)
        response = client.delete(
            "/accounts/feedback/5"
        )

        self.assertEqual(
            response.json(),
            {
                "detail": "Not found"
            }
        )

        self.assertEqual(
            response.status_code, 404
        )