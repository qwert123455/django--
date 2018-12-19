from django.shortcuts import render
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.template import loader
from django.urls import reverse         # 类似前端模板语言 url 函数
from .models import Question, Choice
from django.views import generic        # 从数据库取数据前台渲染列表的操作比较简单重复，django封装了这个过程提供统一的模板。

# Create your views here.
# def index(request):
#     return HttpResponse("""
#         <html>
#             <head>
#             </head>
#             <body>
#                 <h1>hello world<h1>
#             </body>
#         </html>  
#     """)

# def index(request):
#     """
#     展示问题列表
#     :return:
#     """
#     question_list = Question.objects.all().order_by('-pub_date')[0:5]
#
#     print(question_list)
#     output = ''
#     for q in question_list:
#         print(q.id, q.question_text, q.pub_date)
#         output = output + q.question_text
#     print(output)
#
#     output = ','.join([q.question_text for q in question_list])
#     return HttpResponse(output)
#
#     template = loader.get_template('polls/index.html')
#     context = {
#         'question_list':question_list
#     }
#     return HttpResponse(template.render(context, request))


def index(request):
    question_list = Question.objects.order_by('-pub_date')[:5]
    context = {
        'question_list':question_list
    }
    return render(request, 'polls/index.html',context)


def detail(request,question_id):
    """
    显示一个问题的详细信息，问题内容、问题发布时间、选项内容、每个选项投票数。
    """
    try:
        question = Question.objects.get(id=question_id)
        # (基本思想)choice = Choice.objects.filter(question_id=question_id)
        # 由于orm代劳，question直接带出相应的choices
        # choices = Question.choice_set.all()
        # 由于前端模块语言本质是后端代码，可以把上句话放html页面中写，有助于降低后端复杂度。
    except Question.DoesNotExist:
        raise Http404("404,此id的问题不存在")
    print(question)
    context = {
        'question': question
    }
    # question = Question.objects.filter(id=question_id)
    # if not question:
    #     raise Http404()
    # return render(request,'polls/detail.html',context)

    # question = get_object_or_404(Question, id=question_id)
    # print(question)
    return render(request, 'polls/detail.html',{'question':question})

def results(request,question_id):
    """
    投票结果
    """
    question = Question.objects.get(id=question_id)
    return render(request, 'polls/results.html',{'question': question})


def vote(request,question_id):
    """
    投票
    """
    try:
        question = Question.objects.get(id=question_id)
        choices = question.choice_set.all()
        choice_id = request.POST['choice']
        selected_choice = question.choice_set.get(id=choice_id)
    except Question.DoesNotExist as e:
        error_message = '问题内容不存在，-检查问题id'
    except Choice.DoesNotExist as e:
        error_message = '问题对应选项不存在'
        return render(request, 'polls/detail.html',context={
            'question':question,
            'error_message':error_message
        })
    else:
        # sql       update choice set votes=votes+1 where id=2
        selected_choice.votes += 1
        # commit;
        selected_choice.save()
        # 投票完重定向到views.results(qid)
        return HttpResponseRedirect(reverse('polls:results',args=(question.id,)))



# 通用模板示例，跟def index类比着看
class SimpleView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'question_list'

    def get_queryset(self):
        return Question.objects.all()