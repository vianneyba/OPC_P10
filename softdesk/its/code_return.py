from rest_framework.response import Response
from rest_framework import status


USER_NO_EXIST = Response(
    {"message": "user does not exist"},
    status=status.HTTP_404_NOT_FOUND)

PROJECT_NO_EXIST = Response(
    {"message": "project does not exist"},
    status=status.HTTP_404_NOT_FOUND)

PROJECT_DELETE = Response(
    {"message": "project deleted"},
    status=status.HTTP_200_OK)

ISSUE_NOT_EXIST = Response(
    {"message": "issue does not exist"},
    status=status.HTTP_404_NOT_FOUND)

COMMENT_NOT_EXIST = Response(
    {"message": "comment does not exist"},
    status=status.HTTP_404_NOT_FOUND)

COMMENT_DELETE = Response(
    {"message": "comment deleted"}, status=status.HTTP_200_OK)

CONTRIBUTOR_DELETE = Response(
    {"message": "contributor deleted"}, status=status.HTTP_200_OK)

CONTRIBUTOR_ADD = Response(
    {"message": "contributor added"}, status=status.HTTP_200_OK)

ISSUE_DELETE = Response(
    {"message": "issue deleted"}, status=status.HTTP_200_OK)

COMMENT_CREATE = Response(
    {"message": "comment created"}, status=status.HTTP_200_OK)

FORBIDDEN = Response(
    status.HTTP_403_FORBIDDEN)
