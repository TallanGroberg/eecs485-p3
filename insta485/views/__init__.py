"""Views, one for each Insta485 page."""
import insta485.api
from insta485.views.index import show_index
from insta485.views.explore import show_explore
from insta485.views.accounts.account import show_account
from insta485.views.accounts.login import show_login, do_logout, check_login
from insta485.views.accounts.check_password import check_password, hash_password
from insta485.views.accounts.create import show_create
from insta485.views.accounts.edit import show_edit
from insta485.views.accounts.password import show_password, edit_password
from insta485.views.accounts.delete import show_delete
from insta485.views.post import handle_file, add_post
from insta485.views.image import download_file
