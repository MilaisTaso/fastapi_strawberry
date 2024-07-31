from starlette import status

from src.errors.messages.base import BaseMessage


class ErrorMessage:
    class INTERNAL_SERVER_ERROR(BaseMessage):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = "システムエラーが発生しました、管理者に問い合わせてください"

    class OBJECT_INITIALIZE_FAILED(BaseMessage):
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        message = "{}の初期化に失敗しました。"

    class NOT_FOUND(BaseMessage):
        message = "{}が見つかりません"

    class ID_NOT_FOUND(BaseMessage):
        status_code = status.HTTP_404_NOT_FOUND
        message = "このidは見つかりません"

    class PARAM_IS_NOT_SET(BaseMessage):
        message = "{}がセットされていません"

    class ALREADY_DELETED(BaseMessage):
        message = "既に削除済です"

    class SOFT_DELETE_NOT_SUPPORTED(BaseMessage):
        message = "論理削除には未対応です"

    class PERMISSION_ERROR(BaseMessage):
        message = "実行権限がありません"

    class AUTHENTICATION_FAILED(BaseMessage):
        status_code = status.HTTP_403_FORBIDDEN
        message = "ユーザー認証に失敗しました"

    class ENTITY_ALREADY_EXISTS(BaseMessage):
        status_code = status.HTTP_400_BAD_REQUEST
        message = "{}はすでに存在しています"

    class WRONG_PASSWORD(BaseMessage):
        status_code = status.HTTP_400_BAD_REQUEST
        message = "パスワードが違います"
