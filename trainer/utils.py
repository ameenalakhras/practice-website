from fcm_service.utils import send_single_notifications


def send_training_request_push_notification(sender, instance, created, **kwargs):
    """
    this function sends push notifications but we need fcm keys and other configs
    to handle so i'll make it a pass here.
     """
    # there will be
    # user, message_title, message_body):
    message_title = f"new training request by {instance.trainee.user.username}"
    message_body = f"{instance.trainee.user} asked you to train him, do you accept ?"
    # send_single_notifications(instance.trainer.user, message_title, message_body)


def send_training_push_notification_update(training_request, updated_status):
    """
    this function will be ASync to send notification on
    :return:
    """
    if updated_status:
        status = "accepted"
    else:
        status = "rejected"

    message_title = f"training request update"
    message_body = f"{training_request.trainer.user.username} has {status} your training request."
    # send_single_notifications(training_request.trainer.user, message_title, message_body)
