import os

import yaml

from computenestcli.common import project_setup_constant, constant
from computenestcli.service.credentials import CredentialsService
from computenestcli.service.project_setup.setup_handler import SetupHandler


class HelmSetupHandler(SetupHandler):

    def validate_parameters(self):
        # Helm 参数验证逻辑
        pass

    def generate_templates(self):
        self.select_package()

        output_ros_template_path = os.path.join(self.output_base_path, project_setup_constant.OUTPUT_ROS_TEMPLATE_DIR,
                                                project_setup_constant.OUTPUT_ROS_TEMPLATE_NAME)
        self.jinja2Processor.process(project_setup_constant.INPUT_HELM_CHART_ROS_TEMPLATE_NAME, self.parameters,
                                     output_ros_template_path, self.package_name)
        self.developer_logger.info(f"Template rendered to {output_ros_template_path}")
        output_config_path = os.path.join(self.output_base_path, project_setup_constant.OUTPUT_CONFIG_NAME)

        self.jinja2Processor.process(project_setup_constant.INPUT_HELM_CHART_CONFIG_NAME, self.parameters,
                                     output_config_path, project_setup_constant.INPUT_CONFIG_PATH)
        self.developer_logger.info(f"Config rendered to {output_config_path}")

        self.user_logger.info("Template rendering complete.")

    # def _replace_docker_image_docker_compose(self):
    #     if not self.replace_image:
    #         return
    #     self.user_logger.info("docker compose replace docker image start")
    #     docker_compose_path = self.parameters.get(project_setup_constant.DOCKER_COMPOSE_PATH_KEY)
    #     if not os.path.isabs(docker_compose_path):
    #         docker_compose_path = os.path.abspath(docker_compose_path)
    #     # 解析docker-compose.yaml,替换其中的开源镜像
    #     with open(docker_compose_path, 'r') as stream:
    #         docker_compose_json = yaml.load(stream, Loader=yaml.FullLoader)
    #     # 获取计算巢容器镜像仓库路径
    #     response = CredentialsService.get_artifact_repository_credentials(self.context, constant.ACR_IMAGE)
    #     docker_host_path = os.path.dirname(response.body.available_resources[0].path)
    #     acr_image_artifact_parameters = []
    #     # 遍历 services 找到所有的 image_url
    #     services = docker_compose_json.get('services', {})
    #     try:
    #         replaced_image_urls = set()
    #         for service, config in services.items():
    #             image_url = config.get('image')
    #             if not image_url or project_setup_constant.ALI_DOCKER_REPO_HOST_SUFFIX in image_url \
    #                     or config.get('secrets') or config.get("build"):
    #                 continue
    #             image_split = image_url.split("/")
    #             image_split_len = len(image_split)
    #             if image_split_len >= 2:
    #                 # image为<registry>/<namespace>/<image_name>:<tag>类型 或 <namespace>/<image_name>:<tag>类型
    #                 namespace = image_split[-2]
    #                 last_name = image_split[-1]
    #                 last_name_split = last_name.split(":")
    #                 # image_name保留namespace，便于做区分
    #                 image_name = "{}/{}".format(namespace, last_name_split[0])
    #                 image_tag = last_name_split[1] if len(last_name_split) == 2 else 'latest'
    #             else:
    #                 # image为<image_name>:<tag>类型
    #                 last_name_split = image_split[0].split(":")
    #                 image_name = last_name_split[0]
    #                 image_tag = last_name_split[1] if len(last_name_split) == 2 else 'latest'
    #
    #             replaced_image_url = f"{docker_host_path}/{image_name}:{image_tag}"
    #             config['image'] = replaced_image_url
    #             # acr image去重
    #             if replaced_image_url in replaced_image_urls:
    #                 continue
    #             replaced_image_urls.add(replaced_image_url)
    #             artifact_name = "{}-{}".format(constant.ACR_IMAGE, image_name.replace("/", "-"))
    #             artifact_parameter = {
    #                 "ArtifactName": artifact_name,
    #                 "DockerImageUrl": image_url,
    #                 "DockerImageName": image_name,
    #                 "DockerImageTag": image_tag
    #             }
    #             acr_image_artifact_parameters.append(artifact_parameter)
    #     except Exception as e:
    #         self.developer_logger.error(f"docker compose replace docker image fail: {e}")
    #         raise
    #     self.developer_logger.info(f"Docker compose replace image, artifact parameters:{acr_image_artifact_parameters}")
    #     self.parameters[project_setup_constant.ACR_IMAGE_ARTIFACT_PARAMETERS_KEY] = acr_image_artifact_parameters
    #     # 替换过的写到新文件中
    #     target_docker_compose_path = self._get_target_replaced_docker_compose_path(docker_compose_path)
    #     with open(target_docker_compose_path, 'w') as file:
    #         file.write(yaml.dump(docker_compose_json))
    #
    # # 获取需要替换后的docker compose文件路径，src_file_path为用户指定的docker compose文件路径
    # def _get_target_replaced_docker_compose_path(self, src_file_path):
    #     # 1. 替换文件名
    #     base, ext = os.path.splitext(src_file_path)
    #     replaced_file_path = f"{base}-replaced{ext}"
    #     # 2. 获取文件相对于当前命令执行目录的相对路径
    #     relpath = os.path.relpath(replaced_file_path, os.getcwd())
    #     # 3. 获取实际要输出到的目录
    #     replaced_file_output_path = os.path.join(self.output_base_path,
    #                                              project_setup_constant.OUTPUT_DOCKER_COMPOSE_DIR, relpath)
    #     # 4. 判断父目录是否存在，不存在则创建
    #     if not os.path.exists(os.path.dirname(replaced_file_output_path)):
    #         os.makedirs(os.path.dirname(replaced_file_output_path))
    #     return replaced_file_output_path
