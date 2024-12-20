import os
from pathlib import Path

import yaml

from computenestcli.base_log import get_developer_logger, get_user_logger
from computenestcli.common import project_setup_constant
from computenestcli.common.arch import Arch
from computenestcli.common.logging_constant import SETUP_PROJECT
from computenestcli.common.service_type import ServiceType
from computenestcli.common.file_util import FileUtil
from computenestcli.common.str_util import StrUtil
from computenestcli.processor.jinja2 import Jinja2Processor

NECESSARY_DIRS = [project_setup_constant.OUTPUT_ROS_TEMPLATE_DIR,
                  project_setup_constant.OUTPUT_ICON_DIR]

ORIGINAL_REPO_PATH = "/root/code"
WORKSPACE_PATH = "/root/application"

developer_logger = get_developer_logger()
user_logger = get_user_logger(SETUP_PROJECT)


class SetupHandler:
    def __init__(self, output_base_path, parameters, ):
        self.output_base_path = output_base_path
        self.parameters = parameters
        self.jinja2Processor = Jinja2Processor()
        self.package_name = None
        self.user_logger = user_logger
        self.developer_logger = developer_logger

    def validate_parameters(self):
        raise NotImplementedError

    def generate_templates(self):
        raise NotImplementedError

    def generate_specified_templates(self, input_ros_template_path):
        self._service_and_repo_name_pre_process()
        self.parameters[project_setup_constant.ECS_IMAGE_ID_KEY] = \
            f'ecs_image_{self.parameters.get(project_setup_constant.REPO_NAME_KEY)}'

        output_ros_template_path = os.path.join(self.output_base_path, project_setup_constant.OUTPUT_ROS_TEMPLATE_DIR,
                                                project_setup_constant.OUTPUT_ROS_TEMPLATE_NAME)
        self.jinja2Processor.process(input_ros_template_path, self.parameters,
                                     output_ros_template_path, self.package_name)
        self.developer_logger.info(f"Template rendered to {output_ros_template_path}")

        output_config_path = os.path.join(self.output_base_path, project_setup_constant.OUTPUT_CONFIG_NAME)
        self.jinja2Processor.process(project_setup_constant.INPUT_ECS_IMAGE_CONFIG_NAME, self.parameters,
                                     output_config_path,
                                     project_setup_constant.INPUT_CONFIG_PATH)
        self.developer_logger.info(f"Config rendered to {output_config_path}")

        self.user_logger.info("Template rendering complete.")

    def _service_and_repo_name_pre_process(self):
        repo_full_name = self.parameters.get(project_setup_constant.REPO_FULL_NAME_KEY)
        # 兼容逻辑，统一采用REPO_FULL_NAME
        if not repo_full_name:
            repo_full_name = self.parameters.get(project_setup_constant.REPO_NAME_KEY)
        # 采用默认名称
        if not repo_full_name:
            repo_full_name = project_setup_constant.APP_NAME
            repo_name = project_setup_constant.APP_NAME
        else:
            repo_name = str.split(repo_full_name, "/")[1]
        self.parameters[project_setup_constant.REPO_NAME_KEY] = repo_name
        self.parameters[project_setup_constant.REPO_FULL_NAME_KEY] = repo_full_name
        self.parameters[project_setup_constant.SERVICE_NAME] = StrUtil.sanitize_name(repo_name)

    def copy_common_resources(self):
        output_base = Path(self.output_base_path)

        # 复制静态资源文件，包括icon、README.md
        self._copy_icons(output_base)
        self._copy_readme(output_base)
        service_type = self.parameters.get(project_setup_constant.SERVICE_TYPE_KEY)
        if service_type == ServiceType.MANAGED.value:
            self._copy_preset_parameters(output_base)

    def save_computenest_parameters(self):
        output_base = Path(self.output_base_path)
        self._generate_computenest_parameters_yaml(output_base, self.parameters)

    # 根据架构选择不同的模板所在的包
    def select_package(self):
        architecture = self.parameters.get(project_setup_constant.ARCHITECTURE_KEY, Arch.ECS_SINGLE.value)
        if not architecture:
            architecture = Arch.ECS_SINGLE.value
        if Arch.ECS_SINGLE.value == architecture:
            self.package_name = project_setup_constant.INPUT_ROS_TEMPLATE_ECS_SINGLE_PATH
        elif Arch.ECS_CLUSTER.value == architecture:
            self.package_name = project_setup_constant.INPUT_ROS_TEMPLATE_ECS_CLUSTER_PATH
        else:
            # 目前仅支持单节点和集群版（可弹性伸缩）架构
            raise Exception("Invalid architecture.")
        pass

    @staticmethod
    def _copy_icons(output_base):
        icon_dir = project_setup_constant.INPUT_ICON_DIR
        output_icon_dir = output_base / project_setup_constant.OUTPUT_ICON_DIR
        FileUtil.copy_from_package(project_setup_constant.INPUT_ROOT_PATH, icon_dir, output_icon_dir)
        user_logger.info(f"Copied icons to {output_icon_dir}")

    @staticmethod
    def _copy_readme(output_base):
        readme_name = project_setup_constant.INPUT_README_NAME
        FileUtil.copy_from_package(project_setup_constant.INPUT_ROOT_PATH, readme_name, output_base)
        user_logger.info(f"Copied README to {output_base}")

    @staticmethod
    def _copy_preset_parameters(output_base):
        FileUtil.copy_from_package(project_setup_constant.INPUT_ROOT_PATH,
                                   project_setup_constant.INPUT_PRESET_PARAMETERS_NAME, output_base)
        user_logger.info(f"Copied preset parameters to {output_base}")

    @staticmethod
    def _generate_computenest_parameters_yaml(output_base, parameters_json):
        # 自定义多行字符串表示的函数
        def str_presenter(dumper, data):
            """Convert multiple newlines in strings into block style (|)."""
            if '\n' in data:
                return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
            return dumper.represent_scalar('tag:yaml.org,2002:str', data)

        # 自定义将元组转换为列表
        def tuple_presenter(dumper, data):
            return dumper.represent_list(list(data))

        yaml.add_representer(str, str_presenter)
        yaml.add_representer(tuple, tuple_presenter)

        # 复制参数文件
        if not os.path.exists(output_base):
            os.makedirs(output_base)
        output_file_path = output_base / project_setup_constant.OUTPUT_PARAMETERS_FILE_NAME
        with open(output_file_path, 'w') as file:
            yaml.dump(parameters_json, file, default_flow_style=False, sort_keys=False, indent=2, allow_unicode=True)
