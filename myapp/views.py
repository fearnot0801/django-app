from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

nextid = 4
topics = [
    {'id':1, 'title':'routiong', 'body':'Routing is ..'},
    {'id':2, 'title':'View', 'body':'View is ..'},
    {'id':3, 'title':'Model', 'body':'Model is ..'},
]

def HTMLTemplate(articleTag, id=None):
    global topics
    contextUI = ''
    if id != None :
        contextUI = f'''
            <li>
                <form action="/delete/" method="POST">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>
            <li>
                <a href="/update/{id}/">update</a></li>
            </li>
        '''
    ol =''
    for topic in topics:
        ol += f'<li><a href="/read/{topic["id"]}"> {topic["title"]} </a></li>'
    return f'''
    <html>
    <body>
        <h1><a href="/">Django</a></h1>
        <ul>
            {ol}
        </ul>
        {articleTag}
        <ul>
            <h1><a href="/create/">create</a></h1>
            {contextUI}
        </ul>
    </body>
    </h1ml>
    '''

def index(request):
    article = '''
    <h2>Welcome</h2>
    Hello, Django
    '''
    return HttpResponse(HTMLTemplate(article))

def read(request, id=None):
    global topics
    article = ''
    for topic in topics:
        if topic["id"] == int(id):
            article = f'<h2>{topic["title"]}</h2>{topic["body"]}'
    return HttpResponse(HTMLTemplate(article, id))

@csrf_exempt
def create(request):
    global nextid
    if request.method =='GET':
        article = '''
            <form action="/create/" method="POST">
                <p><input type="text" name="title" placeholder="title"></p>
                <p><textarea name="body" placeholder="body"></textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article))
    
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        newTopic = {"id":nextid, "title":title, "body":body}
        topics.append(newTopic)
        url = '/read/'+str(nextid)
        nextid = nextid + 1
        return redirect(url)

@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST['id']
        newTopics = []
        for topic in topics:
            if topic['id'] != int(id):
                newTopics.append(topic)
        topics = newTopics
        return redirect('/')
    
@csrf_exempt
def update(request, id):
    global topics
    for topic in topics:
        if topic['id'] == int(id):
            selectedTopic = {"title":topic['title'],
                             "body":topic['body']
                            }
    if request.method == 'GET':
        article = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name="title" placeholder="title" value={selectedTopic["title"]}></p>
                <p><textarea name="body" placeholder="body">{selectedTopic['body']}</textarea></p>
                <p><input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article, id))
    elif request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = title
                topic['body'] = body
        return redirect(f'/read/{id}')
