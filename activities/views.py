from django.contrib.auth import login as lg, authenticate
from django.core.cache import cache
from django.db import connection
from django.db.models import Sum, Prefetch
from django.http import HttpResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.urls import reverse

from activities.models import Activity
from users.models import User


def login(request):
    print('rew', request.method)
    if request.method == 'GET':
        return render(request, template_name='login.html')
    else:
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)
        user = authenticate(request, username=username, password=password)
        print('rsefdf', user)
        if user:
            lg(request, user)
            return redirect('/')
        else:
            return HttpResponse('Username or password incorrect.')
        # districts = User.objects.values_list('adname', flat=True)
        # return redirect(request, '/')
# ModelBackend


def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    districts = User.objects.values_list('adname', flat=True).distinct()
    return render(request, template_name='home.html', context={'districts': districts})


def get_ranking(request):
    if not request.user.is_authenticated:
        return redirect(reverse('login'))
    adname = request.GET.get('adname')
    type = request.GET.get('type', 'total')
    query_kwargs = {'adname': adname} if adname else {}
    cache_key = ','.join(request.GET.values())
    print('request args', cache_key)


    context = cache.get(cache_key)
    if not context:
        print(1111111)
        if type == 'total':
            label = '总持续时间排行榜'
            head = {'user_id': '用户id', 'user_name': '用户姓名', 'user_gender': '用户性别', 'user_age': '用户年龄',
                    'total_duration': '总时长(s)'}
            query_kwargs = {'user__adname': adname} if adname else {}
            activities = Activity.objects.prefetch_related('user').filter(
                **query_kwargs
            ).values('user_id', 'user__name', 'user__gender', 'user__age').annotate(
                total_activity_time=Sum('duration')
            ).order_by('-total_activity_time')
            # print('activities', activities)
        elif type == 'area':
            label = '区域排行榜'
            head = {'area': '地区', 'total_duration': '总时长(s)'}
            # query_kwargs = {'user__adname': adname} if adname else {}
            activities = User.objects.prefetch_related(
                Prefetch(
                    'activity_set',
                    to_attr='activity_set'
                )
            ).values('adname').annotate(
                total_activity_time=Sum('activity__duration')
            ).order_by('-total_activity_time')
            # print('activities', activities)
            # activities = Activity.objects.prefetch_related('user').filter(
            #     **query_kwargs
            # ).values('adname').annotate(
            #     total_activity_time=Sum('duration')
            # ).order_by('-total_activity_time')
            # print('activities', activities)
        elif type == 'count':
            user_ids = list(User.objects.filter(**query_kwargs).values_list('id', flat=True))
            # print('user_ids', user_ids)
            label = '每分钟运动次数排行榜'
            head = {'user_id': '用户id', 'user_name': '用户姓名', 'user_age': '用户年龄', 'user_gender': '用户性别',
                    'count': '每分钟使用次数', 'duration': '运动时长'}
            if user_ids:
                raw_sql = """
                SELECT user_id, max(m) as max_count, max(d) as max_duration
                FROM
                (
                SELECT user_id, any_value(max(machine_used_per_min)) as m, any_value(SUM(duration)) as d,  COUNT(*) FROM activities_activity GROUP BY user_id, machine_used_per_min
                ) as bests
                WHERE user_id in %s
                GROUP BY user_id
                ORDER BY max_count desc, max_duration desc      
                """
            else:
                raw_sql = """
                            SELECT user_id, max(m) as max_count, max(d) as max_duration
                            FROM
                            (
                            SELECT user_id, any_value(max(machine_used_per_min)) as m, any_value(SUM(duration)) as d,  COUNT(*) FROM activities_activity GROUP BY user_id, machine_used_per_min
                            ) as bests
                            GROUP BY user_id
                            ORDER BY max_count desc, max_duration desc      
                            """
            with connection.cursor() as cursor:
                cursor.execute(raw_sql, [tuple(user_ids), ] if user_ids else None)
                res = cursor.fetchall()
                # print('res', res)
                user_ids = [item[0] for item in res]
                users = User.objects.filter(id__in=user_ids).values('id', 'name', 'gender', 'age')
                users_dict = {
                    user.get('id'): {
                        'user_name': user.get('name'),
                        'user_age': user.get('age'),
                        'user_gender': user.get('gender')
                    }
                    for user in users
                }
                # print('users', users)
                activities = [
                    {'user_id': item[0],
                     'user_name': users_dict.get(item[0]).get('user_name'),
                     'user_age': users_dict.get(item[0]).get('user_age'),
                     'user_gender': users_dict.get(item[0]).get('user_gender'),
                     'count': item[1],
                     'duration': item[2],
                     }

                    for item in res
                ]
        context = {'activities': activities, 'head': head, 'label': label, 'adname': adname}
        cache.set(cache_key, context, timeout=60)

    return render(request, 'ranking.html', context=context)
