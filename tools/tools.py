from board.models import TashkentBoard, TashkentTopic, TashkentMessage, TashkentMember, Message, User, Identifier
import re
from datetime import datetime
import json


def get_messages_view(all_boards, all_topics, all_messages):
    html = str()
    for board in all_boards:
        html += f'<div><div><h1>Board {board.id_board}: {board.name}</h1></div>'
        topics = set(filter(lambda topic: topic.id_board == board, all_topics))
        for topic in topics:
            html += f'<div><hr><br><h2>Topic {topic.id_topic}: {topic.id_first_msg.subject}</h2></div><br>'
            messages = set(filter(lambda message: message.id_topic == topic, all_messages))
            messages = sorted(messages, key=lambda message: message.postertime)
            for message in messages:
                html += f'<div><b>Message {message.id_msg}: ' \
                        f'subject: {message.subject}, ' \
                        f'author: {message.id_member.realname}, ' \
                        f'modifier: {message.modifiedname}, ' \
                        f'date: {message.postertime}</b><br>' \
                        f'{message.body}</div><br>'
    return html


NECESSARY_BOARDS_IDS = {2, 3, 6, 7, 9, 10, 12, 14, 16}
UNNECESSARY_TOPICS_IDS = {14, 15, 68, 110, 3, 57, 77, 109, 35, 40, 84, 42, 85, 86, 111, 116, 49, 52, 56, 73, 118, 132,
                          112, 120, 121, 128, 141, 144, 145}
UNNECESSARY_TOPICS = set(topic for topic in TashkentTopic.objects.all() if topic.id_topic in UNNECESSARY_TOPICS_IDS)
NECESSARY_BOARDS = set(board for board in TashkentBoard.objects.all() if board.id_board in NECESSARY_BOARDS_IDS)
NECESSARY_TOPICS = set(topic for topic in TashkentTopic.objects.all() if topic.id_board in NECESSARY_BOARDS) \
                   - UNNECESSARY_TOPICS
NECESSARY_MESSAGES = set(message for message in TashkentMessage.objects.all() if message.id_topic in NECESSARY_TOPICS)


def get_necessary_members(necessary_messages):
    necessary_members = set()
    for message in necessary_messages:
        necessary_members.add(message.id_member)
        if message.modifiedname != '':
            if message.modifiedname not in [member.realname for member in TashkentMember.objects.all()]:
                print('ERROR: Member', message.modifiedname, 'is not in database')
            else:
                necessary_members.add(TashkentMember.objects.get(realname=message.modifiedname))
    return necessary_members


NECESSARY_MEMBERS = get_necessary_members(NECESSARY_MESSAGES)


def encoding_convert(text):
    patterns = {
        '&#1040;': 'А',
        '&#1072;': 'а',
        '&#1041;': 'Б',
        '&#1073;': 'б',
        '&#1042;': 'В',
        '&#1074;': 'в',
        '&#1043;': 'Г',
        '&#1075;': 'г',
        '&#1044;': 'Д',
        '&#1076;': 'д',
        '&#1045;': 'Е',
        '&#1077;': 'е',
        '&#1025;': 'Ё',
        '&#1105;': 'ё',
        '&#1046;': 'Ж',
        '&#1078;': 'ж',
        '&#1047;': 'З',
        '&#1079;': 'з',
        '&#1048;': 'И',
        '&#1080;': 'и',
        '&#1049;': 'Й',
        '&#1081;': 'й',
        '&#1050;': 'К',
        '&#1082;': 'к',
        '&#1051;': 'Л',
        '&#1083;': 'л',
        '&#1052;': 'М',
        '&#1084;': 'м',
        '&#1053;': 'Н',
        '&#1085;': 'н',
        '&#1054;': 'О',
        '&#1086;': 'о',
        '&#1055;': 'П',
        '&#1087;': 'п',
        '&#1056;': 'Р',
        '&#1088;': 'р',
        '&#1057;': 'С',
        '&#1089;': 'с',
        '&#1058;': 'Т',
        '&#1090;': 'т',
        '&#1059;': 'У',
        '&#1091;': 'у',
        '&#1060;': 'Ф',
        '&#1092;': 'ф',
        '&#1061;': 'Х',
        '&#1093;': 'х',
        '&#1062;': 'Ц',
        '&#1094;': 'ц',
        '&#1063;': 'Ч',
        '&#1095;': 'ч',
        '&#1064;': 'Ш',
        '&#1096;': 'ш',
        '&#1065;': 'Щ',
        '&#1097;': 'щ',
        '&#1066;': 'Ъ',
        '&#1098;': 'ъ',
        '&#1067;': 'Ы',
        '&#1099;': 'ы',
        '&#1068;': 'Ь',
        '&#1100;': 'ь',
        '&#1069;': 'Э',
        '&#1101;': 'э',
        '&#1070;': 'Ю',
        '&#1102;': 'ю',
        '&#1071;': 'Я',
        '&#1103;': 'я',
        '&#160;': '',
        '&#039;': '\'',
        '&#91;': '[',
        '&#8470;': '№',
        '&#221;': 'Ý',
        '&#65533;': '�',
        '&quot;': '"',
        '&lt;': '<',
        '&gt;': '>',
        '&amp;': '&',
        '&nbsp;': ' ',
    }
    keys = re.findall(r'&#\d{5};', text)
    keys.extend(re.findall(r'&#\d{4};', text))
    keys.extend(re.findall(r'&#\d{3};', text))
    keys.extend(re.findall(r'&#\d{2};', text))
    for key in keys:
        replacement = patterns.get(key)
        if replacement is not None:
            text = text.replace(key, replacement)
    return text


def messages_encoding_convert():
    messages = TashkentMessage.objects.all()
    for message in messages:
        message.body = encoding_convert(message.body)
        message.subject = encoding_convert(message.subject)
    TashkentMessage.objects.bulk_update(messages, ['body', 'subject'])


COMBINED_MESSAGES = set(message for message in NECESSARY_MESSAGES
                        if re.search(r'\[color=blue]|\[color=navy]|\[color=green]', message.body))
UNCOMBINED_MESSAGES = NECESSARY_MESSAGES - COMBINED_MESSAGES


def create_new_messages():
    new_messages = set()
    id_counter = 1
    for message in UNCOMBINED_MESSAGES:
        new_messages.add(Message(
            id=id_counter,
            parent_msg_id=id_counter,
            author=message.id_member,
            text=message.body,
            date_created=message.postertime,
            subject=message.subject,
            topic=message.id_topic,
            board=message.id_board
        ))
        id_counter += 1
    teacher_message_marker = r'(?<=\[color=blue]).+?(?=\[/color])|' \
                             r'(?<=\[color=navy]).+?(?=\[/color])|' \
                             r'(?<=\[color=green]).+?(?=\[/color])'
    for message in COMBINED_MESSAGES:
        student_begins = not bool(re.match(r'\[color=blue]|\[color=navy]|\[color=green]', message.body))
        student_messages = re.split(teacher_message_marker, message.body)
        for i in range(len(student_messages)):
            if re.match(r'\[/color]', student_messages[i]):
                student_messages[i] = student_messages[i][8:]
            if re.search(r'\[color=blue]$|\[color=navy]$', student_messages[i]):
                student_messages[i] = student_messages[i][:-12]
            if re.search(r'\[color=green]$', student_messages[i]):
                student_messages[i] = student_messages[i][:-13]
        teacher_messages = re.findall(teacher_message_marker, message.body)
        splitted_messages = list()
        last_index = 0
        for i in range(min(len(teacher_messages), len(student_messages))):
            if student_begins:
                splitted_messages.append(student_messages[i])
                splitted_messages.append(teacher_messages[i])
            else:
                splitted_messages.append(teacher_messages[i])
                splitted_messages.append(student_messages[i])
            last_index = i
        if len(student_messages) > last_index + 1:
            splitted_messages.extend(student_messages[last_index + 1:])
        if len(teacher_messages) > last_index + 1:
            splitted_messages.extend(teacher_messages[last_index + 1:])
        while '' in splitted_messages:
            splitted_messages.remove('')
        for i in range(len(splitted_messages)):
            if splitted_messages[i] in teacher_messages and message.modifiedname != '':
                id_member = TashkentMember.objects.get(realname=message.modifiedname)
            else:
                id_member = message.id_member
            new_messages.add(Message(
                id=id_counter,
                parent_msg_id=id_counter - i,
                author=id_member,
                text=splitted_messages[i],
                date_created=message.postertime + i,
                subject=message.subject,
                topic=message.id_topic,
                board=message.id_board
            ))
            id_counter += 1
    Message.objects.bulk_create(new_messages)


def create_users(necessary_members):
    users = set()
    for member in necessary_members:
        users.add(User(
            id=member.id_member,
            username=member.membername,
            full_name=member.realname,
            email=member.emailaddress,
            admission_year=datetime.fromtimestamp(member.dateregistered).year
        ))
    User.objects.bulk_create(users)


def link_messages_with_users():
    messages = Message.objects.all()
    for message in messages:
        message.user = User.objects.get(id=message.author.id_member)
    Message.objects.bulk_update(messages, ['user'])


# BAD_NAMED_USERS_IDS = {17, 52, 53, 56, 69, 81, 83, 182, 201, 203, 258, 279, 286, 294, 298}


def add_users_first_name_last_name():
    users = User.objects.all()
    for user in users:
        user.last_name, user.first_name = user.full_name.split()
    User.objects.bulk_update(users, ['first_name', 'last_name'])


def update_usernames():
    usernames = set()
    users = User.objects.all()
    for user in users:
        i = 1
        while 'msu_' + str(user.admission_year) + '_' + str(i).zfill(2) in usernames:
            i += 1
        user.username = 'msu_' + str(user.admission_year) + '_' + str(i).zfill(2)
        usernames.add(user.username)
    User.objects.bulk_update(users, ['username'])


def create_identifiers():
    s = str()
    with open('_identifiers.json') as file:
        for line in file:
            s += line
    identifiers = json.loads(s)
    for identifier in identifiers:
        Identifier.objects.create(
            object_type=identifier['type'],
            object_id_in_contest=identifier['id_in_contest'],
            object_name=identifier['name']
        )


PARENT_MESSAGES = set(message for message in Message.objects.all() if message.id == message.parent_msg_id)
""" SQL commands used to distribute messages:
update tashkent_forum._messages set identifier=1 where board in (10, 12);
update tashkent_forum._messages set identifier=1 where topic=12;
update tashkent_forum._messages set identifier=5 where topic=6;
update tashkent_forum._messages set identifier=4 where topic=34;
update tashkent_forum._messages set identifier=6 where topic in (44, 115);
update tashkent_forum._messages set identifier=3 where topic=124;
update tashkent_forum._messages set identifier=2 where topic=143;
delete from tashkent_forum._messages where topic=107;
update tashkent_forum._messages set identifier=1 where topic in (81, 22, 55);
update tashkent_forum._messages set identifier=5 where topic=74; --(Some identifiers have been manually changed)
update tashkent_forum._messages set identifier=5 where topic=28;
update tashkent_forum._messages set identifier=4 where topic=41;
update tashkent_forum._messages set identifier=4 where topic=37;
update tashkent_forum._messages set identifier=6 where topic in (45, 82);
delete from tashkent_forum._messages where topic=87;
update tashkent_forum._messages set identifier=7 where topic=138;
update tashkent_forum._messages set identifier=7 where topic=50; --(Some identifiers have been manually changed)
update tashkent_forum._messages set identifier=7 where topic=53;
delete from tashkent_forum._messages where topic=135;
update tashkent_forum._messages set identifier=3 where topic=123; --(Some identifiers have been manually changed)
update tashkent_forum._messages set identifier=3 where topic=125;
update tashkent_forum._messages set identifier=2 where topic=142; --(Some identifiers have been manually changed)
"""


def get_replies_identifiers_sql():
    replies = set(Message.objects.all()) - PARENT_MESSAGES
    with open('_define_replies_identifiers.sql', 'w') as f:
        for message in replies:
            s = ''
            s += r'update tashkent_forum._messages '
            s += 'set identifier='
            s += '{} where id={};'.format(Message.objects.get(id=message.parent_msg_id).identifier.id, message.id)
            s += '\n'
            f.write(s)


def get_users_json():
    users = list()
    for user in User.objects.all():
        users.append({
            'old_id': user.id,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'admission_year': user.admission_year
        })
    s = json.dumps(users)
    with open('_users.json', 'w') as file:
        file.write(s)


def get_comments_json():
    comments = list()
    for message in Message.objects.all():
        comments.append({
            'old_id': message.id,
            'author': message.author.id,
            'parent_id': message.parent_msg_id,
            'object_type': message.identifier.object_type,
            'object_id': message.identifier.object_id_in_contest,
            # 'text': message.subject + '<br>' + message.text,
            'text': message.text,
            'date_created': message.date_created
        })
    s = json.dumps(comments)
    with open('_comments.json', 'w') as file:
        file.write(s)
