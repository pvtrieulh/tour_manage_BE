from django import template
from django.contrib.admin.templatetags.admin_modify import submit_row as original_submit_row

register = template.Library()


@register.inclusion_tag('admin/submit_line.html', takes_context=True)
def audio_submit_row(context):
    """
        Overrides 'django.contrib.admin.templatetags.admin_modify.submit_row'.
        Manipulates the context going into that function by hiding all of the buttons
        in the submit row if the key `readonly` is set in the context.
        """
    ctx = original_submit_row(context)

    ctx.update({
        'show_save_and_create_voice': True,
    })

    return ctx
