from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy

from django.conf import settings
from django.template.response import TemplateResponse
from django.template import RequestContext
from django.urls import reverse, NoReverseMatch
from django.utils.text import capfirst
from django.apps import apps



    

class MyAdminSite(admin.AdminSite):

    # URL for the "View site" link at the top of each admin page.
    site_url = "/"

    enable_nav_sidebar = True

    # 登录页&首页的标题
    site_header = '登录页&首页的标题'
    # 浏览器的标题
    site_title = '浏览器的标题'
    # 正文的标题
    index_title = '正文的标题'
    
    
    def _build_app_dict(self, request, label=None):
        """
        Build the app dictionary. The optional `label` parameter filters models
        of a specific app.
        """
        app_dict = {}

        if label:
            models = {
                m: m_a
                for m, m_a in self._registry.items()
                if m._meta.app_label == label
            }
        else:
            models = self._registry

        for model, model_admin in models.items():
            app_label = model._meta.app_label

            has_module_perms = model_admin.has_module_permission(request)
            if not has_module_perms:
                continue

            perms = model_admin.get_model_perms(request)

            # Check whether user has any perm for this module.
            # If so, add the module to the model_list.
            if True not in perms.values():
                continue

            info = (app_label, model._meta.model_name)
            model_dict = {
                "model": model,
                "name": capfirst(model._meta.verbose_name_plural),
                "object_name": model._meta.object_name,
                "perms": perms,
                "admin_url": None,
                "add_url": None,
            }
            if perms.get("change") or perms.get("view"):
                model_dict["view_only"] = not perms.get("change")
                try:
                    model_dict["admin_url"] = reverse(
                        "admin:%s_%s_changelist" % info, current_app=self.name
                    )
                except NoReverseMatch:
                    pass
            if perms.get("add"):
                try:
                    model_dict["add_url"] = reverse(
                        "admin:%s_%s_add" % info, current_app=self.name
                    )
                except NoReverseMatch:
                    pass

            if app_label in app_dict:
                app_dict[app_label]["models"].append(model_dict)
            else:
                app_dict[app_label] = {
                    "name": apps.get_app_config(app_label).verbose_name,
                    "app_label": app_label,
                    "app_url": reverse(
                        "admin:app_list",
                        kwargs={"app_label": app_label},
                        current_app=self.name,
                    ),
                    "has_module_perms": has_module_perms,
                    "models": [model_dict],
                }

        return app_dict
    
    
    def get_app_list(self, request, app_label=None):
    
        app_dict = self._build_app_dict(request, app_label)
        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        # Sort the models alphabetically within each app.
        for app in app_list:
            app["models"].sort(key=lambda x: x["name"])

        ## 如果配置了不显示系统菜单，则只显示配置的菜单
        if not settings.SOHO_MENU_LIST['show_system_menu']:
            app_list = settings.SOHO_MENU_LIST['models']
        else:
            print(request.user.get_all_permissions())
            for sohoui_model in settings.SOHO_MENU_LIST['models']:
                default_app_dict = {
                    'name': sohoui_model['name'],
                    'models': []
                }
                ## 判断用户是否有权限model访问，有则添加到app_list   
                for model in sohoui_model['models']:
                    print(model['name'])
                    if model.get('permission', ''):
                        print(request.user.has_perm(model.get('permission')))
                        if  request.user.has_perm(model.get('permission')):
                            default_app_dict['models'].append(model)
                    else:
                        # 判断用户是否有权限model访问，有则添加到app_list   
                        default_app_dict['models'].append(model)
                    print(default_app_dict['models'])
                if default_app_dict['models']:
                    app_list.append(default_app_dict)

        return {
            # 登录背景图片
            'LOGIN_BG_IMAGE': settings.SOHO_LOGIN_BG_IMAGE,
            # 站点标题
            'site_header': settings.SOHO_SITE_HEADER,
            'app_list': app_list
        }
        
    
    
    
    def each_context(self, request):
        """
        Return a dictionary of variables to put in the template context for
        *every* page in the admin site.

        For sites running on a subpath, use the SCRIPT_NAME value if site_url
        hasn't been customized.
        """
        script_name = request.META["SCRIPT_NAME"]
        site_url = (
            script_name if self.site_url == "/" and script_name else self.site_url
        )
        return {
            "site_title": self.site_title,
            "site_header": self.site_header,
            "site_url": site_url,
            "has_permission": self.has_permission(request),
            # "available_apps": self.get_app_list(request),
            "is_popup": False,
            "is_nav_sidebar_enabled": self.enable_nav_sidebar,
            "log_entries": self.get_log_entries(request),
        }
        
    def index(self, request, extra_context=None):
        # app_list = self.get_app_list(request)
        context = {
            **self.each_context(request),
            "title": self.index_title,
            "subtitle": None,
            **(extra_context or {}),
        }
        
        
        context.update({
            'app_list': self.get_app_list(request)['app_list'],
        })
        context.update({
            'available_apps': context['app_list'],
        })

        request.current_app = self.name
        
        return TemplateResponse(
            request, self.index_template or "admin/index.html", context
        )
        
    
    
adminsite = MyAdminSite()


# 注册用户模型
adminsite.register(User, UserAdmin)

# 注册组模型
class GroupAdmin(admin.ModelAdmin):
    filter_horizontal = ['permissions']

adminsite.register(Group, GroupAdmin)