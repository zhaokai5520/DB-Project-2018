from handler.users import UserHandler
from handler.messages import MessageHandler
from handler.hashtags import HashtagHandler
from handler.chats import ChatHandler

from flask import Flask,jsonify, request, session, redirect, url_for, escape, request, render_template,g
from flask_cors import CORS
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)
CORS(app)

loggedUID = 0

########################
#Login Methods#
########################
@app.route('/')
def index():   
    # if 'user' in session:
    #     username = session['user']
    #     return 'Logged in as ' + username + '<br>' + "<b><a href = '/logout'>click here to log out</a></b>" # Not Really#
    # else:  return "You are not logged in <br><a href = '/ChatApp/login'></b>" + "click here to log in</b></a>"
    return render_template('dIndex.html')

@app.route('/ChatApp/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':  # Check for Loggin Attempt
        #session.pop('user', None)
        #session.pop('id', None)
        result = UserHandler().login(request.json)
        if not(result is None):# PassWord Check, insert query here     
            global loggedUID   
            loggedUID = result[1]            
            return jsonify("Logged In")
        else:
           return jsonify(Error="Bad login credentials"), 400 

@app.route('/protected')
def protected():
    if g.user:
        return render_template('protected.html')

    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/logout')
def logout():
    global loggedUID
    if loggedUID !=0:
        loggedUID = 0
        return jsonify("Logged out sucessfully")
    else:
        return jsonify(Error = "You need to be logged in before you can logout"), 404







##### Routes for Users #####

@app.route('/ChatApp/users', methods=['GET','POST'])
def getAllUsers():
    if request.method == 'POST':
        print("Request: ", request.json)
        return UserHandler().insertUserJson(request.json)
    else:
        if not request.args:
            return UserHandler().getAllUsers()

@app.route('/ChatApp/user',methods=['GET'])
def getLoggedUser():
    global loggedUID
    if loggedUID != 0:
        return UserHandler().getUserByID(loggedUID)
    else:
        return jsonify(Error = "User is not logged in."), 404
        
@app.route('/ChatApp/user/loggeduser', methods=['GET','POST'])
def newContact():
    print(request)
    global loggedUID
    if request.method == 'POST':
        return UserHandler().newContact(request.json, loggedUID)

@app.route('/ChatApp/user/<int:uid>', methods=['GET','POST'])
def getUserByID(uid):
    print(request)
    if request.method == 'GET':
        return UserHandler().getUserByID(uid)

@app.route('/ChatApp/user/<username>')
def getUserByUserName(username):
    return UserHandler().getUserByUserName(username)

@app.route('/ChatApp/user/<int:uid>/contacts')
def getAllContactsByID(uid):
    return UserHandler().getAllContactsByID(uid)

@app.route('/ChatApp/user/loggeduser/contacts')
def getContacts():
    global loggedUID
    return UserHandler().getAllContactsByID(loggedUID)


##### Routes for Messages #####

@app.route('/ChatApp/messages', methods=['GET','POST'])
def getAllMessages():
    if request.method == 'POST':
        print("Request: ", request.json)
        return MessageHandler().insertMessageJson(request.json)
    else:
        if not request.args:
            return MessageHandler().getAllMessages()

@app.route('/ChatApp/messages/<int:mid>')
def getMessageByID(mid):
    return MessageHandler().getMessageByID(mid)

@app.route('/ChatApp/messages/user/<int:uid>')
def getAllMessagesByUser(uid):
    return MessageHandler().getAllMessagesByUser(uid)

@app.route('/ChatApp/messages/<int:mid>/likes', methods=['GET','POST'])
def getAllMessageLikesByMID(mid):
    if request.method == 'POST':
        print("Request: ", request.json)
        return MessageHandler().insertMessageLikeJson(request.json)
    else:
        if not request.args:
            return MessageHandler().getAllMessageLikesByMID(mid)

@app.route('/ChatApp/messages/<int:mid>/likes/number')
def getNumberOfLikesByMID(mid):
    return MessageHandler().getNumberOfLikesByMID(mid)

@app.route('/ChatApp/messages/<int:mid>/dislikes',methods=['GET','POST'])
def getAllMessageDislikesByMID(mid):
    if request.method == 'POST':
        print("Request: ", request.json)
        return MessageHandler().insertMessageDislikeJson(request.json)
    else:
        if not request.args:
            return MessageHandler().getAllMessageDislikesByMID(mid)

@app.route('/ChatApp/messages/<int:mid>/dislikes/number')
def getNumberOfDislikesByMID(mid):
    return MessageHandler().getNumberOfDislikesByMID(mid)

@app.route('/ChatApp/messages/<int:mid>/likes/users')
def getUsersThatLikedMessagebyMID(mid):
    return MessageHandler().getUsersThatLikedMessageByMID(mid)

@app.route('/ChatApp/messages/<int:mid>/dislikes/users')
def getUsersThatDislikedMessageByMID(mid):
    return MessageHandler().getUsersThatDislikedMessageByMID(mid)

##### Routes for Hashtags #####

@app.route('/ChatApp/hashtags')
def getAllHashtags():
    return HashtagHandler().getAllHashtags()

@app.route('/ChatApp/hashtag/<int:hid>')
def getHashtagByID(hid):
    return HashtagHandler().getHashtagByID(hid)

@app.route('/ChatApp/hashtag/<text>')
def getAllHashtagsByText(text):
    return HashtagHandler().getHashtagByText(text)

@app.route('/ChatApp/hashtags/top10')
def getTop10Hashtags():
    return HashtagHandler().getTop10Hashtags()

### Routes For Chats ####

@app.route('/ChatApp/chat', methods=['GET', 'POST'])
def getAllChats():
    print(request)
    if request.method == 'GET':
        return ChatHandler().getAllChatGroups()
    elif request.method == 'POST':
        return ChatHandler().newChat(request.json)

@app.route('/ChatApp/chat/<int:cgid>', methods=['GET', 'POST'])
def getChatbyID(cgid):
    if request.method == 'GET':
        return ChatHandler().getChatByID(cgid)
    elif request.method == 'POST':
        global loggedUID
        return ChatHandler().joinChat(request.json, loggedUID)

@app.route('/ChatApp/chat/user/<int:uid>')
def getChatbyUser(uid):
    return ChatHandler().getChatGroupsByUserId(uid)

@app.route('/ChatApp/chat/loggeduser')
def getChatByUser():
    global loggedUID
    return ChatHandler().getChatGroupsByUserId(loggedUID)

@app.route('/ChatApp/chat/user/loggeduser/notmember')
def getChatsNotJoined():
    global loggedUID
    return ChatHandler().getChatsNotJoined(loggedUID)

@app.route('/ChatApp/chat/<int:cgid>/messages')
def getAllMessagesByChat(cgid):
    return ChatHandler().getAllMessagesByChat(cgid)

@app.route('/ChatApp/chat/<int:cgid>/owner')
def getChatOwner(cgid):
    return ChatHandler().getChatOwner(cgid)

@app.route('/ChatApp/chat/<int:cgid>/user/<int:uid>/messages')
def getChatbyName(cgid,uid):
    return ChatHandler().getChatMsgsByUserId(cgid,uid)

@app.route('/ChatApp/chat/<int:cgid>/members')
def getChatMembers(cgid):
    return ChatHandler().getChatMembers(cgid)


#################################
####    DASHBOARD ROUTES    #####
#################################

@app.route('/ChatApp/dash/Trending')
def getTrendingHash():
    return HashtagHandler().getTrending()

@app.route('/ChatApp/dash/MessagesPerDay')
def getMessagesPerDay():
    return MessageHandler().getMessagePerDay()

@app.route('/ChatApp/dash/RepliesPerDay')
def getRepliesPerDay():
    return MessageHandler().getRepliesPerDay()

@app.route('/ChatApp/dash/LikesPerDay')
def getLikesPerDay():
    return MessageHandler().getLikesPerDay()

@app.route('/ChatApp/dash/DislikesPerDay')
def getDislikesPerDay():
    return MessageHandler().getDislikesPerDay()

@app.route('/ChatApp/dash/TopUsers')
def TopUsers():
    return UserHandler().getTopPerDay()




if __name__ == '__main__':
    app.run(debug=True)
