from django.urls import path
# import views of Shop App
from Shop import views
# import settings for MEDIA
from django.conf import settings
from django.conf.urls.static import static
#for login without views.py (coming from forms.py)
from django.contrib.auth import views as auth_views
#import login form class
from . forms import LoginForm
#import ChangePasswordForm form class
from . forms import DoChangePasswordForm
#import PasswordReset Class
from . forms import DoPasswordResetForm
#import DoSetPasswordConfirm to set new password for Reset Password Confirm
from .forms import DoSetPasswordConfirmForm



urlpatterns = [
    #ProductView class from views.py and url name 
    path('', views.ProductView.as_view(), name = 'home'),
    #for product page
    path('product-details/<int:pk>', views.ProductDetailView.as_view(), name ='product-details'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),

    #quantity +/-/remove item
    path('pluscart/', views.plus_cart),
    path('minuscart', views.minus_cart),
    path('removeitem/', views.remove_item),
    
    
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profileview.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    
    #category page
    #for actioncamera category, views: def actioncamera html: actioncamera.html
    path('actioncamera/', views.actioncamera, name='actioncamera'),
    #slug use to conditional calling for data attributes(views.py) 
    path('actioncamera/<slug:data>', views.actioncamera, name='actioncameraitem'),
    
    #for virtulareality category, views: def virtualreality html: virtualreality.html
    path('virtualreality/', views.virtualreality, name='virtualreality'),
    #slug use to conditional calling for data attributes(views.py) 
    path('virtualreality/<slug:data>', views.virtualreality, name='virtualrealityitem'),
    
    #for hoverboard category, views: def hoverboard html: hoverboard.html
    path('hoverboard/', views.hoverboard, name='hoverboard'),
    #slug use to conditional calling for data attributes(views.py) 
    path('hoverboard/<slug:data>', views.hoverboard, name='hoverboarditem'),
    
    #for smartphone category, views: def  smartphone html: smartphone.html
    path('smartphone/', views.smartphone, name='smartphone'),
    #slug use to conditional calling for data attributes(views.py) 
    path('smartphone/<slug:data>', views.smartphone, name='smartphoneitem'),
    
    #for ebook category, views: def  ebook html: ebook.html
    path('ebook/', views.ebook, name='ebook'),
    #slug use to conditional calling for data attributes(views.py) 
    path('ebook/<slug:data>', views.ebook, name='ebookitem'),
    
    #for audiobook category, views: def  audiobook html: audiobook.html
    path('audiobook/', views.audiobook, name='audiobook'),
    #slug use to conditional calling for data attributes(views.py) 
    path('audiobook/<slug:data>', views.audiobook, name='audiobookitem'),
    
    #accout-forms
    #for Signup and Registration
    path('registration/', views.CustomerRegistrationView.as_view(), name='customerregistration'),
    #for login and standard practice accounts/login
    path('accounts/login/', auth_views.LoginView.as_view(template_name = 'Shop/login.html', authentication_form = LoginForm), name='login'),
    #logout and redirect page /next_page = Page Name. Here 'home' page url name
    path('login/', auth_views.LogoutView.as_view(next_page = 'home'), name = 'logout'),
    #passwordchanged url.form_class indicating form class, success_url: redirect to another url after successful change. [no need to work on views.py]
    path('passwordchanged/', auth_views.PasswordChangeView.as_view(template_name = 'Shop/passwordchange.html', form_class=DoChangePasswordForm, success_url='/passwordchangedone/'), name='passwordchange'),
    #password change done url. [no need to work on views.py
    path('passwordchangedone/', auth_views.PasswordChangeView.as_view(template_name = 'Shop/passwordchangedone.html'), name='passwordchangedone'),

    #forget password with 4-steps of Django
    #step-01:password_reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='Shop/passwordreset.html', form_class=DoPasswordResetForm), name='password_reset'),
    #step-02: password_reset_done
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='Shop/passwordresetdone.html'), name='password_reset_done'),
    #step-03: password_reset_confirm
    #must be defined the path below manner as per django documentation
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'Shop/passwordresetconfirm.html', form_class=DoSetPasswordConfirmForm), name = 'password_reset_confirm'),
    #step-04: password reset complete
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'Shop/passwordresetcomplete.html'), name = 'password_reset_complete'),

    #checkout page
    path('checkout/', views.checkout, name='checkout'),
    #paymentdone page
    path('paymentdone/', views.payment_done, name='paymentdone'),
    
    
    ]+static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
#Media Directory settings and root of Media

