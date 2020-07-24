from .main import main
from .bp_commands import *  # NoQA
from .app_commands import *  # NoQA
from .config_commands import *  # NoQA
from .account_commands import *  # NoQA
from .project_commands import *  # NoQA
from .secret_commands import *  # NoQA
from .cache_commands import *  # NoQA
from .completion_commands import *  # NoQA
from .init_command import *  # NoQA
from calm.dsl.api import get_api_client
from .mpis_commands import *  # NoQA
from .app_icon_commands import *  # NoQA
from .user_commands import *  # NoQA
from .group_commands import *  # NoQA
from .role_commands import *  # NoQA
from .directory_service_commands import *  # NoQA
from .acp_commands import *  # NoQA

__all__ = ["main", "get_api_client"]
