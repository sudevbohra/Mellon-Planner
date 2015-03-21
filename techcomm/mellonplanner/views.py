from django.shortcuts import render

# Create your views here.

def resetData(context):
    context['current_num'] = '0'
    context['previous_num'] = ''
    context['current_op'] = ''
    
# The action for the 'calculator/calc' route.
def mellon(request):
    context = {}
    
    # Make sure all fields have their correct initial values
    if 'current_num' in request.GET and request.GET['current_num'] != '':
        context['current_num'] = request.GET['current_num']
    if 'previous_num' in request.GET and request.GET['previous_num'] != '':
        context['previous_num'] = request.GET['previous_num']
    if 'current_op' in request.GET and request.GET['current_op'] != '':
        context['current_op'] = request.GET['current_op']
        
    #Case 1: user pressed an op
    if 'op' in request.GET:
        if ('previous_num' not in request.GET or request.GET['previous_num'] == '') and request.GET['op'] == '=':
            pass
        elif 'previous_num' not in request.GET or request.GET['previous_num'] == '':
            context['previous_num'] = request.GET['current_num']
            context['current_num'] = ''
            context['current_op'] = request.GET['op']
        else:
            if 'current_op' in request.GET:
                try:
                    previous_num = int(request.GET['previous_num'])
                    current_num = int(request.GET['current_num'])
                except ValueError:
                    resetData(context)
                    return render(request, 'calc.html', context)         
                op = request.GET['current_op']
                if(op == '+'):
                    current_num = previous_num + current_num
                elif(op == '-'):
                    current_num = previous_num - current_num
                elif(op == '*'):
                    current_num = previous_num * current_num
                elif(op == '/'):
                    try:
                        current_num = previous_num / current_num
                    except ZeroDivisionError:
                        resetData(context)
                        # reset everything
                        return render(request, 'calc.html', context)
                        
            if(request.GET['op'] == '='):
                context['previous_num'] = ''
                context['current_num'] = str(current_num)
                context['current_op'] = ''
            else:
                context['previous_num'] = str(current_num)
                context['current_num'] = ''
                context['current_op'] = request.GET['op']

    #Case 2: user pressed a digit            
    elif 'digit' in request.GET:
        if 'current_num' in request.GET:
            context['current_num'] = request.GET['current_num']
        try:
            context['current_num'] = str(int(context['current_num'] + request.GET['digit']))
        except ValueError:
            resetData(context)

    return render(request, 'calc.html', context)
