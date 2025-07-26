from django.contrib import admin
from django.utils.html import format_html
from .models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['title', 'priority_badge', 'completed_status', 'due_date_status', 'created_at', 'completed']
    list_filter = ['completed', 'priority', 'created_at', 'due_date']
    search_fields = ['title', 'description']
    list_editable = ['completed']
    ordering = ['-created_at']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Task Details', {
            'fields': ('title', 'description')
        }),
        ('Task Settings', {
            'fields': ('priority', 'due_date', 'completed')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def priority_badge(self, obj):
        colors = {
            'high': '#f14668',
            'medium': '#ffdd57', 
            'low': '#48c774'
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 8px; border-radius: 3px; font-size: 0.8em;">{}</span>',
            colors.get(obj.priority, '#ccc'),
            obj.get_priority_display()
        )
    priority_badge.short_description = 'Priority'
    
    def completed_status(self, obj):
        if obj.completed:
            return format_html('<span style="color: #48c774;">✓ Complete</span>')
        else:
            return format_html('<span style="color: #f14668;">⏰ Pending</span>')
    completed_status.short_description = 'Status'
    
    def due_date_status(self, obj):
        if not obj.due_date:
            return format_html('<span style="color: #999;">No due date</span>')
        elif obj.is_overdue and not obj.completed:
            return format_html('<span style="color: #f14668;">⚠️ Overdue</span>')
        else:
            return format_html('<span style="color: #48c774;">{}</span>', obj.due_date.strftime('%Y-%m-%d %H:%M'))
    due_date_status.short_description = 'Due Date'
    
    actions = ['mark_completed', 'mark_pending', 'set_high_priority', 'set_medium_priority', 'set_low_priority']
    
    def mark_completed(self, request, queryset):
        updated = queryset.update(completed=True)
        self.message_user(request, f'{updated} tasks marked as completed.')
    mark_completed.short_description = "Mark selected tasks as completed"
    
    def mark_pending(self, request, queryset):
        updated = queryset.update(completed=False)
        self.message_user(request, f'{updated} tasks marked as pending.')
    mark_pending.short_description = "Mark selected tasks as pending"
    
    def set_high_priority(self, request, queryset):
        updated = queryset.update(priority='high')
        self.message_user(request, f'{updated} tasks set to high priority.')
    set_high_priority.short_description = "Set selected tasks to high priority"
    
    def set_medium_priority(self, request, queryset):
        updated = queryset.update(priority='medium')
        self.message_user(request, f'{updated} tasks set to medium priority.')
    set_medium_priority.short_description = "Set selected tasks to medium priority"
    
    def set_low_priority(self, request, queryset):
        updated = queryset.update(priority='low')
        self.message_user(request, f'{updated} tasks set to low priority.')
    set_low_priority.short_description = "Set selected tasks to low priority"

# Customize admin site
admin.site.site_header = "Task Master Admin"
admin.site.site_title = "Task Master"
admin.site.index_title = "Welcome to Task Master Administration"