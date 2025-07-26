from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
import json

# a form view for our todos from our models
from django.views import View
from django.views.generic.edit import FormView
from django.views.generic import ListView
from .models import Todo
from .forms import TodoForm

class TodoFormView(FormView):
    template_name = 'todo_form.html'
    form_class = TodoForm
    success_url = '/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos'] = Todo.objects.all().order_by('-created_at')
        return context

class TodoListView(ListView):
    model = Todo
    template_name = 'todo_list.html'
    context_object_name = 'todos'
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        search = self.request.GET.get('search')
        
        if status == 'completed':
            queryset = queryset.filter(completed=True)
        elif status == 'pending':
            queryset = queryset.filter(completed=False)
        
        if search:
            queryset = queryset.filter(title__icontains=search)
            
        return queryset

# Toggle todo completed FormView
class ToggleTodoView(View):
    success_url = '/'
    
    def post(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=self.kwargs['pk'])
        todo.completed = not todo.completed
        todo.save()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'completed': todo.completed,
                'message': f'Task {"completed" if todo.completed else "marked as pending"}'
            })
        
        return redirect(self.success_url)

# Delete todo FormView
class DeleteTodoView(View):
    success_url = '/'
    
    def post(self, request, *args, **kwargs):
        todo = get_object_or_404(Todo, pk=self.kwargs['pk'])
        title = todo.title
        todo.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'Task "{title}" deleted successfully'
            })
        
        return redirect(self.success_url)

# API Views for AJAX operations
@csrf_exempt
@require_http_methods(["GET"])
def todo_stats_api(request):
    """API endpoint to get todo statistics"""
    todos = Todo.objects.all()
    total = todos.count()
    completed = todos.filter(completed=True).count()
    pending = todos.filter(completed=False).count()
    overdue = sum(1 for todo in todos if todo.is_overdue)
    
    completion_rate = round((completed / total * 100) if total > 0 else 0, 1)
    
    return JsonResponse({
        'total': total,
        'completed': completed,
        'pending': pending,
        'overdue': overdue,
        'completion_rate': completion_rate
    })

@csrf_exempt
@require_http_methods(["POST"])
def bulk_action_api(request):
    """API endpoint for bulk actions on todos"""
    try:
        data = json.loads(request.body)
        action = data.get('action')
        todo_ids = data.get('todo_ids', [])
        
        if not todo_ids:
            return JsonResponse({'success': False, 'message': 'No todos selected'})
        
        todos = Todo.objects.filter(id__in=todo_ids)
        
        if action == 'complete_all':
            todos.update(completed=True)
            message = f'{len(todo_ids)} tasks marked as completed'
        elif action == 'delete_all':
            count = todos.count()
            todos.delete()
            message = f'{count} tasks deleted'
        elif action == 'mark_pending':
            todos.update(completed=False)
            message = f'{len(todo_ids)} tasks marked as pending'
        else:
            return JsonResponse({'success': False, 'message': 'Invalid action'})
            
        return JsonResponse({'success': True, 'message': message})
        
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

class DashboardView(View):
    """Dashboard view with analytics"""
    def get(self, request):
        todos = Todo.objects.all()
        context = {
            'todos': todos,
            'total_todos': todos.count(),
            'completed_todos': todos.filter(completed=True).count(),
            'pending_todos': todos.filter(completed=False).count(),
            'overdue_todos': [todo for todo in todos if todo.is_overdue],
            'recent_todos': todos[:5],
        }
        return render(request, 'dashboard.html', context)
