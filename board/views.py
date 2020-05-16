from board.models import TashkentBoard, TashkentTopic, TashkentMessage, Message, User
from tools import tools
from django.http import HttpResponse


def all_messages(request):
    return HttpResponse(tools.get_messages_view(TashkentBoard.objects.all(), TashkentTopic.objects.all(),
                                                TashkentMessage.objects.all()))


def necessary_messages(request):
    return HttpResponse(tools.get_messages_view(tools.NECESSARY_BOARDS, tools.NECESSARY_TOPICS,
                                                tools.NECESSARY_MESSAGES))


def new_messages(request):
    html = str()
    for board in tools.NECESSARY_BOARDS:
        html += f'<div><div><h1>Board {board.id_board}: {board.name}</h1></div>'
        topics = set(filter(lambda topic: topic.id_board == board, tools.NECESSARY_TOPICS))
        for topic in topics:
            html += f'<div><hr><h2>Topic {topic.id_topic}: {topic.id_first_msg.subject}</h2></div>'
            messages = Message.objects.filter(topic=topic)
            messages = sorted(messages, key=lambda message: message.date_created)
            for message in messages:
                html += f'<div><h3>Message {message.id}: ' \
                        f'parent: {message.parent_msg_id}</h3>' \
                        f'<b>{message.author.full_name}: ' \
                        f'{message.subject}<br>' \
                        f'{message.identifier.object_name}</b><br>' \
                        f'{message.text}</div>'
    return HttpResponse(html)


def users(request):
    html = str()
    i = 1
    for user in User.objects.all():
        html += f'<div><b>{i}. ' \
                f'User {user.id}:</b>' \
                f'<div>full name: {user.full_name}</div>' \
                f'<div>username: {user.username}</div>' \
                f'<div><a href="http://localhost:7000/admin/board/user/{user.id}/change/">EDIT</a></div></div><br>'
        i += 1
    return HttpResponse(html)


def topics_list(request):
    html = str()
    for board in tools.NECESSARY_BOARDS:
        html += f'<div><h3>Board {board.id_board}: {board.name}</h3></div>'
        topics = set(filter(lambda topic: topic.id_board == board, tools.NECESSARY_TOPICS))
        for topic in topics:
            html += f'<div>Topic {topic.id_topic}: {topic.id_first_msg.subject}</div>'
    return HttpResponse(html)
