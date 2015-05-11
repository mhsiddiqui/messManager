import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from re import compile
import re
import smtplib
import sys

from django.conf import settings
from django.contrib.auth import SESSION_KEY
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import TemplateDoesNotExist, TemplateSyntaxError
from django.template.context import RequestContext
from django.template.defaultfilters import force_escape, pprint
from django.template.loader import render_to_string
from django.utils.encoding import smart_unicode
from django.utils.html import escape
from django.utils.importlib import import_module
from django.views.debug import get_safe_settings, linebreak_iter
from django.core.urlresolvers import reverse


try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local

_thread_locals = local()

EXEMPT_URLS = [compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]

def get_request():
    return getattr(_thread_locals, 'request', None)


class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware\
requires authentication middleware to be installed. Edit your\
MIDDLEWARE_CLASSES setting to insert\
'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
'django.core.context_processors.auth'."

        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)

        if SESSION_KEY not in request.session:
            path = request.path_info.lstrip('/')
            nextURL = ''
            if path and path.find('.') == -1 and path != 'accounts/login/':
                nextURL = '?next='+path
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL + nextURL)
        last_activity = request.session.get('last_activity', None)
        now = datetime.datetime.now()
        if last_activity and not request.is_ajax():
            request.session['last_activity'] = now
            diff_min = (now - last_activity).total_seconds() / 60
            if diff_min > 10:
                return HttpResponseRedirect(reverse('logout'))
        _thread_locals.request = request
        
    def process_exception(self, request, exception):
        if settings.LOCAL_DEBUG:
            return None
        self.exc_type, self.exc_value, self.tb = sys.exc_info()
        frames = self.get_traceback_frames()
        self.template_does_not_exist = False
        self.loader_debug_info = None
        self.template_info = None
        if self.exc_type and issubclass(self.exc_type, TemplateDoesNotExist):
            from django.template.loader import template_source_loaders
            self.template_does_not_exist = True
            self.loader_debug_info = []
            for loader in template_source_loaders:
                try:
                    module = import_module(loader.__module__)
                    if hasattr(loader, '__class__'):
                        source_list_func = loader.get_template_sources
                    else: # NOTE: Remember to remove this branch when we deprecate old template loaders in 1.4
                        source_list_func = module.get_template_sources
                    # NOTE: This assumes exc_value is the name of the template that
                    # the loader attempted to load.
                    template_list = [{'name': t, 'exists': os.path.exists(t)} \
                        for t in source_list_func(str(self.exc_value))]
                except (ImportError, AttributeError):
                    template_list = []
                if hasattr(loader, '__class__'):
                    loader_name = loader.__module__ + '.' + loader.__class__.__name__
                else: # NOTE: Remember to remove this branch when we deprecate old template loaders in 1.4
                    loader_name = loader.__module__ + '.' + loader.__name__
                self.loader_debug_info.append({
                    'loader': loader_name,
                    'templates': template_list,
                })
        if (settings.TEMPLATE_DEBUG and hasattr(self.exc_value, 'source') and
            isinstance(self.exc_value, TemplateSyntaxError)):
            self.get_template_exception_info()
        for i, frame in enumerate(frames):
            if 'vars' in frame:
                frame['vars'] = [(k, force_escape(pprint(v))) for k, v in frame['vars']]
            frames[i] = frame
        unicode_hint = ''
        if self.exc_type and issubclass(self.exc_type, UnicodeError):
            start = getattr(self.exc_value, 'start', None)
            end = getattr(self.exc_value, 'end', None)
            if start is not None and end is not None:
                unicode_str = self.exc_value.args[1]
                unicode_hint = smart_unicode(unicode_str[max(start-5, 0):min(end+5, len(unicode_str))], 'ascii', errors='replace')
        from django import get_version
        data = {'exception':exception,
                 'is_email': False,
                 'unicode_hint': unicode_hint,
                 'frames': frames,
                 'request': request,
                 'settings': get_safe_settings(),
                 'sys_executable': sys.executable,
                 'sys_version_info': '%d.%d.%d' % sys.version_info[0:3],
                 'server_time': datetime.datetime.now(),
                 'django_version_info': get_version(),
                 'sys_path' : sys.path,
                 'template_info': self.template_info,
                 'template_does_not_exist': self.template_does_not_exist,
                 'loader_debug_info': self.loader_debug_info}
        if self.exc_type:
            data['exception_type'] = self.exc_type.__name__
        if self.exc_value:
            data['exception_value'] = smart_unicode(self.exc_value, errors='replace')
        if frames:
            data['lastframe'] = frames[-1]
        html_content = render_to_string("testing/exception.html",
                                        data)
#        f = open('c:\\temp.html', 'w')
#        f.write(html_content)
#        f.close()
        msg = MIMEMultipart('alternative')
        msg['Subject'] = "Server 500"

        # Record the MIME types of both parts - text/plain and text/html.
        part2 = MIMEText(html_content, 'html')
        part2.add_header('Content-Disposition', 'attachment', filename='errorlog.html')
        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part2)
        server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
#        server.set_debuglevel(1)
        server.ehlo()
        server.starttls()
        server.login(settings.EMAIL_HOST_USER,
                     settings.EMAIL_HOST_PASSWORD)
        server.sendmail(settings.EMAIL_HOST_USER, 
                        [email[1] for email in settings.ADMINS],
                        msg.as_string())
        server.quit()
        return render_to_response('testing/500.html',
                              {},
                              context_instance = RequestContext( request )) 
    
    def get_traceback_frames(self):
        frames = []
        tb = self.tb
        while tb is not None:
            # support for __traceback_hide__ which is used by a few libraries
            # to hide internal frames.
            if tb.tb_frame.f_locals.get('__traceback_hide__'):
                tb = tb.tb_next
                continue
            filename = tb.tb_frame.f_code.co_filename
            function = tb.tb_frame.f_code.co_name
            lineno = tb.tb_lineno - 1
            loader = tb.tb_frame.f_globals.get('__loader__')
            module_name = tb.tb_frame.f_globals.get('__name__')
            pre_context_lineno, pre_context, context_line, post_context = self._get_lines_from_file(filename, lineno, 7, loader, module_name)
            if pre_context_lineno is not None:
                frames.append({
                    'tb': tb,
                    'filename': filename,
                    'function': function,
                    'lineno': lineno + 1,
                    'vars': tb.tb_frame.f_locals.items(),
                    'id': id(tb),
                    'pre_context': pre_context,
                    'context_line': context_line,
                    'post_context': post_context,
                    'pre_context_lineno': pre_context_lineno + 1,
                })
            tb = tb.tb_next

        return frames

    def _get_lines_from_file(self, filename, lineno, context_lines, loader=None, module_name=None):
        """
        Returns context_lines before and after lineno from file.
        Returns (pre_context_lineno, pre_context, context_line, post_context).
        """
        source = None
        if loader is not None and hasattr(loader, "get_source"):
            source = loader.get_source(module_name)
            if source is not None:
                source = source.splitlines()
        if source is None:
            try:
                f = open(filename)
                try:
                    source = f.readlines()
                finally:
                    f.close()
            except (OSError, IOError):
                pass
        if source is None:
            return None, [], None, []

        encoding = 'ascii'
        for line in source[:2]:
            # File coding may be specified. Match pattern from PEP-263
            # (http://www.python.org/dev/peps/pep-0263/)
            match = re.search(r'coding[:=]\s*([-\w.]+)', line)
            if match:
                encoding = match.group(1)
                break
        source = [unicode(sline, encoding, 'replace') for sline in source]

        lower_bound = max(0, lineno - context_lines)
        upper_bound = lineno + context_lines

        pre_context = [line.strip('\n') for line in source[lower_bound:lineno]]
        context_line = source[lineno].strip('\n')
        post_context = [line.strip('\n') for line in source[lineno+1:upper_bound]]

        return lower_bound, pre_context, context_line, post_context
    
    def get_template_exception_info(self):
        origin, (start, end) = self.exc_value.source
        template_source = origin.reload()
        context_lines = 10
        line = 0
        upto = 0
        source_lines = []
        before = during = after = ""
        for num, next in enumerate(linebreak_iter(template_source)):
            if start >= upto and end <= next:
                line = num
                before = escape(template_source[upto:start])
                during = escape(template_source[start:end])
                after = escape(template_source[end:next])
            source_lines.append( (num, escape(template_source[upto:next])) )
            upto = next
        total = len(source_lines)

        top = max(1, line - context_lines)
        bottom = min(total, line + 1 + context_lines)

        self.template_info = {
            'message': self.exc_value.args[0],
            'source_lines': source_lines[top:bottom],
            'before': before,
            'during': during,
            'after': after,
            'top': top,
            'bottom': bottom,
            'total': total,
            'line': line,
            'name': origin.name,
        }
