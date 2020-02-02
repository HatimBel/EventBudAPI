import numpy as np

def contentReccomendation(users, userQuestString):

    for key, value in users.items():

        users[key]['Rating'] = rating(userQuestString, value['Questionnaire'])

    return users

def rating(user, userList):

    u1 = np.array(convertStrList(user))
    u2 = np.array(convertStrList(userList))

    w = np.array([5,10,10,15,7,13,15,10,10,5])

    u4 = ((u1 == u2).astype(int) * w.transpose()) / np.sum(w)

    sum = np.sum(u4)

    return sum


def convertStrList(string):
    int_list = []

    for ch in str(string):
        int_list.append(int(ch))

    return  int_list